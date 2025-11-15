import pygame
from joueur import*
import random

import sys
sys.path.insert(0, 'src')

from mon_projet.inventaire import *

# Fonction utilitaire de génération du niveau de verrouillage
def generer_lock_level(target_row: int) -> int:
    """ 
    Détermine le niveau de verrouillage (0, 1 ou 2) d'une nouvelle porte 
    en fonction de la rangée cible (0=haut, 8=bas).
    """
    if target_row == 8: # Rangée de départ (en bas)
        return 0 
    elif target_row == 0: # Rangée d'arrivée (en haut)
        return 2 
    else:
        # Progression factor va de ~0.0 (rangée 7) à ~1.0 (rangée 1)
        progression_factor = (8 - target_row) / 7 
        
        if random.random() < progression_factor * 0.40: # Chance max de 40% pour un Niveau 2
            return 2
        elif random.random() < progression_factor * 0.75: # Chance max de 75% pour un Niveau 1 ou 2
            return 1
        else:
            return 0 

class FakeRoom:
    """ Simule une pièce du catalogue pour la sélection. """
    def __init__(self, name, cost, color):
        self.nom = name
        self.cost = cost
        self.color = color # Pour l'affichage
        # Charger une image par défaut ou une image de test
        self.image = pygame.Surface((80, 80))
        self.image.fill(color)

class Game:
    def __init__(self):
        #charger le joueur
        self.player = Player()
        self.inventaire = Inventaire()

        #Dimensions de la grille
        self.grid_width = 5
        self.grid_height = 9

        # Représente l'état du manoir. Initialisé avec des valeurs nulles/pièces noires
        # La grille stockera des objets Room
        self.manoir_grid = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]

        # Position actuelle du joueur dans la grille (colonne, rangée)
        self.current_col = 2
        self.current_row = 8

        # Initialisation du Font pour l'UI
        pygame.font.init()
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 30)
        self.font_large = pygame.font.Font(None, 40)

        self.BLUEPRINT_BLUE = (0, 150, 255) # Couleur principale
        self.LIGHT_BLUE = (150, 200, 255)   # Couleur claire pour le texte/cadre
        self.DARK_BLUE = (0, 50, 150)       # Couleur foncée pour le remplissage
        
        # État de la Sélection de Pièce (affichage en bas à droite)
        self.is_selecting_room = False 
        self.current_room_options = [] # Liste des 3 pièces tirées au sort (objets Room)
        self.selected_option_index = 0 # Index de la pièce actuellement sélectionnée
        self.target_row = 0
        self.target_col = 0
    
    def draw_manoir_grid(self,screen):
        """
        Dessine la grille du manoir
        """
        title_size = 80 #taille de l'image d'entrée dans main.py
        pos_depart_x = 10 #grille centré à gauche
        pos_depart_y = 730 

        # Dessiner le cadre et les lignes du quadrillage (look Blueprint)
        BLUE_LINE = self.BLUEPRINT_BLUE

        # --- 1. CADRE EXTÉRIEUR DE LA ZONE DE JEU (NOUVEAU) ---
        GRID_WIDTH_TOTAL = self.grid_width * title_size
        GRID_HEIGHT_TOTAL = self.grid_height * title_size
        # Le cadre doit être ajusté pour ne pas empiéter sur le menu de sélection en bas.
        GAME_RECT = pygame.Rect(pos_depart_x- 10, pos_depart_y - GRID_HEIGHT_TOTAL - 10, 
                                GRID_WIDTH_TOTAL + 20, GRID_HEIGHT_TOTAL + 20)
        
        pygame.draw.rect(screen, self.DARK_BLUE, GAME_RECT)
        pygame.draw.rect(screen, self.BLUEPRINT_BLUE, GAME_RECT, 2)

        # Dessiner les lignes du quadrillage (Blueprint look)
        for i in range(self.grid_width + 1): # Lignes verticales
            x = pos_depart_x+ i * title_size
            pygame.draw.line(screen, BLUE_LINE, (x, pos_depart_y), (x, pos_depart_y - self.grid_height * title_size), 1)

        for i in range(self.grid_height + 1): # Lignes horizontales
            y = pos_depart_y - i * title_size
            pygame.draw.line(screen, BLUE_LINE, (pos_depart_x, y), (pos_depart_x+ self.grid_width * title_size, y), 1)
        
        # Boucle sur les rangées y 
        for r in range(self.grid_height):
            # Boucle sur les colonnes x
            for c in range(self.grid_width):
                room = self.manoir_grid[r][c]

                #Calcul de la position
                y_draw = pos_depart_y - (self.grid_height - r) * title_size
                x_draw = pos_depart_x + c * title_size

                rect = pygame.Rect(x_draw, y_draw, title_size, title_size)

                if room:
                    #Dessiner la Room
                    screen.blit(room.image, (x_draw, y_draw))
                else:
                    #Dessiner un carré noir pour une pièce non découverte
                    pygame.draw.rect(screen, (0, 0, 0),rect)

        # Synchronisation de la position du joueur (pion) avec la grille
        player_x = pos_depart_x + self.current_col * title_size + (title_size - self.player.pion.get_width()) // 2
        player_y = pos_depart_y - (self.grid_height - self.current_row) * title_size + (title_size - self.player.pion.get_height()) // 2
        
        self.player.rect.x = player_x
        self.player.rect.y = player_y

        # Dessiner le pion du joueur (toujours en dernier pour qu'il soit par-dessus)
        #screen.blit(self.player.pion, self.player.rect)

    def draw_ui(self,screen):
        """
        Dessine les éléments d'interface comme l'inventaire, les pas restants etc.
        """

        # Affichage des ressources consommables
        #font = pygame.font.Font(None,30)

        #Définir une zone pour l'inventaire
        ui_x = 500
        ui_y = 30
        WIDTH = 700
        HEIGHT = 280
        hauteur_ligne = 40
        
        # Dessiner le cadre de l'Inventaire (Fond + Contour)
        inventory_rect = pygame.Rect(ui_x- 10, ui_y - 10, WIDTH, HEIGHT)
        # Fond légèrement plus foncé
        pygame.draw.rect(screen, self.DARK_BLUE, inventory_rect)
        # Contour bleu clair pour délimiter
        pygame.draw.rect(screen, self.BLUEPRINT_BLUE, inventory_rect, 2)

        title_text = self.font_large.render("INVENTORY", True, (0, 150, 255))
        screen.blit(title_text, (ui_x, ui_y))

        resources = [
            ("Pas",self.inventaire.pas),
            ("Or", self.inventaire.pieces_or),
            ("Gemmes", self.inventaire.gemmes),
            ("Clés", self.inventaire.cles),
            ("Dés", self.inventaire.des)
            #Ajouter pelle / marteau / detecteur de metaux
        ]

        y_pos = ui_y + 50

        #Dessine les ressources
        for name, value in resources:
            text = self.font_medium.render(f"{name}: {value}", True, (255, 255, 255))
            screen.blit(text, (ui_x,y_pos))
            y_pos += hauteur_ligne
        
        # Séparateur vertical entre consommables et permanents
        x_pos = ui_x + 250
        y_pos = ui_y + 50

        # Titre pour les objets permanents
        title_text = self.font_medium.render("Objets Permanents :",True,(0,150,255))
        screen.blit(title_text,(x_pos ,ui_y))
        y_pos += ui_y + 50

        # Dessiner la liste des objets permanents
        if self.inventaire.objets_permanents:
            for objet in self.inventaire.objets_permanents:
                obj_text = self.font_medium.render(f"- {objet.nom}", True, (150, 255, 150)) # Vert clair
                screen.blit(obj_text, (x_pos + 10, y_pos))
                y_pos += hauteur_ligne

        else:
            none_text = self.font_medium.render("- Aucun", True, (100, 100, 100))
            screen.blit(none_text, (x_pos + 10, y_pos))

    def draw_room(self,screen):
        """
        Affiche les options de pièces à choisir
        """
        x = 500
        y = screen.get_height() - 400
        WIDTH = 600 
        HEIGHT = 300
        image_size = 100

        title = self.font_medium.render("Room : ", True, (255, 255, 255))
        screen.blit(title, (x, y))

        # Calcul de l'espacement pour centrer les trois options
        TOTAL_CONTENT_WIDTH = (3 * image_size) + (2 * 150) # 3 images + 2 espaces (300px)
        # Position X de départ pour centrer l'ensemble des 3 options
        START_OFFSET_X = (WIDTH - TOTAL_CONTENT_WIDTH) // 2

        y_img_pos = y + 40
        y_pos = y_img_pos

        for i, room in enumerate(self.current_room_options):
            
            x_img_pos = x + START_OFFSET_X + i*(image_size+150)

            # Encadrer l'option sélectionnée
            if i == self.selected_option_index:
                pygame.draw.rect(screen, (255, 255, 0), (x_img_pos - 5, y_img_pos - 5, image_size + 10, image_size + 10), 2)
            
            # Afficher l'image/couleur de la pièce
            img=pygame.transform.scale(room.image, (image_size, image_size)) #agrandir l'image pour la selection
            screen.blit(img, (x_img_pos, y_img_pos))
            
            # Afficher le nom et le coût (supposer room.nom et room.cost existent)
            details_text = self.font_small.render(f"{room.nom}", True, (200, 200, 200))
            screen.blit(details_text, (x_img_pos + image_size + 10, y_pos + 10))
            
            cost_text = self.font_small.render(f"Coût: {room.cost} Gemmes", True, (200, 200, 200))
            screen.blit(cost_text, (x_img_pos + image_size + 10, y_pos + 40))
            
            #y_pos += 200 # Espacement entre les options

    def try_move_player(self, direction, screen):
        """
        Tente de déplacer le joueur vers une pièce déjà découverte.
        (W/A/S/D dans main.py)
        """
        
        if direction == "droite":
            dr, dc = 0, 1
        elif direction == "gauche":
            dr, dc = 0, -1
        elif direction == "haut":
            dr, dc = -1, 0
        elif direction == "bas":
            dr, dc = 1, 0
        else:
            return

        r_cible, c_cible = self.current_row + dr, self.current_col + dc
        
        # Coordonnées d'affichage pour les messages d'erreur
        x_erreur = 500
        y_erreur = 500
        
        # 1. Vérifier les limites de la grille
        if not (0 <= r_cible < self.grid_height and 0 <= c_cible < self.grid_width):
            title = self.font_medium.render("Déplacement impossible : il y a un mur", True, (255, 255, 255)) #affichage message d'erreur
            screen.blit(title, (x_erreur, y_erreur))                                                         #sur l'interface (pour l'instant ça marche pas)
            print("Déplacement impossible : il y a un mur")
            return

        # 2. Vérifier si la pièce existe déjà et si la porte est ouverte (non implémenté)
        if self.manoir_grid[r_cible][c_cible] is not None:
            # Effectuer le déplacement
            self.current_row, self.current_col = r_cible, c_cible
            self.inventaire.utiliser_pas(1) # Perte d'un pas
            print(f"Déplacement vers ({c_cible}, {r_cible}). Pas restants: {self.inventaire.pas}")
        else:
            print("Déplacement impossible : la porte n'est pas ouverte. Utilisez ESPACE pour interagir.")


    def check_and_open_door(self, direction):
        """
        Tente d'ouvrir une nouvelle porte (ESPACE dans main.py).
        Déclenche la sélection de pièce si l'ouverture réussit.
        """
        
        # 1. Déterminer la position cible
        if direction == "droite":
            dr, dc = 0, 1
        elif direction == "gauche":
            dr, dc = 0, -1
        elif direction == "haut":
            dr, dc = -1, 0
        elif direction == "bas":
            dr, dc = 1, 0
        else:
            return

        r_cible, c_cible = self.current_row + dr, self.current_col + dc

        # 2. Vérifier si l'ouverture est pertinente
        if not (0 <= r_cible < self.grid_height and 0 <= c_cible < self.grid_width) or self.manoir_grid[r_cible][c_cible] is not None:
            print("Action de porte inutile ici.")
            return
        
        lock_level = generer_lock_level(r_cible)
        print(f"Niveau de verrouillage de la nouvelle porte (vers rangée {r_cible}): {lock_level}")
        
        can_open = False
        if lock_level == 0:
            can_open = True
            print("Porte déverrouillée (Niveau 0).")
        elif self.inventaire.cles > 0:
            self.inventaire.depenser_cles_cles(1)
            can_open = True
            print(f"Clé dépensée. Porte déverrouillée (Niveau {lock_level}).")
        elif lock_level == 1 and self.inventaire.possede_objet("Kit de crochetage"):
            can_open = True
            print("Kit de crochetage utilisé. Porte déverrouillée (Niveau 1).")
        else:
            print(f"La porte est verrouillée (Niveau {lock_level}). Il vous faut une clé.")
        
        # 3. Si l'ouverture est réussie, démarrer la sélection
        if can_open:
            self.target_row, self.target_col = r_cible, c_cible
            self.start_room_selection(direction)


    def start_room_selection(self, door_direction):
        """ Déclenche l'état de sélection de pièce avec les options tirées. """
        
        # Simuler un tirage (utilisez FakeRoom pour l'exemple)
        self.current_room_options = [
            FakeRoom("Antichambre", 0, (50, 50, 150)),
            FakeRoom("Chambre Forte", 3, (150, 50, 50)),
            FakeRoom("Jardin", 1, (50, 150, 50)),
        ]
        self.is_selecting_room = True
        self.selected_option_index = 0
        print(f"Ouverture de porte vers {door_direction}. Choix de pièce activé.")
        
    def handle_selection_movement(self, key):
        """ Gère le mouvement dans le menu de sélection de pièce (Flèches UP/DOWN). """
        if self.is_selecting_room:
            if key == pygame.K_UP:
                self.selected_option_index = (self.selected_option_index - 1) % len(self.current_room_options)
            elif key == pygame.K_DOWN:
                self.selected_option_index = (self.selected_option_index + 1) % len(self.current_room_options)

    def confirm_room_selection(self):
        """ Valide la pièce sélectionnée et l'ajoute à la grille (Entrée). """
        if not self.is_selecting_room:
            return
            
        chosen_room = self.current_room_options[self.selected_option_index]
        
        # Vérification du coût en gemmes
        if self.inventaire.gemmes >= chosen_room.cost:
            self.inventaire.modifier_gemmes(-chosen_room.cost)
            
            # Ajout de la pièce à l'emplacement cible (défini par check_and_open_door)
            self.manoir_grid[self.target_row][self.target_col] = chosen_room 
            
            # Réinitialisation de l'état
            self.is_selecting_room = False
            self.current_room_options = []
            
            # Le joueur avance immédiatement dans la nouvelle pièce
            self.current_row, self.current_col = self.target_row, self.target_col
            self.inventaire.modifier_pas(-1)
            
            print(f"Pièce choisie : {chosen_room.nom} ajoutée au manoir. Déplacement effectué.")
            
        else:
            print("Pas assez de gemmes pour cette pièce. Veuillez en choisir une autre ou appuyer sur une flèche pour annuler/changer.")

    #pour mettre à jour la map quand on choisit une salle
    def update(self):
        pass

    
