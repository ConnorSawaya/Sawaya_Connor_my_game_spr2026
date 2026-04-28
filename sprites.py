from os import path
import random
import pygame as pg
from pygame.sprite import Sprite
import settings
from settings import *


vec = pg.math.Vector2


def tile_center(x, y): # 
    return vec(x + 0.5, y + 0.5) * TILESIZE


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def collide_with_player(sprite, other, direction): # 
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


def handle_water(sprite, up_pressed, down_pressed): # Water function made my codex (prompt was basically asking for how to make a water check effect on the players when there are inside the water and change their players movement)
    if not hasattr(sprite.game, "water") or not sprite.game.water.is_touching(sprite): # checks for water and if player is touching it
        return False

    water_top = sprite.game.water.surface_y() #top of the water in y cord
    depth = max(0, sprite.hit_rect.bottom - water_top) # checks depth of player
    depth_ratio = min(1, depth / TILESIZE) # normalizes depth
    near_surface = sprite.hit_rect.top <= water_top + TILESIZE * 0.35

    # Keep some resistance and buoyancy in water without making movement feel too stiff.
    sprite.vel.x *= 0.97
    sprite.vel.y *= 0.99
    sprite.vel.y += 70 * sprite.game.dt
    sprite.vel.y -= 150 * depth_ratio * sprite.game.dt

    if up_pressed: # If up is pressed, apply upward force to player
        if near_surface:
            sprite.vel.y = min(sprite.vel.y, -JUMP_FORCE * 0.8)
        else:
            sprite.vel.y -= 520 * sprite.game.dt
    elif down_pressed:
        sprite.vel.y += 300 * sprite.game.dt

    # checks for max speed and if it is above max speed, set it to max speed
    if sprite.vel.y < -300:
        sprite.vel.y = -300
    if sprite.vel.y > 460:
        sprite.vel.y = 460
    return True


def apply_vertical_physics(sprite):
    if not (hasattr(sprite.game, "water") and sprite.game.water.is_touching(sprite)):
        sprite.vel.y += GRAVITY * sprite.game.dt
    if sprite.vel.y > MAX_FALL_SPEED:
        sprite.vel.y = MAX_FALL_SPEED


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
        self.pos = tile_center(x, y)
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.rect.center = self.pos
        self.hit_rect.center = self.pos
        self.jumping = False
        self.moving = False
        self.on_ground = False
        self.congrats_played = False
        self.last_update = 0
        self.current_frame = 0
        if self.sprite_sheet:
            self.load_image()
        else:
            self.standing_frames = [self.image]
            self.moving_frames = [self.image]

    def get_keys(self):
        keys = pg.key.get_pressed()
        in_water = hasattr(self.game, "water") and self.game.water.is_touching(self)
        move_speed = PLAYER_SPEED * 0.55 if in_water else PLAYER_SPEED

        self.vel.x = 0
        if keys[self.controls["left"]]:
            self.vel.x = -move_speed
        if keys[self.controls["right"]]:
            self.vel.x = move_speed


        if handle_water(self, keys[self.controls["jump"]], keys[pg.K_s]):
            pass
        elif keys[self.controls["jump"]] and self.on_ground:
            self.vel.y = -JUMP_FORCE
            self.on_ground = False
            if settings.jump_sound:
                settings.jump_sound.set_volume(0.5)
                settings.jump_sound.play()
            
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
        if not self.jumping and not self.moving: # Standing still check
            if now - self.last_update > 3500: 
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.moving: # Animate moving frames
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
        apply_vertical_physics(self) # applys gravity and water physics to player
        
        if self.hit_rect.top <= CONGRATS_SOUND_THRESHOLD and not self.congrats_played:
            if settings.congrats_sound:
                settings.congrats_sound.set_volume(0.5)
                settings.congrats_sound.play()
            # confetti particles
            for _ in range(40):
                self.game.confetti.append(Confetti(self.game, self.rect.centerx, self.rect.centery))
            self.congrats_played = True

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

        # Move player and handle collisions
        self.pos.x += self.vel.x * self.game.dt # moves player horizontally
        self.hit_rect.centerx = self.pos.x # Update hit rect for horizontal movement
        collide_with_walls(self, self.game.all_walls, 'x') # Check for horizontal collisions
        collide_with_player(self, self.game.player2, 'x')
        self.pos.x = self.hit_rect.centerx # Update player position after horizontal collisions

        # Apply vertical movement and check for collisions
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
        # Update sprite rect to match hit rect
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
        self.pos = tile_center(x, y)
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.rect.center = self.pos
        self.hit_rect.center = self.pos
        self.on_ground = False

    def get_keys(self): # Checks key input 
        keys = pg.key.get_pressed()
        in_water = hasattr(self.game, "water") and self.game.water.is_touching(self)
        move_speed = PLAYER_SPEED * 0.55 if in_water else PLAYER_SPEED

        self.vel.x = 0
        if keys[pg.K_LEFT]:  self.vel.x = -move_speed # If left is pressed, set velocity to move left
        if keys[pg.K_RIGHT]: self.vel.x = move_speed # If right is pressed, set velocity to move right

        # water handling for player2, same as player1 but with arrow keys and s for down instead of w for jump
        if handle_water(self, keys[pg.K_UP], keys[pg.K_DOWN]):
            pass
        elif keys[pg.K_UP] and self.on_ground: self.vel.y = -JUMP_FORCE; self.on_ground = False # if jump is pressed and player is on the ground, apply jump force and set on_ground to false
        
    def update(self):
        self.get_keys() # check keys
        apply_vertical_physics(self) # sets up physics

        # Slingshot
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


class Wall(Sprite): # wall class 
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        wall_path = path.join(self.game.img_dir, 'wall.png')
        if not path.exists(wall_path):
            wall_path = path.join(self.game.img_dir, 'Wall.png')
        self.image = pg.image.load(wall_path).convert()
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = tile_center(x, y)
        self.rect.center = self.pos

    def update(self):
        pass


class Confetti(Sprite): # Confetti class for when player wins
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((4, 4))
        self.image.fill(BLACK) 
        self.image.set_colorkey(BLACK)
        self.image.fill(random.choice([RED, YELLOW, GREEN, WHITE, SKY_BLUE])) # makes the confetti random colors
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(random.uniform(-180, 180), random.uniform(-260, -80)) # random velocity 
        self.rect.center = self.pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.vel.y += 500 * self.game.dt # makes the confetti fall down 
        self.pos += self.vel * self.game.dt # updates pos 
        self.rect.center = self.pos # updates rec to match pos
        if pg.time.get_ticks() - self.spawn_time > 1500: # kils the confetti after 1.5 seconds
            if hasattr(self.game, "confetti") and self in self.game.confetti: # removes confetti if it exists
                self.game.confetti.remove(self) # removes confetti from the game confetti list
            self.kill() # kills sprite compeltely
