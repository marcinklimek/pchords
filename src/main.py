import mido
from pychord import Chord
import random
import mido
from mido.ports import multi_receive

SHARPED_SCALE = {
    0: 'C', 1: 'C#', 2: 'D', 3: 'D#',
    4: 'E', 5: 'F', 6: 'F#', 7: 'G',
    8: 'G#', 9: 'A', 10: 'A#', 11: 'B'
}

FLATTED_SCALE = {
    0: 'C', 1: 'Db', 2: 'D', 3: 'Eb',
    4: 'E', 5: 'F', 6: 'Gb', 7: 'G',
    8: 'Ab', 9: 'A', 10: 'Bb', 11: 'B'
}

SCALES_LIST = ('Ab', 'A', 'A#', 'Bb', 'B', 'Cb', 'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#')

chords_to_pass = list(range(0, 18, 1))
qualities = ('m9', 'M9', '9', '7#9#5', '7b9b5')

OCTAVES = list(range(11))
NOTES_IN_OCTAVE = 12

# Open all available inputs.
ports = [mido.open_input(name) for name in mido.get_input_names()]

current_played_notes = []

def getKeysByValue(dictOfElements, valueToFind):
    for item in dictOfElements.items():
        if item[1] == valueToFind:
            return item[0]

    return None


def number_to_note(number: int) -> tuple:
    # 'http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm'

    octave = number // NOTES_IN_OCTAVE
    note = number % NOTES_IN_OCTAVE

    return note, octave


def notes_names_to_index(notes):
    conv_notes = []
    for item in notes:

        index = getKeysByValue(SHARPED_SCALE, item)
        if index is not None:
            conv_notes.append(index)
        else:
            index = getKeysByValue(FLATTED_SCALE, item)
            conv_notes.append(index)

    return conv_notes


def notes_to_index(notes):
    conv_notes = []
    for item in notes:
        conv_notes.append(number_to_note(item)[0])

    return conv_notes


def play_check(notes):

    notes_to_check = notes_names_to_index(notes)

    try:
        for message in multi_receive(ports):
            if message.type == "note_on":
                current_played_notes.append(message.note)

            if message.type == "note_off":
                current_played_notes.remove(message.note)

            current_played_notes.sort()

            notes_played = notes_to_index(current_played_notes)

            if notes_to_check == notes_played:
                print("---------------------------------------------------------------")
                print("OK")
                print("---------------------------------------------------------------")
                break

    except KeyboardInterrupt:
        pass


def generate_chords():
    quality = 'm9'
    scale = 'min'

    while len(chords_to_pass) > 0:
        index = random.choice(chords_to_pass)
        chords_to_pass.remove(index)

        chord_base = Chord.from_note_index(1, 'm9', SCALES_LIST[index] + scale)  # returns I of scale
        # chord_from_third = chord_base[1]

        # chord_from_third =

        print(chord_base)
        notes = chord_base.components()

        print("Od tercji")
        notes_from_3rd = notes[1:]
        print(notes_from_3rd)
        play_check(notes_from_3rd)

        print("Od septymy")
        notes_from_7th = notes[3:] + notes[1:3]
        print(notes_from_7th)
        notes_names_to_index(notes_from_7th)

        play_check(notes_from_7th)

        print("--")


# if __name__ == '__main__':
generate_chords()
# read_midi()
