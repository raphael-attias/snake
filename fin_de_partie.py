import pygame
from pygame.locals import *
import sys

class FinDePartie:
    def __init__(self, score):
        self.ecran = pygame.display.set_mode((1000, 800))
        self.score = score

    def afficher(self):
        self.afficher_fond()
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
        pygame.display.flip()