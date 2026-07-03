"""Random Sound Generator - Main Entry Point

This application plays random MP3 sounds from a configured folder with random intervals.
You can configure the sound folder using the GUI.
"""

from gui import create_gui
from data import play_random_sounds

def main():
    create_gui()

if __name__ == "__main__":
    main()