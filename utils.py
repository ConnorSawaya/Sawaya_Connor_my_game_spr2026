import math
import pygame as pg
from pygame.sprite import Sprite
from settings import *
from sprites import *


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0
                                      ), (x, y, width, height))
        new_image = pg.transform.scale(image, (width, height))
        image = new_image
        return image


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def draw_world(self, surface, sprites):
        for sprite in sprites:
            surface.blit(sprite.image, self.apply(sprite))

    def apply_circular_mask(self, surface, target, radius=CAMERA_RADIUS):
        mask = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        mask.fill((0, 0, 0, 255))
        target_screen_center = self.apply(target).center
        pg.draw.circle(mask, (0, 0, 0, 0), target_screen_center, radius)
        surface.blit(mask, (0, 0))

    def update(self, target):
        # center the camera on player 1
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pg.Rect(x, y, self.width, self.height)


class Cooldown:
    def __init__(self, time):
        self.start_time = 0
        self.width = WIDTH
        self.height = HEIGHT
        self.time = time

    def start(self):
        self.start_time = pg.time.get_ticks()

    def ready(self):
        current_time = pg.time.get_ticks()
        if current_time - self.start_time >= self.time:
            self.start()
            return True
        return False


class line(Sprite): # Class For string between player and player2
    def draw_string_between_player_and_player2(surface, game): # Method to draw string between player and player2
        if not hasattr(game, 'player') or not hasattr(game, 'player2'): # Check if player and player2 exist
            return
        if not SHOW_STRING: # If toggle for showing string is off,
            return
      
        player = game.player # sets up player variable 
        player2 = game.player2 # sets up player2 variable

        # Player pos and getting distance between player and player2 for string calculations
        dx = player.pos.x - player2.pos.x # gets the distance from the plaeyer 1 to player 2 in x and y direction 
        dy = player.pos.y - player2.pos.y # gets the distance from the plaeyer 1 to player 2 in x and y direction
        dist = (dx ** 2 + dy ** 2) ** 0.5 # Calcsulates the actual distance using pythagorean theorem


        stretch = max(0, dist - STRING_DISTANCE) # checks how much the string is stretched beyond its rest length
        t = min(1.0, stretch / STRING_DISTANCE) #  Normalizes it to a value from 0-1 for later color and thickness chaange 

        r = int(255 * t) # Changes Color to more red when tis stretched more
        g = int(255 * (1 - t)) # Changes Color to more green when tis stretched less
        color = (r, g, 0) # Color changes

        thickness = 2 + int(t * 3) # Thickness changes based on stretch

        player_screen = game.camera.apply(player).center # Gets pos of player and player2 on screen
        player2_screen = game.camera.apply(player2).center # Gets pos of player and player2 on screen

        pg.draw.line(surface, color, player_screen, player2_screen, thickness) # Draws the actual line




#                  Made my Codex- Prompt was asking for a pygame python code for rising water that can kill the player if they touch it, and also has a wave effect on top. I also added a little bit of code to make it so it can be used in the game and interact with the player.

class Water: 
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        self.water_height = WATER_HEIGHT
        self.height = WATER_HEIGHT
        self.water_top = self.world_height - self.height
        self.rise_speed = WATER_RISE_SPEED
        self.delay_ms = WATER_RISE_DELAY
        self.start_time = pg.time.get_ticks()
        self.color = (40, 120, 220, 90)
        self.wave_color = (190, 220, 255, 150)

    def spawn_splash(self, game, center_x):
        for _ in range(150):
            angle = random.uniform(0.15, math.pi - 0.15)
            radius = random.uniform(8, 40)
            spawn_x = center_x + math.cos(angle) * radius
            spawn_y = self.water_top - math.sin(angle) * radius
            Water_particle(game, spawn_x, spawn_y)

    def update(self, dt, game): 
        # Starting delay of water rising for time to go upwards before water gets there

        if pg.time.get_ticks() - self.start_time >= self.delay_ms: #Check for delay to start rising
            self.height = min(self.world_height, self.height + self.rise_speed * dt)

        # Water Top is used for checking if player is touching the water by using the top cords of the current hieght of the rising water
        self.water_top = self.world_height - self.height

        # Player 1 Particles and Sound
        player1_touching = self.is_touching(game.player)
        if player1_touching and not game.player.was_touching_water:
            if settings.splash_sound: # checks for splash sound in setting before playing
                settings.splash_sound.play()  # plays the splash sound when the player enters the water

            self.spawn_splash(game, game.player.hit_rect.centerx)
        game.player.was_touching_water = player1_touching



        # Player 2 Particles and Sound
        player2_touching = self.is_touching(game.player2)
        if player2_touching and not game.player2.was_touching_water:
            if settings.splash_sound: # checks for splash sound in setting before playing
                settings.splash_sound.play()  # plays the splash sound when the player enters the water

            self.spawn_splash(game, game.player2.hit_rect.centerx) 
        game.player2.was_touching_water = player2_touching

        if player1_touching or player2_touching:
            game.health -= WATER_DAMAGE * dt
        return self.water_top
    

    def is_touching(self, sprite, water_top=None): # methond to check for touching
        # Simple check: if the player's feet are below the water line, they are in water.
        if water_top is None:
            water_top = self.water_top
        return sprite.hit_rect.bottom >= water_top

    def surface_y(self):
        return self.water_top # returns the y cord of top of water

    def draw(self, surface, camera, water_top=None): # draw method for the water, it draws a rectangle for the water and then a wave line on top of it
        if water_top is None:
            water_top = self.water_top
        
        water_rect = pg.Rect(0, water_top, self.world_width, self.height) 
        screen_rect = camera.apply_rect(water_rect) # applies the camera rect to water rect so it moves at the same speed as camera

        # Draw on a transparent surface so the water is see-through.
        water_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        pg.draw.rect(water_surface, self.color, screen_rect)

        # Tiny wave line so the top is not perfectly flat
        points = [] # lists for all the wave points to draw the wave line

        for x in range(0, self.world_width + 1, 20): # Sample points every 20 pixels across the width of the water
            # calculate the wave height using sine function 
            wave_y = water_top + math.sin(pg.time.get_ticks() * 0.004 + x * 0.03) * 4
            screen_x = x + camera.camera.x 
            screen_y = wave_y + camera.camera.y 
            points.append((screen_x, screen_y))
 
        if len(points) > 1: # only draw the wave line if we have enough points
            pg.draw.lines(water_surface, self.wave_color, False, points, 2)

        surface.blit(water_surface, (0, 0)) # draws the water surface on the main screen

class health_bar:
    def __init__(self, player):
        self.player = player
        self.width = 100
        self.height = 12
        self.color = (255, 0, 0)

    def draw(self, surface, x, y):
        health_ratio = self.player.health / self.player.max_health
        current_width = int(self.width * health_ratio)
        back_rect = pg.Rect(x, y, self.width, self.height)
        health_rect = pg.Rect(x, y, current_width, self.height)
        pg.draw.rect(surface, WHITE, back_rect, 2)
        pg.draw.rect(surface, self.color, health_rect)
