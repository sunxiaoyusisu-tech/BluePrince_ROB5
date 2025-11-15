""" Logique du jeu (gestion de l'inventaire, déplacements, catalogue de pièces) """

from module1 import Room, Porte, Pouvoir, Direction, CouleurPiece

def creer_piece(type_piece: str) -> Room:
    """
    Pour créer des instances de pièces
    
    Args:
        type_piece: Le nom/type de la pièce à créer
        
    Returns:
        Room: Une instance de Room configurée selon le type
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
    
    # Récupérer la configuration de la pièce
    if type_piece not in pieces_config:
        raise ValueError(f"Type de pièce '{type_piece}' non reconnu")
    
    config = pieces_config[type_piece]
    
    # Créer et retourner l'instance de Room
    return Room(
        nom=config["nom"],
        portes=config["portes"],
        rarete=config["rarete"], # 0 : CommonPlace ou N\A / 1 : Standard / 2: Unusual / 3 : Rare
        objets=config["objets"],
        proba_obj=config["proba_obj"],
        cout_gemmes=config["cout_gemmes"],
        #couleur=config["couleur"],
        image_path=config["image_path"]
    )
