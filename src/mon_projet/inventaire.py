"""
Inventaire du joueur : gestion des ressources et des objets permanents.
"""

class Inventaire:
    """Objets consommables + Objets permanents"""
    def __init__(self):
        # Objets consommalbes
        self.pas:int=70
        self.pieces_or:int=0
        self.gemmes:int=2
        self.cles:int=0
        self.des:int=0
        # Objets permanents

    # operation sur pas
    def ajouter_pas(self,n:int):
        if n>0:
            self.pas +=n

    def utiliser_pas(self,n:int) ->bool:
    # normalment pour bouger =1, mais pour pieces rouges =n pas
        if n>0 and self.pas >=n:
            self.pas -=n
            return True
        return False # GAME OVER!
    
    # operation sur gold
    def ajouter_or(self,n:int):
        if n>0:
            self.pieces_or +=n

    def depenser_or(self,n:int) -> bool:
        if n> 0 and self.pieces_or >= n:
            self.pieces_or -=n
            return True
        return False
    
    # operation sur gemmes
    def ajouter_gemmes(self,n:int):
        if n>0:
            self.gemmes +=n

    def depenser_gemmes(self,n:int) -> bool:
        if n> 0 and self.gemmes >= n:
            self.gemmes -=n
            return True
        return False

    # operation sur cles
    def ajouter_cles(self,n:int=1):
        if n>0:
            self.cles +=n

    def depenser_cles(self,n:int=1) ->bool:
    # we can only use one cle one time 
        if self.cles >=1:
            self.cles -=n
            return True
        return False
    
    # operation sur des
    def ajouter_des(self,n:int=1):
        if n>0:
            self.des += n

    def depenser_des(self,n:int=1)-> bool:
        if self.des>=1:
            self.des -=n
            return True
        return False
    

