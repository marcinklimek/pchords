from pychord import Chord
import random
import mido
from mido.ports import multi_receive

from constans import SCALES_LIST
from utils import notes_names_to_index, midi_to_index

chords_to_pass = list(range(0, 18, 1))

# Open all available inputs.
ports = [mido.open_input(name) for name in mido.get_input_names()]

current_played_notes = []


def play_and_check(notes):
    notes_to_check = notes_names_to_index(notes)

    try:
        for message in multi_receive(ports):
            if message.type == "note_on":
                current_played_notes.append(message.note)

            if message.type == "note_off":
                current_played_notes.remove(message.note)

            current_played_notes.sort()

            notes_played = midi_to_index(current_played_notes)

            if notes_to_check == notes_played:
                print("---------------------------------------------------------------")
                print("OK")
                print("---------------------------------------------------------------")
                break

    except KeyboardInterrupt:
        pass


def generate_chords(quality, scale):
    while len(chords_to_pass) > 0:
        index = random.choice(chords_to_pass)
        chords_to_pass.remove(index)

        chord_base = Chord.from_note_index(1, quality, SCALES_LIST[index] + scale)  # returns I of scale

        print(chord_base)
        notes = chord_base.components()

        print("From 3rd")
        notes_from_3rd = notes[1:]
        print(notes_from_3rd)
        play_and_check(notes_from_3rd)

        print("From seventh")
        notes_from_7th = notes[3:] + notes[1:3]
        print(notes_from_7th)
        notes_names_to_index(notes_from_7th)

        play_and_check(notes_from_7th)

        print("--")


if __name__ == '__main__':
    generate_chords(quality='M9', scale='maj')
    generate_chords(quality='m9', scale='min')
