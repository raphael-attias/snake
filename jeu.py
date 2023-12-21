import pygame
from pygame.locals import *
import random
from menu import *

TAILLE = 40
COULEUR_FOND = (110, 110, 5)

class CollisionDetectedError(Exception):
    pass

class Pomme:
    def __init__(self, ecran_parent):
        self.ecran_parent = ecran_parent
        self.image = pygame.image.load("sources/apple.png").convert()
        self.bouger()

    def dessiner(self):
        self.ecran_parent.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def bouger(self):
        self.x = random.randint(1, 24) * TAILLE
        self.y = random.randint(1, 19) * TAILLE

class Serpent:
    def __init__(self, ecran_parent):
        self.ecran_parent = ecran_parent
        self.image = pygame.image.load("sources/block.jpg").convert()
        self.direction = 'bas'
        self.direction_precedente = 'bas'  # propriété pour stocker la direction précédente
        self.longueur = 1
        self.x = [40]
        self.y = [40]

    def deplacer(self):
        for i in range(self.longueur - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # vérification pour éviter le demi-tour
        if (self.direction == 'gauche' and self.direction_precedente == 'droite' or
            self.direction == 'droite' and self.direction_precedente == 'gauche' or
            self.direction == 'haut' and self.direction_precedente == 'bas' or
            self.direction == 'bas' and self.direction_precedente == 'haut'):
            self.direction = self.direction_precedente

        if self.direction == 'gauche':
            self.x[0] -= TAILLE
        if self.direction == 'droite':
            self.x[0] += TAILLE
        if self.direction == 'haut':
            self.y[0] -= TAILLE
        if self.direction == 'bas':
            self.y[0] += TAILLE

        self.direction_precedente = self.direction
        self.dessiner()

    def dessiner(self):
        for i in range(self.longueur):
            self.ecran_parent.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def augmenter_longueur(self):
        self.longueur += 1
        self.x.append(-1)
        self.y.append(-1)

class Jeu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Jeu Snake et Pomme")

        pygame.mixer.init()

        self.ecran = pygame.display.set_mode((1000, 800))
        self.serpent = Serpent(self.ecran)
        self.pomme = Pomme(self.ecran)
        self.clock = pygame.time.Clock()  # Ajout de l'horloge

    def reinitialiser(self):
        self.serpent = Serpent(self.ecran)
        self.pomme.bouger()

    def collision(self, x1, y1, x2, y2):
        return x2 <= x1 < x2 + TAILLE and y2 <= y1 < y2 + TAILLE

    def afficher_fond(self):
        fond = pygame.image.load("sources/background.jpg")
        self.ecran.blit(fond, (0, 0))

    def jouer(self):
        self.afficher_fond()
        self.serpent.deplacer()
        self.pomme.dessiner()
        self.afficher_score()
        pygame.display.flip()

        for i in range(self.serpent.longueur):
            if self.collision(self.serpent.x[i], self.serpent.y[i], self.pomme.x, self.pomme.y):
                self.serpent.augmenter_longueur()
                self.pomme.bouger()

        for i in range(3, self.serpent.longueur):
            if self.collision(self.serpent.x[0], self.serpent.y[0], self.serpent.x[i], self.serpent.y[i]):
                raise CollisionDetectedError("Collision détectée")

        if not (0 <= self.serpent.x[0] <= 1000 and 0 <= self.serpent.y[0] <= 800):
            raise CollisionDetectedError("Collision avec la limite détectée")

    def afficher_score(self):
        police = pygame.font.SysFont('arial', 30)
        score = police.render(f"Score : {self.serpent.longueur}", True, (200, 200, 200))
        self.ecran.blit(score, (850, 10))

    def afficher_game_over(self):
        from fin_de_partie import FinDePartie
        fin_partie = FinDePartie(self.serpent.longueur)
        fin_partie.afficher()

        attendre_entree = True
        while attendre_entree:
            for evenement in pygame.event.get():
                if evenement.type == KEYDOWN and evenement.key == K_RETURN:
                    attendre_entree = False

        menu = afficher_accueil()
        menu.executer()

    def executer(self):
        en_cours = True
        pause = False

        while en_cours:
            for evenement in pygame.event.get():
                if evenement.type == KEYDOWN:
                    if evenement.key == K_ESCAPE:
                        en_cours = False
                    if evenement.key == K_RETURN:
                        pause = False
                    if not pause:
                        if evenement.key == K_LEFT:
                            self.serpent.direction = 'gauche'
                        if evenement.key == K_RIGHT:
                            self.serpent.direction = 'droite'
                        if evenement.key == K_UP:
                            self.serpent.direction = 'haut'
                        if evenement.key == K_DOWN:
                            self.serpent.direction = 'bas'
                elif evenement.type == QUIT:
                    en_cours = False  # Fermeture de la fenêtre

            try:
                if not pause:
                    self.jouer()
            except CollisionDetectedError:
                self.afficher_game_over()
                pause = True
                self.reinitialiser()

            self.clock.tick(12) # taux de rafraîchissement

        pygame.quit()  

if __name__ == '__main__':
    jeu = Jeu()
    jeu.executer()
