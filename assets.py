import pygame
import os, sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS 
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_image(path):
    """Load an image with alpha transparency from the given path."""
    return pygame.image.load(resource_path(path)).convert_alpha()

def load_players_with_names(prefix, folder="assets/players"):
    """
    Load player images and extract their names based on filename pattern.
    Expected format: prefix-name.png (e.g. p1n-player1.png)
    """
    folder_path = resource_path(folder)
    players = []
    for file in sorted(os.listdir(folder_path)):
        if file.endswith(".png") and file.startswith(prefix):
            parts = file.split('-', 1)
            name = parts[1].rsplit('.', 1)[0] if len(parts) == 2 else "Unknown"
            img_path = os.path.join(folder, file)
            img = load_image(img_path) 
            players.append({"image": img, "name": name})
    return players
