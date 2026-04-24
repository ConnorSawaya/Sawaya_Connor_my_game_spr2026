import os
import pygame as pg

STRING_DISTANCE = 180    # Rest length of elastic string (slack below this)
SHOW_STRING = True       # Toggle to show/hide string
FRICTION = 0.97      # Velocity multiplier per frame 1 = none, 0 = stop

GRAVITY = 800           #Gravity strength
MAX_FALL_SPEED = 800     # Terminal velocity to prevent tunneling through floors

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
CAMERA_RADIUS = 1200 # Radius of camera mask in pixels

#Water Settings
WATER_RISE_SPEED = 10
WATER_HEIGHT = 0
WATER_RISE_DELAY = 8000


script_dir = os.path.dirname(__file__)  # File path of the current script
IMG_DIR = os.path.join(script_dir, "images") # File path of the images folder
SOUND_DIR = os.path.join(script_dir, "sounds") # File path of the sounds folder



PLAYER_SPEED = 220  # Player Speed for moving
JUMP_FORCE = 500    # Upward velocity for jump

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
