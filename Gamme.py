from enum import Enum


class Gamme(Enum):
    DO_diese = 15
    FA_diese = 14
    SI = 13
    MI = 12
    LA = 11
    RE = 10
    SOL = 9
    DO = 8
    FA = 7
    SI_bemol = 6
    MI_bemol = 5
    LA_bemol = 4
    RE_bemol = 3
    SOL_bemol = 2
    DO_bemol = 1

    def liste_alterations(self):
        alteration = []
        # altération en dièse
        if self.value > 8:  # Sol maj
            alteration.append("FA_diese")
            if self.value > 9:  # Ré maj
                alteration.append("DO_diese")
                if self.value > 10:  # La maj
                    alteration.append("SOL_diese")
                    if self.value > 11:  # Mi maj
                        alteration.append("RE_diese")
                        if self.value > 12:  # Si maj
                            alteration.append("LA_diese")
                            if self.value > 13:  # Fa maj - Mi diese
                                alteration.append("FA")
                                if self.value > 14:  # Do maj - Si diese
                                    alteration.append("DO")
        # altération en bémol
        if self.value < 8:  # Si bémol
            alteration.append("LA_diese")
            if self.value < 7:  # Mi bémol
                alteration.append("RE_diese")
                if self.value < 6:  # La bémol
                    alteration.append("SOL_diese")
                    if self.value < 5:  # Re bémol
                        alteration.append("DO_diese")
                        if self.value < 4:  # Sol bémol
                            alteration.append("FA_diese")
                            if self.value < 3:  # Do bémol
                                alteration.append("SI")
                                if self.value < 2:  # Fa bémol
                                    alteration.append("MI")
        return alteration

    def affichage_armure_sol(self, nombre):
        if self.value > 8:
            note_armure = [78, 73, 80, 75, 70, 76, 71]  #ok
        else:
            note_armure = [71, 76, 70, 75, 68, 73, 66]  #ok
        return note_armure[nombre]

    def affichage_armure_fa(self, nombre):
        if self.value > 8:
            note_armure = [54, 49, 56, 51, 46, 52, 47]  #ok
        else:
            note_armure = [47, 52, 46, 51, 44, 49, 42]  #ok
        return note_armure[nombre]

    def nb_alteration(self):
        return len(self.liste_alterations())

    def est_alteree(self, note):
        if note.name in self.liste_alterations():
            return True
        return False

    def affiche_becarre(self, note, note_alteree):
        # affiche un becarre si note sup/inf est altérée
        if self.value > 8:
            # note_sup = Note(Note.definir_note(note_midi + 1))
            # si la note supérieur est altérée et que ce n'est ni fa pour l'armure 14 ni fa et do pour l'armure 15
            if self.est_alteree(note_alteree) and (self.value != 14 or note.name != 'FA') and \
                    (self.value != 15 or note.name != 'DO' and note.name != 'FA'):
                return True
        else:
            # note_inf = Note(Note.definir_note(note_midi - 1))
            # si la note inferieur est altérée et que ce n'est ni si pour l'armure 2 ni mi et si pour l'armure 1
            if self.est_alteree(note_alteree) and (self.value != 2 or note.name != 'SI') and \
                    (self.value != 1 or note.name != 'MI' and note.name != 'SI'):
                return True
        return False

    def placement_altere_diese(self, nom_note):
        if self.value == 14 and nom_note == 'DO' \
                or self.value == 15 and (nom_note == 'DO' or nom_note == 'FA'):
            return True
        return False
