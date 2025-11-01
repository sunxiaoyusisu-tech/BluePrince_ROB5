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
            "portes": Porte(0, 1, 1, 1),  # Seulement vers le haut
            "rarete": 3,
            "objets": [],
            "proba_obj": [],
            "cout_gemmes": 0,
            "ouleur":CouleurPiece.BLEUE,
            "image_path": "images/The_Foundation.png"
        },
        
        "Entrance Hall": {
            "nom": "Entrance Hall",
            "portes": Porte(1, 0, 1, 1),  # Seulement vers le haut
            "rarete": 0,
            "objets": [],
            "proba_obj": [],
            "cout_gemmes": 0,
            "ouleur":CouleurPiece.BLEUE,
            "image_path": "images/Entrance_Hall.png"
        },
        
        "Spare Room": {
            "nom": "Spare Room",
            "portes": Porte(1, 1, 0, 0),  # Seulement vers le haut
            "rarete": 0,
            "objets": [],
            "proba_obj": [],
            "cout_gemmes": 0,
            "ouleur":CouleurPiece.BLEUE,
            "image_path": "images/Spare_Room.png"
        },
        
        "Nook": {
            "nom": "Nook",
            "portes": Porte(0, 1, 0, 1),  # Seulement vers le haut
            "rarete": 0,
            "objets": ["cle"],
            "proba_obj": [1.0],
            "cout_gemmes": 0,
            "ouleur":CouleurPiece.BLEUE,
            "image_path": "images/Nook.png"
        },
        
        "Garage": {
            "nom": "Garage",
            "portes": Porte(0, 1, 0, 0),  # Seulement vers le haut
            "rarete": 2,
            "objets": ["cle","cle","cle"],
            "proba_obj": [1.0,1.0,1.0],
            "cout_gemmes": 0,
            "ouleur":CouleurPiece.BLEUE,
            "image_path": "images/Garage.png"
        },
        
        "Music Room": {
            "nom": "Music Room",
            "portes": Porte(0, 1, 0, 1),  # Seulement vers le haut
            "rarete": 2,
            "objets": ["cle","cle"],
            "proba_obj": [1.0,1.0],
            "cout_gemmes": 2,
            "ouleur":CouleurPiece.BLEUE,
            "image_path": "images/Music_Room.png"
        },
        
        "Drawing Room": {
            "nom": "Drawing Room",
            "portes": Porte(0, 1, 1, 1),  # Seulement vers le haut
            "rarete": 0,
            "objets": [],
            "proba_obj": [],
            "cout_gemmes": 1,
            "ouleur":CouleurPiece.BLEUE,
            "image_path": "images/Drawing_Room.png"
        },
        
        "Study": {
            "nom": "Study",
            "portes": Porte(0, 1, 0, 0),  # Seulement vers le haut
            "rarete": 2,
            "objets": [],
            "proba_obj": [],
            "cout_gemmes": 0,
            "ouleur":CouleurPiece.BLEUE,
            "image_path": "images/Study.png"
        },
        
        "Library": {
            "nom": "Library",
            "portes": Porte(0, 1, 0, 1),  # Seulement vers le haut
            "rarete": 2,
            "objets": [],
            "proba_obj": [],
            "cout_gemmes": 0,
            "ouleur":CouleurPiece.BLEUE,
            "image_path": "images/Library.png"
        },
        
        "Sauna": {
            "nom": "Sauna",
            "portes": Porte(0, 1, 0, 0),  # Seulement vers le haut
            "rarete": 2,
            "objets": [],
            "proba_obj": [],
            "cout_gemmes": 0,
            "ouleur":CouleurPiece.BLEUE,
            "image_path": "images/Sauna.png"
        },
        
        "Coat Check": {
            "nom": "Coat Check",
            "portes": Porte(0, 1, 0, 0),  # Seulement vers le haut
            "rarete": 1,
            "objets": [],
            "proba_obj": [],
            "cout_gemmes": 0,
            "ouleur":CouleurPiece.BLEUE,
            "image_path": "images/Coat_Check.png"
        },
        
        "Mail Room": {
            "nom": "Mail Room",
            "portes": Porte(0, 1, 0, 0),  # Seulement vers le haut
            "rarete": 2,
            "objets": [],
            "proba_obj": [],
            "cout_gemmes": 0,
            "ouleur":CouleurPiece.BLEUE,
            "image_path": "images/Mail_Room.png"
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
        rarete=config["rarete"],
        objets=config["objets"],
        proba_obj=config["proba_obj"],
        cout_gemmes=config["cout_gemmes"],
        couleur=config["couleur"],
        image_path=config["image_path"]
    )
