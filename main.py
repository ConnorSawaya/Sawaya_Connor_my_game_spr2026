# game engine using template from Chris Bradfield's "Making Games with Python & Pygame"
# I can push from vscode
'''
'''

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from utils import *
vec = pg.math.Vector2

# import settings


# the game class that will be instantiated in order to run the game...
class Game:
    def __init__(self):
        pg.init()
        # setting up pygame screen using tuple value for width height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE) # window title (from settings
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.game_cooldown = Cooldown(5000) # cooldown thing 
        

    
    # a method is a function tied to a Class

    def load_data(self):
        self.game_dir = path.dirname(__file__)
        self.map = Map(path.join(self.game_dir, 'level1.txt'))
        print('data is loaded')

def new(self):
    self.load_data()
    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_mobs = pg.sprite.Group()
    # self.player = Player(self, 15, 15)
    # self.mob = Mob(self, 4, 4) 
    #  self.wall = Wall(self, WIDTH/2/TILESIZE, HEIGHT/2/TILESIZE)
    for row, tiles in enumerate(self.map.data):
        for col, tile, in enumerate(tiles):
            if tile == '1':
                # call class constructor without assigning variable...when
                Wall(self, col, row)
            if tile == 'P':
                self.player = Player(self, col, row)
        self.run()
   

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000 # Clock Ticks in seconds
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
        

    def quit(self):
        pass

    def update(self):
        self.all_sprites.update() # Updates all sprites 
        
        

    
    def draw(self): # draws everything on the screen 
        self.screen.fill(BLUE) # Screen Fill Blue 
        self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
        # self.draw_text(str(self.game_cooldown.time), 24, WHITE, WIDTH/2, HEIGHT/.5)
        self.draw_text(str(self.game_cooldown.ready()), 24, WHITE, WIDTH/2, HEIGHT/3)
        self.draw_text(str(self.player.pos), 24, WHITE, WIDTH/2, HEIGHT/2)
        self.all_sprites.draw(self.screen)

       
        pg.display.flip() # Update the full display Surface to the screen

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

if __name__ == "__main__": 
    g = Game()

while g.running: # while game is running 
    g.new() # start a new game


pg.quit()


    

    
