import os

import pygame as pg

STRING_DISTANCE = 200    # Rest length of elastic string (slack below this)
SHOW_STRING = True       # Toggle to show/hide string
MOB_FRICTION = 0.97      # Velocity multiplier per frame(1 = no friction, 0 = full stop)

GRAVITY = 1600           # Gravity strength (pixels/sec^2)

STRING_SPRING_K = 0.18   # How hard the string pulls when its stretched to far
PLAYER_STRING_SPRING_K = 2.0  # How hard the string pulls the player back when stretched
SLINGSHOT_FORCE = 10
MAX_PULL_DIST = 200      # Max String Distence 



WIDTH = 800
HEIGHT = 600
TITLE = "The Best Game Evahh"
FPS = 60
TILESIZE = 32
BORDER_THICKNESS = 2
CAMERA_RADIUS = 480





script_dir = os.path.dirname(__file__) 

PLAYER_SPEED = 280  # Player Speed for moving
JUMP_FORCE = 600    # Upward velocity applied on jump (pixels/sec)

PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE, TILESIZE)  # Player Hitbox 

# Color Values

# Tuple storing RGB values 
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)