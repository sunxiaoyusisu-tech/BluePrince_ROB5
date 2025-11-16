""" classes de base (Room, Porte, Objet, Proba) """

from enum import *
import numpy as np
from random import random
import pygame

class Direction(Enum):
    
    """Énumération pour les directions des portes (utilisé pour les index)"""

    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3

class Porte:

    """
    Classe représentant les portes d'une pièce
    """
    
    def __init__(self, up, down, right, left):

        """
        Initialise les portes d'une pièce.

        Args:
            up (int): 1 si porte vers le haut, 0 sinon.
            down (int): 1 si porte vers le bas, 0 sinon.
            right (int): 1 si porte vers la droite, 0 sinon.
            left (int): 1 si porte vers la gauche, 0 sinon.
        """

        self.positions = [up, down, right, left]  # [up, down, right, left]
        self.niveaux_verrouillage = [0, 0, 0, 0]  # Sera défini lors du placement
        self.franchissement = [False, False, False, False]  # Indique si la porte a été franchie
    

    def a_porte(self, direction: Direction) -> bool:
        
        """
        Vérifie si une porte existe dans la direction donnée.

        Args:
            direction (Direction): La direction à vérifier (UP, DOWN, RIGHT, LEFT).

        Returns:
            bool: True si une porte est présente, False sinon.
        """

        return self.positions[direction.value] == 1
    
    def a_ete_franchie(self, direction: Direction) -> bool:
        
        """
        Marque une porte comme franchie (méthode de transition).
        
        Args:
            direction (Direction): La direction de la porte franchie.
        """

        self.franchissement[direction.value] = True
        pass
   
    
    def definir_verrouillage(self, direction: Direction, niveau: int):
        
        """
        Définit le niveau de verrouillage d'une porte.

        Args:
            direction (Direction): Direction de la porte.
            niveau (int): 0 (déverrouillée), 1 (verrouillée), 2 (double tour).
        """

        if self.a_porte(direction):
            self.niveaux_verrouillage[direction.value] = niveau

    def rotate_clockwise(self, quarter_turns:int= 1):
        
        """
        Fait tourner les positions des portes de 90° dans le sens horaire.

        Args:
            quarter_turns (int): Nombre de rotations de 90° (par défaut 1).
        """

        for _ in range(quarter_turns):
            up,down,right,left =self.positions
            self.positions = [left,right,up,down]


class Proba:

    """
    Classe gérant la probabilité de tirage d'une pièce en fonction de sa rareté.
    """
    
    def __init__(self, rarete: int):
        
        """
        Initialise la probabilité d'une pièce.

        Args:
            rarete (int): Niveau de rareté (0 à 3).
        """

        self.rarete = rarete
        self.poids = self._calculer_poids()

    def _calculer_poids(self) -> float:

        """
        Calcule le poids pour le tirage aléatoire.
        La probabilité est divisée par trois pour chaque incrément de rareté.

        Returns:
            float: Le poids pour le tirage pondéré.
        """
        # Rareté 0: poids = 1.0
        # Rareté 1: poids = 1/3 (0.33)
        # Rareté 2: poids = 1/9 (0.11)
        # Rareté 3: poids = 1/27 (0.037)

        return 1.0 / (3 ** self.rarete)


class Room:

    """
    Classe représentant une pièce dans le jeu (le nœud du manoir).
    """
    
    def __init__(self, 
                 nom: str,
                 portes: Porte, 
                 rarete: int, 
                 objets: list = None,
                 proba_obj: list = None,
                 cout_gemmes: int = 0,
                 #pouvoir: Pouvoir = None, nom_du_pouvoir: str = None,
                 image_path: str = None):
       
        """
        Initialise une pièce.

        Args:
            nom (str): Nom de la pièce.
            portes (Porte): Instance de la classe Porte.
            rarete (int): Niveau de rareté (0 à 3).
            objets (list, optional): Liste des objets présents dans la pièce. Defaults to None.
            proba_obj (list, optional): Probabilités d'apparition des objets. Defaults to None.
            cout_gemmes (int, optional): Coût en gemmes pour choisir cette pièce. Defaults to 0.
            image_path (str, optional): Chemin vers l'image de la pièce. Defaults to None.
        """

        self.nom = nom
        self.portes = portes
        self.rarete = Proba(rarete)
        self.objets = objets if objets is not None else []
        self.proba_obj = proba_obj if proba_obj is not None else [] #liste de meme taille que objets
        self.cout_gemmes = cout_gemmes
        self.image_path = image_path
        self.visitee = False
        self.orientation=0

        if self.image_path:

            # Charger l'image à partir du chemin
            temp_image = pygame.image.load(self.image_path).convert_alpha()
            temp_image = pygame.transform.smoothscale(temp_image, (80, 80))
            self.base_image=temp_image
            self.image=temp_image
            
            # Redimensionner l'image à la taille standard de la grille (80x80 pixels, d'après jeu.py)
            
        else:
            # Créer une surface par défaut (carré noir) si le chemin est manquant
            self.image = pygame.Surface((80, 80))
            self.base_image.fill((0, 0, 0))
            self.image=self.base_image

    def rotate_clockwise(self,quarter_turns:int=1):

        """
        Fait tourner la pièce et l'objet Porte associé de 90° dans le sens horaire.

        Args:
            quarter_turns (int): Nombre de rotations de 90° (par défaut 1).
        """
        
        for _ in range(quarter_turns):
            if self.portes is not None:
                self.portes.rotate_clockwise(1)
            self.orientation=(self.orientation+1)%4

    def update_image_from_orientation(self):

        """
        Met à jour l'image affichée de la pièce en fonction de son orientation actuelle.
        """

        angle=-90*self.orientation
        
        # On utilise self.base_image pour une rotation correcte (image non déformée)
        self.image=pygame.transform.rotate(self.base_image, angle)