#On importe pygame et ses modules dans la page
import pygame,sys
from pygame.locals import *
import random

#On initialse pygame et ses modules
pygame.init()
pygame.font.init()
mainclock= pygame.time.Clock()

#On nomme la page
pygame.display.set_caption("Space-Adventurer-You Win")

#On crée la page avec ses dimensions 
fenetre = pygame.display.set_mode((600, 640))

#On crée le fond
fond = pygame.image.load("gamenwin.png").convert()
fond= pygame.transform.scale(fond, (600, 640))
fenetre.blit(fond, (0, 0))

#On crée la musique de fond
pygame.mixer.init()
pygame.mixer.music.load("Son-Gagner.mp3")
#On la lance
pygame.mixer.music.play(-1)
#On définit son volume
pygame.mixer.music.set_volume(0.3)

boucle=True

pygame.display.flip()
 

while boucle:
    #Si on ferme la fenetre, le programme s'arrete de s'executer
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            boulce=False
            pygame.quit()
            
                
        #Gestion de la  musique avec les touches
        if event.type == KEYDOWN: 
            #Cliquer sur ESPACE pour fermer l'écran
            if event.key == K_SPACE:
               pygame.quit()
        #Si on clique sur l'image de fond d'écran avec la souris, on lance le jeu
        if event.type == pygame.MOUSEBUTTONDOWN:
            if fond.get_rect().collidepoint(pygame.mouse.get_pos()):
                boucle=0
                #On importe le fichier space
                import space
