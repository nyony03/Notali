from enum import Enum


class Note(Enum):
    DO = 0
    DO_diese = 1
    RE = 2
    RE_diese = 3
    MI = 4
    FA = 5
    FA_diese = 6
    SOL = 7
    SOL_diese = 8
    LA = 9
    LA_diese = 10
    SI = 11

    @staticmethod
    def definir_note(numero_midi):
        return int(numero_midi % 12)

    @staticmethod
    def definir_octave(numero_midi):
        return int(numero_midi / 12 - 1)

    @staticmethod
    def hauteur_placement(numero_midi):
        note = Note(Note.definir_note(numero_midi))
        diese = 0
        if note.value >= 10:
            diese = 5
        elif note.value >= 8:
            diese = 4
        elif note.value >= 6:
            diese = 3
        elif note.value >= 3:
            diese = 2
        elif note.value >= 1:
            diese = 1
        return 590 - (Note.definir_octave(numero_midi) * 7 + note.value + 1 - diese) * 13

    def to_string(self, num_midi, num_armure, est_alteree):
        if num_armure < 8 and est_alteree and (len(self.name) > 3 or (self.name == 'SI' or self.name == 'MI')):
            tab_bemol = [10, 3, 8, 1, 6, 11, 4]
            noms_bemol = ['SI_bemol', 'MI_bemol', 'LA_bemol', 'RE_bemol', 'SOL_bemol', 'DO_bemol', 'FA_bemol']
            nom_note = " " + noms_bemol[tab_bemol.index(self.value)]
        elif num_armure > 8 and est_alteree and (self.name == 'FA' or self.name == 'DO'):
            tab_diese = [0, 5]
            noms_diese = ['SI_diese', 'MI_diese']
            nom_note = " " + noms_diese[tab_diese.index(self.value)]
        else:
            nom_note = " " + self.name
        return str(self.definir_octave(num_midi)) + nom_note