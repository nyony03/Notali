import mido
import threading


class AcquereurNote:

    def __init__(self):
        self._midi_input = None
        self._midi_output = None
        self._observers = []

    def acquerir_note(self):
        #  Boucle d'acquisition et d'affichage des messages envoyés par VMPK,

        with self._midi_input as inport:  # connexion VMPK-Out à RtMidi-In

            for msg in inport:  # passe contenu 'inport' à 'msg'
                self._midi_output.send(msg)  # envoie contenu 'msg' à RtMidi-Out vers PC-speaker
                for observer in self._observers:
                    observer.notifier(msg.note, msg.type == "note_on")

    def lancer_processus(self):
        processus_piano = threading.Thread(target=self.acquerir_note, daemon=True)
        processus_piano.start()

    # si le processus est lancé, l'appel du setter l'arrêtera puisqu'on close le port de la boucle !
    def set_midi_in(self, port_in):
        if self._midi_input is not None:
            self._midi_input.close()

        self._midi_input = mido.open_input(port_in)

    def set_midi_out(self, port_out):
        if self._midi_output is not None:
            self._midi_output.close()

        self._midi_output = mido.open_output(port_out)

    def ajouterObserver(self, Observer):
        self._observers.append(Observer)

    def supprimerObserver(self, Observer):
        self._observers.remove(Observer)
