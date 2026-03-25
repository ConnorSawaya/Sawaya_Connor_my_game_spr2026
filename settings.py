STRING_DISTANCE = 200    # Rest length of elastic string (slack below this)
SHOW_STRING = True       # Toggle to show/hide string
MOB_FRICTION = 0.90      # Velocity multiplier per frame (close to 1 = low friction)
STRING_SPRING_K = 0.18   # Spring constant — how snappy the elastic is
MOB_LAUNCH_FORCE = 22    # Extra force multiplier when slingshot key is pressed
import os

import pygame as pg

WIDTH = 800
HEIGHT = 600
TITLE = "My cool game..."
FPS = 60
TILESIZE = 32
BORDER_THICKNESS = 2
CAMERA_RADIUS = 480





script_dir = os.path.dirname(__file__) 

PLAYER_SPEED = 280 # Player Speed for moving

PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE, TILESIZE)  # Player Hitbox 

# Color Values

# Tuple storing RGB values 
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)