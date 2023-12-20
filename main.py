import pygame
from pygame.locals import *
import time
import random

# Taille d'une cellule (snake, apple, background)
TAILLE = 40
COULEUR_FOND = (110, 110, 5)

class Pomme:
    def __init__(self, ecran_parent):
        self.ecran_parent = ecran_parent
        self.image = pygame.image.load("sources/apple.png").convert()
        self.x = 120
        self.y = 120

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

        self.longueur = 1
        self.x = [40]
        self.y = [40]

    def deplacer_gauche(self):
        self.direction = 'gauche'

    def deplacer_droite(self):
        self.direction = 'droite'

    def deplacer_haut(self):
        self.direction = 'haut'

    def deplacer_bas(self):
        self.direction = 'bas'

    def marcher(self):
        # Mettre à jour le corps
        for i in range(self.longueur - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # Mettre à jour la tête
        if self.direction == 'gauche':
            self.x[0] -= TAILLE
        if self.direction == 'droite':
            self.x[0] += TAILLE
        if self.direction == 'haut':
            self.y[0] -= TAILLE
        if self.direction == 'bas':
            self.y[0] += TAILLE

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
        self.serpent.dessiner()
        self.pomme = Pomme(self.ecran)
        self.pomme.dessiner()

    def reinitialiser(self):
        self.serpent = Serpent(self.ecran)
        self.pomme = Pomme(self.ecran)

    def est_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + TAILLE:
            if y1 >= y2 and y1 < y2 + TAILLE:
                return True
        return False

    def afficher_fond(self):
        fond = pygame.image.load("sources/background.jpg")
        self.ecran.blit(fond, (0, 0))

    def jouer(self):
        self.afficher_fond()
        self.serpent.marcher()
        self.pomme.dessiner()
        self.afficher_score()
        pygame.display.flip()

        # Scénario où le serpent mange la pomme
        for i in range(self.serpent.longueur):
            if self.est_collision(self.serpent.x[i], self.serpent.y[i], self.pomme.x, self.pomme.y):
                self.jouer_son("ding")
                self.serpent.augmenter_longueur()
                self.pomme.bouger()

        # Scénario où le serpent entre en collision avec lui-même
        for i in range(3, self.serpent.longueur):
            if self.est_collision(self.serpent.x[0], self.serpent.y[0], self.serpent.x[i], self.serpent.y[i]):
                self.jouer_son('crash')
                raise "Collision détectée"

        # Scénario où le serpent entre en collision avec les limites de la fenêtre
        if not (0 <= self.serpent.x[0] <= 1000 and 0 <= self.serpent.y[0] <= 800):
            self.jouer_son('crash')
            raise "Collision avec la limite détectée"

    def afficher_score(self):
        police = pygame.font.SysFont('arial', 30)
        score = police.render(f"Score : {self.serpent.longueur}", True, (200, 200, 200))
        self.ecran.blit(score, (850, 10))

    def afficher_game_over(self):
        self.afficher_fond()
        police = pygame.font.SysFont('arial', 30)
        ligne1 = police.render(f"Perdu ! Votre score est {self.serpent.longueur}", True, (255, 255, 255))
        self.ecran.blit(ligne1, (200, 300))
        ligne2 = police.render("Appuyez sur Entrée pour rejouer ou Échap pour quitter!", True, (255, 255, 255))
        self.ecran.blit(ligne2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def executer(self):
        en_cours = True
        pause = False

        while en_cours:
            for evenement in pygame.event.get():
                if evenement.type == KEYDOWN:
                    if evenement.key == K_ESCAPE:
                        en_cours = False

                    if evenement.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if evenement.key == K_LEFT:
                            self.serpent.deplacer_gauche()

                        if evenement.key == K_RIGHT:
                            self.serpent.deplacer_droite()

                        if evenement.key == K_UP:
                            self.serpent.deplacer_haut()

                        if evenement.key == K_DOWN:
                            self.serpent.deplacer_bas()

                elif evenement.type == QUIT:
                    en_cours = False
            try:
                if not pause:
                    self.jouer()

            except Exception as e:
                self.afficher_game_over()
                pause = True
                self.reinitialiser()

            time.sleep(.1)

if __name__ == '__main__':
    jeu = Jeu()
    jeu.executer()
