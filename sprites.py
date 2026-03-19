from os import path
from random import random, choice
from time import time
import pygame as pg
from pygame.sprite import Sprite
from sympy import true
from settings import *
from utils import *


vec = pg.math.Vector2


def collide_hit_rect(one, two): # Creating a Function to check for collisio
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir):
    if dir == 'x':  # Only checking horizontal collisions
        
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            print("collided with wall from x dir")
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':  # Only checking vertical collisions
        # spritecollide checks if sprite hits any sprite in group
        # False = don't delete walls if collision happens
        # collide_hit_rect = custom collision detection function
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            print("collided with wall from y dir")
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        # use the shared spritesheet loaded by the Game (may be None)
        self.sprite_sheet = getattr(self.game, 'sprite_sheet', None)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.hit_rect =  PLAYER_HIT_RECT
        self.jumping = False
        self.moving = False
        self.last_update = 0
        self.current_frame = 0
        # load animation frames if spritesheet is available
        if self.sprite_sheet:
            self.load_image()
        else:
            self.standing_frames = [self.image]
            self.moving_frames = [self.image]
        
    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if keys[pg.K_p]:
            p = Projectile(self.game, self.rect.x, self.rect.y)
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        self.moving = (self.vel.x != 0 or self.vel.y != 0)


    def load_image(self): # Loading frames from spritesheet for animations
        self.standing_frames = [self.sprite_sheet.get_image(0, 0, TILESIZE, TILESIZE), self.sprite_sheet.get_image(0, TILESIZE, TILESIZE, TILESIZE)] # Graps frames in the first column of the spritesheet for standing animation
        self.moving_frames = [self.sprite_sheet.get_image(TILESIZE, 0, TILESIZE, TILESIZE), self.sprite_sheet.get_image(TILESIZE, TILESIZE, TILESIZE, TILESIZE)]

        for frame in self.standing_frames: # Sets the color key for transparency to black for each frame
            frame.set_colorkey(BLACK) # Set to background of spritesheet 
        for frame in self.moving_frames:
            frame.set_colorkey(BLACK)


    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.moving:
            if now - self.last_update > 3500:
                self.last_update = now # Time in milliseconds since last frame change
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames) # loops standing frames

                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
                bottom = self.rect.bottom
                self.image = self.moving_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            
    def state_check(self):
        if self.vel != vec(0,0):
            self.moving = True
        else: 
            self.moving = False

        

           


    def update(self):
        # print("player updating")
        self.animate()
        self.get_keys()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center




class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(1,0)
        self.pos = vec(x,y) * TILESIZE
        self.speed = 10

    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
 
        if hits:
            print("collided")  # debug message
            self.speed = -self.speed   # increase speed after hitting wall
 
        # If mob goes off screen horizontally
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1      # reverse direction
            self.pos.y += TILESIZE  # move down one row
 
        self.pos += self.speed * self.vel
        self.rect.center = self.pos
        




class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load(path.join(self.game.img_dir, 'wall.png')).convert()

        self.rect = self.image.get_rect()
        
        self.vel = vec(0,0) 
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
    def update(self):
        pass 
            




class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
    def update(self):
        pass

    
class Projectile(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(1,0)
        self.pos = vec(x,y) * TILESIZE
        self.speed = 10
        print("Working Projectile init")
    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, true)
        print("hits")
        self.pos += self.speed * self.vel
        self.rect.center = self.pos
 
