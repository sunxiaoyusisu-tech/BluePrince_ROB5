import pygame
import numpy as np
from joueur import*
from src.mon_projet.objets import EndroitACreuser
from src.mon_projet.module1 import*
import random

import sys
sys.path.insert(0, 'src')

from mon_projet.inventaire import * 
from mon_projet.sous_package.module2 import *

DIR_FROM_STR = {
    "haut": Direction.UP,
    "bas": Direction.DOWN,
    "droite": Direction.RIGHT,
    "gauche": Direction.LEFT,
}

OPPOSITE = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.RIGHT: Direction.LEFT,
    Direction.LEFT: Direction.RIGHT,
}

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

        # Variables d'etat pour l'interaction
        self.is_interacting = False
        self.current_interaction_object = None
        self.interaction_message = ""
        self.message_timer = 0 #pour les messages temporaires

        # Message pour les changements d'inventaire et les effets
        self.system_messages = []
        self.MESSAGE_DURATION = 3000 # 3 secondes

        # Gestion de la pioche dynamique
        self.modeles_disponibles = self.tous_les_modeles() 
        self.pioche_disponible = self.initialiser_pioche()

        # Pour accelerer le tirage
        self.piece_metadata_cache = {}
        for nom_piece in self.modeles_disponibles:
            metadata = get_piece(nom_piece)
            if metadata:
                self.piece_metadata_cache[nom_piece] = metadata
            else:
                print(f"Avertissement : Métadonnées manquantes pour {nom_piece}")

        # Dupliquer explicitement certaines pièces pour augmenter le nombre total
        self.ajouter_pieces_au_catalogue(["Spare Room", "Spare Room", "Nook", "Chapel","The pool","Master Bedroom","Bedroom","Chapel","Nook","Music Room",
                                         "Garage","Chamber of mirrors","Veranda","Furnace","Greenhouse","Office","Study","Drawing Room","Spare Room", "Spare Room", "Nook", "Chapel","The pool","Master Bedroom","Bedroom","Chapel","Nook","Music Room",
                                         "Garage","Chamber of mirrors","Veranda","Furnace","Greenhouse","Office","Study","Drawing Room","Spare Room", "Spare Room", "Nook", "Chapel","The pool","Master Bedroom","Bedroom","Chapel","Nook","Music Room",
                                         "Garage","Chamber of mirrors","Veranda","Furnace","Greenhouse","Office","Study","Drawing Room"])


        self.manoir_grid[8][2] = creer_piece("Entrance Hall")

        # Variables d'état pour les effets de modification de probabilité
        self.modificateur_chance_veranda = False
        self.modificateur_tirage_furnace = False
        self.modificateur_tirage_greenhouse = False

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
        self.last_move_dir_str = None
    
    #Methodes pour les messages
    def add_message(self, message:str,color=(255,255,100)):
        """
        Ajoute un message système à afficher
        """
        timestamp = pygame.time.get_ticks() + self.MESSAGE_DURATION
        self.system_messages.append((message, timestamp, color))
        print(f"[GAME] {message}")
    
    def draw_system_messages(self, screen):
        """Dessine les messages système à l'écran"""
        current_time = pygame.time.get_ticks()
        
        # Supprime les messages expirés
        self.system_messages = [
            (msg, ts, col) for msg, ts, col in self.system_messages 
            if ts > current_time
        ]
        
        # Dessine les messages actifs
        y_offset = 350
        for message, timestamp, color in self.system_messages:
            text_surface = self.font_medium.render(message, True, color)
            screen.blit(text_surface, (500, y_offset))
            y_offset += 35
    
    def collect_item(self,item_name:str):
        """
        Collecte un objet et met à jour l'inventaire
        """
        item_effects = {
            "cle": ("Trouvé une Clé!", lambda: self.inventaire.modifier_cles(1)),
            "gemme": ("Trouvé un gemme!", lambda: self.inventaire.modifier_gemmes(1)),
            "or": ("Trouvé de l'Or!", lambda: self.inventaire.modifier_or(1)),
            "dé": ("Trouvé un dé!", lambda: self.inventaire.modifier_des(1)),
            "pomme": ("Trouvé une Pomme! (+2 pas)!", lambda: self.inventaire.modifier_pas(2)),
            "banane": ("Trouvé une Banane! (+3 pas)!", lambda: self.inventaire.modifier_pas(3)),
            "fruit": ("Trouvé un Fruit! (+2 pas)", lambda: self.inventaire.modifier_pas(2)),
            "shovel": ("Trouvé une pelle!", lambda: setattr(self.inventaire, 'possede_pelle', True)),
            "marteau": ("Trouvé un Marteau!", lambda: setattr(self.inventaire, 'possede_marteau', True)),
            "sledgehammer": ("Trouvé un Marteau!", lambda: setattr(self.inventaire, 'possede_marteau', True)),
            "kit de crochetage": ("Trouvé un kit de crochetage!", lambda: setattr(self.inventaire, 'possede_kit_crochetage', True)),
            "metal detector": ("Trouvé Détecteur de Métaux!", lambda: setattr(self.inventaire, 'possede_detecteur_metaux', True)),
            "patte de lapin": ("Trouvé Patte de Lapin!", lambda: setattr(self.inventaire, 'possede_patte_lapin', True)),
        }

        if item_name in item_effects:
            message, action = item_effects[item_name]
            action()
            self.add_message(message,(100,255,100))
        else:
            self.add_message(f"Trouvé {item_name}", (200, 200, 100))

    # Gestion du catalogue et de la pioche
    
    def tous_les_modeles(self):
        """ Retourne le nom des pieces disponibles """
        return ["The Foundation", "Entrance Hall", "Spare Room", "Nook", "Garage", "Music Room", 
                "Drawing Room", "Study", "Sauna", "Coat Check", "Mail Room", 
                "The pool", "Chamber of mirrors", "Veranda", "Furnace", 
                "Greenhouse", "Office", "Bedroom", "Chapel", "Master Bedroom"]
    
    def initialiser_pioche(self):
        """ Liste initiale des noms de pièces """
        pioche = self.tous_les_modeles()
        pioche.remove("Entrance Hall")
        return pioche
    
    def ajouter_pieces_au_catalogue(self, noms_pieces: list):
        """ Ajoute une ou plusieurs pièces à la pioche disponible (pour l'effet 'The pool'). """
        self.pioche_disponible.extend(noms_pieces)
        self.add_message(f"Catalogue mis à jour : {len(noms_pieces)} pièces ajoutées!", (100, 255, 100))
    
    def tirer_pieces(self, nombre_options: int = 3, r_cible: int = 0) -> list:
        """ tirer aleatoirement des pieces dans la pioche"""
        options = []
        pioche_avec_cout_zero = [
            nom for nom in self.pioche_disponible 
            if self.piece_metadata_cache.get(nom, {}).get('cout_gemmes', 1) == 0
        ]

        if not self.pioche_disponible:
            print("Erreur critique : Pioche vide.")
            return []
            
        # 1. Tirer d'abord la pièce de coût 0 (si nécessaire)
        if pioche_avec_cout_zero and not any(nom in options for nom in pioche_avec_cout_zero):
            choix_zero = random.choice(pioche_avec_cout_zero)
            self.pioche_disponible.remove(choix_zero)
            options.append(choix_zero) 
        
        # 2. Remplir le reste des options (en utilisant la rareté/pondération)
        while len(options) < nombre_options and self.pioche_disponible:
            
            noms = [nom for nom in self.pioche_disponible if nom not in options]
            
            # Utilisation du Cache pour les Poids (RAPIDE)
            poids = [self.piece_metadata_cache.get(nom, {}).get('poids', 0) for nom in noms]
            
            # Nouveau: effet patte de lapin
            if self.inventaire.possede_patte_lapin:
                print("patte de lapin activee")
                for i, nom in enumerate(noms):
                    rarete = self.piece_metadata_cache.get(nom, {}).get('rarete', 0)
                    # Si la pièce est rare (Niveau 2 ou 3), on double son poids
                    if rarete >= 2:
                        poids[i] *= 2
            
            total_poids = sum(poids)
            
            if total_poids == 0:
                print("Erreur: total des poids = 0 pour le tirage.")
                break
                
            poids_normalises = [p / total_poids for p in poids]
            
            # Tirage pondéré
            choix_nom = np.random.choice(a=noms, size=1, p=poids_normalises)[0] 

            self.pioche_disponible.remove(choix_nom)
            options.append(choix_nom)
            
        return options
    
    def draw_manoir_grid(self,screen):
        """
        Dessine la grille du manoir
        """
        title_size = 80 #taille de l'image d'entrée dans main.py
        pos_depart_x = 10 #grille centré à gauche
        pos_depart_y = 730 

        # Dessiner le cadre et les lignes du quadrillage (look Blueprint)
        BLUE_LINE = self.BLUEPRINT_BLUE

        # CADRE EXTÉRIEUR DE LA ZONE DE JEU
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

        # Dessiner le message d'interaction s'il est actif
        if self.is_interacting and pygame.time.get_ticks() < self.message_timer:
            self.draw_interaction_prompt(screen)

        self.draw_system_messages(screen)

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

        permanents = [
        ("Pelle", self.inventaire.possede_pelle),
        ("Marteau", self.inventaire.possede_marteau),
        ("Kit de crochetage", self.inventaire.possede_kit_crochetage),
        ("Détecteur de métaux", self.inventaire.possede_detecteur_metaux),
        ("Patte de lapin", self.inventaire.possede_patte_lapin)
    ]

        # Dessiner la liste des objets permanents
        if any(possede for _, possede in permanents): # Vérifie si au moins un est possédé
            y_draw = ui_y + hauteur_ligne # Commence après le titre
            
            for name, possede in permanents:
            # Choisir la couleur et le statut en fonction du booléen
                if possede:
                    color = (150, 255, 150)  # Vert clair pour "Possédé"
                    status = " [Possédé]"
                else:
                    color = (100, 100, 100)  # Gris foncé pour "Non possédé"
                    status = " [Non possédé]"

                obj_text = self.font_medium.render(f"- {name}{status}", True, color)
                screen.blit(obj_text, (x_pos + 10, y_draw))
                y_draw += hauteur_ligne
    
        else:
            # Aucun objet permanent possédé
            none_text = self.font_medium.render("- Aucun", True, (100, 100, 100))
            screen.blit(none_text, (x_pos + 10, ui_y + hauteur_ligne))

    def draw_room(self,screen):
        """
        Affiche les options de pièces à choisir
        """
        x = 500
        y = screen.get_height() - 400
        WIDTH = 600 
        HEIGHT = 300
        image_size = 140

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
            img = pygame.transform.smoothscale(room.image, (image_size, image_size)) 
            screen.blit(img, (x_img_pos, y_img_pos))
            
            # Afficher le nom et le coût (supposer room.nom et room.cost existent)
            details_text = self.font_small.render(f"{room.nom}", True, (200, 200, 200))
            screen.blit(details_text, (x_img_pos + image_size + 10, y_pos + 10))
            
            cost_text = self.font_small.render(f"{room.cout_gemmes} Gemmes", True, (200, 200, 200))
            screen.blit(cost_text, (x_img_pos + image_size + 10, y_pos + 40))
            
            #y_pos += 200 # Espacement entre les options
    
    def draw_interaction_prompt(self,screen) : 
        """
        Dessine la boîte de dialogue pour l'interaction (ex: creuser)
        """
        if not self.is_interacting:
            return
        
        x,y = 50, screen.get_height() - 100
        width, height = 400,80

        rect = pygame.Rect(x,y,width,height)
        pygame.draw.rect(screen,self.DARK_BLUE,rect)
        pygame.draw.rect(screen, (255,255,255),rect,2)

        text_lines = [
            self.interaction_message,
            "Confirmer (Entrée) / Annuler (Echap)"
        ]

        for i,line in enumerate(text_lines):
            text_surface = self.font_medium.render(line, True, (255,255,255))
            screen.blit(text_surface,(x+10,y+10+i*25))
    
    #initialiser l'interaction
    def start_interaction(self,current_room : Room) : 
        """
        Vérifie les objets de la pièce et commence une interaction si possible
        """
        if self.is_selecting_room:
            return
        
        #Trouver un objet interactif (EndroitACreuser)
        for obj in current_room.objets:
            if isinstance(obj,EndroitACreuser):

                #Verifie si l'interaction est possible
                if self.inventaire.possede_pelle and not obj.est_utilise:

                    self.is_interacting = True
                    self.current_interaction_object = obj
                    self.interaction_message = f"Voulez-vous creuser avec la Pelle à {obj.nom} ?"
                    self.message_timer = pygame.time.get_ticks() + 10000 # 10 secondes pour répondre
                    return # Un seul dig spot à la fois
                elif not self.inventaire.possede_pelle:
                    self.add_message("Il vous faut une Pelle pour creuser!", (255, 100, 100))
                    #self.interaction_message = "Il y a un endroit à creuser, mais il vous faut une Pelle."
                    #self.message_timer = pygame.time.get_ticks() + 3000
                    return

                elif obj.est_utilise:
                    self.add_message("Cet endroit a déjà été creusé.", (150, 150, 150))
                    #self.interaction_message = "Cet endroit a déjà été creusé."
                    #self.message_timer = pygame.time.get_ticks() + 3000
                    return
        
        #Vérifier les objets collectables
        collected_something = False
        items_to_remove = []

        for item in current_room.objets :
            if isinstance(item,str) :
                collected_something = True
                items_to_remove.append(item)
                self.collect_item(item)

        #Retirer les objets collectés
        for item in items_to_remove:
            current_room.objets.remove(item)
        
        if not collected_something:
            self.add_message("Rien d'interactif ici.", (150, 150, 150))

        #self.interaction_message = "Rien d'interactif"
        #self.message_timer = pygame.time.get_ticks() + 3000
    
    def digging(self):
        """
        Execute l'action de creuser
        """
        if not self.is_interacting or not isinstance(self.current_interaction_object, EndroitACreuser):
            return 
        
        dig_spot: EndroitACreuser = self.current_interaction_object
        
        # Appeler la méthode pour effectuer le creusage
        result = dig_spot.effectuer_creusage(self)

        if result == "rien":
            self.add_message("Vous creusez... et ne trouvez rien.")
        elif result == "pas de pelle":
            self.add_message("Erreur: vous n'avez pas de pelle.")
        elif result == "already_used":
            self.add_message("Cet endroit est déjà vide.")
        else: # Un objet a été trouvé (result est le nom de l'objet)
            #if result == "cle":
            #    self.inventaire.modifier_cles(1)
            #elif result == "gemme":
            #    self.inventaire.modifier_gemmes(1)
            #elif result == "or":
            #    self.inventaire.modifier_or(1)
            #elif result == "dé":
            #    self.inventaire.modifier_des(1)
            #elif result == "pomme":
            #    self.inventaire.modifier_pas(2)
            #elif result == "banane":
            #    self.inventaire.modifier_pas(3)
            #elif result == "shovel":
            #    self.inventaire.possede_pelle = True
            #elif result == "marteau":
            #    self.inventaire.possede_marteau = True
            #elif result == "kit de crochetage":
            #    self.inventaire.possede_kit_crochetage = True
            #elif result == "détecteur de métaux":
            #    self.inventaire.possede_detecteur_metaux = True
            #elif result == "patte de lapin":
            #    self.inventaire.possede_patte_lapin = True

            self.collect_item(result)
        
        #Reinitialiser l'etat d'interaction
        self.is_interacting = False
        self.current_interaction_object = None
        #self.message_timer = pygame.time.get_ticks() + 3000


    def try_move_player(self, direction):
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
        if 0 <= r_cible < self.grid_height and 0 <= c_cible < self.grid_width and self.manoir_grid[r_cible][c_cible] is not None:
            
            chosen_room = self.manoir_grid[r_cible][c_cible]
            
            # --- APPLICATION DE L'EFFET D'ENTRÉE POUR LA PREMIÈRE FOIS ---
            # Vérifier si c'est une pièce à effet d'entrée
            is_entry_effect = hasattr(chosen_room, 'moment_effet') and chosen_room.moment_effet == "entree"

            if is_entry_effect:
                # Si l'effet est permanent (comme Chapel), on déclenche l'effet sans condition de visite.
                # Pour les autres, on ne le fait qu'à la première visite.
                
                # Solution 1: Déclencher l'effet de la Chapel à chaque fois
                if chosen_room.nom == "Chapel":
                    chosen_room.appliquer_effet(self)
                
                # Solution 2: Déclencher l'effet pour la première fois pour les autres
                elif not chosen_room.visitee:
                    chosen_room.appliquer_effet(self)
                
            # Marquer comme visitée (uniquement si l'effet n'est PAS permanent,
            # mais pour simplifier, on le fait après l'effet pour éviter la boucle infinie de re-visite)
            if not chosen_room.visitee:
                chosen_room.visitee = True

        # 2. Vérifier si la pièce existe déjà et si la porte est ouverte (non implémenté)
        if self.manoir_grid[r_cible][c_cible] is not None:
            # Effectuer le déplacement
            self.current_row, self.current_col = r_cible, c_cible
            self.inventaire.modifier_pas(-1) # Perte d'un pas
            self.add_message(f"Déplacé vers {chosen_room.nom}. Pas: {self.inventaire.pas}", (150, 200, 255))
            items_to_remove = []
            for item in chosen_room.objets:
                if isinstance(item, str):
                    items_to_remove.append(item)
                    self.collect_item(item)
            for item in items_to_remove:
                chosen_room.objets.remove(item)
            else:
                self.add_message("Porte non ouverte. Utilisez ESPACE pour interagir.", (255, 150, 100))
        
        current_room = self.manoir_grid[self.current_row][self.current_col]
        
        if current_room and current_room.portes:
            direction_enum = DIR_FROM_STR[direction]
        
        if not current_room.portes.a_porte(direction_enum):
            self.add_message("Pas de porte dans cette direction!", (255, 100, 100))
            return

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
        
        current_room = self.manoir_grid[self.current_row][self.current_col]
        
        if current_room and current_room.portes:
            direction_enum = DIR_FROM_STR[direction]
        
        if not current_room.portes.a_porte(direction_enum):
            self.add_message("Pas de porte dans cette direction!", (255, 100, 100))
            return
        
        lock_level = generer_lock_level(r_cible)
        print(f"Niveau de verrouillage de la nouvelle porte (vers rangée {r_cible}): {lock_level}")
        
        can_open = False
        if lock_level == 0:
            can_open = True
            self.add_message("Porte déverrouillée (Niveau 0)!", (100, 255, 100))
        elif self.inventaire.cles > 0:
            self.inventaire.modifier_cles(-1)
            can_open = True
            self.add_message(f"Clé utilisée. Porte déverrouillée (Niveau {lock_level})!", (100, 255, 100))
        elif lock_level == 1 and self.inventaire.possede_objet("Kit de crochetage"):
            can_open = True
            self.add_message("Kit de crochetage utilisé. Porte déverrouillée!", (100, 255, 100))
        else:
            self.add_message(f"Porte verrouillée (Niveau {lock_level}). Il faut une clé!", (255, 100, 100))
        
        # 3. Si l'ouverture est réussie, démarrer la sélection
        if can_open:
            self.target_row, self.target_col = r_cible, c_cible
            self.last_move_dir_str = direction 
            self.start_room_selection(direction)

    def use_dice_for_reroll(self):
        """
        Consomme un dé pour tirer 3 nouvelles options de pièce.
        """
        if not self.is_selecting_room:
            self.add_message("Vous ne pouvez utiliser le dé que lors de la sélection de pièce.", (255, 100, 100))
            return
        # Check de
        if self.inventaire.des>0:
            self.inventaire.modifier_des(-1)
            self.add_message("Dé utilisé! Nouveau tirage!", (255, 255, 100))
        # Tirer de nouvelles pieces
            new_room_names=self.tirer_pieces(
                    nombre_options=3, 
                    r_cible=self.target_row    
            )
            try:
                
                    self.current_room_options = [creer_piece(name) for name in new_room_names]
            except NameError:
                
                    self.current_room_options = new_room_names 
                    self.add_message("Erreur: Impossible de créer les pièces. Vérifiez 'creer_piece'.", (255, 0, 0))


            self.selected_option_index = 0
            
            if not self.current_room_options:
                    self.add_message("Pioche vide. Tirage échoué. Annulation de la sélection.", (255, 100, 100))
                    self.reset_room_selection()
        else:
            self.add_message("Vous n'avez pas de dé!", (255, 100, 100))
        


    def start_room_selection(self, door_direction):
        """ Déclenche l'état de sélection de pièce avec les options tirées. """
        
        # 1. Tirage des 3 NOMS de pièces (rapide grâce au cache)
        options_noms = self.tirer_pieces(nombre_options=3, r_cible=self.target_row)

        # 2. Instanciation des objets Room complets (avec chargement d'image) (1 seule fois)
        # C'est l'équivalent de la boucle for dans le code externe.
        self.current_room_options = [creer_piece(nom) for nom in options_noms]

        # 2. Aligner chaque pièce tirée au sort
        # La nouvelle pièce doit avoir une porte qui fait face à la pièce actuelle.
        for room in self.current_room_options:
            self.align_room_with_door(room,door_direction)
        
        # 3. Activation de l'état de sélection
        self.is_selecting_room = True
        self.selected_option_index = 0

        if self.current_room_options:
            self.add_message(f"Choisissez parmi {len(self.current_room_options)} pièces!", (255, 200, 100))
        else :
            print("Erreur: Aucune pièce n'a pu être tirée.")
            self.is_selecting_room = False
        
    def handle_selection_movement(self, key):
        """ Gère le mouvement dans le menu de sélection de pièce (Flèches UP/DOWN). """
        if self.is_selecting_room:
            if key == pygame.K_LEFT:
                self.selected_option_index = (self.selected_option_index - 1) % len(self.current_room_options)
            elif key == pygame.K_RIGHT:
                self.selected_option_index = (self.selected_option_index + 1) % len(self.current_room_options)

    def handle_door_action(self, direction, screen):
        """
        Gère l'action "ESPACE" : Déplacement si pièce existante, ou Tente d'ouvrir si pièce nouvelle.
        """

        #Gestion de l'interaction si active
        if self.is_interacting:
            return

        # 1. Calculer la position cible
        dr, dc = 0, 0
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
        
        # 2. Vérifier les limites de la grille (Mur)
        if not (0 <= r_cible < self.grid_height and 0 <= c_cible < self.grid_width):
            self.add_message("Impossible de bouger : il y a un mur!", (255, 100, 100)) 
            return
        
        current_room = self.manoir_grid[self.current_row][self.current_col]
        
        if current_room and current_room.portes:
            direction_enum = DIR_FROM_STR[direction]
        
        if not current_room.portes.a_porte(direction_enum):
            self.add_message("Pas de porte dans cette direction!", (255, 100, 100))
            return

        # 3. Vérifier si la pièce cible existe déjà
        if self.manoir_grid[r_cible][c_cible] is not None:
            # La pièce existe, on se déplace
            #self.try_move_player(direction) 
            self.try_move_player(direction)

        else:
            # La pièce n'existe pas, on tente d'ouvrir une nouvelle porte
            self.check_and_open_door(direction)
        

    def confirm_room_selection(self):
        """ Valide la pièce sélectionnée et l'ajoute à la grille (Entrée). """
        if not self.is_selecting_room:
            return
            
        chosen_room = self.current_room_options[self.selected_option_index]
        
        # Vérification du coût en gemmes
        if self.inventaire.gemmes >= chosen_room.cout_gemmes:
            if chosen_room.cout_gemmes > 0:
                self.inventaire.modifier_gemmes(-chosen_room.cout_gemmes)
                self.add_message(f"Dépensé {chosen_room.cout_gemmes} gemmes", (255, 200, 100))
            
            # Ajout de la pièce à l'emplacement cible (défini par check_and_open_door)
            self.manoir_grid[self.target_row][self.target_col] = chosen_room 

            #APPLICATION DE L'EFFET DE SÉLECTION
            if hasattr(chosen_room, 'moment_effet') and chosen_room.moment_effet == "selection_complete":
                chosen_room.appliquer_effet(self)
            
            # Réinitialisation de l'état
            self.is_selecting_room = False
            self.current_room_options = []
            
            # Le joueur avance immédiatement dans la nouvelle pièce
            self.current_row, self.current_col = self.target_row, self.target_col

            # APPLICATION DE L'EFFET D'ENTRÉE
            #is_entry_effect = hasattr(chosen_room, 'moment_effet') and chosen_room.moment_effet == "entree"

            #if is_entry_effect:
                # Si l'effet est permanent (Chapel), on déclenche l'effet sans condition de visite.
            #    if chosen_room.nom == "Chapel":
             #       chosen_room.appliquer_effet(self)
                # Sinon (Bedroom, Master Bedroom), l'effet se déclenche à la première entrée
              #  else:
               #     chosen_room.appliquer_effet(self)

            # Marquer comme visitée (uniquement si l'effet n'est PAS Chapel/permanent)
            #if chosen_room.nom != "Chapel":
             #   chosen_room.visitee = True

            #chosen_room.visitee = True
            #self.inventaire.modifier_pas(-1)
            #print(f"Pièce choisie : {chosen_room.nom} ajoutée au manoir. Déplacement effectué.")
            #self.check_for_loss_condition()
            
        #else:
         #   print("Pas assez de gemmes pour cette pièce. Veuillez en choisir une autre ou appuyer sur une flèche pour annuler/changer.")

            if hasattr(chosen_room, 'moment_effet') and chosen_room.moment_effet == "entree":
                print(f"[DEBUG] Application effet entrée pour: {chosen_room.nom}")
                # Chapel s'applique à chaque fois, les autres à la première entrée
                if chosen_room.nom == "Chapel":
                    chosen_room.appliquer_effet(self)
                else:
                    chosen_room.appliquer_effet(self)

            # Marquer comme visitée (sauf Chapel qui peut être visitée plusieurs fois pour l'effet)
            if chosen_room.nom != "Chapel":
                chosen_room.visitee = True

            items_to_remove = []
            for item in chosen_room.objets:
                if isinstance(item, str):
                    items_to_remove.append(item)
                    self.collect_item(item)

            for item in items_to_remove:
                chosen_room.objets.remove(item)

            self.inventaire.modifier_pas(-1)
            
            # Message de placement de pièce
            self.add_message(f"{chosen_room.nom} ajoutée! Entrée dans la pièce.", (100, 255, 150))

            
        else:
            # Message d'erreur de gemmes
            self.add_message(f"Besoin de {chosen_room.cout_gemmes} gemmes (vous avez {self.inventaire.gemmes})", (255, 100, 100))
    
    def align_room_with_door(self, room: Room, move_dir_str: str):
        """ 
        Fait tourner la pièce jusqu'à ce qu'une porte soit sur le côté requis 
        (opposé à la direction de mouvement).
        """

        move_dir = DIR_FROM_STR[move_dir_str] 
        required_side = OPPOSITE[move_dir]
        idx_required = required_side.value 
        
        if room.portes is None:
            return
        
        # Tenter jusqu'à 4 rotations (un tour complet)
        for _ in range(4):
            if room.portes.a_porte(required_side):
                # Mise à jour de l'image après la rotation
                room.update_image_from_orientation() 
                return
            # Si pas de porte, on tourne
            room.rotate_clockwise(1)

        room.update_image_from_orientation()
    
    def disperser_or_dans_manoir(self, quantite: int = 3):
        """
        Disperse un nombre spécifié de pièces d'or de manière aléatoire
        dans les pièces déjà placées du manoir. (Effet de l'Office)
        """
        pieces_existantes = []
        for r in range(self.grid_height):
            for c in range(self.grid_width):
                room = self.manoir_grid[r][c]
                # Ne distribuer que dans les pièces qui existent et qui ne sont pas la pièce actuelle
                if room is not None and (r != self.current_row or c != self.current_col):
                    pieces_existantes.append(room)

        if not pieces_existantes:
            self.add_message("Aucune autre pièce disponible pour disperser l'or.", (200, 200, 100))
            return

        import random

        for _ in range(quantite):
            # Choisir une pièce au hasard parmi celles disponibles
            piece_cible = random.choice(pieces_existantes)
            
            # Ajouter l'objet "or" à sa liste d'objets (pour que le joueur le ramasse plus tard)
            piece_cible.objets.append("or")
            print(f"  -> Ajout d'une pièce d'or à : {piece_cible.nom}")

        self.add_message(f"{quantite} pièces d'or dispersées dans le manoir!", (255, 215, 0))

    #pour mettre à jour la map quand on choisit une salle
    def update(self):
        pass

    