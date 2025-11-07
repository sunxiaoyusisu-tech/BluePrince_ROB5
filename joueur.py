import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.velocity=80
        self.image = pygame.image.load('image/joueur.png')
        self.direction = pygame.image.load('image/joueur_dir.png')
        self.pion = self.image
        self.rect = self.pion.get_rect()
        self.rect.x = 175
        self.rect.y = 655

    def droite(self):
        self.rect.x += self.velocity
    
    def gauche(self):
        self.rect.x -= self.velocity

    def haut(self):
        self.rect.y -= self.velocity

    def bas(self):
        self.rect.y += self.velocity