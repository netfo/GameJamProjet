import pygame
from pygame.locals import *

from data import *
from sprites import *

class Level:

    def __init__(self, lvl=1):
        self.level = pygame.image.load(filepath("lvl.png")).convert()
        self.x = 0
        self.y = 0
        for y in range(self.level.get_height()):
            self.y = y
            for x in range(self.level.get_width()):
                self.x = x
                color = self.level.get_at((self.x, self.y))
                if color == (0, 0, 0, 255):
                    l=r=False
                    tile = "middle"
                    if self.get_at(0, -1) != (0, 0, 0, 255):
                        tile = "top"
                    if self.get_at(-1, 0) != (0, 0, 0, 255):
                        l=True
                    if self.get_at(1, 0) != (0, 0, 0, 255):
                        r=True
                    Platform((self.x*32, self.y*32), tile, l, r)

                if color == (109, 127, 63, 255):
                    l=r=False
                    tile = "1"
                    if self.get_at(0, -1) != (109, 127, 63, 255):
                        tile = "2"
                    if self.get_at(-1, 0) != (109, 127, 63, 255):
                        l=True
                    if self.get_at(1, 0) != (109, 127, 63, 255):
                        r=True
                    Brick((self.x*32, self.y*32), tile, l, r)

                if color == (255, 255, 0, 255):
                    Coin((self.x*32 + 4, self.y*32 + 4))
                if color == (0, 200, 0, 255):
                    Spring((self.x*32, self.y*32))
                if color == (0, 220, 0, 255):
                    Spring2((self.x*32, self.y*32))

    def get_at(self, dx, dy):
        try:
            return self.level.get_at((self.x+dx, self.y+dy))
        except:
            pass

    def get_size(self):
        return [self.level.get_size()[0]*32, self.level.get_size()[1]*32]
