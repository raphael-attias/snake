import pygame
from pygame.locals import *
import sys

class FinDePartie:
    def __init__(self, score):
        self.ecran = pygame.display.set_mode((1000, 800))
        self.score = score

    def afficher(self):
        self.afficher_fond()
        police = pygame.font.SysFont('arial', 30)
        ligne1 = police.render(f"Perdu ! Votre score est {self.score}", True, (255, 255, 255))
        self.ecran.blit(ligne1, (200, 300))
        ligne2 = police.render("1. Rejouer", True, (255, 255, 255))
        self.ecran.blit(ligne2, (200, 350))
        ligne3 = police.render("2. Quitter", True, (255, 255, 255))
        self.ecran.blit(ligne3, (200, 400))
        pygame.display.flip()

        attendre_entree = True
        while attendre_entree:
            for evenement in pygame.event.get():
                if evenement.type == KEYDOWN:
                    if evenement.key == K_1:
                        attendre_entree = False
                        self.rejouer()
                    elif evenement.key == K_2:
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
        fond = pygame.image.load("sources/background.jpg")
        self.ecran.blit(fond, (0, 0))
        pygame.display.flip()