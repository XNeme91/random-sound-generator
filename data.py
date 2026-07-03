import json
from pathlib import Path
import pygame
import random
import time
import threading

# Global flag to control sound playback
_sound_thread = None
_stop_sounds = False

def load_config():
    """Load configuration from config.json."""
    config_path = Path("config.json")
    
    if config_path.exists():
        with open(config_path, "r") as f:
            data = json.load(f)
    else:
        data = {"min_interval": 5, "max_interval": 10, "path": "sounds"}
        with open(config_path, "w") as f:
            json.dump(data, f, indent=4)
    
    return data

def _play_sounds_loop():
    """Internal function to play sounds in a loop (runs in background thread)."""
    global _stop_sounds
    pygame.mixer.init()
    
    config = load_config()
    min_interval = config["min_interval"]
    max_interval = config["max_interval"]
    sounds_folder = Path(config["path"])
    
    while not _stop_sounds:
        try:
            sound_files = list(sounds_folder.glob("*.mp3"))
            if not sound_files:
                print(f"No MP3 files found in {sounds_folder}")
                break
            
            sound_file = random.choice(sound_files)
            print(f"Playing sound: {sound_file.name}")
            pygame.mixer.music.load(str(sound_file))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() and not _stop_sounds:
                time.sleep(0.1)
            
            if not _stop_sounds:
                interval = random.randint(min_interval, max_interval)
                print(f"Waiting for {interval} seconds before playing the next sound.")
                time.sleep(interval)
        except Exception as e:
            print(f"Error playing sound: {e}")
            break

def start_sounds():
    """Start playing sounds in a background thread."""
    global _sound_thread, _stop_sounds
    
    if _sound_thread is not None and _sound_thread.is_alive():
        print("Sounds are already playing.")
        return
    
    _stop_sounds = False
    _sound_thread = threading.Thread(target=_play_sounds_loop, daemon=True)
    _sound_thread.start()
    print("Sound player started.")

def stop_sounds():
    """Stop playing sounds."""
    global _stop_sounds, _sound_thread
    _stop_sounds = True
    if _sound_thread is not None:
        _sound_thread.join(timeout=2)
    print("Sound player stopped.")

def play_random_sounds():
    """Play random sounds (blocking version for standalone use)."""
    start_sounds()
    # Keep the thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_sounds()

if __name__ == "__main__":
    play_random_sounds()