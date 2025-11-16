from typing import List, Optional
# On importe les types d'objets, pas les instances
from src.mon_projet.objets import*

"""
Inventaire du joueur : gestion des ressources et des objets permanents.
"""

class Inventaire:
    """Objets consommables + Objets permanents"""
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
        self.possede_boussole_magique : bool = False
        self.passe_muraille: int = 1
        self.PASSE_MURAILLE_MAX: int = 1
        #self.objets_permanents: List[ObjetPermanent] = []

    # operation sur pas
    def modifier_pas(self,n:int) -> bool :
        """ (positif = gain, négatif = perte). 
        Retourne True si l'opération est valide (pas >= 0) """
        self.pas += n
        if self.pas < 0:
            self.pas = 0
            return False #plus de pas
        return True
    
    # operation sur gold
    def modifier_or(self,n:int) -> bool : 
        # Retourne True si le solde final est >= 0
        self.pieces_or += n
        return self.pieces_or >= 0

    
    # operation sur gemmes
    def modifier_gemmes(self,n:int) -> bool :
        self.gemmes +=n
        return self.gemmes >=0


    # operation sur cles
    def modifier_cles(self,n: int) -> bool:
        """ modifie le nb de cles. Retourne True si le solde final est >= 0 """
        self.cles +=n
        return self.cles >=0
    
    # operation sur des
    def modifier_des(self,n:int) -> bool :
        """Modifie les dés. Retourne True si le solde final est >= 0."""
        self.des += n
        return self.des >= 0
    def modifier_passe_muraille(self, n: int) -> bool:
        """
        Modifie les Passes-muraille.
        Retourne True si l'opération réussit, False si on dépasse le max.
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
        "verifie si le joueur possede un objet permanent precis"
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
        if nom_objet == "Boussole Magique":
            return self.possede_boussole_magique
        return False
    

def use_wall_pass(self, direction):
        """
        Tente d'utiliser un Passe-muraille pour CRÉER une porte là où il y a un mur.
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

        # 4. Action ! (Consommer l'objet)
        # On essaie de consommer l'objet
        consommation_reussie = self.inventaire.modifier_passe_muraille(-1)
        
        if not consommation_reussie:
             # Ne devrait jamais arriver si l'étape 1 a fonctionné, mais c'est une sécurité
             self.add_message("Erreur: Impossible d'utiliser le Passe-muraille.", (255, 0, 0))
             return

        self.add_message("Passe-muraille utilisé! Un passage s'ouvre.", (255, 215, 0))

        # 5. (La magie est ici)
        current_room.portes.positions[direction_enum.value] = 1 
        
        # 6. Réutiliser la logique de porte existante !
        self.check_and_open_door(direction)