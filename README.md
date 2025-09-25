![ezgif-74f18015b0a0ed](https://github.com/user-attachments/assets/e2d36ab0-8f1c-49ba-86ed-7f222193134b)

# MP3 Tag Editor

A web application to read and modify ID3 tags in MP3 files. Perfect for managing metadata like title, artist, lyricist (author), composer, text and melody, and copyright information. Creates a new file with copyright in the filename.

## Features

- **Web-based GUI** - Upload files through a modern web interface
- Read and display current MP3 tags
- Edit title, artist, lyricist (author), composer, text and melody, and copyright information
- Interactive interface with validation
- Safe tag editing with validation
- Support for removing tags by leaving fields empty
- **Creates a new file** with the naming pattern: `Title ©️ Stiftelsen Skjulte Skatter Forlag.mp3`
- **Copy Song Info** feature generates formatted text with emojis showing artist, title, author, composer, copyright, and website

## Installation

1. Install Python 3.6 or higher
2. Install dependencies:

   ```bash
   pip3 install -r requirements.txt
   ```

## Usage

Start the web application:

```bash
python3 app.py
```

Then open your browser to `http://localhost:8000`

### How to Use the Web App

1. **Upload** your MP3 file by dragging and dropping or clicking to browse
2. **View current tags** - All existing metadata is displayed
3. **Edit tags** - Modify any of the supported fields:
   - Title
   - Artist
   - Lyricist (Author)
   - Composer
   - Copyright (defaults to standard copyright text)
   - Comment (automatically set to AC URL)
4. **Copy Song Info** - Generate formatted text with emojis showing artist-title, author, composer, copyright, and website
5. **Download** - Click "Download Modified MP3" to get your file with:
   - Updated tags
   - New filename: `Title ©️ Stiftelsen Skjulte Skatter Forlag.mp3`

### Tag Fields Supported

- **Title (TIT2)**: Song title
- **Artist (TPE1)**: Artist/performer name
- **Lyricist (TEXT)**: Writer of the lyrics (author)
- **Composer (TCOM)**: Composer of the melody
- **Copyright (TCOP)**: Copyright information (defaults to "Copyright © Stiftelsen Skjulte Skatters Forlag. All Rights Reserved.")
- **Comment (COMM)**: Automatically set to "https://activechristianity.org"

## Dependencies

- `mutagen==1.47.0` - Python multimedia library for audio metadata
- `Flask==2.3.3` - Web framework
- `Werkzeug==2.3.7` - WSGI utility library

## Notes

- The application creates ID3v2.4 tags if they don't exist
- Changes are only saved when you download the modified file (creates a copy with copyright in filename)
- Empty values will remove the corresponding tag from the file
- The application validates that the input file is an MP3 file
- New files are created with the pattern: `Title ©️ Stiftelsen Skjulte Skatter Forlag.mp3`

## Error Handling

The application handles common errors such as:

- File not found
- Invalid file format (non-MP3 files)
- Permission issues when saving
- Corrupted ID3 tags (creates new ones automatically)
