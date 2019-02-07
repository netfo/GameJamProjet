import pygame, os
from pygame.locals import *


import data, menu

import menu,data

def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.mouse.set_visible(0)
    pygame.display.set_icon(pygame.image.load(data.filepath("coin1.png")))
    pygame.display.set_caption("Easy Money")
    screen = pygame.display.set_mode((640, 480))
    menu.Menu(screen)

main();
