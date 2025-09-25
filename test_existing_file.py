#!/usr/bin/env python3
"""Test reading lyricist from existing MP3 file"""

from app import MP3Tagger

# Use the existing HV 19.mp3 file
file_path = "/Users/lukaszpolok/Dev/copyrighter/HV 19.mp3"

try:
    tagger = MP3Tagger(file_path)
    all_tags = tagger.get_all_tags()

    print(f"All tags: {all_tags}")
    print(f"Lyricist: '{tagger.get_tag('lyricist')}'")

    # Check raw ID3 tags
    print(f"Raw TEXT frame: {tagger.tags.get('TEXT', 'NOT FOUND')}")

except Exception as e:
    print(f"Error: {e}")

