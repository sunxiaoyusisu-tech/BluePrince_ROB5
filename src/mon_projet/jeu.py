# -*- coding: utf-8 -*-
import pygame
from joueur import Joueur
# Importer les objets pour les tests
from objets import Pelle, Pomme

class Jeu:
    """
    Classe principale du jeu.
    Gère la boucle de jeu, l'état du jeu, le joueur, et la grille (non implémentée).
    """
    def __init__(self):
        # [cite_start]Initialisation de Pygame [cite: 147]
        pygame.init()
        self.taille_ecran = (800, 600)
        self.ecran = pygame.display.set_mode(self.taille_ecran)
        pygame.display.set_caption("Projet POO - Blue Prince Simplifié")
        
        # [cite_start]Le manoir est une grille de 5x9 [cite: 27]
        self.largeur_grille = 5
        self.hauteur_grille = 9
        
        # Initialise le joueur à la position de départ
        # (Par exemple, en bas au milieu de la grille 5x9)
        self.joueur = Joueur(start_x=2, start_y=8)
        
        self.en_cours = True # Le jeu est-il en cours d'exécution ?
        self.clock = pygame.time.Clock()

    def boucle_principale(self):
        """
        La boucle de jeu principale.
        """
        print("Démarrage de la boucle de jeu...")
        
        # --- Exemple: Donner des objets au joueur pour tester ---
        self.joueur.inventaire.ajouter_objet_permanent(Pelle())
        self.joueur.utiliser_objet(Pomme())
        # --- Fin de l'exemple ---
        
        while self.en_cours:
            # 1. Gérer les événements (entrées clavier)
            self.gerer_entrees()
            
            # 2. Mettre à jour l'état du jeu
            self.mettre_a_jour()
            
            # 3. Dessiner le jeu
            self.dessiner()
            
            # Contrôler la vitesse de la boucle
            self.clock.tick(60)
            
        print("Fin du jeu.")
        pygame.quit()

    def gerer_entrees(self):
        """
        Gère les entrées de l'utilisateur (clavier, souris).
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.en_cours = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z: # Z (Haut) [cite: 117]
                    self.joueur.se_deplacer(0, -1)
                elif event.key == pygame.K_s: # S (Bas) [cite: 117]
                    self.joueur.se_deplacer(0, 1)
                elif event.key == pygame.K_q: # Q (Gauche) [cite: 117]
                    self.joueur.se_deplacer(-1, 0)
                elif event.key == pygame.K_d: # D (Droite) [cite: 117]
                    self.joueur.se_deplacer(1, 0)
                elif event.key == pygame.K_ESCAPE:
                    self.en_cours = False

    def mettre_a_jour(self):
        """
        Met à jour la logique du jeu (par ex: vérifier les conditions de défaite).
        """
        # [cite_start]Vérifier la condition de défaite: plus de pas [cite: 34]
        if not self.joueur.est_en_vie():
            print("Défaite: Vous n'avez plus de pas !")
            self.en_cours = False
            
        # (Ici, on vérifierait aussi la condition de victoire ou de blocage) [cite_start][cite: 31, 33]

    def dessiner(self):
        """
        Dessine l'état actuel du jeu à l'écran.
        """
        self.ecran.fill((0, 0, 0)) # Fond noir [cite: 44]
        
        # (Ici, on dessinerait la grille, les pièces, le joueur, l'inventaire)
        
        # Exemple: Afficher le nombre de pas
        font = pygame.font.Font(None, 30)
        texte_pas = font.render(f"Pas restants: {self.joueur.inventaire.pas}", True, (255, 255, 255))
        self.ecran.blit(texte_pas, (10, 10))

        pygame.display.flip()

# --- Point d'entrée pour lancer le jeu ---
if __name__ == "__main__":
    jeu = Jeu()
    jeu.boucle_principale()