
from abc import ABC, abstractmethod

# Fait venir la classe Joueur pour éviter les dépendances circulaires
# avec les type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from joueur import Joueur

class Objet(ABC):
    """
    Classe abstraite de base pour tous les objets du jeu.
    """
    def __init__(self, nom: str):
        self.nom = nom # Le nom de l'objet

    @abstractmethod
    def utiliser(self, joueur: 'Joueur'):
        """
        Méthode abstraite pour utiliser l'objet.
        L'effet dépendra du type d'objet.
        """
        pass

    def __str__(self):
        return self.nom

class ObjetPermanent(Objet):
    """
    Classe pour les objets permanents qui fournissent un avantage constant.
    Pelle, Marteau, Kit de crochetage.
    """
    def __init__(self, nom: str):
        super().__init__(nom)

    def utiliser(self, joueur: 'Joueur'):
        """
        Les objets permanents sont généralement passifs ou leur utilisation
        est contextuelle (par exemple, avoir la pelle permet de creuser).
        Cette méthode pourrait ne rien faire directement.
        """
        print(f"L'objet {self.nom} est un objet passif.")
        pass

class ObjetConsommable(Objet):
    """
    Classe pour les objets consommables, comme la nourriture qui redonne des pas.
    Pomme, Banane, Gâteau.
    """
    def __init__(self, nom: str, pas_rendus: int):
        super().__init__(nom)
        self.pas_rendus = pas_rendus # Nombre de pas que cet objet restaure

    def utiliser(self, joueur: 'Joueur'):
        """
        Utiliser l'objet consommable.
        Augmente les pas du joueur.
        """
        # On ne peut pas importer Joueur en haut à cause d'une dépendance circulaire
        # avec Inventaire, donc on accède à l'inventaire comme ça.
        joueur.inventaire.modifier_pas(self.pas_rendus)
        print(f"{self.nom} utilisé. Vous gagnez {self.pas_rendus} pas.")

# Exemples d'objets spécifiques

# Objets Permanents
class Pelle(ObjetPermanent):
    def __init__(self):
        super().__init__("Pelle")

class Marteau(ObjetPermanent):
    def __init__(self):
        super().__init__("Marteau")

class KitCrochetage(ObjetPermanent):
    def __init__(self):
        super().__init__("Kit de crochetage")

#Objets Consommables (Nourriture)
class Pomme(ObjetConsommable):
    def __init__(self):
        super().__init__("Pomme", 2) #Redonne 2 pas

class Banane(ObjetConsommable):
    def __init__(self):
        super().__init__("Banane", 3) # Redonne 3 pas

class Gateau(ObjetConsommable):
    def __init__(self):
        super().__init__("Gâteau", 10) # Redonne 10 pas

class ObjetInteractif(Objet):
    """
    Classe de base pour les objets interactifs (non ramassables).
    """
    def __init__(self, nom: str):
        super().__init__(nom)
        self.est_utilise = False 

    def interagir(self, joueur: 'Joueur'):
        """
        Méthode d'interaction, à redéfinir dans les sous-classes.
        """
        pass


class EndroitACreuser(ObjetInteractif):
    """
    Endroit à creuser : peut être utilisé avec une pelle.
    """
    def __init__(self, contenu_possibles):
        super().__init__("Endroit à creuser")
        self.contenu_possibles = contenu_possibles

    def interagir(self, joueur: 'Joueur'):
        if self.est_utilise:
            print("Tu as déjà creusé ici.")
            return
        if not joueur.inventaire.possede("Pelle"):
            print("Tu n'as pas de pelle pour creuser.")
            return

        self.est_utilise = True
        import random
        if random.random() < 0.7:
            objet = random.choice(self.contenu_possibles)
            joueur.inventaire.ajouter(objet)
            print(f"Tu as trouvé {objet.nom} !")
        else:
            print("Rien ici...")
