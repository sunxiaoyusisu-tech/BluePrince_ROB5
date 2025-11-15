import pygame
from joueur import*
from jeu import*
#from module1 import*

pygame.init()
pygame.font.init()

pygame.display.set_caption("Blue Prince")

screen = pygame.display.set_mode((1280,740))

direction = "haut" # Position par défaut au début du jeu

#charger l'arrière plan
background= (30, 30, 100)

#charger l'entrée
entrance = pygame.image.load('Rooms/Entrance_Hall.png')
entrance = pygame.transform.scale(entrance,(80,80))

#charger l'entrée
antechamber = pygame.image.load('Rooms/Antechamber.png')
antechamber = pygame.transform.scale(antechamber,(80,80))

#charger le jeu
game = Game()

running = True
while running:
    #Appliquer l'arrière plan
    screen.fill(background)

    # Appliquer la grille du manoir (Zone Gauche)
    game.draw_manoir_grid(screen)

    #appliquer la pièce d'entrée
    screen.blit(entrance,(170,650))

    #appliquer la pièce antechamber
    screen.blit(antechamber,(170,10))

    #Dessiner l'interface utilisateur
    game.draw_ui(screen)

    # Appliquer la sélection de pièce (Zone Bas-Droite, si active)
    if game.is_selecting_room:
        game.draw_room(screen)

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

        elif event.type == pygame.KEYDOWN:

            # quitter avec escape
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                print("Fermeture du jeu par ESC")

            # CONTRÔLES D'INTERFACE (Sélection de Pièce)
            if game.is_selecting_room:
                # Flèches UP/DOWN pour naviguer, RETURN (Entrée) pour confirmer
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    game.handle_selection_movement(event.key)
                elif event.key == pygame.K_RETURN: 
                    game.confirm_room_selection()
                    
            # CONTRÔLES DE JEU (Mouvement et Interaction)
            else:
                # W/A/S/D pour sélectionner la direction de la porte/du mouvement
                if event.key == pygame.K_d:
                    direction = "droite"
                    game.player.pion = pygame.transform.rotate(game.player.direction, -90)
                elif event.key == pygame.K_a:
                    direction = "gauche"
                    game.player.pion = pygame.transform.rotate(game.player.direction, 90)
                elif event.key == pygame.K_w:
                    direction = "haut"
                    game.player.pion = game.player.direction
                elif event.key == pygame.K_s:
                    direction = "bas"
                    game.player.pion = pygame.transform.rotate(game.player.direction, 180)
                
                # ESPACE pour l'action : tenter d'ouvrir/déverrouiller
                elif event.key == pygame.K_SPACE:
                    
                    # Tenter d'ouvrir/déverrouiller une porte (déclenchera la sélection si réussie)
                    game.check_and_open_door(direction)
                    
                # ENTRÉE pour le mouvement (facultatif, si ESPACE est trop chargé)
                elif event.key == pygame.K_RETURN:
                    # Tenter de se déplacer dans la direction courante
                    game.try_move_player(direction)

game.update()
