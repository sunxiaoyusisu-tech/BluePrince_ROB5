""" classes de base (Room, Porte, Objet, Proba) """

from enum import *
import numpy as np
from random import random
import pygame

class Direction(Enum):
    """Énumération pour les directions des portes"""
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3

class Porte:
    """
    Classe représentant les portes d'une pièce
    
    Attributs:
        positions: Liste de 4 entiers [up, down, right, left]
                  1 = porte présente, 0 = pas de porte
        niveaux_verrouillage: Liste des niveaux de verrouillage pour chaque porte
                             0 = déverrouillée, 1 = verrouillée, 2 = double tour
    """
    
    def __init__(self, up, down, right, left):
        """
        Initialise les portes d'une pièce
        
        Args:
            up, down, right, left: 1 si porte présente, 0 sinon
        """
        self.positions = [up, down, right, left]  # [up, down, right, left]
        self.niveaux_verrouillage = [0, 0, 0, 0]  # Sera défini lors du placement
        self.franchissement = [False, False, False, False]  # Indique si la porte a été franchie
    

    def a_porte(self, direction: Direction) -> bool:
        """Vérifie si une porte existe dans la direction donnée"""
        return self.positions[direction.value] == 1
    
    def a_ete_franchie(self, direction: Direction) -> bool:
        """Vérifie si une porte a été franchie (exemple d'utilisation future)"""
        self.franchissement[direction.value] = True
        pass
   
    
    def definir_verrouillage(self, direction: Direction, niveau: int):
        """
        Définit le niveau de verrouillage d'une porte
        
        Args:
            direction: Direction de la porte
            niveau: 0 (déverrouillée), 1 (verrouillée), 2 (double tour)
        """
        if self.a_porte(direction):
            self.niveaux_verrouillage[direction.value] = niveau

    def rotate_clockwise(self, quarter_turns:int= 1):
        """Fait tourner les portes de 90° dans le sens horaire."""
        for _ in range(quarter_turns):
            up,down,right,left =self.positions
            self.positions = [left,right,up,down]
#class CouleurPiece(Enum):
#    JAUNE = "jaune"       # magasins
#    VERTE = "verte"       # jardins d’intérieur
#    VIOLETTE = "violette" # chambres (rendre des pas)
#    ORANGE = "orange"     # couloirs (souvent beaucoup de portes)
#    ROUGE = "rouge"       # effets indésirables
#    BLEUE = "bleue"       # communes, variées

class OutilCreusage(Enum):
    PELLE = auto()             # Shovel
    PELLE_DETECTEUR = auto()   # Detector Shovel
    MARTEAU_PIQUEUR = auto()   # Jack Hammer

class Proba:
    """
    Classe gérant la probabilité de tirage d'une pièce
    
    Attributs:
        rarete: Niveau de rareté (0 à 3)
        poids: Poids calculé pour le tirage aléatoire
    """
    
    def __init__(self, rarete: int):
        """
        Initialise la probabilité d'une pièce
        
        Args:
            rarete: Niveau de rareté (0 à 3)
            poids: Poids pour le tirage aléatoire
        """
        self.rarete = rarete
        self.poids = self._calculer_poids()

    def _calculer_poids(self) -> float:
        """Calcule le poids pour le tirage aléatoire
        Rareté 0: poids = 1.0 (CommonPlace)
        Rareté 1: poids = 0.33 (Standard)
        Rareté 2: poids = 0.11 (Unusual)
        Rareté 3: poids = 0.037 (rare)
        """
        return 1.0 / (3 ** self.rarete)



#class Pouvoir:
    """
    Classe représentant un pouvoir spécial d'une pièce
    
    Attributs:
        description: Description du pouvoir
        effet: Effet du pouvoir (fonction ou valeur)
    """
    
#    def __init__(self):
        
 #   def trou(self,nb_pelle):
  #      if nb_pelle>1:  # vérifie si y'a une pelle
            #permet de récupérer les objets du trou
   #         pass
    
    #def magasin(self,argent):
     #   if argent>=c:
            #permet d'acheter un objet de cout c
            #ajouter objet à l'inventaire
      #      pass
    
    #def plus_de_pas(self):
        #retire 1 pas de plus dans l'inventaire
     #   pass


class Room:
    """
    Classe représentant une pièce dans le jeu
    
    Attributs:
        nom: Nom de la pièce
        portes: Instance de la classe Porte
        rarete: Niveau de rareté de la pièce (0 à 3)
        objets: Liste des objets présents dans la pièce
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
        Initialise une pièce
        
        Args:
            nom: Nom de la pièce
            portes: Instance de la classe Porte
            rarete: Niveau de rareté (0 à 3)
            objets: Liste des objets présents dans la pièce
            proba_obj: Instance de la classe Proba pour les objets
            cout_gemmes: Coût en gemmes pour choisir cette pièce
            pouvoir: Instance de la classe Pouvoir (optionnel)
            image_path: Chemin vers l'image de la pièce (optionnel)
        """
        self.nom = nom
        self.portes = portes
        self.rarete = Proba(rarete)
        self.objets = objets if objets is not None else []
        self.proba_obj = proba_obj if proba_obj is not None else [] #liste de meme taille que objets
        self.cout_gemmes = cout_gemmes
        #self.pouvoir = pouvoir.nom_du_pouvoir if pouvoir is not None else []
        self.image_path = image_path
        self.visitee = False
        #self.image = nom + ".png"  # Nom de l'image associée à la pièce
        self.orientation=0
        #pos oringinal #0:0de 1:90de etc...

        if self.image_path:
            # Charger l'image à partir du chemin
            temp_image = pygame.image.load(self.image_path).convert_alpha()
            temp_image=pygame.transform.scale(temp_image,(80,80))
            self.base_image=temp_image
            self.image=temp_image
            
            # Redimensionner l'image à la taille standard de la grille (80x80 pixels, d'après jeu.py)
            
        else:
            # Créer une surface par défaut (carré noir) si le chemin est manquant
            self.image = pygame.Surface((80, 80))
            self.base_image.fill((0, 0, 0))
            self.image=self.base_image

    #def apparait(self) -> bool: #c'est généré objet
        """
        Détermine si un objet apparaît dans la pièce selon sa probabilité
        
        Args:
            objet: Instance de la classe Objet
            
        Returns:
            bool: True si l'objet apparaît, False sinon
        """
        #return (np.random.choice(self.objets, np.random.choice([0, 1, 2, 3],1,p=[0.4,0.3,0.2,0.1]), p=self.proba_obj))
    
    #def appliquer_effet(self, jeu_state):
        """
        Applique l'effet spécial de la pièce
        À override dans les sous-classes si nécessaire
        
        Args:
            jeu_state: État du jeu (inventaire, autres pièces, etc.)
        """
        #pass

    #def generer_objets_lucky(self, mods: ChanceModifiers):
        """
        Génère éventuellement des objets bonus dans la pièce
        selon sa couleur et les ChanceModifiers (Rabbit Foot, etc.)
        """
        # Table des objets potentiels par couleur
     #   loot_by_color = {
      #      CouleurPiece.VERTE:  ["gemme", "banane", "pelle"],
       #     CouleurPiece.VIOLETTE: ["pomme", "gateau"],
        #    CouleurPiece.JAUNE:  ["piece_or", "cle"],
         #   CouleurPiece.BLEUE:  ["pomme", "gemme", "piece_or"],
          #  CouleurPiece.ROUGE:  ["gemme"],  # très faible proba
           # CouleurPiece.ORANGE: [],
        #}

        #base_chance = {
         #   CouleurPiece.VERTE:  0.40,
          #  CouleurPiece.VIOLETTE: 0.30,
           # CouleurPiece.JAUNE:  0.20,
            #CouleurPiece.BLEUE:  0.15,
            #CouleurPiece.ROUGE:  0.05,
            #CouleurPiece.ORANGE: 0.00,
        #}

        #loot_table = loot_by_color.get(self.couleur, [])
        #p = base_chance.get(self.couleur, 0.1)

        #if not loot_table or p <= 0:
         #   return  # rien à faire

        # “if you’re lucky” → tirage de base
        #if not self.tirage_avec_chance(p, "object", mods, reroll_if_close=True):
         #   return

        # Si réussite : on choisit un objet bonus
        #objet = random.choice(loot_table)
        #self.objets.append(objet)
        #self.proba_obj.append(1.0)  # objet garanti une fois ajouté
        #print(f"Chanceux ! Un objet bonus '{objet}' apparaît dans {self.nom}.")
    def rotate_clockwise(self,quarter_turns:int=1):
        # faire rotation de room et puis uptade portes
        for _ in range(quarter_turns):
            if self.portes is not None:
                self.portes.rotate_clockwise(1)
            self.orientation=(self.orientation+1)%4
    def update_image_from_orientation(self):
        angle=-90*self.orientation
        self.image=pygame.transform.rotate(self.base_image, angle)