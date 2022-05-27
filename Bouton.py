import pygame

pygame.init()


# les deux images doivent être de même taille, ou alors une dimension doit-être donné avec bouton.resize()
class Bouton:

    def __init__(self, pos_x, pos_y, chemin_img_fixe, chemin_img_clique):
        self._img_fixe = pygame.image.load(chemin_img_fixe)
        self._img_clique = pygame.image.load(chemin_img_clique)
        self._rect = self._img_clique.get_rect()
        self._rect.x = pos_x
        self._rect.y = pos_y
        self._est_clique = False

    def redimensionner(self, largeur, hauteur):
        pox_x = self._rect.x
        pos_y = self._rect.y
        self._img_fixe = pygame.transform.scale(self._img_fixe, (largeur, hauteur))
        self._img_clique = pygame.transform.scale(self._img_clique, (largeur, hauteur))
        self._rect = self._img_clique.get_rect()
        self._rect.x = pox_x
        self._rect.y = pos_y

    def blit(self, surface):
        if self._est_clique:
            surface.blit(self._img_clique, self._rect)
        else:
            surface.blit(self._img_fixe, self._rect)

    def clique(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._rect.collidepoint(event.pos):
                self._est_clique = True

        if self._est_clique:
            if event.type == pygame.MOUSEBUTTONUP:
                self._est_clique = False
                return True

        return False

    def get_surface(self):
        if self._est_clique:
            return self._img_clique
        else:
            return self._img_fixe

    def get_rect(self):
        return self._rect


