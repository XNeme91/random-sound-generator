import json
from pathlib import Path
import pygame
import random
import time

pygame.mixer.init()
sounds_folder = Path("sounds")
print(f"Available sounds:")
for sound_file in sounds_folder.glob("*.mp3"):
    print(f" - {sound_file.name}")

config_path = Path("config.json")

if config_path.exists():
    with open(config_path, "r") as f:
        data = json.load(f)
else:
    data = {"min_interval": 5, "max_interval": 10}
    with open(config_path, "w") as f:
        json.dump(data, f, indent=4)

min_interval = data["min_interval"]
max_interval = data["max_interval"]

while True:
    sound_file = random.choice(list(sounds_folder.glob("*.mp3")))
    print(f"Playing sound: {sound_file.name}")
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    interval = random.randint(min_interval, max_interval)
    print(f"Waiting for {interval} seconds before playing the next sound.")
    time.sleep(interval)