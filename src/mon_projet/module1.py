""" classes de base (Room, Porte, Objet, Proba) """

from enum import *
import numpy as np

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
    
    def _init_(self, up, down, right, left):
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

class Proba:
    """
    Classe gérant la probabilité de tirage d'une pièce
    
    Attributs:
        rarete: Niveau de rareté (0 à 3)
        poids: Poids calculé pour le tirage aléatoire
    """
    
    def __init__(self, rarete: int, poids: float):
        """
        Initialise la probabilité d'une pièce
        
        Args:
            rarete: Niveau de rareté (0 à 3)
            poids: Poids pour le tirage aléatoire
        """
        self.rarete = rarete
        self.poids = poids

    def _calculer_poids(self) -> float:
        """Calcule le poids pour le tirage aléatoire
        Rareté 0: poids = 1.0
        Rareté 1: poids = 0.33
        Rareté 2: poids = 0.11
        Rareté 3: poids = 0.037
        """
        return 1.0 / (3 ** self.rarete)



class Pouvoir:
    """
    Classe représentant un pouvoir spécial d'une pièce
    
    Attributs:
        description: Description du pouvoir
        effet: Effet du pouvoir (fonction ou valeur)
    """
    
    def __init__(self):
        """
        Initialise un pouvoir
        """
        
    def trou(self,nb_pelle):
        if nb_pelle>1:  # vérifie si y'a une pelle
            #permet de récupérer les objets du trou
            pass
    
    def magasin(self,argent):
        if argent>=c:
            #permet d'acheter un objet de cout c
            #ajouter objet à l'inventaire
            pass
    
    def plus_de_pas(self):
        #retire 1 pas de plus dans l'inventaire
        pass


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
                 pouvoir: Pouvoir = None, nom_du_pouvoir: str = None,
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
        self.pouvoir = pouvoir.nom_du_pouvoir if pouvoir is not None else []
        self.image_path = image_path
        self.visitee = False
        #self.image = nom + ".png"  # Nom de l'image associée à la pièce

    def apparait(self) -> bool: #c'est généré objet
        """
        Détermine si un objet apparaît dans la pièce selon sa probabilité
        
        Args:
            objet: Instance de la classe Objet
            
        Returns:
            bool: True si l'objet apparaît, False sinon
        """
        return (np.random.choice(self.objets, np.random.choice([0, 1, 2, 3],1,p=[0.4,0.3,0.2,0.1]), p=self.proba_obj))



    
    def appliquer_effet(self, jeu_state):
        """
        Applique l'effet spécial de la pièce
        À override dans les sous-classes si nécessaire
        
        Args:
            jeu_state: État du jeu (inventaire, autres pièces, etc.)
        """
        pass
