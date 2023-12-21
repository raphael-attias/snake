import pygame
from pygame.locals import *

BLEU_TURQUOISE_FONCE = (0, 102, 102)
BLANC = (255, 255, 255)

largeur_fenetre_accueil = 1034
hauteur_fenetre_accueil = 511

pygame.init()

fenetre_accueil = pygame.display.set_mode((largeur_fenetre_accueil, hauteur_fenetre_accueil))
pygame.display.set_caption("Menu du Snake")

police = pygame.font.Font(None, 36)

def afficher_texte(texte, x, y, couleur, surface):
    texte_surface = police.render(texte, True, couleur)
    texte_rect = texte_surface.get_rect(center=(x, y))
    surface.blit(texte_surface, texte_rect)

def afficher_accueil():
    # Mise en place fond d'écran
    fond = pygame.image.load("sources/acceuil.png")
    fenetre_accueil.blit(fond, (0, 0))
    pygame.display.flip()

    # Attendre touche
    attendre_entree = True
    while attendre_entree:
        for evenement in pygame.event.get():
            if evenement.type == KEYDOWN:
                if evenement.key == K_KP_ENTER or evenement.key == K_RETURN:
                    attendre_entree = False
                    return True  # Retourner True si la touche Entrée est pressée
                
            elif evenement.type == QUIT:
                    en_cours = False  # Fermeture de la fenêtre
                    
    return False  # Retourner False si la fenêtre est fermée sans appuyer sur Entrée

if __name__ == '__main__':
    if afficher_accueil():
        from jeu import Jeu
        jeu = Jeu()
        jeu.executer()
