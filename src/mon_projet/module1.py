""" classes de base (Room, Porte, Objet, Proba) """

from enum import Enum

class Direction(Enum):
    """Énumération pour les directions des portes"""
    HAUT = 0
    BAS = 1
    DROITE = 2
    GAUCHE = 3


class Porte:
    """
    Classe représentant les portes d'une pièce
    
    Attributs:
        positions: Liste de 4 entiers [up, down, right, left] 
                   1 = porte présente, 0 = pas de porte
        niveaux_verrouillage: Liste des niveaux de verrouillage pour chaque porte
                              0 = déverrouillée, 1 = verrouillée (nécessite une clé), 2 = double tour (nécessite deux clés)
    """
    
    def _init_(self, haut=0, bas=0, droite=0, gauche=0):
        """
        Initialise les portes d'une pièce
        
        Args:
            haut, bas, droite, gauche: 1 si porte présente, 0 sinon
        """
        self.positions = [haut, bas, droite, gauche]
        self.niveaux_verrouillage = [0, 0, 0, 0]  # sera défini lors du placement
    
    def porte_existence (self, direction: Direction) -> bool: #renvoie un bool
        """Vérifie si une porte existe dans la direction donnée"""
        return self.positions[direction.value] == 1
    
    def nombre_portes(self) -> int: #renvoie un entier
        """Retourne le nombre total de portes"""
        return sum(self.positions)
    
    def definir_verrouillage(self, direction: Direction, niveau: int):
        """
        Définit le niveau de verrouillage d'une porte
        
        Args:
            direction: Direction de la porte
            niveau: 0 (déverrouillée), 1 (verrouillée), 2 (double tour)
        """
        if self.porte_existence(direction): #s'il y a une porte dans la direction donnée
            self.niveaux_verrouillage[direction.value] = niveau



class Proba:
    """
    Classe gérant la probabilité de tirage d'une pièce
    
    Attributs:
        rarete: Niveau de rareté (0 à 3)
        poids: Poids calculé pour le tirage aléatoire
    """
    
    def _init_(self, rarete: int = 0):
        """
        Initialise la probabilité
        
        Args:
            rarete: 0 (commun) à 3 (très rare)
            Chaque niveau divise la probabilité par 3
        """
        self.rarete = rarete
        self.poids = self._calculer_poids()
    
    def _calculer_poids(self) -> float:
        """
        Calcule le poids (probabilité) pour le tirage aléatoire
        Rareté 0: poids = 1.0
        Rareté 1: poids = 0.33
        Rareté 2: poids = 0.11
        Rareté 3: poids = 0.037
        """
        return 1.0 / (3 ** self.rarete)


class Room:
    """
    Classe de base représentant une pièce du manoir
    
    Attributs:
        nom: Nom de la pièce
        portes: Objet Porte définissant les portes disponibles
        probabilite: Objet Proba gérant la rareté
        objets: Liste des objets présents dans la pièce
        cout_gemmes: Coût en gemmes pour choisir cette pièce
        couleur: Couleur de la pièce
        effet_special: Description de l'effet spécial (optionnel)
        image_path: Chemin vers l'image de la pièce
    """
    
    def _init_(self, 
                 nom: str,
                 portes: Porte,
                 rarete: int = 0,
                 objets: List[Objet] = None,
                 cout_gemmes: int = 0,
                 couleur: Couleur = Couleur.BLEU,
                 effet_special: str = None,
                 image_path: str = None):
        """
        Initialise une pièce
        
        Args:
            nom: Nom de la pièce
            portes: Objet Porte avec les portes disponibles
            rarete: Niveau de rareté (0-3)
            objets: Liste des objets dans la pièce
            cout_gemmes: Coût en gemmes
            couleur: Couleur de la pièce
            effet_special: Description de l'effet (si applicable)
            image_path: Chemin vers l'image
        """
        self.nom = nom
        self.portes = portes
        self.probabilite = Proba(rarete)
        self.objets = objets if objets else []
        self.cout_gemmes = cout_gemmes
        self.couleur = couleur
        self.effet_special = effet_special
        self.image_path = image_path
        self.visitee = False
    
    def generer_objets(self) -> List[Objet]:
        """
        Génère la liste des objets qui apparaissent effectivement
        selon leurs probabilités
        """
        objets_presents = []
        for objet in self.objets:
            if objet.apparait():
                objets_presents.append(objet)
        return objets_presents
    
    def appliquer_effet(self, jeu_state):
        """
        Applique l'effet spécial de la pièce
        À override dans les sous-classes si nécessaire
        
        Args:
            jeu_state: État du jeu (inventaire, autres pièces, etc.)
        """
        pass