import json
from pathlib import Path
import pygame
import random
import time

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

def play_random_sounds():
    """Play random sounds from the configured folder with random intervals."""
    pygame.mixer.init()
    
    config = load_config()
    min_interval = config["min_interval"]
    max_interval = config["max_interval"]
    sounds_folder = Path(config["path"])
    
    # Play random sounds
    while True:
        sound_files = list(sounds_folder.glob("*.mp3"))
        if not sound_files:
            print(f"No MP3 files found in {sounds_folder}")
            break
        
        sound_file = random.choice(sound_files)
        print(f"Playing sound: {sound_file.name}")
        pygame.mixer.music.load(str(sound_file))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        interval = random.randint(min_interval, max_interval)
        print(f"Waiting for {interval} seconds before playing the next sound.")
        time.sleep(interval)

if __name__ == "__main__":
    play_random_sounds()