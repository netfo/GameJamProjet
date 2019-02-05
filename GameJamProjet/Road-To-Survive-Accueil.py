#On importe pygame et ses modules dans la page
import pygame
import sys
from pygame.locals import *

#Initalisation du pygame
pygame.init()

#On nomme la page
pygame.display.set_caption("ROADtoSURVIVE Accueil")

#Création de la page 
fenetre = pygame.display.set_mode((700, 500))

#Chargement et collage du fond
fond = pygame.image.load("img/fond.png").convert()
fond= pygame.transform.scale(fond, (700, 620))
fenetre.blit(fond, (0,0))

#Couleurs
white= (255,255,255)

#On initialise le font
myfont = pygame.font.SysFont("Carlito", 40)

#On écrit le texte
label = myfont.render("ROADtoSURVIVE",1, white)
fenetre.blit(label, (220, 100))

#Image1
x=100
y=330
image = pygame.image.load("img/jouer.png").convert()
image= pygame.transform.scale(image, (150,100))
fenetre.blit(image, (x,y))

#Image2
x2=450
y2=330
image2= pygame.image.load("img/quitter.png").convert()
image2= pygame.transform.scale(image2, (150, 100))
fenetre.blit(image2, (x2,y2))

#Sons
# pygame.mixer.init()
# pygame.mixer.music.load("Star-Wars.mp3")
# pygame.mixer.music.play(-1)
# pygame.mixer.music.set_volume(0.3)


pygame.display.flip()

accueil = True
while accueil:

    #Si on ferme la fenetre, le programme s'arrete
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            accueil=False
            pygame.quit()


        #Gestion de la  musique avec les touches
        if event.type == KEYDOWN:
            #Cliquer sur ESPACE pour mettre une pause sur la musique
            if event.key == K_SPACE:
                pygame.mixer.music.pause()


            #Cliquer sur ENTRER pour reprendre la musique où elle a été arreté
            if event.key == K_RETURN:
                pygame.mixer.music.unpause()




            #Cliquer sur DROITE pour fermer la fenetre
            if event.key == K_RIGHT:
                accueil =False
                pygame.quit()
                pygame.display.flip()

        #Cliquer sur l'image de Maitre Yoda pour lancer le jeu
        if event.type == MOUSEBUTTONDOWN and event.button==1 and (100<event.pos[0]<250) and (330<event.pos[1]<480):
            accueil=0
            import space

        #Cliquer sur l'image de Dark Vador pour quitter
        if event.type == MOUSEBUTTONDOWN and event.button==1 and (500<event.pos[0]<650) and (330<event.pos[1]<480):
            accueil=0
            import Over



pygame.quit()
