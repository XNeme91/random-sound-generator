"""Random Sound Generator - Main Entry Point

This application plays random MP3 sounds from a configured folder with random intervals.
You can configure the sound folder using the GUI with a system tray icon.
"""

from gui import create_gui, create_tray_icon
import threading

def main():
    """Start the GUI and tray icon in separate threads."""
    # Start GUI in main thread (required for Tkinter on some systems)
    gui_thread = threading.Thread(target=create_gui, daemon=False)
    gui_thread.start()
    
    # Give GUI time to start before showing tray icon
    import time
    time.sleep(1)
    
    # Start tray icon in main thread
    try:
        icon = create_tray_icon()
        icon.run()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()