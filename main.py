#Tuto bien : Graven développement, créer un jeu en python

import pygame
from joueur import*
from jeu import*
#from module1 import*

pygame.init()

pygame.display.set_caption("Blue Prince")
screen = pygame.display.set_mode((1080,720))

#charger l'arrière plan
background = pygame.image.load('image/Fond.png')

#charger l'entrée
#entrance_room = Room
entrance = pygame.image.load('image/Entrance_Hall.png')
entrance = pygame.transform.scale(entrance,(80,80))
#charger le jeu
game = Game()

running = True
while running:
    #Appliquer l'arrière plan
    screen.blit(background,(0,0))

    #appliquer la pièce d'entrée
    screen.blit(entrance,(160,640))

    #Appliquer l'image du joueur
    screen.blit(game.player.pion,game.player.rect)

    #mettre à jour la fenetre
    pygame.display.flip()

    #initialisation de la pièce dans laquelle on est
    #room = entrance_room

    # Ferme la fenetre si le joueur clique sur croix
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("fermeture du jeu")
        #Détecter le clavier
        elif event.type == pygame.KEYDOWN:
            #quelle touche est appuyé
            if event.key == pygame.K_RIGHT and game.player.rect.x + game.player.velocity < 400:
                game.player.pion = pygame.transform.rotate(game.player.direction, -90) #pour indiquer la direction que la joueur choisit
                screen.blit(game.player.pion,game.player.rect)
                pygame.display.flip()
                
                game.player.droite()

            elif event.key == pygame.K_LEFT and game.player.rect.x - game.player.velocity > 0:
                game.player.pion = pygame.transform.rotate(game.player.direction, 90) #pour indiquer la direction que la joueur choisit
                screen.blit(game.player.pion,game.player.rect)
                pygame.display.flip()

                game.player.gauche()

            elif event.key == pygame.K_UP and game.player.rect.y - game.player.velocity > 0:
                game.player.pion = game.player.direction
                screen.blit(game.player.pion,game.player.rect)
                pygame.display.flip()

                game.player.haut()

            elif event.key == pygame.K_DOWN and game.player.rect.y + game.player.velocity < 720:
                game.player.pion = pygame.transform.rotate(game.player.direction, 180) #pour indiquer la direction que la joueur choisit
                screen.blit(game.player.pion,game.player.rect)
                pygame.display.flip()

                game.player.bas()
