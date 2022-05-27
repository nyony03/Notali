import pygame
import mido
from Bouton import Bouton

port_in = 'init'
port_out = 'init'


# la fonction renvoi la liste des ports ainsi que la liste des rects sur lesquels on peut cliquer
# (qui corresponds au texte des ports affichés)
def afficher_ports(screen, height):
    hauteur_in = 90
    hauteur_out = height / 2 + 10
    # creation textes
    police = pygame.font.Font('police/Garet-Book.ttf', 20)
    texte_choix_ports = police.render("Veuillez choisir les ports :)", True, (0, 0, 0))
    texte_ports_midi_in = police.render("ports midi IN : ", True, (0, 0, 0))
    texte_ports_midi_out = police.render("ports midi OUT : ", True, (0, 0, 0))
    screen.blit(texte_choix_ports, (10, 10))
    screen.blit(texte_ports_midi_in, (10, hauteur_in - 5))
    screen.blit(texte_ports_midi_out, (10, hauteur_out - 5))
    ports_in = mido.get_input_names()
    ports_out = mido.get_output_names()
    rect_in = []
    rect_out = []

    valeur_decal = 30
    somme_decal = 40
    for port in ports_in:
        if port == port_in:  # si c'est le port utilisé on change sa couleur
            texte = police.render(port, True, (10, 130, 100))
        else:
            texte = police.render(port, True, (0, 0, 0))
        rect = texte.get_rect()
        rect.x = 10
        rect.y = hauteur_in + somme_decal
        screen.blit(texte, rect)
        rect.y = rect.y + valeur_decal
        rect_in.append(rect)
        somme_decal += valeur_decal

    somme_decal = 40
    valeur_decal = 30
    for port in ports_out:
        if port == port_out:  # si c'est le port utilisé on change sa couleur
            texte = police.render(port, True, (100, 130, 100))
        else:
            texte = police.render(port, True, (0, 0, 0))
        rect = texte.get_rect()
        rect.x = 10
        rect.y = hauteur_out + somme_decal
        screen.blit(texte, rect)
        rect.y = rect.y + valeur_decal
        rect_out.append(rect)
        somme_decal += valeur_decal

    return ports_in, rect_in, ports_out, rect_out


# on initialise les ports midi aux premiers ports in et out qu'on trouve, si on en trouve
def initialiser_ports_midi():
    ports_in = mido.get_input_names()
    ports_out = mido.get_output_names()
    if len(ports_in) != 0:
        port_in = ports_in[0]
    else:
        port_in = "init"
    if len(ports_out) != 0:
        port_out = ports_out[0]
    else:
        port_out = "init"

    return [port_in, port_out]


def afficher(screen, width, height):
    global port_in, port_out
    ports = initialiser_ports_midi()
    port_in = ports[0]
    port_out = ports[1]

    # Ajout fond d'écran/ load : charger une image a un chemin spécifique
    background = pygame.image.load("img/background.jpg")

    # import bouton pour lancer la partie
    play_button = Bouton(430, 220, "img/start.png", "img/startClique.png")
    play_button.redimensionner(250, 100)


    # import bouton réglage port
    button_set = Bouton(430, 300, "img/start.png", "img/startClique.png")
    button_set.redimensionner(250, 100)

    # volet settings
    volet_ports_midi = pygame.image.load("img/bouton.png")
    volet_ports_midi = pygame.transform.scale(volet_ports_midi, (width / 2.7, height / 1.1))
    volet_ports_midi_rect = volet_ports_midi.get_rect()
    volet_ports_midi_rect.x = 20
    volet_ports_midi_rect.y = 30

    # alerte quand aucun port n'est disponible
    boite_alert_0_ports = pygame.image.load("img/bouton.png")
    boite_alert_0_ports = pygame.transform.scale(volet_ports_midi, (width / 2, height / 10))
    boite_alert_0_ports_rect = boite_alert_0_ports.get_rect()
    boite_alert_0_ports_rect.x = width/4
    boite_alert_0_ports_rect.y = button_set.get_rect().y + button_set.get_rect().height + 10
    police_texte = pygame.font.Font('police/Garet-Book.ttf', 17)
    texte_alert_0_ports = police_texte.render("Attention, aucun port midi in/out disponible !", 1, '#8f4231')
    texte_alert_0_ports_in = police_texte.render("Attention, aucun port midi in disponible !", 1, '#8f4231')
    texte_alert_port_in_out_pareil = police_texte.render("Attention, même port midi in et out !", 1, '#8f4231')
    texte_alert_0_ports_out = police_texte.render("Attention, aucun port midi out disponible !", 1, '#8f4231')

    # maintenir eveiller et reste eveiller
    running = True

    volet_ports_midi_ouvert = False
    police = pygame.font.Font('police/Academy.ttf', 32)

    # Boucle pour maintenir la fenêtre ouverte
    while running:
        # appliquer arriere plan jeu
        # screen.blit : ajouter une image à un endroit spécifique de la fenêtre (largeur, hauteur)
        screen.blit(background, (0, 0))

        # gestion du volet settings
        if volet_ports_midi_ouvert:
            screen.blit(volet_ports_midi, volet_ports_midi_rect)

        # affichage des erreurs de ports midi
        if len(mido.get_input_names()) == 0 and len(mido.get_output_names()) == 0:
            screen.blit(boite_alert_0_ports, boite_alert_0_ports_rect)
            screen.blit(texte_alert_0_ports, (boite_alert_0_ports_rect.x+80, boite_alert_0_ports_rect.y + boite_alert_0_ports_rect.height/3))
        elif len(mido.get_input_names()) == 0:
            screen.blit(boite_alert_0_ports, boite_alert_0_ports_rect)
            screen.blit(texte_alert_0_ports_in, (boite_alert_0_ports_rect.x+80, boite_alert_0_ports_rect.y + boite_alert_0_ports_rect.height/3))
        elif len(mido.get_output_names()) == 0:
            screen.blit(boite_alert_0_ports, boite_alert_0_ports_rect)
            screen.blit(texte_alert_0_ports_out, (boite_alert_0_ports_rect.x + 80, boite_alert_0_ports_rect.y + boite_alert_0_ports_rect.height / 3))
        elif port_in == port_out:
            screen.blit(boite_alert_0_ports, boite_alert_0_ports_rect)
            screen.blit(texte_alert_port_in_out_pareil, (boite_alert_0_ports_rect.x+80, boite_alert_0_ports_rect.y + boite_alert_0_ports_rect.height/3))

        # Appliquer image bouton
        play_button.blit(screen)
        button_set.blit(screen)

        # Texte
        texte1 = police.render("Commencer", 1, '#8f4231')
        screen.blit(texte1, (460, 260))
        texte2 = police.render("Reglages", 1, '#8f4231')
        screen.blit(texte2, (475, 340))

        # mettre à jour la fenêtre
        pygame.display.flip()

        # si le joueur ferme la fenêtre
        for event in pygame.event.get():
            # que l'evènement est fermeture de fenetre
            if event.type == pygame.QUIT:
                return ['quitter']

            # quand l'apprenti appuie sur les boutons
            if play_button.clique(event):
                running = False
                return ['Notali', port_in, port_out]

            if button_set.clique(event):
                volet_ports_midi_ouvert = not volet_ports_midi_ouvert
                afficher_ports(volet_ports_midi, height)  # pour forcer l'affichage dès l'appui du bouton

            if event.type == pygame.MOUSEBUTTONDOWN:
                # quand le volet des ports midi est activé, alors on capture les clique sur les noms des ports
                if volet_ports_midi_ouvert:
                    liste_ports = afficher_ports(volet_ports_midi, height)
                    i = 0
                    for rect_port in liste_ports[1]:
                        if rect_port.collidepoint(event.pos):
                            port_in = liste_ports[0][i]
                            afficher_ports(volet_ports_midi, height)
                            # pour forcer le refreshing de la couleur du port quand on clique dessus
                        i += 1

                    i = 0
                    for rect_port in liste_ports[3]:
                        if rect_port.collidepoint(event.pos):
                            port_out = liste_ports[2][i]
                            afficher_ports(volet_ports_midi, height)
                            # pour forcer le refreshing de la couleur du port quand on clique dessus
                        i += 1


def set_port_in(midi_in):
    global port_in
    port_in = midi_in


def set_port_out(midi_out):
    global port_out
    port_out = midi_out
