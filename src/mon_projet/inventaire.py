# -*- coding: utf-8 -*-
from typing import List, Optional
# On importe les types d'objets, pas les instances
from .objets import ObjetPermanent, Objet

class Inventaire:
    """
    Gère l'inventaire du joueur, y compris les ressources
    [cite_start]consommables et les objets permanents. [cite: 45]
    """
    def __init__(self):
        # [cite_start]Initialisation des ressources selon le document [cite: 47-51]
        self.pas: int = 70
        self.pieces_or: int = 0
        self.gemmes: int = 2
        self.cles: int = 0
        self.des: int = 0
        
        # [cite_start]Liste pour stocker les objets permanents acquis [cite: 52]
        self.objets_permanents: List[ObjetPermanent] = []

    def modifier_pas(self, quantite: int):
        """
        Ajoute ou retire des pas.
        """
        self.pas += quantite
        if self.pas < 0:
            self.pas = 0
        print(f"Pas: {self.pas}")

    def modifier_gemmes(self, quantite: int):
        """
        Ajoute ou retire des gemmes.
        """
        self.gemmes += quantite
        print(f"Gemmes: {self.gemmes}")
        
    def modifier_cles(self, quantite: int):
        """
        Ajoute ou retire des clés.
        """
        self.cles += quantite
        print(f"Clés: {self.cles}")

    def modifier_pieces_or(self, quantite: int):
        """
        Ajoute ou retire des pièces d'or.
        """
        self.pieces_or += quantite
        print(f"Pièces d'or: {self.pieces_or}")
        
    def modifier_des(self, quantite: int):
        """
        Ajoute ou retire des dés.
        """
        self.des += quantite
        print(f"Dés: {self.des}")

    def ajouter_objet_permanent(self, objet: ObjetPermanent):
        """
        Ajoute un objet permanent à l'inventaire.
        """
        if isinstance(objet, ObjetPermanent):
            self.objets_permanents.append(objet)
            print(f"Objet '{objet.nom}' ajouté à l'inventaire.")
        else:
            print(f"Erreur: '{objet.nom}' n'est pas un objet permanent.")

    def possede_objet(self, nom_objet: str) -> bool:
        """
        Vérifie si le joueur possède un objet permanent spécifique
        par son nom (par ex. "Pelle").
        """
        for objet in self.objets_permanents:
            if objet.nom == nom_objet:
                return True
        return False