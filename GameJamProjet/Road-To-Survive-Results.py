#On importe pygame et ses modules dans la page
import pygame,sys
from pygame.locals import *
import random

#On initialse pygame et ses modules
pygame.init()
pygame.font.init()
mainclock= pygame.time.Clock()

#On nomme la page
pygame.display.set_caption("ROADtoSURVIVE-Results")

#On crée la page avec ses dimensions
fenetre = pygame.display.set_mode((600, 620))

#Chargement et collage du fond
fond = pygame.image.load("img/fond.png").convert()
fond= pygame.transform.scale(fond, (700, 620))
fenetre.blit(fond, (0,0))

#Couleurs
white= (255,255,255)
navyblue = (0,0,128)
bright_red = (255,0,0)

#On initialise le font
myfont = pygame.font.SysFont("Carlito", 40)

#On écrit le texte
label = myfont.render("ROADtoSURVIVE",1, white)
fenetre.blit(label, (165, 100))

#Distance Parcourue
myfont = pygame.font.SysFont("Carlito", 30)
start = myfont.render("Distance Parcourue: ",1, white)
fenetre.blit(start, (80, 280))

#Score
myfont = pygame.font.SysFont("Carlito", 30)
exit = myfont.render("Score: ",1, white)
fenetre.blit(exit, (250, 320))

# #Image1
# x=100
# y=430
# image = pygame.image.load("img/rejouer.png").convert()
# image= pygame.transform.scale(image, (150,100))
# fenetre.blit(image, (x,y))
#
# #Image2
# x2=350
# y2=430
# image2= pygame.image.load("img/quitter.png").convert()
# image2= pygame.transform.scale(image2, (150, 100))
# fenetre.blit(image2, (x2,y2))

#On crée la musique de fond
# pygame.mixer.init()
# pygame.mixer.music.load("Son-Gagner.mp3")
# #On la lance
# pygame.mixer.music.play(-1)
# #On définit son volume
# pygame.mixer.music.set_volume(0.3)

boucle=True

pygame.display.flip()

def text_objects(text, font):
    font = pygame.font.SysFont("Carlito",20)
    textSurface = font.render(text, True,  (255, 0, 0))
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(pygame.Surface([200,50]), ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(pygame.Surface([200,50]), ic,(x,y,w,h))

    smallText = pygame.font.SysFont("Carlito",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    fenetre.blit(textSurf, textRect)



button("Quitter",300,450,30,50,None,navyblue,None)


while boucle:
    #Si on ferme la fenetre, le programme s'arrete de s'executer
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            boucle=False
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
                pygame.quit()
