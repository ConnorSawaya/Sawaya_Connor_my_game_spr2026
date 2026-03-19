# game engine using template from Chris Bradfield's "Making Games with Python & Pygame"

'''
Sprite Sheet llama made  By CaptainBrosset
'''

import pygame as pg
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
        # project/script directory and image directory
        self.script_dir = self.game_dir
        self.img_dir = path.join(self.game_dir, 'images')
        # load shared spritesheet 
        try:
            self.sprite_sheet = Spritesheet(path.join(self.img_dir, 'sprite_sheet.png'))
        except Exception:
            # If spritesheet not present, leave attribute so callers can still reference it
            self.sprite_sheet = None
        
        self.map_generator = MapGenerator() # generates a random map using the MapGenerator class from utils.py
        self.map = self.map_generator.generate()  # Ensure this returns an iterable (list of lists)
        self.camera = Camera(self.map_generator.width * TILESIZE, self.map_generator.height * TILESIZE)
        print('data is loaded')

    def new(self):
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()
        #self.player = Player(self, 15, 15)
        #self.mob = Mob(self, 4, 4) 
        #self.wall = Wall(self, WIDTH/2/TILESIZE, HEIGHT/2/TILESIZE)
        for row, tiles in enumerate(self.map):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    # call class constructor without assigning variable...when
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
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
        print(len(self.all_sprites))
        # keep camera centered on the player once they exist
        if hasattr(self, 'player'):
            self.camera.update(self.player)

        
        

    
    def draw(self): # draws everything on the screen 

        self.screen.fill(BLUE) # Screen Fill Blue 

        self.camera.draw_world(self.screen, self.all_sprites) # Updats the circle for the camera
        if hasattr(self, 'player'):
            self.camera.apply_circular_mask(self.screen, self.player)
            
        # hud text should be drawn in screen space, not world space
        self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
        # self.draw_text(str(self.game_cooldown.time), 24, WHITE, WIDTH/2, HEIGHT/.5)
        self.draw_text(str(self.game_cooldown.ready()), 24, WHITE, WIDTH/2, HEIGHT/3)
        if hasattr(self, 'player'):
            self.draw_text(str(self.player.pos), 24, WHITE, WIDTH/2, HEIGHT/2)

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


    

    
