import pygame as pg
from settings import *
from sprites import *
from main import *
import random 




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

        

        self.camera = pg.Rect(x, y, self.width, self.height) # Update camera based on target
        


class Cooldown:
    def __init__(self, time):
        self.start_time = 0
        
        self.width = WIDTH
        self.height = HEIGHT

        self.time = time # time in milliseconds for cooldown
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






def draw_string_between_player_and_mob(surface, game): # MADE WITh Claude Code! 
    from settings import SHOW_STRING, STRING_DISTANCE
    if not hasattr(game, 'player') or not hasattr(game, 'all_mobs'):
        return
    if not SHOW_STRING:
        return
    player = game.player
    # Draw string to the first mob (can be extended for multiple mobs)
    for mob in game.all_mobs:
        # Use world coords for distance, screen coords for drawing
        dx = player.pos.x - mob.pos.x
        dy = player.pos.y - mob.pos.y
        dist = (dx ** 2 + dy ** 2) ** 0.5 
        if dist <= STRING_DISTANCE:
            player_screen = game.camera.apply(player).center  #
            mob_screen = game.camera.apply(mob).center # 
            pg.draw.line(surface, (255, 255, 0), player_screen, mob_screen, 3) #
        
        # Only draw to the first mob for now
        break
            