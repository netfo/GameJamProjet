#! /usr/bin/env python

import pygame, sys
from pygame.locals import *

from game import *
from ezmenu import *
from data import *
from cutscenes import *

def RunGame(screen):
    Game(screen)
    # play_music("title.ogg", 0.75)
def Credit(screen):
    cutscene(screen, ["Credits",
    "",
    "BULOT Andy : Developpeur",
    "BOISSIN Rowin : Developpeur",
    "FERNANDEZ Thibaud : Chef de groupe",
    "FOURRIER Quentin : Developpeur",
    "SEBAG Samuel : Developpeur",
    ""])
def source(screen):
    cutscene(screen, ["Source",
    "",
    "https://openclassrooms.com/fr/",
    "courses/235344-apprenez-a-",
    "programmer-en-python",
    "",
    "https://www.pygame.org/",
    "",
    "https://www.python.org/",
    ""])

class Menu(object):

    def __init__(self, screen):
        self.screen = screen
        self.menu = EzMenu(["Jouer", lambda: RunGame(screen)],["Credits", lambda: Credit(screen)],["Source", lambda: source(screen)],["Quitter", sys.exit],)

        # couleur par defaut
        self.menu.set_normal_color((255, 255, 255))
        self.menu.center_at(300, 400)
        self.bg = load_image("menu.png")
        self.font = pygame.font.SysFont("Carlito", 16)
        self.font2 = pygame.font.SysFont("Carlito", 45)
        self.main_loop()

    def main_loop(self):
        while 1:
            events = pygame.event.get()
            self.menu.update(events)
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    pygame.quit()
                    return

            self.screen.blit(self.bg, (0, 0))
            ren = self.font2.render("ROAD to SURVIVE ", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 180))
            ren = self.font2.render("Python", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 235))
            self.menu.draw(self.screen)
            pygame.display.flip()
