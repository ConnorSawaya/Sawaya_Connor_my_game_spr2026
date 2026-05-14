import math
import random
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
        self.wave_time = 0

    def spawn_splash(self, game, center_x):
        for _ in range(150):
            angle = random.uniform(0.15, math.pi - 0.15)
            radius = random.uniform(8, 40)
            spawn_x = center_x + math.cos(angle) * radius
            spawn_y = self.water_top - math.sin(angle) * radius
            Water_particle(game, spawn_x, spawn_y)

    def update(self, dt, game): 
        # Starting delay of water rising for time to go upwards before water gets there
        self.wave_time += dt

        if pg.time.get_ticks() - self.start_time >= self.delay_ms: #Check for delay to start rising

            highest_player_y = min(game.player.hit_rect.top, game.player2.hit_rect.top) # Gets highest pos player y to calculate the speed of rising wave
            distance_above_water = self.water_top - highest_player_y
            catchup_speed = 0 # if the player is much higher than the water it will rise faster to catch up to them.

            if distance_above_water > TILESIZE * 6: # if player is more than 6 tiles above water -> increase catchup speed.
                catchup_speed = self.rise_speed * min(2.5, distance_above_water / (TILESIZE * 8)) # max catchup speed is 2.5 times normal rise speed

            self.height = min(self.world_height, self.height + (self.rise_speed + catchup_speed) * dt) # increase the height of the water based on rise speed and the catchup speed

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
            game.health.damage(WATER_DAMAGE * dt)
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
            wave_y = water_top + math.sin(self.wave_time * 4 + x * 0.03) * 4 # sine wave that changes over time
            screen_x = x + camera.camera.x 
            screen_y = wave_y + camera.camera.y 
            points.append((screen_x, screen_y))
 
        if len(points) > 1: # only draw the wave line if we have enough points
            pg.draw.lines(water_surface, self.wave_color, False, points, 2)

        surface.blit(water_surface, (0, 0)) # draws the water surface on the main screen

class Health: # Health class and health bar
    def __init__(self, game):
        self.game = game
        self.max_health = MAX_HEALTH
        self.current = self.max_health
        self.death_time = None
        self.restart_delay = 3000
        self.width = 100
        self.height = 12
        self.color = (255, 0, 0)

    def reset(self): # resets health stats
        self.current = self.max_health # reset health to max health, used for restarting the game
        self.death_time = None

    def damage(self, amount): # Damage function using for damage over time
        self.current = max(0, self.current - amount)
        if self.is_dead() and self.death_time is None:
            self.death_time = pg.time.get_ticks()

    def is_dead(self): # Checks if your dead
        return self.current <= 0 # Check if health is 0 or below to determine if player is dead

    def can_restart(self): # Check if you can restart based on the 3 seconds needed to wait after death before restarting,
        if not self.is_dead() or self.death_time is None:
            return False
        return pg.time.get_ticks() - self.death_time >= self.restart_delay

    def draw(self, surface, x, y): # Draw health bar + Text + Game Over and Restart Text when dead
        health_ratio = self.current / self.max_health # calculate health ratio for how much should be filled
        current_width = int(self.width * health_ratio) # calcualte current width of the health bar based on health ratio

        # Fonts 
        health_bar_font = pg.font.SysFont("copperplategothic", 18, bold=True) # font 
        health_amount_font = pg.font.SysFont("copperplategothic", 14, bold=True) # font for health amount text
        game_over_font = pg.font.SysFont("copperplategothic", 64, bold=True)
        restart_font = pg.font.SysFont("copperplategothic", 28, bold=True)

        # Texts for health bar
        health_text = health_bar_font.render("Health", True, WHITE)
        health_amount_text = health_amount_font.render(f"{int(self.current)} / {self.max_health}", True, WHITE)

        surface.blit(health_text, health_text.get_rect(center=(x + self.width / 2, y - 10))) # draws health bar above the actual bar
        surface.blit(health_amount_text, health_amount_text.get_rect(center=(x + self.width / 2, y + self.height + 15))) # draws health amount below the health bar

        pg.draw.rect(surface, WHITE, (x, y, self.width, self.height), 2)
        pg.draw.rect(surface, self.color, (x, y, current_width, self.height))
        
        if self.is_dead(): # When the player is dead(game over text, restart checker, and restart text)
            
            game_over_text = game_over_font.render("Game Over", True, RED)
            
            if self.can_restart():
                restart_message = "Press any key to Restart"
                restart_color = RED
            else:
                restart_message = ""
                restart_color = GREEN
            restart_text = restart_font.render(restart_message, True, restart_color) 
            surface.blit(game_over_text, game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
            surface.blit(restart_text, restart_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 60)))
           
            
