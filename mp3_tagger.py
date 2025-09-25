#!/usr/bin/env python3
"""
MP3 Tag Editor

A Python program to read and modify ID3 tags in MP3 files.
Supports editing title, artist, lyricist (author), composer, text and melody, and copyright information.
Creates a new file with copyright in the filename: "Title ©️ Stiftelsen Skjulte Skatter Forlag.mp3"

Usage:
    python3 mp3_tagger.py <mp3_file>

Dependencies:
    pip3 install mutagen
"""

import sys
import os
from mutagen.id3 import ID3, TIT2, TPE1, TEXT, TCOP, TCOM, TXXX, COMM, error as ID3Error


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
            tag_name (str): Tag name ('title', 'artist', 'lyricist', 'composer', 'copyright')

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
            tag_name (str): Tag name ('title', 'artist', 'lyricist', 'composer', 'copyright')
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

    def save_as_new_file(self, output_directory=None):
        """
        Save the tags to a new MP3 file with copyright in filename.

        Args:
            output_directory (str, optional): Directory to save the new file. Defaults to current directory.

        Returns:
            str: Path to the new file
        """
        title = self.get_tag('title')
        if not title:
            title = "Untitled"

        # Create new filename with copyright
        new_filename = f"{title} ©️ Stiftelsen Skjulte Skatter Forlag.mp3"

        if output_directory:
            output_path = os.path.join(output_directory, new_filename)
        else:
            # Save in same directory as original file
            output_path = os.path.join(os.path.dirname(self.file_path), new_filename)

        # Copy the original file to new location
        import shutil
        shutil.copy2(self.file_path, output_path)

        # Save tags to the new file
        self.tags.save(output_path)

        return output_path

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


def print_banner():
    """Print the program banner."""
    print("=" * 50)
    print("         MP3 Tag Editor")
    print("=" * 50)
    print()


def display_current_tags(tagger):
    """
    Display current tag values.

    Args:
        tagger (MP3Tagger): The tagger instance
    """
    print(f"File: {os.path.basename(tagger.file_path)}")
    print("-" * 40)

    tags = tagger.get_all_tags()
    for tag_name, value in tags.items():
        print("12")

    print()


def get_user_choice():
    """
    Get user's menu choice.

    Returns:
        str: User's choice
    """
    print("Choose an option:")
    print("1. Edit Title")
    print("2. Edit Artist")
    print("3. Edit Lyricist")
    print("4. Edit Composer")
    print("5. Edit Copyright")
    print("6. Copy Song Info")
    print("7. Save as New File")
    print("8. Exit")
    print()

    while True:
        choice = input("Enter your choice (1-8): ").strip()
        if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
            return choice
        print("Invalid choice. Please enter 1-8.")


def edit_tag(tagger, tag_name, display_name):
    """
    Edit a specific tag.

    Args:
        tagger (MP3Tagger): The tagger instance
        tag_name (str): Internal tag name
        display_name (str): Display name for the tag
    """
    current_value = tagger.get_tag(tag_name)
    print(f"Current {display_name}: {current_value}")

    new_value = input(f"Enter new {display_name} (leave empty to remove): ").strip()
    tagger.set_tag(tag_name, new_value)

    if new_value:
        print(f"{display_name} updated to: {new_value}")
    else:
        print(f"{display_name} removed")
    print()


def main():
    """Main program function."""
    if len(sys.argv) != 2:
        print("Usage: python mp3_tagger.py <mp3_file>")
        sys.exit(1)

    mp3_file = sys.argv[1]

    try:
        tagger = MP3Tagger(mp3_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    print_banner()
    display_current_tags(tagger)

    while True:
        choice = get_user_choice()

        if choice == '1':
            edit_tag(tagger, 'title', 'Title')
        elif choice == '2':
            edit_tag(tagger, 'artist', 'Artist')
        elif choice == '3':
            edit_tag(tagger, 'lyricist', 'Lyricist (Author)')
        elif choice == '4':
            edit_tag(tagger, 'composer', 'Composer')
        elif choice == '5':
            edit_tag(tagger, 'copyright', 'Copyright')
        elif choice == '6':
            # Copy song info
            title = tagger.get_tag('title').strip() or 'Untitled'
            artist = tagger.get_tag('artist').strip() or 'Unknown Artist'
            lyricist = tagger.get_tag('lyricist').strip() or 'Unknown'
            composer = tagger.get_tag('composer').strip() or 'Unknown'

            song_info = f"""🎵: {artist} - {title}
✍️: {lyricist}
🎼: {composer}

Music and Lyrics © : Stiftelsen Skjulte Skatters Forlag
🔗: hiddentreasures.org"""

            print("\n" + "="*50)
            print("SONG INFO (Copy and paste this text):")
            print("="*50)
            print(song_info)
            print("="*50 + "\n")
        elif choice == '7':
            try:
                # Set default copyright if empty
                current_copyright = tagger.get_tag('copyright')
                if not current_copyright.strip():
                    tagger.set_tag('copyright', 'Copyright © Stiftelsen Skjulte Skatters Forlag. All Rights Reserved.')

                # Always set the comment to www.activechristianity.org
                tagger.set_tag('comment', 'www.activechristianity.org')
                new_file_path = tagger.save_as_new_file()
                print(f"New file created: {os.path.basename(new_file_path)}")
                print("All tags have been applied to the new file.")
                print()
            except Exception as e:
                print(f"Error creating new file: {e}")
                print()
        elif choice == '8':
            print("Goodbye!")
            break

        # Display updated tags after each operation
        if choice in ['1', '2', '3', '4', '5']:
            display_current_tags(tagger)


if __name__ == "__main__":
    main()
