# MP3 Tag Editor

A Python program to read and modify ID3 tags in MP3 files. Perfect for managing metadata like title, artist, lyricist (author), composer, text and melody, and copyright information. Creates a new file with copyright in the filename.

## Features

- **Web-based GUI** - Upload files through a modern web interface
- **Command-line interface** - Original CLI version still available
- Read and display current MP3 tags
- Edit title, artist, lyricist (author), composer, text and melody, and copyright information
- Interactive interfaces with validation
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

## Web Application (Recommended)

Start the web server:

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

## Command Line Application

Run the program with an MP3 file as an argument:

```bash
python3 mp3_tagger.py your_song.mp3
```

### Interactive Menu

The CLI provides an interactive menu with the following options:

1. **Edit Title** - Change the song title
2. **Edit Artist** - Change the artist name
3. **Edit Lyricist** - Change the lyricist (author) information
4. **Edit Composer** - Change the composer information
5. **Edit Copyright** - Change copyright information
6. **Copy Song Info** - Generate formatted text with emojis showing artist-title, author, composer, copyright, and website
7. **Save as New File** - Create a new file with copyright in filename
8. **Exit** - Quit the program

### Tag Fields Supported

- **Title (TIT2)**: Song title
- **Artist (TPE1)**: Artist/performer name
- **Lyricist (TEXT)**: Writer of the lyrics (author)
- **Composer (TCOM)**: Composer of the melody
- **Copyright (TCOP)**: Copyright information (defaults to "Copyright © Stiftelsen Skjulte Skatters Forlag. All Rights Reserved.")
- **Comment (COMM)**: Automatically set to "www.activechristianity.org"

## Dependencies

- `mutagen==1.47.0` - Python multimedia library for audio metadata

## Notes

- The program creates ID3v2.4 tags if they don't exist
- Changes are only saved when you explicitly choose "Save as New File" (creates a copy with copyright in filename)
- Empty values will remove the corresponding tag from the file
- The program validates that the input file is an MP3 file
- New files are created with the pattern: `Title ©️ Stiftelsen Skjulte Skatter Forlag.mp3`

## Examples

```bash
# Edit a single MP3 file
python3 mp3_tagger.py "My Song.mp3"

# The program will display current tags and present a menu
# Make your changes and save when done
```

## Error Handling

The program handles common errors such as:

- File not found
- Invalid file format (non-MP3 files)
- Permission issues when saving
- Corrupted ID3 tags (creates new ones automatically)