#!/usr/bin/env python3
"""
MP3 Tag Editor Web Application

A Flask web application for editing MP3 ID3 tags.
Upload an MP3 file, edit tags, and download the modified version.

Usage:
    python3 app.py

Then open your browser to http://localhost:8000

Dependencies:
    pip3 install flask mutagen
"""

import os
import tempfile
import shutil
import uuid
from flask import Flask, request, render_template, send_file, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from mutagen.id3 import ID3, TIT2, TPE1, TEXT, TCOP, TCOM, TXXX, COMM, error as ID3Error

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mp3-tagger-secret-key'
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


class MP3Tagger:
    """MP3 tag editor class for handling ID3 metadata."""

    def __init__(self, file_path):
        """
        Initialize the MP3 tagger with a file path.

        Args:
            file_path (str): Path to the MP3 file

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is not an MP3 file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if not file_path.lower().endswith('.mp3'):
            raise ValueError("File must be an MP3 file")

        self.file_path = file_path
        self.tags = None
        self._load_tags()

    def _load_tags(self):
        """Load ID3 tags from the MP3 file."""
        try:
            self.tags = ID3(self.file_path)
        except ID3Error:
            # Create new ID3 tag if none exists
            self.tags = ID3()

    def get_tag(self, tag_name):
        """
        Get the value of a specific tag.

        Args:
            tag_name (str): Tag name ('title', 'artist', 'lyricist', 'composer', 'copyright', 'comment')

        Returns:
            str: Tag value or empty string if not found
        """
        tag_map = {
            'title': 'TIT2',
            'artist': 'TPE1',
            'lyricist': 'TEXT',
            'composer': 'TCOM',
            'copyright': 'TCOP',
            'comment': 'COMM::eng'
        }

        if tag_name not in tag_map:
            raise ValueError(f"Unknown tag: {tag_name}")

        frame_id = tag_map[tag_name]
        if frame_id in self.tags:
            return str(self.tags[frame_id])
        return ""

    def set_tag(self, tag_name, value):
        """
        Set the value of a specific tag.

        Args:
            tag_name (str): Tag name ('title', 'artist', 'lyricist', 'composer', 'copyright', 'comment')
            value (str): New tag value
        """
        tag_map = {
            'title': TIT2,
            'artist': TPE1,
            'lyricist': TEXT,
            'composer': TCOM,
            'copyright': TCOP,
            'comment': COMM
        }

        if tag_name not in tag_map:
            raise ValueError(f"Unknown tag: {tag_name}")

        frame_class = tag_map[tag_name]
        if value.strip():
            if tag_name == 'comment':
                # COMM frame needs language and description parameters
                self.tags['COMM::eng'] = COMM(encoding=3, lang='eng', desc='', text=value)
            else:
                self.tags[frame_class.__name__] = frame_class(encoding=3, text=value)
        else:
            # Remove tag if value is empty
            if tag_name == 'comment':
                frame_id = 'COMM::eng'
            else:
                frame_id = frame_class.__name__
            if frame_id in self.tags:
                del self.tags[frame_id]

    def save(self):
        """Save the tags to the MP3 file."""
        self.tags.save(self.file_path)

    def save_as_new_file(self, output_path):
        """
        Save the tags to a new MP3 file with copyright in filename.

        Args:
            output_path (str): Path for the new file

        Returns:
            str: Path to the new file
        """
        title = self.get_tag('title')
        if not title:
            title = "Untitled"

        # Create new filename with copyright
        new_filename = f"{title} ©️ Stiftelsen Skjulte Skatter Forlag.mp3"
        output_dir = os.path.dirname(output_path)
        final_path = os.path.join(output_dir, new_filename)

        # Copy the original file to new location
        shutil.copy2(self.file_path, final_path)

        # Save tags to the new file
        self.tags.save(final_path)

        return final_path

    def get_all_tags(self):
        """
        Get all supported tags.

        Returns:
            dict: Dictionary with tag names and their values
        """
        return {
            'title': self.get_tag('title'),
            'artist': self.get_tag('artist'),
            'lyricist': self.get_tag('lyricist'),
            'composer': self.get_tag('composer'),
            'copyright': self.get_tag('copyright'),
            'comment': self.get_tag('comment')
        }


@app.route('/', methods=['GET', 'POST'])
def index():
    """Main page with file upload."""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if file and file.filename.lower().endswith('.mp3'):
            # Save uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Store file path in session
            session_id = str(uuid.uuid4())
            session[session_id] = file_path

            return redirect(url_for('edit_tags', session_id=session_id))

        else:
            flash('Please upload a valid MP3 file')
            return redirect(request.url)

    return render_template('index.html')


@app.route('/edit/<session_id>', methods=['GET', 'POST'])
def edit_tags(session_id):
    """Edit tags page."""
    # Get file path from session
    if session_id not in session:
        flash('Session expired. Please upload the file again.')
        return redirect(url_for('index'))

    file_path = session[session_id]

    try:
        tagger = MP3Tagger(file_path)
    except (FileNotFoundError, ValueError) as e:
        flash(f'Error loading file: {e}')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Update tags from form
        copyright_value = request.form.get('copyright', '').strip()
        if not copyright_value:
            copyright_value = 'Copyright © Stiftelsen Skjulte Skatters Forlag. All Rights Reserved.'

        tagger.set_tag('title', request.form.get('title', ''))
        tagger.set_tag('artist', request.form.get('artist', ''))
        tagger.set_tag('lyricist', request.form.get('lyricist', ''))
        tagger.set_tag('composer', request.form.get('composer', ''))
        tagger.set_tag('copyright', copyright_value)

        # Always set the comment to https://activechristianity.org
        tagger.set_tag('comment', 'https://activechristianity.org')

        # Create new file with copyright in filename
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.mp3')
        try:
            new_file_path = tagger.save_as_new_file(output_path)
            # Clean up the session after successful download
            if session_id in session:
                # Remove the temporary uploaded file
                try:
                    os.unlink(session[session_id])
                except:
                    pass
                del session[session_id]

            flash('File successfully created and downloaded! Upload another file to continue.', 'success')
            return send_file(new_file_path, as_attachment=True, download_name=os.path.basename(new_file_path))
        except Exception as e:
            flash(f'Error creating file: {e}')
            return redirect(request.url)

    # Get current tags for display
    current_tags = tagger.get_all_tags()
    filename = os.path.basename(file_path)

    return render_template('edit.html', tags=current_tags, filename=filename)


import atexit

def cleanup_temp_files():
    """Clean up temporary files on exit."""
    try:
        import shutil
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            shutil.rmtree(app.config['UPLOAD_FOLDER'])
    except:
        pass

# Register cleanup function
atexit.register(cleanup_temp_files)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
