from fileinput import filename
import pygame as pg
from settings import *
# this class creates a countdown timer for a cooldown\





class Map:
    def __init__(self, filename):
        # creating the data for builing the map using a list
        self.data = []

        # open a specific file and close it with 'with'
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        # 
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Spritesheet: # Class for loading spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert() # loads image and converts to format or pygame

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y, width, height))
        new_image = pg.transform.scale(image, (width, height))
        image = new_image
        return image
    



class Camera: # Camera Class so the camera can follow the player 
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height) 
        # Width and height of the map for camera 
        self.width = width 
        self.height = height

    def apply(self, entity): # Applies camera offest 
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect): # Applies camera offest to rec
        return rect.move(self.camera.topleft)

    def draw_world(self, surface, sprites): # Works with camera to draw everything on the world
        for sprite in sprites: # for each sprite it puts it on the screen with tis 
            surface.blit(sprite.image, self.apply(sprite))

    def apply_circular_mask(self, surface, target, radius=CAMERA_RADIUS):
        mask = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        mask.fill((0, 0, 0, 255))
        target_screen_center = self.apply(target).center
        pg.draw.circle(mask, (0, 0, 0, 0), target_screen_center, radius)
        surface.blit(mask, (0, 0))

    def update(self, target): # Makes camera follow the player

        # center camera on target
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit moving to the map size
        x = min(0, x)
        x = max(-(self.width - WIDTH), x)
        y = min(0, y)
        y = max(-(self.height - HEIGHT), y)

        self.camera = pg.Rect(x, y, self.width, self.height) # Update camera based on target
        


class Cooldown:
    def __init__(self, time):
        self.start_time = 0
        # Allows us to set property for time until cooldown
        self.time = time
    def start(self):
        self.start_time = pg.time.get_ticks()
    def ready(self):
        # sets current time to 
        current_time = pg.time.get_ticks()
        # if the difference between current and start time are greater than self.time
        # return True
        if current_time - self.start_time >= self.time: # where time is in milliseconds
            self.start()
            return True
        return False