from time import sleep
import threading
import pygame

metronome_on = False
BPM = 0


def metronome(bpm):
    global BPM
    BPM = bpm

    # seconde par battement = 60 / BPM
    pygame.mixer.init()
    pygame.mixer.music.load('son/metro.mp3')
    while True:
        if metronome_on:
            sleep(60 / BPM)
            pygame.mixer.music.play(0)


def lancer(bpm):
    processus_metronome = threading.Thread(target=metronome, args=bpm, daemon=True)
    processus_metronome.start()


def mute():
    global metronome_on
    metronome_on = False


def mute_demute():
    global metronome_on
    metronome_on = not metronome_on


def changer_bpm(bpm):
    global BPM
    BPM = bpm
