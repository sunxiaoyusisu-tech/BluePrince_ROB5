""" Logique du jeu (gestion de l'inventaire, déplacements, catalogue de pièces) """

from module1 import Room, Porte, Pouvoir, Direction

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
        "Entrance Hall": {
            "nom": "Entrance Hall",
            "portes": Porte(1, 0, 0, 0),  # Seulement vers le haut
            "rarete": 0,
            "objets": ["gemme", "gemme"],
            "proba_obj": [0.5, 0.5],
            "cout_gemmes": 0,
            "pouvoir": None,
            "image_path": "images/entrance_hall.png"
        },
        
        "Antechamber": {
            "nom": "Antechamber",
            "portes": Porte(0, 1, 0, 0),  # Seulement vers le bas
            "rarete": 0,
            "objets": [],
            "proba_obj": [],
            "cout_gemmes": 0,
            "pouvoir": None,
            "image_path": "images/antechamber.png"
        },
        
        "Vault": {
            "nom": "Vault",
            "portes": Porte(0, 1, 0, 0),  # Une seule porte
            "rarete": 3,  # Très rare
            "objets": ["piece_or"] * 40,  # 40 pièces d'or
            "proba_obj": [1.0/40] * 40,
            "cout_gemmes": 3,
            "pouvoir": None,
            "image_path": "images/vault.png"
        },
        
        "Veranda": {
            "nom": "Veranda",
            "portes": Porte(1, 1, 0, 0),  # Deux portes
            "rarete": 2,
            "objets": ["gemme", "trou", "objet_permanent"],
            "proba_obj": [0.6, 0.3, 0.1],  # Haute probabilité gemme
            "cout_gemmes": 2,
            "pouvoir": Pouvoir(),  # Augmente proba pièces vertes
            "nom_du_pouvoir": "augmente_pieces_vertes",
            "image_path": "images/veranda.png"
        },
        
        "Den": {
            "nom": "Den",
            "portes": Porte(1, 1, 0, 0),
            "rarete": 1,
            "objets": ["gemme", "coffre"],
            "proba_obj": [1.0, 0.3],  # Toujours une gemme, parfois coffre
            "cout_gemmes": 0,
            "pouvoir": None,
            "image_path": "images/den.png"
        },
        
        "Chapel": {
            "nom": "Chapel",
            "portes": Porte(1, 1, 1, 0),
            "rarete": 1,
            "objets": ["pas"],  # Redonne des pas
            "proba_obj": [1.0],
            "cout_gemmes": 0,
            "pouvoir": Pouvoir(),
            "nom_du_pouvoir": "donne_pas",
            "image_path": "images/chapel.png"
        },
        
        "Bedroom": {
            "nom": "Bedroom",
            "portes": Porte(1, 1, 0, 0),
            "rarete": 1,
            "objets": ["sandwich"],  # Nourriture qui redonne 15 pas
            "proba_obj": [1.0],
            "cout_gemmes": 0,
            "pouvoir": Pouvoir(),
            "nom_du_pouvoir": "donne_pas",
            "image_path": "images/bedroom.png"
        },
        
        "Lavatory": {
            "nom": "Lavatory",
            "portes": Porte(1, 1, 1, 1),  # Beaucoup de portes
            "rarete": 0,
            "objets": [],
            "proba_obj": [],
            "cout_gemmes": 0,
            "pouvoir": None,
            "image_path": "images/lavatory.png"
        },
        
        "Locker Room": {
            "nom": "Locker Room",
            "portes": Porte(1, 1, 0, 0),
            "rarete": 1,
            "objets": ["casier", "casier", "casier"],
            "proba_obj": [0.33, 0.33, 0.34],
            "cout_gemmes": 0,
            "pouvoir": None,
            "image_path": "images/locker_room.png"
        },
        
        "Greenhouse": {
            "nom": "Greenhouse",
            "portes": Porte(1, 1, 1, 0),
            "rarete": 2,
            "objets": ["gemme", "trou"],
            "proba_obj": [0.7, 0.3],
            "cout_gemmes": 1,
            "pouvoir": Pouvoir(),
            "nom_du_pouvoir": "augmente_pieces_vertes",
            "image_path": "images/greenhouse.png"
        },
        
        "Shop": {
            "nom": "Shop",
            "portes": Porte(1, 1, 0, 0),
            "rarete": 1,
            "objets": [],  # Magasin - échange or contre objets
            "proba_obj": [],
            "cout_gemmes": 0,
            "pouvoir": Pouvoir(),
            "nom_du_pouvoir": "magasin",
            "image_path": "images/shop.png"
        },
        
        "Cellar": {
            "nom": "Cellar",
            "portes": Porte(1, 1, 1, 0),
            "rarete": 0,
            "objets": ["cle", "piece_or"],
            "proba_obj": [0.6, 0.4],
            "cout_gemmes": 0,
            "pouvoir": None,
            "image_path": "images/cellar.png"
        },
        
        "Furnace": {
            "nom": "Furnace",
            "portes": Porte(1, 1, 0, 0),
            "rarete": 2,
            "objets": [],
            "proba_obj": [],
            "cout_gemmes": 0,
            "pouvoir": Pouvoir(),
            "nom_du_pouvoir": "augmente_pieces_rouges",  # Effet négatif
            "image_path": "images/furnace.png"
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
        pouvoir=config["pouvoir"],
        nom_du_pouvoir=config.get("nom_du_pouvoir"),
        image_path=config["image_path"]
    )
