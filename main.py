import json
from pathlib import Path
import pygame
import random
import time

pygame.mixer.init()
sound = pygame.mixer.Sound("sounds/bark-fart_XRsy1HE.mp3")
sound_length = sound.get_length()

config_path = Path("config.json")

if config_path.exists():
    with open(config_path, "r") as f:
        data = json.load(f)
else:
    data = {"min_interval": 60, "max_interval": 300}
    with open(config_path, "w") as f:
        json.dump(data, f, indent=4)

min_interval = data["min_interval"]
max_interval = data["max_interval"]

random_number = random.randint(min_interval, max_interval)
print(f"Random number between {min_interval} and {max_interval}: {random_number}")
sound.play()
time.sleep(sound_length)