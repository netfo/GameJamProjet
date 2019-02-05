import pygame
from pygame.locals import *

#Ouverture de la fenêtre Pygame

fenetre = pygame.display.set_mode((640, 480))


#Rafraîchissement de l'écran

pygame.display.flip()


#BOUCLE INFINIE

continuer = 1

while continuer:

    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_SPACE:

            print("Espace")
            
        if event.type == QUIT:

            continuer = 0
