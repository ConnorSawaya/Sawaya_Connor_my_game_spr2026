# game engine using template from Chris Bradfield's "Making Games with Python & Pygame"

"""
Sprite Sheet llama made By CaptainBrosset
"""

import pygame as pg
from os import path
from settings import *
from sprites import *
from utils import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True

    def load_data(self):
        self.game_dir = path.dirname(__file__)

        self.background = pg.image.load(path.join(self.img_dir, 'background.png')).convert()
        self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))
        try:
            self.sprite_sheet = Spritesheet(path.join(self.img_dir, 'sprite_sheet.png'))
        except Exception:
            self.sprite_sheet = None

        map_path = path.join(self.game_dir, 'level1.txt')
        with open(map_path, 'r') as f:
            self.map = [line.rstrip('\n') for line in f]


        self.camera = Camera(len(self.map[0]) * TILESIZE, len(self.map) * TILESIZE)
        print('data is loaded')

    def new(self):
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()

        for row, tiles in enumerate(self.map):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(
                        self,
                        col,
                        row,
                        controls={"left": pg.K_a, "right": pg.K_d, "jump": pg.K_w},
                        color=WHITE,
                    )
                if tile == 'M':
                    self.player2 = Player2(self, col, row)
        self.run()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False



            if event.type == pg.KEYDOWN and event.key == pg.K_t: # Checks for t press
                import settings
                settings.SHOW_STRING = not settings.SHOW_STRING # Check toggle for showing the string between player and player2



    def quit(self):
        pass

    def update(self):
        self.all_sprites.update()
        if hasattr(self, 'player'): # Only update camera if player exists
            self.camera.update(self.player) # Update camera to follow player

    def draw(self):
        self.screen.blit(self.background, (0, 0)) # Background Code From Chatgpt prompt was basically asking how to change the blue to a image

        self.camera.draw_world(self.screen, self.all_sprites) # Draw the world using the camera's draw_world method

        if hasattr(self, 'player') and hasattr(self, 'player2'):
            line.draw_string_between_player_and_player2(self.screen, self) # Draw String methond

        if hasattr(self, 'player'): 
            self.camera.apply_circular_mask(self.screen, self.player)
            self.draw_text("P1: WASD/W   P2: Arrow Keys", 24, WHITE, WIDTH / 2, 15) # Controlls text on screen

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
