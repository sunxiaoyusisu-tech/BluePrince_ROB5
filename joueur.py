import pygame

class Player(pygame.sprite.Sprite):

    """
    Représente le pion du joueur à l'écran, héritant de pygame.sprite.Sprite.
    """

    def __init__(self):

        """
        Initialise le joueur (pion, vitesse, position initiale).
        """

        super().__init__()
        self.velocity=80
        self.image = pygame.image.load('image/joueur.png')
        self.direction = pygame.image.load('image/joueur_dir.png')
        self.pion = self.image
        self.rect = self.pion.get_rect()
        self.rect.x = 175 # Position X initiale
        self.rect.y = 655 # Position Y initiale

    def droite(self):

        """Déplace le pion vers la droite"""

        self.rect.x += self.velocity
    
    def gauche(self):

        """Déplace le pion vers la gauche"""

        self.rect.x -= self.velocity

    def haut(self):

        """Déplace le pion vers le haut """

        self.rect.y -= self.velocity

    def bas(self):

        """Déplace le pion vers le bas """

        self.rect.y += self.velocity