#Blue_Prince
#Tuto bien : Graven développement, créer un jeu en python

import pygame
from joueur import*
from jeu import*

pygame.init()

pygame.display.set_caption("Blue Prince")
screen = pygame.display.set_mode((1080,720))

#charger l'arrière plan
background = pygame.image.load('image/Fond.png') #fausra changer la grenouille
#charger le jeu
game = Game()

running = True
while running:
    #Appliquer l'arrière plan
    screen.blit(background,(0,0))

    #Appliquer l'image du joueur
    screen.blit(game.player.image,game.player.rect)

    #mettre à jour la fenetre
    pygame.display.flip()

    # Ferme la fenetre si le joueur clique sur croix
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("fermeture du jeu")
        #Détecter le clavier
        elif event.type == pygame.KEYDOWN:
            #quelle touche est appuyé
            if event.key == pygame.K_RIGHT:
                print("déplacement vers la droite")
                game.player.droite()
            elif event.key == pygame.K_LEFT:
                game.player.gauche()
            elif event.key == pygame.K_UP:
                game.player.haut()
            elif event.key == pygame.K_DOWN:
                game.player.bas()
