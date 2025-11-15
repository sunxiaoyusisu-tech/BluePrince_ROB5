from typing import List, Optional
# On importe les types d'objets, pas les instances
from .objets import ObjetPermanent, Objet

"""
Inventaire du joueur : gestion des ressources et des objets permanents.
"""

class Inventaire:
    """Objets consommables + Objets permanents"""
    def __init__(self):
        # Objets consommables
        self.pas:int=70
        self.pieces_or:int=5
        self.gemmes:int=2
        self.cles:int=5
        self.des:int=0

        #Objets permanents
        self.possede_pelle : bool = False
        self.possede_marteau : bool = False
        self.possede_kit_crochetage : bool = False
        self.possede_detecteur_metaux : bool = False
        self.possede_patte_lapin: bool = False

        #self.objets_permanents: List[ObjetPermanent] = []

    # operation sur pas
    def modifier_pas(self,n:int) -> bool :
        """ (positif = gain, négatif = perte). 
        Retourne True si l'opération est valide (pas >= 0) """
        self.pas += n
        if self.pas < 0:
            self.pas = 0
            return False #plus de pas
        return True

    #def utiliser_pas(self,n:int) ->bool:
    # normalment pour bouger =1, mais pour pieces rouges =n pas
    #    if n>0 and self.pas >=n:
    #        self.pas -=n
    #        return True
    #    return False # GAME OVER!
    
    # operation sur gold
    def modifier_or(self,n:int) -> bool : 
        # Retourne True si le solde final est >= 0
        self.pieces_or += n
        return self.pieces_or >= 0

    #def depenser_or(self,n:int) -> bool:
    #    if n> 0 and self.pieces_or >= n:
    #        self.pieces_or -=n
    #        return True
    #    return False
    
    # operation sur gemmes
    def modifier_gemmes(self,n:int) -> bool :
        self.gemmes +=n
        return self.gemmes >=0

    #def depenser_gemmes(self,n:int) -> bool:
    #    if n> 0 and self.gemmes >= n:
    #        self.gemmes -=n
    #        return True
    #    return False

    # operation sur cles
    def modifier_cles(self,n: int) -> bool:
        """ modifie le nb de cles. Retourne True si le solde final est >= 0 """
        self.cles +=n
        return self.cles >=0

    #def depenser_cles(self,n:int=1) ->bool:
    # we can only use one cle one time 
     #   if self.cles >=1:
      #      self.cles -=n
       #     return True
        #return False
    
    # operation sur des
    def modifier_des(self,n:int) -> bool :
        """Modifie les dés. Retourne True si le solde final est >= 0."""
        self.des += n
        return self.des >= 0

    #def depenser_des(self,n:int=1)-> bool:
    #    if self.des>=1:
    #        self.des -=n
    #        return True
    #    return False

    def possede_objet(self,nom_objet = str) -> bool :
        "verifie si le joueur possede un objet permanent precis"
        if nom_objet == "Kit de crochetage":
            return self.possede_kit_crochetage
        if nom_objet == "Pelle":
            return self.possede_pelle
        if nom_objet == "Marteau":
            return self.possede_marteau
        if nom_objet == "Detecteur_metaux":
            return self.possede_detecteur_metaux
        if nom_objet == "Patte de lapin":
            return self.possede_patte_lapin
        return False

    

