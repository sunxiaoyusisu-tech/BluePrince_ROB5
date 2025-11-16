
from abc import ABC, abstractmethod
from src.mon_projet.inventaire import*
import random

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

class BoussoleMagique(ObjetPermanent):
    """
    Objet permanent qui révèle la direction optimale vers l'Antechamber 
    """
    def __init__(self):
        super().__init__("Boussole Magique")

    def utiliser(self, joueur : 'Joueur'):
        print(f"L'objet {self.nom} est un objet passif")
        pass

        # Direction optimale vers l'Antechamber
        #current_row = game.current_row
        #current_col = game.current_col

        # Position de l'Antechamber
        #target_row = 0
        #target_col = 2

        #direction_optimale = []

        #Direction verticale
        #if current_row > target_row:
         #   direction_optimale.append('haut')
        #elif current_row < target_row :
         #   direction_optimale.append('bas')

        #Direction horizontale
        #if current_col > target_col : 
        #    direction_optimale.append('gauche')
        #elif current_col < target_col :
        #    direction_optimale.append('droite')
        
        # Analyse des portes adjacentes
        #current_room = game.manoir_grid[current_row][current_col]
        #infos_portes = {}
        
        #if current_room and current_room.portes:
         #   directions = ["haut", "bas", "droite", "gauche"]
          #  for i, direction in enumerate(directions):
           #     if current_room.portes.positions[i] == 1:
            #        niveau = current_room.portes.niveaux_verrouillage[i]
             #       infos_portes[direction] = niveau
       # return {
        #    'direction optimale' : direction_optimale,
         #   'infos_portes' : infos_portes,
         #   'distance_restante' : abs(current_row - target_row) + abs(current_col - target_col)
        #}
    
    # Ajouter à la classe Inventaire
    #def ajouter_boussole_magique_inventaire(inventaire):
     #   """Extension pour l'inventaire - à ajouter dans inventaire.py"""
      #  inventaire.possede_boussole_magique = False

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
    def __init__(self, contenu_possibles : list):
        super().__init__("Endroit à creuser")
        self.contenu_possibles = contenu_possibles

    def utiliser(self, joueur: 'Joueur'):
        """
        Implémentation requise de la méthode abstraite 'utiliser' de la classe Objet.
        Pour un objet interactif non consommable comme EndroitACreuser, elle ne fait rien.
        """
        pass

    def interagir(self, joueur: 'Joueur') -> str :
        """
        Simule l'interaction. Retourne le nom de l'objet trouvé si creusage simulé réussi, sinon None
        """
        if self.est_utilise:
            print("Tu as déjà creusé ici.")
            return
        
        # Le joueur a la pelle. L'interface lui demande de confirmer l'action
        print("Prêt à creuser")
        return


        #if not joueur.inventaire.possede("Pelle"):
        #    print("Tu n'as pas de pelle pour creuser.")
        #    return

        #self.est_utilise = True
        #import random
        #if random.random() < 0.7:
        #    objet = random.choice(self.contenu_possibles)
        #    joueur.inventaire.ajouter(objet)
        #    print(f"Tu as trouvé {objet.nom} !")
        #else:
        #    print("Rien ici...")

    def effectuer_creusage(self,game) -> str : 
        """
        Effectue le creusage et met à jour l'inventaire si un objet est trouvé 
        """

        if not game.inventaire.possede_pelle:
            return "pas de pelle"
        self.est_utilise = True
        import random

        chance_de_trouver = 0.7
        #loot_table = self.contenu_possibles.copy()
        if game.inventaire.possede_detecteur_metaux:
            chance_de_trouver=1.0
            print("Détecteur de métaux activé!")

        loot_table = self.contenu_possibles.copy()

        if game.inventaire.possede_patte_lapin:
            loot_table.extend(["gemme", "cle", "or", "dé"]) 
            print("Patte de lapin activée!")
        if random.random() < chance_de_trouver:
            if not loot_table:
                return "rien"
            
            #l'objet doit etre instancié / tirer un objet aléatoirement
            nom_objet = random.choice(loot_table)
            return nom_objet
        else:
            return "rien"
        
class Coffre(ObjetInteractif):
    """
    Coffre : peut être ouvert avec une clé ou un marteau.
    Contient des objets aléatoires
    """
    def __init__(self, niveau_verrouillage: int = 1):
        super().__init__("Coffre")
        self.niveau_verouillage = niveau_verrouillage
    
    def utiliser(self, game):
        """ Implémentation pour la méthode abstraite"""
        pass

    def ouvrir_coffre(self,game)->str:
        """
        Ouvre le coffre et retourne le contenu obtenu aléatoirement
        """
        if self.est_utilise:
            return "déjà ouvert"
        
        #Vérifier si on peut ouvrir
        peut_ouvrir_marteau = game.inventaire.possede_marteau
        peut_ouvrir_cle = game.inventaire.cles > 0

        if not (peut_ouvrir_marteau or peut_ouvrir_cle):
            return "impossible"
        
        # Si on a le marteau, on l'utilise (gratuit)
        if peut_ouvrir_marteau:
            print("Coffre ouvert avec le marteau!")
        # Sinon on utilise une clé
        else:
            game.inventaire.modifier_cles(-1)
            print("Coffre ouvert avec une clé!")
        
        #Marquer comme utilisé
        self.est_utilise = True

        # Tirage aleatoire du contenu
        
        #objets possibles dans le coffre + leur probabilité
        coffre_contenu = [
            ("or", 0.25),               # 25% - 1 pièce d'or
            ("or", 0.15),               # 15% - 1 pièce d'or 
            ("gemme", 0.20),            # 20% - 1 gemme
            ("cle", 0.15),              # 15% - 1 clé
            ("dé", 0.10),               # 10% - 1 dé
            ("pomme", 0.08),            # 8% - 1 pomme (+ 2 pas)
            ("banane",0.05),            # 5% - 1 banane (+3 pas)
            ("rien", 0.07)              # 7% - rien
        ]

        # Effet de la boussole 
        if game.inventaire.possede_boussole_magique:
            print("Boussole Magique activée! Augmentation de la chance de Clés.")
            coffre_contenu = [
                ("or", 0.20),               # 20%
                ("or", 0.10),               # 10%
                ("gemme", 0.20),            # 20%
                ("cle", 0.25),              # 25% (AUGMENTÉ)
                ("dé", 0.10),               # 10%
                ("pomme", 0.08),            # 8%
                ("banane", 0.05),           # 5%
                ("rien", 0.02)              # 2% (RÉDUIT)
            ]

        # Tirer un objet selon les probabilités
        objets = [item[0] for item in coffre_contenu]
        probas = [item[1] for item in coffre_contenu]

        objet_trouve = random.choices(objets, weights=probas, k =1)[0]

        return objet_trouve

