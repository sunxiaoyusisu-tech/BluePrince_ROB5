# BluePrince_ROB5
Projet POO 2025 – Sorbonne ROB – Jeu Blue Prince en Python/Pygame

## Introduction
Le jeu à implémenter est un jeu qui se joue en solo. Le joueur se situe dans un manoir comportant 45 pièces disposées dans une grille de dimensions (5 x 9). Ce manoir est "magique", et les pièces qui le composent sont choisies par le joueur au fur et à mesure du jeu.

Quand le joueur ouvre une porte menant vers une nouvelle pièce, le jeu propose de choisir parmi trois salles tirées au sort, celle qui remplira cette position dans la grille. Le but du jeu est de progressivement construire un chemin menant vers la dernière pièce du manoir, située tout en haut de la grille.

## Fonctionnalités
1. Qualité de l'interface graphique et facilité de prise en main.
2. Déplacement dans le manoir et ouverture d'une porte.
3. Tirage et choix des pièces.
4. Gagner des pas avec la nourriture, perdre des pas pendant les déplacements.
5. Fin de la partie (gagner en atteignant l'antichambre, perdre si on n'a plus de pas).
6. Ramasser des gemmes, dépenser les gemmes pour choisir une pièce.
7. Ramasser des clés, dépenser les clés pour ouvrir les portes.
8. Ramasser des dés, dépenser les dés pour tirer à nouveau des pièces.
9. Aléatoire dans les objets disponibles dans les pièces.
10. Aléatoire dans les pièces tirées au sort et prise en compte de la rareté des pièces.
11. Aléatoire dans les niveaux de verrouillage des portes.
12. Détecteur de métaux et patte de lapin (et effets associés).
13. Kit de crochetage et ouverture des portes de niveau 1.
14. Marteau et ouverture des coffres
15. Pelle et possibilit´e de creuser dans des ”endroits ou creuser”
16.  Autre type d’objet different des autres.
## Auteurs 
sunxiaoyusisu-tech sur github : Xiaoyu SUN, numéro étudiant : 28620139
ChloeSalameh sur github : Chloé SALAMEH, numéro étudiant : 21211219
Batmaaaan-4848 sur github : Léa BOUBLIL, numéro étudiant : 21226914

## Lancement
Prérequis
Pour lancer ce projet, vous aurez besoin de Python 3 et des bibliothèques suivantes :
. pygame
. numpy
1. Vous pouvez installer toutes les dépendances requises en utilisant le fichier requirements.txt fourni : 
pip install -r requirements.txt

Instructions
1. Assurez-vous que toutes les dépendances sont installées.
2. Clonez ce dépôt.
3. Exécutez le fichier main.py depuis votre terminal :
python main.py

## Commandes
1. W / A / S / D : Sélectionner la direction (Haut / Gauche / Bas / Droite).
2. ESPACE : Ouvrir une nouvelle porte ou se déplacer dans la direction sélectionnée.
3. FLÈCHES GAUCHE / DROITE : Naviguer dans les options de sélection de pièce.
4. R : (Pendant la sélection) Utiliser un Dé pour relancer les 3 options de pièce
5. ESC : Quitter le jeu ou annuler une interaction.
6. C : Interagir avec la pièce actuelle pour Creuser
7. O : Interagir avec la pièce actuelle pour Ouvrir un coffre (locked trunk)。
8. F : Traverser un mur sans porte.