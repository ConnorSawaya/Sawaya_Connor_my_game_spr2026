from os import path
import pygame as pg
from pygame.sprite import Sprite
from settings import *


vec = pg.math.Vector2


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def collide_with_player(sprite, other, direction):
    if not sprite.hit_rect.colliderect(other.hit_rect):
        return

    if direction == 'x':
        if other.hit_rect.centerx > sprite.hit_rect.centerx:
            sprite.pos.x = other.hit_rect.left - sprite.hit_rect.width / 2
        if other.hit_rect.centerx < sprite.hit_rect.centerx:
            sprite.pos.x = other.hit_rect.right + sprite.hit_rect.width / 2
        sprite.vel.x = 0
        sprite.hit_rect.centerx = sprite.pos.x

    if direction == 'y':
        if other.hit_rect.centery > sprite.hit_rect.centery:
            sprite.pos.y = other.hit_rect.top - sprite.hit_rect.height / 2
        if other.hit_rect.centery < sprite.hit_rect.centery:
            sprite.pos.y = other.hit_rect.bottom + sprite.hit_rect.height / 2
        sprite.vel.y = 0
        sprite.hit_rect.centery = sprite.pos.y


def collide_with_walls(sprite, group, direction):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if not hits:
        return

    if direction == 'x':
        if hits[0].rect.centerx > sprite.hit_rect.centerx:
            sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
        if hits[0].rect.centerx < sprite.hit_rect.centerx:
            sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
        sprite.vel.x = 0
        sprite.hit_rect.centerx = sprite.pos.x

    if direction == 'y':
        if hits[0].rect.centery > sprite.hit_rect.centery:
            sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
        if hits[0].rect.centery < sprite.hit_rect.centery:
            sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
        sprite.vel.y = 0
        sprite.hit_rect.centery = sprite.pos.y


class Player(Sprite):
    def __init__(self, game, x, y, controls=None, color=WHITE):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.controls = controls or {
            "left": pg.K_a,
            "right": pg.K_d,
            "jump": pg.K_w,
        }
        self.sprite_sheet = getattr(self.game, 'sprite_sheet', None)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.jumping = False
        self.moving = False
        self.on_ground = False
        self.last_update = 0
        self.current_frame = 0
        if self.sprite_sheet:
            self.load_image()
        else:
            self.standing_frames = [self.image]
            self.moving_frames = [self.image]

    def get_keys(self):
        self.vel.x = 0
        keys = pg.key.get_pressed()
        if keys[self.controls["left"]]:
            self.vel.x = -PLAYER_SPEED
        if keys[self.controls["right"]]:
            self.vel.x = PLAYER_SPEED
        if keys[self.controls["jump"]] and self.on_ground:
            self.vel.y = -JUMP_FORCE
            self.on_ground = False
        self.moving = self.vel.x != 0

    def load_image(self):
        self.standing_frames = [
            self.sprite_sheet.get_image(0, 0, TILESIZE, TILESIZE),
            self.sprite_sheet.get_image(0, TILESIZE, TILESIZE, TILESIZE),
        ]
        self.moving_frames = [
            self.sprite_sheet.get_image(TILESIZE, 0, TILESIZE, TILESIZE),
            self.sprite_sheet.get_image(TILESIZE, TILESIZE, TILESIZE, TILESIZE),
        ]

        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        for frame in self.moving_frames:
            frame.set_colorkey(BLACK)

    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.moving:
            if now - self.last_update > 3500:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
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

    def update(self):
        self.animate()
        self.get_keys()
        self.vel.y += GRAVITY * self.game.dt # Apply gravity to vertical velocity
        if self.vel.y > MAX_FALL_SPEED:
            self.vel.y = MAX_FALL_SPEED

        # Apply string force from player2 to the player
        player2 = self.game.player2
        dx = player2.pos.x - self.pos.x 
        dy = player2.pos.y - self.pos.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        # Apply string force if stretched beyond rest length
        if dist > STRING_DISTANCE and dist > 0:
            direction = vec(dx, dy).normalize()
            stretch = dist - STRING_DISTANCE
            self.vel += direction * PLAYER_STRING_SPRING_K * stretch

        self.pos.x += self.vel.x * self.game.dt # moves player horizontally
        self.hit_rect.centerx = self.pos.x # Update hit rect for horizontal movement
        collide_with_walls(self, self.game.all_walls, 'x') # Check for horizontal collisions
        collide_with_player(self, self.game.player2, 'x')
        self.pos.x = self.hit_rect.centerx # Update player position after horizontal collisions

        self.on_ground = False # Assume player is in the air until we check for collisions
        was_falling = self.vel.y > 0 # checks for falling player
        self.pos.y += self.vel.y * self.game.dt # moves player vertically
        self.hit_rect.centery = self.pos.y # Update hit rect for vertical movement
        collide_with_walls(self, self.game.all_walls, 'y')
        collide_with_player(self, self.game.player2, 'y')


        # Update player position after vertical collisions
        self.pos.y = self.hit_rect.centery
        if was_falling and self.vel.y == 0:
            self.on_ground = True

        self.rect.center = self.hit_rect.center # Update sprite rect to match hit rect




class Player2(Sprite): # another player that is controlled by the player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.on_ground = False

    def get_keys(self): # Checks key input 
        self.vel.x = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:  self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT]: self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] and self.on_ground: self.vel.y = -JUMP_FORCE; self.on_ground = False

        
    def update(self):
        self.get_keys()
        self.vel.y += GRAVITY * self.game.dt
        if self.vel.y > MAX_FALL_SPEED:
            self.vel.y = MAX_FALL_SPEED

        dx = self.game.player.pos.x - self.pos.x
        dy = self.game.player.pos.y - self.pos.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist > STRING_DISTANCE and dist > 0:
            direction = vec(dx, dy).normalize()
            stretch = dist - STRING_DISTANCE
            self.vel += direction * STRING_SPRING_K * stretch
        # Applys Slingshot Force
        self.pos.x += self.vel.x * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        collide_with_player(self, self.game.player, 'x')
        self.pos.x = self.hit_rect.centerx
        # Applys Slingshot Force
        self.on_ground = False # Assume player is in the air until we check for collisions
        was_falling = self.vel.y > 0 # checks for falling player
        self.pos.y += self.vel.y * self.game.dt # moves player vertically
        self.hit_rect.centery = self.pos.y # Update hit rect for vertical movement
        # Check for vertical collisions with walls and player
        collide_with_walls(self, self.game.all_walls, 'y')
        collide_with_player(self, self.game.player, 'y')
        self.pos.y = self.hit_rect.centery

        if was_falling and self.vel.y == 0: # checks for landing player
            self.on_ground = True

        self.rect.center = self.hit_rect.center  # Update sprite rect to match hit rect


class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load(path.join(self.game.img_dir, 'wall.png')).convert()
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos

    def update(self):
        pass











class Projectile(Sprite):
    def __init__(self, game, x, y, direction=None):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((8, 8))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.speed = 400
        if direction is not None and direction.length() > 0:
            self.vel = direction.normalize() * self.speed
        else:
            self.vel = vec(1, 0) * self.speed
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.vel.y += GRAVITY * self.game.dt
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollide(self, self.game.all_walls, False):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > 2000:
            self.kill()
