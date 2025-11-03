import pygame
from enum import *

pygame.init()

pygame.display.set_caption("Blue Prince")
screen = pygame.display.set_mode((1080,720))

background = pygame.image.load('image/Fond.png') #fausra changer la grenouille
running = True
while running:
    #Appliquer l'arrière plan
    screen.blit(background,(0,0))

    #mettre à jour la fenetre
    pygame.display.flip()

    # Ferme la fenetre si le joueur clique sur croix
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("fermeture du jeu")