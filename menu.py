import pygame
import sys

BLEU_TURQUOISE_FONCE = (0, 102, 102)
BLANC = (255, 255, 255)

largeur_fenetre_accueil = 400
hauteur_fenetre_accueil = 300

pygame.init()

fenetre_accueil = pygame.display.set_mode((largeur_fenetre_accueil, hauteur_fenetre_accueil))
pygame.display.set_caption("Menu du Snake")

police = pygame.font.Font(None, 36)

def afficher_texte(texte, x, y, couleur, surface):
    texte_surface = police.render(texte, True, couleur)
    texte_rect = texte_surface.get_rect(center=(x, y))
    surface.blit(texte_surface, texte_rect)

def afficher_accueil():
    while True:
        fenetre_accueil.fill(BLEU_TURQUOISE_FONCE)

        afficher_texte('Menu du Snake', largeur_fenetre_accueil // 2, hauteur_fenetre_accueil // 4, BLANC, fenetre_accueil)

        pygame.draw.rect(fenetre_accueil, BLANC, (50, 150, 300, 50))
        afficher_texte('Jouer', largeur_fenetre_accueil // 2, 175, BLEU_TURQUOISE_FONCE, fenetre_accueil)

        pygame.display.flip()

        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                x, y = evenement.pos
                if 50 <= x <= 350 and 150 <= y <= 200:
                    return "jouer"

if __name__ == '__main__':
    resultat = afficher_accueil()

    if resultat == "jouer":
        from jeu import Jeu
        jeu = Jeu()
        jeu.executer()
