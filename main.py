# game engine using template from Chris Bradfield's "Making Games with Python & Pygame"

"""
Sprite Sheet llama made By CaptainBrosset
Codex for the Wave made by ChatGPT
Some parts are asked by chatgpt but mostly it was for debugging and code that had been removing
"""

import pygame as pg
from os import path
import settings
from settings import *
from sprites import *  # Ensure Camera is imported
from utils import *


class Game:
    def __init__(self):
        pg.init()
        pg.font.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.paused = False

    def load_data(self):
        self.game_dir = path.dirname(__file__)
        self.img_dir = IMG_DIR

        ###################---Sound Loading---###################
        try: # jump sound loading
            if not pg.mixer.get_init():
                pg.mixer.init()
            settings.jump_sound = pg.mixer.Sound(path.join(SOUND_DIR, "jump.wav"))
        except pg.error: # if theres a error loading in sound will set it to none so it wont crash
            settings.jump_sound = None
        try: # splash sound loading
            if not pg.mixer.get_init():
                pg.mixer.init()
            settings.splash_sound = pg.mixer.Sound(path.join(SOUND_DIR, "water_splash.wav"))
        except pg.error:# if theres a error loading in sound will set it to none so it wont crash
            settings.splash_sound = None
        try: # congrats sound loading
            if not pg.mixer.get_init():
                pg.mixer.init()
            settings.congrats_sound = pg.mixer.Sound(path.join(SOUND_DIR, "congrats.wav"))
        except pg.error: # if theres a error loading in sound will set it to none so it wont crash
            settings.congrats_sound = None
        ###################---Sound Loading---###################


        ###################---Image Loading---###################
        try: # background loading 
            self.background = pg.image.load(self.img_dir + '/background.png').convert()
            self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))
        except pg.error: # if theres a error it will load the solid blue background instead of a crash
            self.background = pg.Surface((WIDTH, HEIGHT))
            self.background.fill(SKY_BLUE)
            print(f"background error {pg.error}")

        try: # sprite sheet loading
            self.sprite_sheet = Spritesheet(path.join(self.img_dir, 'sprite_sheet.png')) 
        except Exception:
            self.sprite_sheet = None

        ###################---Image Loading---###################

        # Map loading 
        map_path = path.join(self.game_dir, 'level1.txt') # loads the level 1
        with open(map_path, 'r') as f:
            self.map = [line.rstrip('\n') for line in f]


        self.camera = Camera(len(self.map[0]) * TILESIZE, len(self.map) * TILESIZE)  # Camera must be defined in sprites.py
        print('data is loaded')

    def new(self): # Start a new game
        self.playing = True
        self.paused = False
        self.load_data() # loads all data first of images and sounds and map 
        #loading sprites
        self.all_sprites = pg.sprite.Group() 
        self.all_walls = pg.sprite.Group()
        self.confetti = []
        self.dead_printed = False
        self.health = Health(self)
        self.health.reset()

        self.water = Water(self.camera.width, self.camera.height)

        for row, tiles in enumerate(self.map):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'F': # fall through platforms
                    FakePlatform(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    self.player2 = Player2(self, col, row)
        self.run()

    def run(self):
        while self.running and self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()

            if not self.paused: # Update and draw if not paused
                self.update() 
            self.draw()

    def events(self):
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                # Paused toggle check
            if event.type == pg.KEYDOWN and event.key == pg.K_p and not self.health.is_dead():
                self.paused = not self.paused
            if self.health.can_restart() and event.type == pg.KEYDOWN and event.key != pg.K_p:
                 self.playing = False


    def quit(self):
        pass

    def update(self):
        self.water.update(self.dt, self)
        if self.health.is_dead() and not self.dead_printed:
            print("died")
            self.dead_printed = True
            
        self.all_sprites.update()
        if hasattr(self, 'player'): # Only update camera if player exists
            self.camera.update(self.player) # Update camera to follow player

    def draw(self):
        self.screen.blit(self.background, (0, 0)) # Background Code From Chatgpt prompt was basically asking how to change the blue to a image

        self.camera.draw_world(self.screen, self.all_sprites) # Draw the world using the camera's draw_world method
        self.water.draw(self.screen, self.camera)

        if hasattr(self, 'player') and hasattr(self, 'player2'): # check if both players exist 
            line.draw_string_between_player_and_player2(self.screen, self) # Draw String methond

        if hasattr(self, 'player'): 
            self.camera.apply_circular_mask(self.screen, self.player)
            self.draw_text("P1: WASD/W   P2: Arrow Keys", 24, WHITE, WIDTH / 2, 15) # Controlls text on screen
            self.health.draw(self.screen, 20, 50)
        if self.paused: # paused text
            self.draw_text("Paused", 48, WHITE, WIDTH / 2, HEIGHT / 2)

        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    g = Game()

    while g.running:
        g.new()

pg.quit()
