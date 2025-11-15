# -*- coding: utf-8 -*-
from inventaire import Inventaire
from objets import ObjetConsommable

class Joueur:
    """
    [cite_start]Représente le joueur dans le jeu. [cite: 27]
    Contient l'inventaire et gère la position et les actions de base.
    """
    def __init__(self, start_x: int, start_y: int):
        # [cite_start]Le joueur possède un inventaire [cite: 45]
        self.inventaire = Inventaire()
        
        # Position actuelle sur la grille (par exemple, (0, 0))
        self.x = start_x
        self.y = start_y
        print(f"Joueur initialisé à la position ({self.x}, {self.y})")

    def se_deplacer(self, dx: int, dy: int):
        """
        Tente de se déplacer vers une nouvelle case.
        [cite_start]Consomme 1 pas si le déplacement est effectué. [cite: 47]
        (La logique de validation du mur/porte sera dans la classe Jeu/Grille)
        """
        # Pour l'instant, on suppose que le déplacement est toujours valide
        # et on consomme un pas.
        self.inventaire.modifier_pas(-1)
        self.x += dx
        self.y += dy
        print(f"Le joueur se déplace vers ({self.x}, {self.y}).")

    def est_en_vie(self) -> bool:
        """
        Vérifie si le joueur a encore des pas.
        [cite_start]Une des conditions de défaite est d'épuiser son compte de pas. [cite: 34]
        """
        return self.inventaire.pas > 0

    def utiliser_objet(self, objet: ObjetConsommable):
        """
        [cite_start]Utilise un objet consommable (comme de la nourriture). [cite: 72]
        """
        # Délègue l'action à la méthode 'utiliser' de l'objet
        objet.utiliser(self)