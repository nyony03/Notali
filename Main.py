import pygame
import Accueil
from Notali import Notali
from Acquereur_note import AcquereurNote
import Metronome

pygame.init()

size = width, height = 1080, 720
pygame.display.set_caption("Notali")
pygame_icon = pygame.image.load('img/icone.png')
pygame.display.set_icon(pygame_icon)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)

notali = Notali(screen)
acquereur_note = AcquereurNote()
acquereur_note.ajouterObserver(notali)
Metronome.lancer([120])

action = ['Accueil']

while len(action) > 0 and action[0] != 'quitter':

    if action[0] == 'Accueil':
        action = Accueil.afficher(screen, width, height)

    if action[0] == 'Notali':
        if action[1] != "init" and action[2] != "init":
            acquereur_note.set_midi_in(action[1])
            acquereur_note.set_midi_out(action[2])
            acquereur_note.lancer_processus()
            action = notali.afficher()
        else:
            action = ['Accueil']

pygame.quit()
