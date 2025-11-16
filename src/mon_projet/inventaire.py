from typing import List, Optional
import numpy as np
from src.mon_projet.module1 import*

"""
Inventaire du joueur : gestion des ressources et des objets permanents.
"""

DIR_FROM_STR = {
    "haut": Direction.UP,
    "bas": Direction.DOWN,
    "droite": Direction.RIGHT,
    "gauche": Direction.LEFT,
}

class Inventaire:
    
    """
    Gère tous les objets consommables (pas, or, gemmes, clés, dés) 
    et les objets permanents du joueur.
    """

    def __init__(self):

        # Objets consommables
        self.pas:int=70
        self.pieces_or:int=5
        self.gemmes:int=2
        self.cles:int=5
        self.des:int=2

        #Objets permanents
        self.possede_pelle : bool = False
        self.possede_marteau : bool = False
        self.possede_kit_crochetage : bool = False
        self.possede_detecteur_metaux : bool = False
        self.possede_patte_lapin: bool = False
        self.passe_muraille: int = 1
        self.PASSE_MURAILLE_MAX: int = 1

    # operation sur pas
    def modifier_pas(self,n:int) -> bool :
        
        """ 
        Modifie le nombre de pas. 

        Args:
            n (int): La quantité de pas à ajouter (positif) ou retirer (négatif).

        Returns:
            bool: True si l'opération est valide (pas >= 0), False sinon (défaite).
        """

        self.pas += n
        if self.pas < 0:
            self.pas = 0
            return False #plus de pas
        return True
    
    # operation sur gold
    def modifier_or(self,n:int) -> bool : 

        """ 
        Modifie le nombre de pièces d'or.

        Args:
            n (int): La quantité d'or à ajouter ou retirer.

        Returns:
            bool: True si le solde final est >= 0, False si l'achat échoue.
        """

        # Retourne True si le solde final est >= 0
        self.pieces_or += n
        return self.pieces_or >= 0

    
    # operation sur gemmes
    def modifier_gemmes(self,n:int) -> bool :

        """ 
        Modifie le nombre de gemmes.

        Args:
            n (int): La quantité de gemmes à ajouter ou retirer.

        Returns:
            bool: True si le solde final est >= 0.
        """

        self.gemmes +=n
        return self.gemmes >=0


    # operation sur clés
    def modifier_cles(self,n: int) -> bool:

        """ 
        Modifie le nombre de clés.

        Args:
            n (int): La quantité de clés à ajouter ou retirer.

        Returns:
            bool: True si le solde final est >= 0.
        """
        
        self.cles +=n
        return self.cles >=0
    
    # operation sur dés
    def modifier_des(self,n:int) -> bool :

        """
        Modifie le nombre de dés.

        Args:
            n (int): La quantité de dés à ajouter ou retirer.

        Returns:
            bool: True si le solde final est >= 0.
        """
        
        self.des += n
        return self.des >= 0
    
    def modifier_passe_muraille(self, n: int) -> bool:

        """
        Modifie le nombre de Passes-muraille possédés.

        Gère l'ajout jusqu'à une limite maximale (PASSE_MURAILLE_MAX) et la soustraction
        jusqu'à zéro.

        Args:
            n (int): La quantité de Passes-muraille à ajouter (positif) ou à retirer (négatif).

        Returns:
            bool: True si l'opération réussit (ajout ou retrait dans les limites), 
              False si l'ajout est impossible car le maximum est atteint, ou si 
              le retrait est impossible car le stock est déjà vide.
        """

        # Si on essaie d'en AJOUTER (n > 0)
        if n > 0:
            if self.passe_muraille >= self.PASSE_MURAILLE_MAX:
                self.passe_muraille = self.PASSE_MURAILLE_MAX # Assurer qu'on reste au max
                return False # Échec : Déjà plein
            
            self.passe_muraille += n
            return True
        
        # Si on essaie d'en ENLEVER (n < 0)
        else:
            if self.passe_muraille <= 0:
                return False # Échec : Déjà vide
            self.passe_muraille += n
            return True # L'utilisation réussit

    def possede_objet(self,nom_objet = str) -> bool :

        """
        Vérifie si le joueur possède un objet permanent précis.

        Args:
            nom_objet (str): Le nom de l'objet permanent (ex: "Kit de crochetage").

        Returns:
            bool: True si le joueur possède l'objet, False sinon.
        """
        
        if nom_objet == "Kit de crochetage":
            return self.possede_kit_crochetage
        if nom_objet == "Pelle":
            return self.possede_pelle
        if nom_objet == "Marteau":
            return self.possede_marteau
        if nom_objet == "Detecteur_metaux":
            return self.possede_detecteur_metaux
        if nom_objet == "Patte de lapin":
            return self.possede_patte_lapin
        return False
    

def use_wall_pass(self, direction):
        
        """
        Tente d'utiliser un Passe-muraille pour CRÉER une porte dans la pièce actuelle
        vers une case non découverte (mur), puis lance le processus de sélection de pièce.

        L'action échoue si :
        - L'objet n'est pas possédé.
        - Une porte existe déjà dans cette direction.
        - La direction mène hors de la grille.
        - La case cible est déjà occupée par une pièce.

        Args:
            direction (str): La direction dans laquelle tenter de créer la porte 
                         ("haut", "bas", "droite", "gauche").
        """

        # 1. Vérifier si on a l'objet
        if self.inventaire.passe_muraille <= 0:
            self.add_message("Vous n'avez pas de Passe-muraille.", (255, 100, 100))
            return

        current_room = self.manoir_grid[self.current_row][self.current_col]
        direction_enum = DIR_FROM_STR[direction]

        # 2. Vérifier si une porte EXISTE DÉJÀ
        if current_room.portes.a_porte(direction_enum):
            self.add_message("Il y a déjà une porte ici. Utilisez ESPACE.", (255, 200, 100))
            return

        # 3. Vérifier les limites de la grille (logique copiée de handle_door_action)
        dr, dc = 0, 0
        if direction == "droite": dr, dc = 0, 1
        elif direction == "gauche": dr, dc = 0, -1
        elif direction == "haut": dr, dc = -1, 0
        elif direction == "bas": dr, dc = 1, 0
        
        r_cible, c_cible = self.current_row + dr, self.current_col + dc

        if not (0 <= r_cible < self.grid_height and 0 <= c_cible < self.grid_width):
            self.add_message("Impossible de créer une porte hors du manoir!", (255, 100, 100))
            return
        if self.manoir_grid[r_cible][c_cible] is not None:
            self.add_message("Cet espace est déjà occupé!", (255, 100, 100))
            return

        # 4. On essaie de consommer l'objet
        consommation_reussie = self.inventaire.modifier_passe_muraille(-1)
        
        if not consommation_reussie:
             # Ne devrait jamais arriver si l'étape 1 a fonctionné, mais c'est une sécurité
             self.add_message("Erreur: Impossible d'utiliser le Passe-muraille.", (255, 0, 0))
             return

        self.add_message("Passe-muraille utilisé! Un passage s'ouvre.", (255, 215, 0))

        current_room.portes.positions[direction_enum.value] = 1 
        
        # Réutiliser la logique de porte existante
        self.check_and_open_door(direction)