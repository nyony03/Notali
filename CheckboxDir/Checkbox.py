import pygame

pygame.init()


class Checkbox:

    def __init__(self, pos_x, pos_y):
        self._est_check = False
        self._img_on = pygame.image.load("CheckboxDir/img/chkON.png")
        self._img_on = pygame.transform.scale(self._img_on, (25.73, 22.72))
        self._img_off = pygame.image.load("CheckboxDir/img/chkOFF.png")
        self._img_off = pygame.transform.scale(self._img_off, (25.73, 22.72))
        self._rect = self._img_on.get_rect()
        self._rect.x = pos_x
        self._rect.y = pos_y

    def blit(self, surface):
        if self._est_check:
            surface.blit(self._img_on, self._rect)
        else:
            surface.blit(self._img_off, self._rect)

    # à mettre dans les evenements pygame, retourne vrai ou faux si on clique sur lui ou pas et change l'état de la box
    def clique(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._rect.collidepoint(event.pos):
                self._est_check = not self._est_check
                return True

        return False

    def get_rect(self):
        return self._rect

    def get_surface(self):
        if self._est_check:
            return self._img_on

        return self._img_off

    def est_check(self):
        return self._est_check

    def set_est_check(self, bool):
        self._est_check = bool
