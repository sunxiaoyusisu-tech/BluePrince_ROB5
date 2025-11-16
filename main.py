import pygame
from joueur import*
from jeu import*

pygame.init()
pygame.font.init()

pygame.display.set_caption("Blue Prince")
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((1280,740),pygame.FULLSCREEN)

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

    # Vérifier la condition de victoire
    if game.check_for_win_condition():
        game.animation_victoire(screen)

    if game.check_for_loss_condition():
        game.animation_defaite(screen)

    #mettre à jour la fenetre
    pygame.display.flip()
    

    # Ferme la fenetre si le joueur clique sur croix
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("fermeture du jeu")

        elif event.type == pygame.KEYDOWN:

            # quitter avec escape
            if event.key == pygame.K_ESCAPE:
                if game.is_interacting:
                    game.is_interacting = False
                    game.current_interaction_object = None
                    print("Intéraction annulée")
                else : 
                    running = False
                    pygame.quit()
                    print("Fermeture du jeu par ESC")
            
            # Gestion de l'interaction
            if game.is_interacting:

                if isinstance(game.current_interaction_object, Magasin):
                    shop: Magasin = game.current_interaction_object
                    
                    if event.key == pygame.K_RETURN:
                        result = shop.confirmer_achat(game)
                        if result == "achat_reussi":
                            game.add_message(f"Achat réussi!", (100, 255, 100))
                        elif result == "pas_assez_or":
                            game.add_message(f"Pas assez d'or!", (255, 100, 100))
                        elif result == "fermé_apres_achat":
                            game.add_message(f"Magasin vidé! Interaction terminée.", (150, 150, 150))

                    elif event.key == pygame.K_LEFT:
                        shop.update_selection("gauche")
                    
                    elif event.key == pygame.K_RIGHT:
                        shop.update_selection("droite")


                elif event.key == pygame.K_RETURN:
                    if isinstance(game.current_interaction_object, EndroitACreuser):
                        game.digging()
                    elif isinstance(game.current_interaction_object, Coffre):
                        game.ouvrir_coffre()
                    elif isinstance(game.current_interaction_object, Magasin):
                        obj.selection_item()
                        if event.key == pygame.K_RETURN:
                            obj.confirm_purchase()
                            

                elif event.key == pygame.K_ESCAPE : 
                    game.is_interacting = False
                    game.current_interaction_object = None
                    print("Interaction annulée par le joueur")

            # CONTRÔLES D'INTERFACE (Sélection de Pièce)
            elif game.is_selecting_room:

                # Flèches UP/DOWN pour naviguer, RETURN (Entrée) pour confirmer

                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    game.handle_selection_movement(event.key)

                elif event.key == pygame.K_RETURN:
                    game.confirm_room_selection()

                elif event.key == pygame.K_r: 
                    game.use_dice_for_reroll()
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
                elif event.key == pygame.K_f:
                    # 'direction' est déjà définie par les touches W/A/S/D
                    game.use_wall_pass(direction)
                # ESPACE pour l'action : tenter d'ouvrir/déverrouiller
                elif event.key == pygame.K_SPACE:
                    
                    # Nouvelle logique : Vérifier si on peut se déplacer OU ouvrir une porte
                    game.handle_door_action(direction, screen)


                # C pour creuser 
                elif event.key == pygame.K_c :
                    current_room = game.manoir_grid[game.current_row][game.current_col]
                    if current_room:
                        #Chercher un endroit a creuser
                        for obj in current_room.objets:
                            if isinstance(obj, EndroitACreuser):
                                game.current_interaction_object = obj
                                game.is_interacting = True
                                obj.interagir(game)
                                break #sortir de la boucle apres avoir trouve

                # O pour ouvrir un coffre
                elif event.key == pygame.K_o:
                    current_room = game.manoir_grid[game.current_row][game.current_col]
                    if current_room:
                        #Chercher un coffre dans la piece
                        for obj in current_room.objets:
                            if isinstance(obj,Coffre):
                                game.current_interaction_object = obj
                                game.is_interacting = True
                                # Afficher un message pour confirmer
                                print("Appuyez sur ENTRÉE pour ouvrir le coffre, ou ESC pour annuler")
                                break

                # ENTRÉE pour interagir avec la case actuelle (Creuser / Ramasser)
                #elif event.key == pygame.K_RETURN:
                    # Récupérer la pièce actuelle
                #    current_room = game.manoir_grid[game.current_row][game.current_col]
                #    if current_room:
                        # Tenter de commencer une interaction
                #        game.start_interaction(current_room)

                # ENTRÉE pour le mouvement (facultatif, si ESPACE est trop chargé)
                #elif event.key == pygame.K_RETURN:
                    # Tenter de se déplacer dans la direction courante
                 #   game.try_move_player(direction,screen)
            


