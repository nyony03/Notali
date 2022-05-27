import pygame
import Metronome
from Gamme import Gamme
from Observer import Observer
from Note import Note
from CheckboxDir import Checkbox as chk
from Bouton import Bouton


class Notali(Observer):

    def __init__(self, screen):
        self._screen = screen
        self._tab_num_notes_on = []

    def notifier(self, num_note, note_on):
        # ajoute la note qu'on viens de frapper
        if note_on:
            self._tab_num_notes_on.append(num_note)
        else:
            # supprime la note qu'on relache
            for numero_note in self._tab_num_notes_on:
                if numero_note == num_note:
                    self._tab_num_notes_on.remove(num_note)

    def afficher(self):
        # hauteurNoteLa0_clefFa = 592
        self._tab_num_notes_on = []
        input_metronome_actif = False

        # chargement background et note
        portee = pygame.image.load("img/composition.png")
        note_simple = pygame.image.load("img/notesimple.png")
        barre = pygame.image.load("img/barre.png")
        diese = pygame.image.load("img/diese.png")
        bemol = pygame.image.load("img/bemol.png")
        becarre = pygame.image.load("img/becarre.png")
        colonne_haut = pygame.image.load("img/colonneHaut.png")
        colonne_bas = pygame.image.load("img/colonneBas.png")

        # creation boutons accueil
        bouton_accueil = Bouton(10, 20, "img/accueil.png", "img/boutonAccueilClique.png")
        bouton_accueil.redimensionner(30, 30)

        # boutons armure
        bouton_plus = Bouton(1000, 400, "img/boutonPlus.png", "img/boutonPlusClique.png")
        bouton_plus.redimensionner(32, 32)
        bouton_moins = Bouton(800, 400, "img/boutonMoins.png", "img/boutonMoinsClique.png")
        bouton_moins.redimensionner(32, 32)
        cadre_nom_gamme = pygame.image.load("img/nomTonalite.png")
        cadre_nom_gamme = pygame.transform.scale(cadre_nom_gamme, (153.6, 38.4))

        #bouton checkbox
        bouton_metronome = chk.Checkbox(790, 155)
        bouton_affiche_note = chk.Checkbox(790, 95)

        # Métronome
        input_metronome = pygame.image.load("img/texte.png")
        input_metronome = pygame.transform.scale(input_metronome, (110, 110))
        input_metronome_rect = input_metronome.get_rect()
        input_metronome_rect.x = 820
        input_metronome_rect.y = 155
        bouton_ok = Bouton(935, 185, "img/boutonOK.png", "img/boutonOKClique.png")
        bouton_ok.redimensionner(50, 50)

        # texte et texte des boutons
        police_texte = pygame.font.Font('police/Garet-Book.ttf', 17)
        texte_aide = police_texte.render("Appuie sur une touche de ton clavier :)", 1, (0, 0, 0))
        user_texte = '120'
        # Texte
        txt_bouton_note = police_texte.render("Afficher noms des notes", 1, 'black')
        metronome = police_texte.render("Métronome", 1, 'black')
        texte_ok_input = police_texte.render('OK', True, (255, 255, 255))

        # initialisation
        choix_gamme = 8
        armure = Gamme(choix_gamme)
        bouton_affiche_note.set_est_check(True)
        running = True

        # boucle d'affichage
        while running:

            pygame.draw.rect(self._screen, pygame.Color('black'), input_metronome_rect)

            # texte à update
            user_texte_metronome = police_texte.render(user_texte, True, (0, 0, 0))

            #NEW -----------------------------------------------------

            # affichage/superposition des images/textes
            self._screen.fill((245, 233, 228))
            self._screen.blit(portee, (0, 102))
            self._screen.blit(colonne_haut, (755, 20))
            self._screen.blit(colonne_bas, (755, 290))
            bouton_accueil.blit(self._screen)
            bouton_metronome.blit(self._screen)
            bouton_affiche_note.blit(self._screen)


            # Screen texte
            self._screen.blit(txt_bouton_note, (820, 95))
            self._screen.blit(texte_aide, (250, 15))
            self._screen.blit(metronome, (820, 153))
            self._screen.blit(input_metronome, input_metronome_rect)
            self._screen.blit(user_texte_metronome, (input_metronome_rect.x + 40, input_metronome_rect.y + 43))
            bouton_ok.blit(self._screen)
            self._screen.blit(texte_ok_input, (945, 195))

            # Screen armure
            bouton_plus.blit(self._screen)
            bouton_moins.blit(self._screen)
            self._screen.blit(cadre_nom_gamme, (840, 398))

            # Armure
            texte_gamme = police_texte.render(armure.name, 1, (0, 0, 0))
            self._screen.blit(texte_gamme, (870, 404))
            nb_symbol = armure.nb_alteration()
            symbol = diese
            if nb_symbol > 0:
                if armure.value < 8:
                    symbol = bemol
                position_x = 100
                for i in range(nb_symbol):
                    midi = armure.affichage_armure_sol(i)
                    note_armure = Note(Note.definir_note(midi))
                    self._screen.blit(symbol, (position_x, note_armure.hauteur_placement(midi)))
                    midi = armure.affichage_armure_fa(i)
                    note_armure = Note(Note.definir_note(midi))
                    self._screen.blit(symbol, (position_x, note_armure.hauteur_placement(midi)))
                    position_x += 25

            # notes
            note_precedente = None
            nb_note_decale = 0

            for numero_midi in self._tab_num_notes_on:

                note = Note(Note.definir_note(numero_midi))
                # bloc pour décaler une note en cas d'accord serré : si une note se trouve à moins de 1
                # ou deux cran d'écart : c'est soit la même note en dièse, soit la note juste au dessus,
                # dans tout les cas on la décale pour éviter qu'elles se chevauchent
                position_x = 350
                if note_precedente is not None:
                    if note.value - note_precedente.value <= 2 \
                            or note.value - note_precedente.value <= 3 and len(note.name) > 3:
                        nb_note_decale += 1
                        position_x += 50 * nb_note_decale

                # affiche la note
                placement_note_midi = numero_midi
                # toutes les touches en bémol sont décalées vers le haut
                if armure.value < 8 and armure.est_alteree(note):
                    placement_note_midi += 1
                # exception diese : deux touches sont décalées vers le bas
                if armure.placement_altere_diese(note.name):
                    placement_note_midi -= 1
                placement = Note.hauteur_placement(placement_note_midi)
                self._screen.blit(note_simple, (position_x, placement))

                # affiche un dièse si note est dièse et non intégrée dans la gamme
                alteree = armure.est_alteree(note)
                if len(note.name) > 3:
                    if not alteree:
                        self._screen.blit(symbol, (position_x - 40, placement))

                # affiche un becarre si note sup/inf est altérée
                if armure.value != 8:
                    if armure.value > 8:  # note supérieur altérée
                        note_adjacente = Note(Note.definir_note(numero_midi + 1))
                    else:  # note inférieur altérée
                        note_adjacente = Note(Note.definir_note(numero_midi - 1))
                    if armure.affiche_becarre(note, note_adjacente):
                        self._screen.blit(becarre, (position_x - 40, placement))

                # if armure.value > 8:
                #     note_sup = Note(Note.definir_note(numero_midi + 1))
                #     # si la note supérieur est altérée et que ce n'est ni fa pour l'armure 14 ni fa et do pour l'armure 15
                #     if armure.est_alteree(note_sup) and (armure.value != 14 or note.name != 'FA') and \
                #             (armure.value != 15 or note.name != 'DO' and note.name != 'FA'):
                #         self._screen.blit(becarre, (position_x - 40, placement))
                # if armure.value < 8:
                #     note_inf = Note(Note.definir_note(numero_midi - 1))
                #     # si la note inferieur est altérée et que ce n'est ni si pour l'armure 2 ni mi et si pour l'armure 1
                #     if armure.est_alteree(note_inf) and (armure.value != 2 or note.name != 'SI') and \
                #             (armure.value != 1 or note.name != 'MI' and note.name != 'SI'):
                #         self._screen.blit(becarre, (position_x - 40, placement))

                # affiche une barre de portée si note hors de la portée
                if numero_midi < 41:
                    placement = 371
                    difference = int((40 - numero_midi + 3) / 3)
                    for i in range(difference):
                        self._screen.blit(barre, (position_x, placement))
                        placement += 26
                if numero_midi > 80:
                    placement = 59
                    difference = int((numero_midi - 81 + 3) / 3)
                    for i in range(difference):
                        self._screen.blit(barre, (position_x, placement))
                        placement -= 26
                if placement_note_midi == 60 or placement_note_midi == 61:
                    self._screen.blit(barre, (position_x, placement))

                # affiche le nom de la note

                affichage_nom_note = police_texte.render(note.to_string(numero_midi, armure.value, alteree), 1,
                                                         (0, 0, 0))
                if bouton_affiche_note.est_check():
                    if note_precedente is None:
                        self._screen.blit(affichage_nom_note, (position_x, 650))

                # pour l'affichage des accords
                note_precedente = note

            pygame.display.flip()

            for event in pygame.event.get():
                if bouton_metronome.clique(event):
                    Metronome.mute_demute()

                if bouton_plus.clique(event):
                    if choix_gamme < 15:
                        choix_gamme += 1
                        armure = Gamme(choix_gamme)

                if bouton_moins.clique(event):
                    if choix_gamme > 1:
                        choix_gamme -= 1
                        armure = Gamme(choix_gamme)

                if bouton_ok.clique(event):
                    Metronome.changer_bpm(int(user_texte))

                if event.type == pygame.KEYDOWN:
                    # raccourcis nom note
                    if event.key == pygame.K_n:
                        bouton_affiche_note.set_est_check(not bouton_affiche_note.est_check())
                    # raccourcis accueil
                    if event.key == pygame.K_a:
                        Metronome.mute()
                        return ['Accueil']
                    # raccourcis gamme
                    if choix_gamme < 15:
                        if event.key == pygame.K_d:
                            choix_gamme += 1
                            armure = Gamme(choix_gamme)
                    if choix_gamme > 1:
                        if event.key == pygame.K_b:
                            choix_gamme -= 1
                            armure = Gamme(choix_gamme)
                    # raccourcis metronome
                    if event.key == pygame.K_m:
                        Metronome.mute_demute()
                        bouton_metronome.set_est_check(not bouton_metronome.est_check())

                    # valeur à entrer dans le input metronome
                    if input_metronome_actif:
                        # Check for backspace
                        if event.key == pygame.K_BACKSPACE:
                            user_texte = user_texte[:-1]
                        # unicode stock la valeur de la touche frappé
                        else:
                            user_texte += event.unicode

                bouton_affiche_note.clique(event)
                if bouton_accueil.clique(event):
                    return ['Accueil']

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    input_metronome_actif = False

                    if input_metronome_rect.collidepoint(event.pos):
                        input_metronome_actif = True
                        user_texte = ""

                    elif bouton_ok.get_rect().collidepoint(event.pos):
                        Metronome.changer_bpm(int(user_texte))

                elif event.type == pygame.QUIT:
                    return ['quitter']

