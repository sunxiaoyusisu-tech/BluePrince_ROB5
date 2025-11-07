import pygame
from joueur import*
from inventaire import *

class Game:
    def __init__(self):
        #charger le joueur
        self.player = Player()
        self.inventaire = Inventaire()

    #pour mettre à jour la map quand on choisit une salle
    def update(self):
        pass

    
