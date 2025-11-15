""" Logique du jeu (gestion de l'inventaire, déplacements, catalogue de pièces) """

from src.mon_projet.module1 import*
from src.mon_projet.objets import*
import random

# Classes (enfants) pour gerer les effets speciaux

class RoomEffetEntree(Room):
    """
    Piece avec un effet qui se declenche quand le joueur y entre
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.moment_effet = "entree"

    def appliquer_effet(self, game_instance):
        """Applique l'effet à l'inventaire ou à l'état du jeu."""
        # Ceci est la méthode abstraite qui sera implémentée dans les classes enfants
        pass

class RoomEffetSelection(Room):
    """Pièce avec un effet qui se déclenche lorsque la pièce est choisie (ajoutée au manoir)."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.moment_effet = "selection_complete"

    def appliquer_effet(self, game_instance):
        # Ceci est la méthode abstraite qui sera implémentée dans les classes enfants
        pass

#Pieces Speciales
class BedroomRoom(RoomEffetEntree):
    """ Gagne deux pas """
    def appliquer_effet(self, game_instance):
        game_instance.inventaire.modifier_pas(2)
        print(f"Effet {self.nom} : Gagne 2 pas")

class ChapelRoom(RoomEffetEntree):
    """Perd 1 pièce d'or."""
    def appliquer_effet(self, game_instance):
        game_instance.inventaire.modifier_or(-1)
        print(f"Effet {self.nom} : Perd 1 pièce d'or")

class NookRoom(RoomEffetEntree):
    """Gagne 1 clé"""
    def appliquer_effet(self, game_instance):
        game_instance.inventaire.modifier_cles(1)
        print(f"Effet {self.nom} : Gagne 1 clé")

class MusicRoom(RoomEffetEntree):
    """Gagne 2 clés"""
    def appliquer_effet(self, game_instance):
        game_instance.inventaire.modifier_cles(2)
        print(f"Effet {self.nom} : Gagne 2 clés")

class GarageRoom(RoomEffetEntree):
    """Gagne 3 clés"""
    def appliquer_effet(self, game_instance):
        game_instance.inventaire.modifier_cles(3)
        print(f"Effet {self.nom} : Gagne 3 clés")

class PoolRoom(RoomEffetSelection):
    """
    Ajoute des pieces au catalogue quand elle est selectionnee
    """
    def appliquer_effet(self, game_instance):
        # ajoute une piece (sauna, locker room et pump room) au catalogue des pieces
        pieces_a_ajouter = ["Sauna", "Coat Check"] # a ajouter locker room? pump room?
        game_instance.ajouter_pieces_au_catalogue(pieces_a_ajouter)
        print(f"Effet {self.nom} : Ajout de {pieces_a_ajouter} au catalogue !")

class MasterBedroom(RoomEffetEntree):
    """
    Gagne +1 pas par piece deja dans le manoir
    """
    def appliquer_effet(self, game_instance):
        count_pieces = sum(1 for row in game_instance.manoir_grid for room in row if room is not None)
        game_instance.inventaire.modifier_pas(count_pieces)
        print(f"Effet {self.nom} : Gagne {count_pieces} pas (1 par pièce placée)")

class ChamberOfMirrorsRoom(RoomEffetSelection):
    """Ajoute une deuxième copie d'une pièce que j'ai déjà au catalogue."""
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
    """ modifie la proba de trouver certains objets"""
    def appliquer_effet(self, game_instance):
        # Active le modificateur de chance pour trouver des objets
        game_instance.modificateur_chance_veranda = True # Variable d'état dans Game
        print(f"Effet {self.nom} : Active le modificateur de chance de trouver des objets.")

class FurnaceRoom(RoomEffetEntree):
    """ modifie la proba de tirer des pieces rouges"""
    def appliquer_effet(self, game_instance):
        # Active le modificateur de tirage pour les pièces Rouges
        game_instance.modificateur_tirage_furnace = True # Variable d'état dans Game
        print(f"Effet {self.nom} : Active le modificateur de tirage pour les pièces Rouges.")

class GreenhouseRoom(RoomEffetEntree):
    """Modifie la probabilité de tirer des pièces vertes"""
    def appliquer_effet(self, game_instance):
        # Active le modificateur de tirage pour les pièces Vertes
        game_instance.modificateur_tirage_greenhouse = True # Variable d'état dans Game
        print(f"Effet {self.nom} : Active le modificateur de tirage pour les pièces Vertes.")

class OfficeRoom(RoomEffetEntree):
    """Disperse de l'or dans d'autres pièces"""
    def appliquer_effet(self, game_instance):
        game_instance.disperser_or_dans_manoir(quantite=3) 
        print(f"Effet {self.nom} : 3 pièces d'ors ont été dispersés dans le manoir.")

#Pieces speciales pour la selection

class StudyRoom(RoomEffetSelection):
    """Permet de dépenser des gemmes pour reroll pendant le draft"""
    def appliquer_effet(self, game_instance):
        game_instance.capacite_reroll_draft_study= True
        print(f"Effet {self.nom} : Active la capacité de reroll du draft.")

class DrawingRoom(RoomEffetSelection):
    """Permet de tirer de nouvelles options pendant le draft"""
    def appliquer_effet(self, game_instance):
        game_instance.capacite_nouveau_draft_drawing = True
        print(f"Effet {self.nom} : Active la capacité de tirer de nouvelles options de draft.")

def creer_piece(type_piece: str) -> Room:
    """
    Pour créer des instances de pièces
    
    Args:
        type_piece: Le nom/type de la pièce à créer
        
    Returns:
        Room: Une instance de Room configurée selon le type
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
    }
    
    DIG_SPOT_contenu = ["gemme","cle","or","pomme","banane","dé"]
    classe_piece = classes.get(type_piece, Room) #classe a instantier/ Room par defaut

    # Dictionnaire de configuration des pièces
    pieces_config = {
        "The Foundation": {
            "nom": "The Foundation",
            "portes": Porte(0, 1, 1, 1),  
            "rarete": 3,
            "objets": [EndroitACreuser(DIG_SPOT_contenu) for _ in range(3)],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"Couleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/The_Foundation_Icon.png"
        },
        
        "Entrance Hall": {
            "nom": "Entrance Hall",
            "portes": Porte(1, 0, 1, 1),  
            "rarete": 0,
            "objets": [],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"Couleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Entrance_Hall.PNG"
        },
        
        "Spare Room": {
            "nom": "Spare Room",
            "portes": Porte(1, 1, 0, 0),
            "rarete": 0,
            "objets": ["cle","cle","shovel","sledgehammer"],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Spare_Room.PNG"
        },
        
        "Nook": {
            "nom": "Nook",
            "portes": Porte(0, 1, 0, 1), 
            "rarete": 0,
            "objets": ["dé"],
            #"proba_obj": [1.0],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Nook.PNG"
        },
        
        "Garage": {
            "nom": "Garage",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 2,
            "objets": ["shovel","metal detector","sledgehammer"],
            #"proba_obj": [1.0,1.0,1.0],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Garage_Icon.png"
        },
        
        "Music Room": {
            "nom": "Music Room",
            "portes": Porte(0, 1, 0, 1),
            "rarete": 2,
            "objets": ["sledgehammer"],
            #"proba_obj": [1.0,1.0],
            "cout_gemmes": 2,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Music_Room.PNG"
        },
        
        "Drawing Room": {
            "nom": "Drawing Room",
            "portes": Porte(0, 1, 1, 1), 
            "rarete": 0,
            "objets": [],
            #"proba_obj": [],
            "cout_gemmes": 1,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Drawing_Room.PNG"
        },
        
        "Study": {
            "nom": "Study",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 2,
            "objets": [],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Study.PNG"
        },
        
        "Sauna": {
            "nom": "Sauna",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 2,
            "objets": ["cle","gemme","gemme","gemme","gemme","or","or","or"],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Sauna.PNG"
        },
        
        "Coat Check": {
            "nom": "Coat Check",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 1,
            "objets": ["gemme","gemme","or","or","or","or","or"],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Coat_Check.PNG"
        },
        
        "Mail Room": {
            "nom": "Mail Room",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 2,
            "objets": [],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Mail_Room_Icon.png"
        },

        "The pool": {
            "nom": "The pool",
            "portes": Porte(0, 1, 1, 1),
            "rarete": 1,
            "objets": [EndroitACreuser(DIG_SPOT_contenu), EndroitACreuser(DIG_SPOT_contenu),EndroitACreuser(DIG_SPOT_contenu)],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/The_Pool_Icon.png"
        },

        "Chamber of mirrors": {
            "nom": "Chamber of mirrors",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 3,
            "objets": ["fruit","fruit","fruit","fruit","cle","cle","cle","cle","gemme","gemme","gemme","gemme","or","or","or","or"],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Chamber_of_mirrors.PNG"
        },

        "Veranda": {
            "nom": "Veranda",
            "portes": Porte(1, 1, 0, 0),
            "rarete": 2,
            "objets": ["gemme","locked trunk","metal detector","shovel","sledgehammer",EndroitACreuser(DIG_SPOT_contenu), EndroitACreuser(DIG_SPOT_contenu),EndroitACreuser(DIG_SPOT_contenu), EndroitACreuser(DIG_SPOT_contenu)],
            #"proba_obj": [],
            "cout_gemmes": 2,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Veranda.PNG"
        },
        
        "Furnace": {
            "nom": "Furnace",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 3,
            "objets": ["gemme","locked trunk","metal detector","shovel","sledgehammer"],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Furnace_Icon.png"
        },

        "Greenhouse": {
            "nom": "Greenhouse",
            "portes": Porte(1, 0, 0, 0),
            "rarete": 1,
            "objets": ["watering can","metal detector","shovel","sledgehammer"],
            #"proba_obj": [],
            "cout_gemmes": 1,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Greenhouse_Icon.png"
        },

        "Office": {
            "nom": "Office",
            "portes": Porte(0, 1, 0, 1),
            "rarete": 1,
            "objets": ["pomme","dé","dé","or","or","or"],
            #"proba_obj": [],
            "cout_gemmes": 2,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Office.PNG"
        },

        "Bedroom": {
            "nom": "Bedroom",
            "portes": Porte(0, 1, 0, 1),
            "rarete": 0,
            "objets": ["pomme","dé","cle","gemme","or","or","or"],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Bedroom.PNG"
        },

        "Chapel": {
            "nom": "Chapel",
            "portes": Porte(0, 1, 1, 1),
            "rarete": 0,
            "objets": ["gemme","gemme","or","or","or"],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Chapel_Icon.png"
        },

        "Master Bedroom": {
            "nom": "Master Bedroom",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 3,
            "objets": ["dé","dé","cle","gemme","gemme","or","or","or","or"],
            #"proba_obj": [],
            "cout_gemmes": 2,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Master_Bedroom.PNG"
        },

    }

    config = pieces_config.get(type_piece)
    
    if config:
        positions_initiales = config["portes"].positions
        portes_instance = Porte(*positions_initiales)
    
    # Récupérer la configuration de la pièce
    #config = pieces_config[type_piece]
    #positions_initiales = config["portes"].positions

    #if len(positions_initiales) != 4:
    #    raise ValueError(f"Configuration de porte invalide pour {type_piece} (doit avoir 4 positions).")
    
    #portes_instance = Porte(*positions_initiales)

    # Créer et retourner l'instance de Room
    return classe_piece(
        nom=config["nom"],
        portes=portes_instance,
        rarete=config["rarete"], # 0 : CommonPlace ou N\A / 1 : Standard / 2: Unusual / 3 : Rare
        objets=config.get("objets", []),
        #proba_obj=config["proba_obj"],
        cout_gemmes=config["cout_gemmes"],
        #couleur=config["couleur"],
        image_path=config["image_path"]
    )

def get_piece(type_piece : str) -> dict:
    """
    Récupère uniquement les métadonnées essentielles d'une pièce 
    (nom, rareté, coût) sans instancier la Room complète ni charger l'image.
    """
    # Dictionnaire de configuration des pièces
    pieces_config = {
        "The Foundation": {
            "nom": "The Foundation",
            "portes": Porte(0, 1, 1, 1),  
            "rarete": 3,
            "objets": [],
            # 2-5 dig spots
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"Couleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/The_Foundation_Icon.png"
        },
        
        "Entrance Hall": {
            "nom": "Entrance Hall",
            "portes": Porte(1, 0, 1, 1),  
            "rarete": 0,
            "objets": [],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"Couleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Entrance_Hall.PNG"
        },
        
        "Spare Room": {
            "nom": "Spare Room",
            "portes": Porte(1, 1, 0, 0),
            "rarete": 0,
            "objets": ["cle","cle","shovel","sledgehammer"],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Spare_Room.PNG"
        },
        
        "Nook": {
            "nom": "Nook",
            "portes": Porte(0, 1, 0, 1), 
            "rarete": 0,
            "objets": ["dé"],
            #"proba_obj": [1.0],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Nook.PNG"
        },
        
        "Garage": {
            "nom": "Garage",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 2,
            "objets": ["shovel","metal detector","sledgehammer"],
            #"proba_obj": [1.0,1.0,1.0],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Garage_Icon.png"
        },
        
        "Music Room": {
            "nom": "Music Room",
            "portes": Porte(0, 1, 0, 1),
            "rarete": 2,
            "objets": ["sledgehammer"],
            #"proba_obj": [1.0,1.0],
            "cout_gemmes": 2,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Music_Room.PNG"
        },
        
        "Drawing Room": {
            "nom": "Drawing Room",
            "portes": Porte(0, 1, 1, 1), 
            "rarete": 0,
            "objets": [],
            #"proba_obj": [],
            "cout_gemmes": 1,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Drawing_Room.PNG"
        },
        
        "Study": {
            "nom": "Study",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 2,
            "objets": [],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Study.PNG"
        },
        
        "Sauna": {
            "nom": "Sauna",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 2,
            "objets": ["cle","gemme","gemme","gemme","gemme","or","or","or"],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Sauna.PNG"
        },
        
        "Coat Check": {
            "nom": "Coat Check",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 1,
            "objets": ["gemme","gemme","or","or","or","or","or"],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Coat_Check.PNG"
        },
        
        "Mail Room": {
            "nom": "Mail Room",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 2,
            "objets": [],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Mail_Room_Icon.png"
        },

        "The pool": {
            "nom": "The pool",
            "portes": Porte(0, 1, 1, 1),
            "rarete": 1,
            "objets": [],
            #between 2 and 5 Dig Spots (2,3 commonly)
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/The_Pool_Icon.png"
        },

        "Chamber of mirrors": {
            "nom": "Chamber of mirrors",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 3,
            "objets": ["fruit","fruit","fruit","fruit","cle","cle","cle","cle","gemme","gemme","gemme","gemme","or","or","or","or"],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Chamber_of_mirrors.PNG"
        },

        "Veranda": {
            "nom": "Veranda",
            "portes": Porte(1, 1, 0, 0),
            "rarete": 2,
            "objets": ["gemme","locked trunk","metal detector","shovel","sledgehammer"],
            #2-4 dig spots
            #"proba_obj": [],
            "cout_gemmes": 2,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Veranda.PNG"
        },
        
        "Furnace": {
            "nom": "Furnace",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 3,
            "objets": ["gemme","locked trunk","metal detector","shovel","sledgehammer"],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Furnace_Icon.png"
        },

        "Greenhouse": {
            "nom": "Greenhouse",
            "portes": Porte(1, 0, 0, 0),
            "rarete": 1,
            "objets": ["watering can","metal detector","shovel","sledgehammer"],
            #"proba_obj": [],
            "cout_gemmes": 1,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Greenhouse_Icon.png"
        },

        "Office": {
            "nom": "Office",
            "portes": Porte(0, 1, 0, 1),
            "rarete": 1,
            "objets": ["pomme","dé","dé","or","or","or"],
            #"proba_obj": [],
            "cout_gemmes": 2,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Office.PNG"
        },

        "Bedroom": {
            "nom": "Bedroom",
            "portes": Porte(0, 1, 0, 1),
            "rarete": 0,
            "objets": ["pomme","dé","cle","gemme","or","or","or"],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Bedroom.PNG"
        },

        "Chapel": {
            "nom": "Chapel",
            "portes": Porte(0, 1, 1, 1),
            "rarete": 0,
            "objets": ["gemme","gemme","or","or","or"],
            #"proba_obj": [],
            "cout_gemmes": 0,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Chapel_Icon.png"
        },

        "Master Bedroom": {
            "nom": "Master Bedroom",
            "portes": Porte(0, 1, 0, 0),
            "rarete": 3,
            "objets": ["dé","dé","cle","gemme","gemme","or","or","or","or"],
            #"proba_obj": [],
            "cout_gemmes": 2,
            #"ouleur":CouleurPiece.BLEUE,
            "image_path": "Rooms/Master_Bedroom.PNG"
        },

    }

    config = pieces_config.get(type_piece)

    if config:
        proba = Proba(config["rarete"])
        return {"nom": config["nom"],
            "rarete": config["rarete"],
            "poids": proba.poids,
            "cout_gemmes": config["cout_gemmes"]}
    return None