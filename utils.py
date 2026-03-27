import pygame as pg
from pygame.sprite import Sprite
from settings import *


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
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
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)
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


class line(Sprite):
    def draw_string_between_player_and_mob(surface, game):
        if not hasattr(game, 'player') or not hasattr(game, 'player2'):
            return
        if not SHOW_STRING:
            return

        player = game.player
        mob = game.player2
        dx = player.pos.x - mob.pos.x
        dy = player.pos.y - mob.pos.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        stretch = max(0, dist - STRING_DISTANCE)
        t = min(1.0, stretch / STRING_DISTANCE)
        r = int(255 * t)
        g = int(255 * (1 - t))
        color = (r, g, 0)
        thickness = 2 + int(t * 3)

        player_screen = game.camera.apply(player).center
        mob_screen = game.camera.apply(mob).center
        pg.draw.line(surface, color, player_screen, mob_screen, thickness)
