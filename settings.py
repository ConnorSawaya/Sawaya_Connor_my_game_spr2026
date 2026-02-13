import pygame as pg

WIDTH = 800
HEIGHT = 600
TITLE = "My cool game..."
FPS = 60
TILESIZE = 32
BORDER_THICKNESS = 2

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