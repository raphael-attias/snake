import pygame
from pygame.locals import *
import sys

class FinDePartie:
    scores = []  # Liste pour stocker les scores des parties précédentes

    def __init__(self, score):
        pygame.init()
        self.ecran = pygame.display.set_mode((1034, 698))
        self.score = score

    def afficher(self):
        self.afficher_fond()
        self.afficher_scores()
        pygame.display.flip()

        attendre_entree = True
        while attendre_entree:
            for evenement in pygame.event.get():
                if evenement.type == KEYDOWN:
                    if evenement.key == K_SPACE:
                        attendre_entree = False
                        self.rejouer()
                    elif evenement.key == K_ESCAPE:
                        attendre_entree = False
                        self.quitter()

    def rejouer(self):
        from jeu import Jeu
        jeu = Jeu()
        jeu.executer()

    def quitter(self):
        pygame.quit()
        sys.exit()

    def afficher_fond(self):
        fond = pygame.image.load("sources/findepartie.png")
        self.ecran.blit(fond, (0, 0))

    def afficher_scores(self):
        # Ajouter le score actuel à la liste des scores
        self.scores.append(self.score)

        # Afficher les trois derniers scores en haut de la fenêtre
        police = pygame.font.SysFont('arial', 30)
        y = 20  # Ajustez la position Y en conséquence
        for i, score in enumerate(self.scores[-3:]):
            texte = police.render(f"Score précédent {i + 1} : {score}", True, (255, 255, 255))
            self.ecran.blit(texte, (400, y))
            y += 40


# Code de test
if __name__ == '__main__':
    fin_partie = FinDePartie(10)
    fin_partie.afficher()