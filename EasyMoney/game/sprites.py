import pygame
from pygame.locals import *

from data import *
import math

TOP_SIDE    = 0
BOTTOM_SIDE = 2
LEFT_SIDE   = 3
RIGHT_SIDE  = 1

def speed_to_side(dx,dy):
    if abs(dx) > abs(dy):
        dy = 0
    else:
        dx = 0
    if dy < 0:
        return 0
    elif dx > 0:
        return 1
    elif dy > 0:
        return 2
    elif dx < 0:
        return 3
    else:
        return 0, 0

class Collidable(pygame.sprite.Sprite):

    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.collision_groups = []
        self.xoffset = 0
        self.yoffset = 0

    def collide(self, group):
        if group not in self.collision_groups:
            self.collision_groups.append(group)

    def move(self, dx, dy, collide=True):
        if collide:
            if dx!=0:
                dx  = self.__move(dx,0)
            if dy!=0:
                 dy = self.__move(0,dy)
        else:
            self.rect.move_ip(dx, dy)
        return dx, dy

    def clamp_off(self, sprite, side):
        if side == TOP_SIDE:
            self.rect.top = sprite.rect.bottom
        if side == RIGHT_SIDE:
            self.rect.right = sprite.rect.left
        if side == BOTTOM_SIDE:
            self.rect.bottom = sprite.rect.top
        if side == LEFT_SIDE:
            self.rect.left = sprite.rect.right

    def __move(self,dx,dy):
        oldr = self.rect
        self.rect.move_ip(dx, dy)
        side = speed_to_side(dx, dy)

        for group in self.collision_groups:
            for spr in group:
                if spr.rect.colliderect(self.rect):
                    self.on_collision(side, spr, group)

        return self.rect.left-oldr.left,self.rect.top-oldr.top

    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)

    def draw(self, surf):
        surf.blit(self.image, (self.rect[0]+self.xoffset, self.rect[1]+self.yoffset))

class Player(Collidable):

    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.left_images = []
        for i in self.right_images:
            self.left_images.append(pygame.transform.flip(i, 1, 0))
        self.image = self.right_images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.jump_speed = 0
        self.jump_accel = 0.3
        self.jumping = False
        self.frame = 0
        self.facing = 1
        self.angle = 0
        self.dying = False
        self.still_timer = 0
        self.hp = 1
        self.hit_timer = 0
        self.springing = False

    def kill(self):
        pygame.sprite.Sprite.kill(self)
        PlayerDie(self.rect.center, self.facing)

    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)
        if side == TOP_SIDE:
            self.jump_speed = 0
        if side == BOTTOM_SIDE:
            self.jump_speed = 0
            self.jumping = False
            self.springing = False
            if isinstance(sprite, Spring):
                self.jump_speed = -20
                sprite.spring_time = 5
                self.jumping = True
                self.springing = True
            if isinstance(sprite, Spring2):
                self.jump_speed = -13
                sprite.spring_time = 5
                self.jumping = True
                self.springing = True
            if isinstance(sprite, Brick):
                key = pygame.key.get_pressed()
                self.jump_speed = -5
                sprite.spring_time = 5
                self.jumping = True
                self.springing = True
                if key[K_z] or key[K_UP]:
                    self.jump_accel = 0.05
                else:
                    self.jump_accel = 0.4
            if isinstance(sprite, Platform):
                key = pygame.key.get_pressed()
                sprite.spring_time = 5
                self.jumping = False
                self.springing = False
                if key[K_z] or key[K_UP]:
                    self.jump_accel = 0.3
                else:
                    self.jump_accel = 0.6

    def hit(self):
        if self.hit_timer <= 0:
            self.hit_timer = 20
            self.hp -= 1
            if self.hp <= 0:
                self.kill()

    def jump(self):
        if not self.jumping and self.still_timer <= 0:
            self.jump_speed = -13
            self.jumping = True
            self.move(0, -4)

    def update(self):
        self.frame += 1
        self.still_timer -= 1
        self.hit_timer -= 1
        dx = 0
        key = pygame.key.get_pressed()

        if self.jump_speed < 8:
            self.jump_speed += self.jump_accel
        if self.jump_speed > 3:
            self.jumping = True

        if self.still_timer <= 0:
            if key[K_LEFT]:
                dx = -1
                self.facing = dx
            if key[K_RIGHT]:
                dx = 1
                self.facing = dx

        if self.facing > 0:
            self.image = self.right_images[0]
        if self.facing < 0:
            self.image = self.left_images[0]
        if dx > 0:
            self.image = self.right_images[self.frame/6%5]
        if dx < 0:
            self.image = self.left_images[self.frame/6%5]
        if self.facing > 0 and self.jumping:
            self.image = self.right_images[5]
        if self.facing < 0 and self.jumping:
            self.image = self.left_images[5]
        if self.hit_timer > 0:
            if not self.frame % 2:
                if self.facing > 0:
                    self.image = self.right_images[2]
                if self.facing < 0:
                    self.image = self.left_images[2]

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top >= 475:
            pygame.sprite.Sprite.kill(self)

        self.move(3*dx, self.jump_speed)

class Platform(Collidable):
    def __init__(self, pos, tile, l, r):
        Collidable.__init__(self, self.groups)
        self.image = self.images["platform-%s.png" % tile]
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = l
        self.on_right = r

class Brick(Collidable):
    def __init__(self, pos, tile, l, r):
        Collidable.__init__(self, self.groups)
        self.image = self.images["brick%s.png" % tile]
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = l
        self.on_right = r

class Spring(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.spring_time = 0
        self.on_left = False
        self.on_right = False
    def update(self):
        self.image = self.images[0]
        self.spring_time -= 1
        if self.spring_time > 0:
            self.image = self.images[1]

class Spring2(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.spring_time = 0
        self.on_left = False
        self.on_right = False
    def update(self):
        self.image = self.images[0]
        self.spring_time -= 1
        if self.spring_time > 0:
            self.image = self.images[1]

class Coin(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 0
    def update(self):
        self.frame += 1
        self.image = self.images[self.frame/6%4]

class CoinDie(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = pos)
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer < 12:
            self.image = self.images[self.timer/4%3]
        else:
            self.kill()

class PlayerDie(Collidable):
    def __init__(self, pos, facing):
        Collidable.__init__(self, self.groups)
        self.left_images = []
        for i in self.right_images:
            self.left_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = pos)
        self.facing = facing
        self.timer = 0

    def update(self):
        if self.facing > 0:
            self.images = self.right_images
        else:
            self.images = self.left_images
        self.timer += 1
        if self.timer <= 20:
            self.image = self.images[0]
        elif self.timer <= 45:
            self.image = self.images[1]
        elif self.timer <= 57:
            self.image = self.images[self.timer/4%3]
        else:
            self.kill()
