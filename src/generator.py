import random

from pychord import Chord

from constans import SCALES_LIST


class Generator:

    def __init__(self):
        self.test_list = []
        self.index = 0

        self.generate_chords(quality='M9', scale='maj')
        self.generate_chords(quality='m9', scale='min')

    def get(self):
        if self.index < len(self.test_list):
            val = self.test_list[self.index]
            self.index += 1
            return val

        self.index = 0

        self.generate_chords(quality='M9', scale='maj')
        self.generate_chords(quality='m9', scale='min')

        return self.test_list[self.index]

    def generate_chords(self, quality, scale):

        self.test_list = []
        chords_to_pass = list(range(0, 18, 1))

        while len(chords_to_pass) > 0:

            index = random.choice(chords_to_pass)
            chords_to_pass.remove(index)

            chord_base = Chord.from_note_index(1, quality, SCALES_LIST[index] + scale)  # returns I of scale

            notes = chord_base.components()

            #3rd
            chord_name = str(chord_base) + " - From 3rd"
            notes_from_3rd = notes[1:]
            self.test_list.append((str(chord_base.root), chord_name, notes_from_3rd))

            #7th
            chord_name = str(chord_base) + " - From 7th"
            notes_from_7th = notes[3:] + notes[1:3]
            self.test_list.append((str(chord_base.root), chord_name, notes_from_7th))