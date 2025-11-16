""" Logique du jeu (gestion de l'inventaire, déplacements, catalogue de pièces) """

from src.mon_projet.module1 import*
from src.mon_projet.objets import*
import random
from src.mon_projet.objets import (
    PasseMuraille  # <-- Assurez-vous que ceci est ajouté
)

def random_objects_selection(objets_possibles, probabilites):

    """
    Sélectionne aléatoirement quels objets apparaissent dans une pièce en 
    fonction des probabilités données.

    Args : 
        objets_possibles (list): Liste de tous les objets qui peuvent apparaître (instances ou str).
        probabilites (list): Liste des probabilités (0.0 à 1.0) pour chaque objet.
    
    Returns : 
        list : Liste des objets qui apparaissent réellement dans la pièce.

    """

    objets_selectionnes = []

    # S'assure que les listes ont la même longueur
    while len(probabilites) < len(objets_possibles):
        # utilise 50% par défaut pour les objets sans probabilité spécifiée
        probabilites.append(0.5) 

    for i, objet in enumerate(objets_possibles):
        if random.random() < probabilites[i]:
            objets_selectionnes.append(objet)
    return objets_selectionnes

# Classes (enfants) pour gerer les effets speciaux

class RoomEffetEntree(Room):

    """
    Classe parente abstraite pour les pièces avec un effet qui se déclenche 
    quand le joueur y entre pour la première fois (ou à chaque fois pour certaines)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.moment_effet = "entree"

    def appliquer_effet(self, game_instance):

        """Méthode abstraite. Applique l'effet à l'inventaire ou à l'état du jeu.
        Doit être implémentée dans les classes enfants.

        Args:
            game_instance (Game): L'instance actuelle du jeu.
        
        """

        # Ceci est la méthode abstraite qui sera implémentée dans les classes enfants
        pass

class RoomEffetSelection(Room):

    """
    Classe parente abstraite pour les pièces avec un effet qui 
    se déclenche lorsque la pièce est choisie (ajoutée au manoir)
    par le joueur
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.moment_effet = "selection_complete"

    def appliquer_effet(self, game_instance):

        """
        Méthode abstraite. Applique l'effet à l'inventaire ou à l'état du jeu lors de la sélection.
        Doit être implémentée dans les classes enfants.

        Args:
            game_instance (Game): L'instance actuelle du jeu.
        """

        # Ceci est la méthode abstraite qui sera implémentée dans les classes enfants
        pass


#Pièces Spéciales

class BedroomRoom(RoomEffetEntree):
    
    """ 
    Pièce spéciale: Gagne deux pas lors de la première entrée.
    Hérite de RoomEffetEntree.
    """

    def appliquer_effet(self, game_instance):

        game_instance.inventaire.modifier_pas(2)
        print(f"Effet {self.nom} : Gagne 2 pas")

class ChapelRoom(RoomEffetEntree):

    """ 
    Pièce spéciale: Perd 1 pièce d'or à chaque entrée.
    Hérite de RoomEffetEntree.
    """

    def appliquer_effet(self, game_instance):

        # Utilise modifier_or, qui gère si le solde devient négatif
        game_instance.inventaire.modifier_or(-1)
        print(f"Effet {self.nom} : Perd 1 pièce d'or")

class NookRoom(RoomEffetEntree):

    """ 
    Pièce spéciale: Gagne 1 clé lors de la première entrée.
    Hérite de RoomEffetEntree.
    """
    
    def appliquer_effet(self, game_instance):

        game_instance.inventaire.modifier_cles(1)
        print(f"Effet {self.nom} : Gagne 1 clé")

class MusicRoom(RoomEffetEntree):
    
    """
    Pièce spéciale: Gagne 2 clés lors de la première entrée.
    Hérite de RoomEffetEntree.
    """

    def appliquer_effet(self, game_instance):

        game_instance.inventaire.modifier_cles(2)
        print(f"Effet {self.nom} : Gagne 2 clés")

class GarageRoom(RoomEffetEntree):
    
    """
    Pièce spéciale: Gagne 3 clés lors de la première entrée.
    Hérite de RoomEffetEntree.
    """

    def appliquer_effet(self, game_instance):

        game_instance.inventaire.modifier_cles(3)
        print(f"Effet {self.nom} : Gagne 3 clés")

class PoolRoom(RoomEffetSelection):

    """
    Pièce spéciale: Ajoute des pièces spécifiques au catalogue
    lorsqu'elle est sélectionnée. Hérite de RoomEffetSelection.
    """

    def appliquer_effet(self, game_instance):

        # Ajoute des pièces spécifiques au catalogue des pièces
        pieces_a_ajouter = ["Sauna", "Coat Check"]
        game_instance.ajouter_pieces_au_catalogue(pieces_a_ajouter)
        print(f"Effet {self.nom} : Ajout de {pieces_a_ajouter} au catalogue !")

class MasterBedroom(RoomEffetEntree):

    """
    Pièce spéciale: Gagne +1 pas par pièce déjà dans le manoir
    lors de la première entrée. Hérite de RoomEffetEntree.
    """

    def appliquer_effet(self, game_instance):

        # Compte le nombre de pièces placées (non None)
        count_pieces = sum(1 for row in game_instance.manoir_grid for room in row if room is not None)
        game_instance.inventaire.modifier_pas(count_pieces)
        print(f"Effet {self.nom} : Gagne {count_pieces} pas (1 par pièce placée)")

class ChamberOfMirrorsRoom(RoomEffetSelection):
    
    """
    Pièce spéciale: Ajoute une deuxième copie d'une pièce que
    j'ai déjà au catalogue. Hérite de RoomEffetSelection.
    """

    def appliquer_effet(self, game_instance):

        #choisir une pièce aléatoire déjà disponible et la dupliquer
        if game_instance.pioche_disponible:
            piece_a_dupliquer = random.choice(game_instance.pioche_disponible)
            game_instance.ajouter_pieces_au_catalogue([piece_a_dupliquer])
            print(f"Effet {self.nom} : Ajout d'une copie de '{piece_a_dupliquer}' au catalogue.")
        else:
            print(f"Effet {self.nom} : Le catalogue est vide, aucun ajout possible.")


# Pieces avec effet sur l'aleatoire
class VerandaRoom(RoomEffetEntree):

    """ 
    Pièce spéciale: Active le modificateur de chance pour trouver
    certains objets lors de la première entrée. Hérite de RoomEffetEntree.
    """
    
    def appliquer_effet(self, game_instance):

        # Active le modificateur de chance pour trouver des objets
        game_instance.modificateur_chance_veranda = True # Variable d'état dans Game
        print(f"Effet {self.nom} : Active le modificateur de chance de trouver des objets.")

class FurnaceRoom(RoomEffetEntree):
    
    """ 
    Pièce spéciale: Active le modificateur de tirage pour les pièces Rouges
    lors de la première entrée. Hérite de RoomEffetEntree.
    """

    def appliquer_effet(self, game_instance):

        # Active le modificateur de tirage pour les pièces Rouges
        game_instance.modificateur_tirage_furnace = True # Variable d'état dans Game
        print(f"Effet {self.nom} : Active le modificateur de tirage pour les pièces Rouges.")

class GreenhouseRoom(RoomEffetEntree):
    
    """
    Pièce spéciale: Active le modificateur de tirage pour les pièces Vertes
    lors de la première entrée. Hérite de RoomEffetEntree.
    """

    def appliquer_effet(self, game_instance):

        # Active le modificateur de tirage pour les pièces Vertes
        game_instance.modificateur_tirage_greenhouse = True # Variable d'état dans Game
        print(f"Effet {self.nom} : Active le modificateur de tirage pour les pièces Vertes.")

class OfficeRoom(RoomEffetEntree):
    
    """
    Pièce spéciale: Disperse de l'or dans d'autres pièces du manoir
    lors de la première entrée. Hérite de RoomEffetEntree.
    """

    def appliquer_effet(self, game_instance):
        game_instance.disperser_or_dans_manoir(quantite=3) 
        print(f"Effet {self.nom} : 3 pièces d'ors ont été dispersés dans le manoir.")

#Pieces spéciales pour la sélection

class StudyRoom(RoomEffetSelection):

    """
    Pièce spéciale: Permet de dépenser des gemmes pour reroll pendant le draft
    lorsqu'elle est sélectionnée. Hérite de RoomEffetSelection.
    """
    
    def appliquer_effet(self, game_instance):

        game_instance.capacite_reroll_draft_study= True
        print(f"Effet {self.nom} : Active la capacité de reroll du draft.")

class DrawingRoom(RoomEffetSelection):
    
    """
    Pièce spéciale: Permet de tirer de nouvelles options pendant le draft
    lorsqu'elle est sélectionnée. Hérite de RoomEffetSelection.
    """

    def appliquer_effet(self, game_instance):

        game_instance.capacite_nouveau_draft_drawing = True
        print(f"Effet {self.nom} : Active la capacité de tirer de nouvelles options de draft.")

class Portail(RoomEffetEntree):
    
    """ 
    Salle de téléportation : téléporte le joueur vers une pièce aléatoire
    découverte et donne +5 pas (une seule fois). Hérite de RoomEffetEntree.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.teleportation_utilisee = False

    def appliquer_effet(self, game_instance):

        """
        Effectue la téléportation et donne le bonus de pas, si non déjà utilisé.
        """

        if self.teleportation_utilisee:
            game_instance.add_message("La magie de téléportation est épuisée...", (150, 150, 150))
            return

        pieces_decouvertes = []
        current_pos = (game_instance.current_row, game_instance.current_col)
        
        # Trouver toutes les pièces découvertes (sauf celle actuelle)
        for row in range(game_instance.grid_height):
            for col in range(game_instance.grid_width):
                # La pièce doit exister (non None) et ne pas être la pièce actuelle
                if game_instance.manoir_grid[row][col] is not None and (row, col) != current_pos:
                    pieces_decouvertes.append((row, col))
        
        if not pieces_decouvertes:
            game_instance.add_message("Pas d'autre destination pour la téléportation!", (255, 100, 100))
            return
            
        # Choisir une destination aléatoire
        nouvelle_position = random.choice(pieces_decouvertes)

        #Effectuer la téléportation et donner le bonus
        game_instance.current_row = nouvelle_position[0]
        game_instance.current_col = nouvelle_position[1]
        game_instance.inventaire.modifier_pas(5)

        destination = game_instance.manoir_grid[nouvelle_position[0]][nouvelle_position[1]]
        game_instance.add_message("Téléportation vers {destination.nom} (+5 pas)",(255,215,0))

        # Marquer comme utilisé
        self.teleportation_utilisee = True

def creer_piece(type_piece: str) -> Room:

    """
    Crée et configure une instance de Room ou de RoomEnfant selon le type_piece.
    
    Args:
        type_piece (str): Le nom/type de la pièce à créer.
        
    Returns:
        Room: Une instance de Room configurée.
    """

    classes = {
        "The Pool" : PoolRoom,
        "Master Bedroom" : MasterBedroom,
        "Bedroom" : BedroomRoom,
        "Chapel" : ChapelRoom,
        "Nook": NookRoom,
        "Music Room": MusicRoom,
        "Garage": GarageRoom,
        "Chamber of mirrors": ChamberOfMirrorsRoom,
        "Veranda": VerandaRoom,
        "Furnace": FurnaceRoom,
        "Greenhouse": GreenhouseRoom,
        "Office": OfficeRoom,
        "Study": StudyRoom,
        "Drawing Room": DrawingRoom,
        "Portail Mystique": Portail,
    }
    
    # Contenu possible pour les EndroitACreuser
    DIG_SPOT_contenu = ["gemme","cle","or","pomme","banane","dé","boussole magique","boussole magique","boussole magique"]
    classe_piece = classes.get(type_piece, Room) #classe a instantier/ Room par defaut


    # Dictionnaire de configuration des pièces
    pieces_config = {
        "The Foundation": {
            "nom": "The Foundation",
            "portes": Porte(0, 1, 1, 1),  
            "rarete": 3,
            "objets_possibles": [EndroitACreuser(DIG_SPOT_contenu) for _ in range(3)],
            "probabilites": [1.0, 1.0, 1.0],
            "cout_gemmes": 0,
            "image_path": "Rooms/The_Foundation_Icon.png"
        },
        
        "Entrance Hall": {
            "nom": "Entrance Hall",
            "portes": Porte(1, 0, 1, 1),  
            "rarete": 0,
            "objets_possibles": [], "probabilites": [],
            "cout_gemmes": 0,
            "image_path": "Rooms/Entrance_Hall.PNG"
        },
        
        "Spare Room": {
            "nom": "Spare Room",
            "portes": Porte(1, 1, 0, 0),
            "rarete": 0,
            "objets_possibles": ["cle","cle","shovel","sledgehammer",Coffre(niveau_verrouillage=1)],
            "probabilites": [0.5, 0.3, 0.2, 0.2],
            "cout_gemmes": 0,
            "image_path": "Rooms/Spare_Room.PNG"
        },
        
        "Nook": {
            "nom": "Nook",
            "portes": Porte(0, 1, 0, 1), 
            "rarete": 0,
            "objets_possibles": ["dé"],
            "probabilites": [1.0, 0.3],
            "cout_gemmes": 0,
            "image_path": "Rooms/Nook.PNG"
        },
        
        "Garage": {
            "nom": "Garage",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 2,
            "objets_possibles": ["shovel","metal detector","sledgehammer",Coffre(niveau_verrouillage=1),Coffre(niveau_verrouillage=2)],
            "probabilites": [0.5, 0.3, 0.4],
            "cout_gemmes": 0,
            "image_path": "Rooms/Garage_Icon.png"
        },
        
        "Music Room": {
            "nom": "Music Room",
            "portes": Porte(0, 1, 0, 1),
            "rarete": 2,
            "objets_possibles": ["sledgehammer"],
            "probabilites": [0.2, 0.4],
            "cout_gemmes": 2,
            "image_path": "Rooms/Music_Room.PNG"
        },
        
        "Drawing Room": {
            "nom": "Drawing Room",
            "portes": Porte(0, 1, 1, 1), 
            "rarete": 0,
            "objets_possibles": [], "probabilites": [],
            "cout_gemmes": 1,
            "image_path": "Rooms/Drawing_Room.PNG"
        },
        
        "Study": {
            "nom": "Study",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 2,
            "objets_possibles": [], "probabilites": [],
            "cout_gemmes": 0,
            "image_path": "Rooms/Study.PNG"
        },
        
        "Sauna": {
            "nom": "Sauna",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 2,
            "objets_possibles": ["cle","gemme","gemme","gemme","gemme","or","or","or", Coffre(niveau_verrouillage=1)],
            "probabilites": [0.4, 0.5, 0.6, 0.3],
            "cout_gemmes": 0,
            "image_path": "Rooms/Sauna.PNG"
        },
        
        "Coat Check": {
            "nom": "Coat Check",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 1,
            "objets_possibles": ["gemme","gemme","or","or","or","or","or"],
           "probabilites": [0.4, 0.7],
            "cout_gemmes": 0,
            "image_path": "Rooms/Coat_Check.PNG"
        },
        
        "Mail Room": {
            "nom": "Mail Room",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 2,
            "objets_possibles": [EndroitACreuser(DIG_SPOT_contenu)], "probabilites": [],
            "cout_gemmes": 0,
            "image_path": "Rooms/Mail_Room_Icon.png"
        },

        "The pool": {
            "nom": "The pool",
            "portes": Porte(0, 1, 1, 1),
            "rarete": 1,
            "objets_possibles": [EndroitACreuser(DIG_SPOT_contenu), EndroitACreuser(DIG_SPOT_contenu),EndroitACreuser(DIG_SPOT_contenu)],
            "probabilites": [0.8, 0.7, 0.6],
            "cout_gemmes": 0,
            "image_path": "Rooms/The_Pool_Icon.png"
        },

        "Chamber of mirrors": {
            "nom": "Chamber of mirrors",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 3,
            "objets_possibles": ["fruit","fruit","fruit","fruit","cle","cle","gemme","gemme","or","or"],
            "probabilites": [0.7, 0.4, 0.3, 0.5],
            "cout_gemmes": 0,
            "image_path": "Rooms/Chamber_of_mirrors.PNG"
        },

        "Veranda": {
            "nom": "Veranda",
            "portes": Porte(1, 1, 0, 0),
            "rarete": 2,
            "objets_possibles": ["gemme","metal detector","shovel","sledgehammer",EndroitACreuser(DIG_SPOT_contenu), EndroitACreuser(DIG_SPOT_contenu),EndroitACreuser(DIG_SPOT_contenu), EndroitACreuser(DIG_SPOT_contenu)],
            "probabilites": [0.5, 0.1, 0.4],
            "cout_gemmes": 2,
            "image_path": "Rooms/Veranda.PNG"
        },
        
        "Furnace": {
            "nom": "Furnace",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 3,
            "objets_possibles": ["gemme","locked trunk","metal detector","shovel","sledgehammer"],
            "probabilites": [0.1, 0.1, 0.1, 0.1, 0.1],
            "cout_gemmes": 0,
            "image_path": "Rooms/Furnace_Icon.png"
        },

        "Greenhouse": {
            "nom": "Greenhouse",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 1,
            "objets_possibles": ["metal detector","shovel","sledgehammer",EndroitACreuser(DIG_SPOT_contenu)],
            "probabilites": [0.1, 0.1, 0.1],
            "cout_gemmes": 1,
            "image_path": "Rooms/Greenhouse_Icon.png"
        },

        "Office": {
            "nom": "Office",
            "portes": Porte(0, 1, 0, 1),
            "rarete": 1,
            "objets_possibles": ["pomme","dé","dé","or","or","or",Coffre(niveau_verrouillage=1)],
            "probabilites": [0.4, 0.5, 0.6, 0.3],
            "cout_gemmes": 2,
            "image_path": "Rooms/Office.PNG"
        },

        "Bedroom": {
            "nom": "Bedroom",
            "portes": Porte(0, 1, 0, 1),
            "rarete": 0,
            "objets_possibles": ["pomme","dé","gemme","or",Coffre(niveau_verrouillage=1)],
            "probabilites": [0.4, 0.3, 0.2, 0.2, 0.1],
            "cout_gemmes": 0,
            "image_path": "Rooms/Bedroom.PNG"
        },

        "Chapel": {
            "nom": "Chapel",
            "portes": Porte(0, 1, 1, 1),
            "rarete": 0,
            "objets_possibles": ["gemme","gemme","or","or","or",PasseMuraille()],
           "probabilites": [0.3, 0.3, 0.5, 0.5, 0.5, 1.0],
            "cout_gemmes": 0,
            "image_path": "Rooms/Chapel_Icon.png"
        },

        "Master Bedroom": {
            "nom": "Master Bedroom",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 3,
            "objets_possibles": ["dé","dé","gemme","gemme","or","or"],
            "probabilites": [0.5, 0.3, 0.4],
            "cout_gemmes": 2,
            "image_path": "Rooms/Master_Bedroom.PNG"
        },
        "Portail Mystique": {
            "nom": "Portail Mystique",
            "portes": Porte(1, 1, 1, 1),
            "rarete": 3,
            "objets_possibles": ["gemme"],
            "probabilites": [1.0, 0.1, 0.3],
            "cout_gemmes": 2,
            "image_path": "Rooms/Portail.PNG" 
        },
        "GiftShop": {
            "nom": "GiftShop",
            "portes": Porte(1, 1, 1, 1),
            "rarete": 1,
            # Le Magasin est un objet interactif unique avec son propre catalogue
            "objets_possibles": [
                Magasin(catalogue={
                    "pomme": 3, 
                    "cle": 5, 
                    "dé": 10, 
                    "kit de crochetage": 15
                })
            ], 
            "probabilites": [1.0], # Le magasin apparaît toujours si la pièce est tirée
            "cout_gemmes": 0,
            "image_path": "Rooms/GiftShop.png" 
        },

    }

    config = pieces_config.get(type_piece)

    if not config:
        # Configuration par défaut si le type de pièce est inconnu
        return Room(
            nom=type_piece,
            portes=Porte(1, 1, 1, 1), # Porte par défaut
            rarete=1,
            objets=[],
            cout_gemmes=0,
            image_path=f"Rooms/{type_piece}.png" 
        )

    # Appliquer la sélection aléatoire d'objets
    objets_reels = random_objects_selection(
        config.get("objets_possibles", []), 
        config.get("probabilites", [])
    )

    positions_initiales = config["portes"].positions
    portes_instance = Porte(*positions_initiales)

    # Créer et retourner l'instance de Room
    return classe_piece(
        nom=config["nom"],
        portes=portes_instance,
        rarete=config["rarete"], # 0 : CommonPlace ou N\A / 1 : Standard / 2: Unusual / 3 : Rare
        objets=objets_reels,
        cout_gemmes=config["cout_gemmes"],
        image_path=config["image_path"]
    )

def get_piece(type_piece : str) -> dict:
    
    """
    Récupère uniquement les métadonnées essentielles d'une pièce 
    (nom, rareté, coût) sans instancier la Room complète ni charger l'image.
    
    Args:
        type_piece (str): Le nom/type de la pièce.

    Returns:
        dict: Un dictionnaire contenant les métadonnées de la pièce, ou None.
    """
    
    pieces_metadata = {
        "Entrance Hall": {"rarete": 0, "cout_gemmes": 0},
        "Spare Room": {"rarete": 0, "cout_gemmes": 0},
        "Bedroom": {"rarete": 0, "cout_gemmes": 0},
        "Chapel": {"rarete": 0, "cout_gemmes": 0},
        "Nook": {"rarete": 0, "cout_gemmes": 0},
        "Garage": {"rarete": 2, "cout_gemmes": 0},
        "Music Room": {"rarete": 2, "cout_gemmes": 2},
        "Drawing Room": {"rarete": 0, "cout_gemmes": 1},
        "Study": {"rarete": 2, "cout_gemmes": 0},
        "Sauna": {"rarete": 2, "cout_gemmes": 0},
        "Coat Check": {"rarete": 1, "cout_gemmes": 0},
        "Mail Room": {"rarete": 2, "cout_gemmes": 0},
        "The pool": {"rarete": 1, "cout_gemmes": 0},
        "Chamber of mirrors": {"rarete": 3, "cout_gemmes": 0},
        "Veranda": {"rarete": 2, "cout_gemmes": 2},
        "Furnace": {"rarete": 3, "cout_gemmes": 0},
        "Greenhouse": {"rarete": 1, "cout_gemmes": 1},
        "Office": {"rarete": 1, "cout_gemmes": 2},
        "Master Bedroom": {"rarete": 3, "cout_gemmes": 2},
        "Portail Mystique": {"rarete": 3, "cout_gemmes": 2}, # Nouvelle pièce
        "The Foundation": {"rarete": 3, "cout_gemmes": 0},
        "GiftShop" : {"rarete":1,"cout_gemmes":0}
    }
    
    config = pieces_metadata.get(type_piece)

    if config:
        rarete = config["rarete"]
        proba = Proba(rarete) # Instancie Proba pour obtenir le poids
        return {
            "nom": type_piece,
            "rarete": rarete,
            "poids": proba.poids,
            "cout_gemmes": config["cout_gemmes"]
        }
    return None