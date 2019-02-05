#! /usr/bin/env python

import pygame, sys
from pygame.locals import *

from game import *
from ezmenu import *
from data import *
from cutscenes import *

def RunGame(screen):
    Game(screen)
    play_music("title.ogg", 0.75)





class Menu(object):

    def __init__(self, screen):
        self.screen = screen
        self.menu = EzMenu(["Jouer", lambda: RunGame(screen)], ["Quitter", sys.exit])
        self.menu.set_highlight_color((255, 0, 0))
        self.menu.set_normal_color((255, 255, 255))
        self.menu.center_at(300, 400)
        self.menu.set_font(pygame.font.Font(filepath("fonts/font.ttf"), 16))
        self.bg = load_image("menu.png")
        self.font = pygame.font.SysFont("Carlito", 16)
        self.font2 = pygame.font.SysFont("Carlito", 45)
        play_music("title.ogg", 0.75)
        self.clock = pygame.time.Clock()
        events = pygame.event.get()
        self.menu.update(events)
        self.menu.draw(self.screen)
        self.main_loop()

    def main_loop(self):
        while 1:
            self.clock.tick(40)
            events = pygame.event.get()
            self.menu.update(events)
            for e in events:
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
