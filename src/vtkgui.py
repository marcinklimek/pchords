# -*- coding: utf-8 -*-

import tkinter
import time
import threading
import logging
from pychord import Chord
import random
import mido
from mido.ports import multi_receive

from constans import SCALES_LIST
from utils import notes_names_to_index, midi_to_index, index_to_note_name

logging.basicConfig(level=logging.INFO)


class State:
    quit = False
    played_notes = []


state = State()


class MidiThread(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)

        logging.info(f"Start thread {self.name}")

        self.name = name
        self.played_notes = []

        # Open all available inputs.
        self.ports = [mido.open_input(name) for name in mido.get_input_names()]

    def run(self):

        while not state.quit:
            for message in multi_receive(self.ports, block=False):
                if message.type == "note_on":
                    self.played_notes.append(message.note)

                if message.type == "note_off":
                    self.played_notes.remove(message.note)

                self.played_notes.sort()

                state.played_notes = midi_to_index(self.played_notes)

            time.sleep(0.1)


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


class UI:

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('998x998')

        self.root.resizable(0, 0)
        self.root.resizable(False, False)
        self.root.resizable(width=False, height=False)

        self.canvas = tkinter.Canvas(
            self.root,
            width=998,
            height=998
        )
        self.canvas.pack()

        self.img = tkinter.PhotoImage(file='bin/paper.png')

        self.canvas.create_image(
            0,
            0,
            anchor=tkinter.NW,
            image=self.img
        )

        self.time_current = "-"
        self.title_str = "PChord"

        self.chord_str = "Chord"
        self.chord_notes_str = "Notes"
        self.played_notes_str = "Played"

        self.chord = "?"
        self.chord_scale = ""
        self.chord_notes = "[?, ?, ?, ?]"
        self.played_notes = "[?, ?, ?, ?, ?, ?]"

        self.current_chord = None
        self.notes_to_check = []

        self.time_text = self.canvas.create_text(870, 40, fill="black", font="Segoe 25", anchor=tkinter.SW, text="")
        self.title_text = self.canvas.create_text(160, 66 + 100, fill="black", font="Segoe 70", anchor=tkinter.SW,
                                                  text=self.title_str)

        self.chord_lbl = self.canvas.create_text(165, 411, fill="black", font="Segoe 45", anchor=tkinter.SW,
                                                 text=self.chord_str)
        self.chord_text = self.canvas.create_text(400, 411, fill="black", font="Segoe 45", anchor=tkinter.SW,
                                                  text=self.chord)

        self.notes_lbl = self.canvas.create_text(165, 511, fill="black", font="Segoe 45", anchor=tkinter.SW,
                                                 text=self.chord_notes_str)
        self.notes_text = self.canvas.create_text(400, 511, fill="black", font="Segoe 45", anchor=tkinter.SW,
                                                  text=self.chord_notes)

        self.played_lbl = self.canvas.create_text(165, 661, fill="black", font="Segoe 45", anchor=tkinter.SW,
                                                  text=self.played_notes_str)
        self.played_text = self.canvas.create_text(400, 661, fill="black", font="Segoe 45", anchor=tkinter.SW,
                                                   text=self.played_notes)

        self.generator = Generator()

        self.next_chord()
        self.update_texts()

    def next_chord(self):

        self.current_chord = self.generator.get()

        self.chord_scale = self.current_chord[0]
        self.chord = self.current_chord[1]
        self.chord_notes = self.current_chord[2]
        self.notes_to_check = notes_names_to_index(self.chord_notes)

    def update_texts(self):
        self.canvas.itemconfig(self.chord_text, text=self.chord)
        self.canvas.itemconfig(self.notes_text, text=self.chord_notes)
        self.canvas.itemconfig(self.played_text, text=state.played_notes)

    def tick(self):
        time_str = time.strftime('%H:%M:%S')

        if time_str != self.time_current:
            self.time_current = time_str

            self.canvas.itemconfig(self.time_text, text=self.time_current)

        self.root.after(200, self.tick)

    def update(self):

        if len(state.played_notes) > 0:

            if self.notes_to_check == state.played_notes:
                self.next_chord()
                self.update_texts()

            played_notes = index_to_note_name(state.played_notes, self.chord_scale)
        else:
            played_notes = ""

        self.canvas.itemconfig(self.played_text, text=played_notes)

        self.root.after(100, self.update)

    def run(self):
        self.tick()
        self.update()

        self.root.mainloop()


if __name__ == '__main__':

    midiThread = MidiThread("client")
    midiThread.start()

    try:
        UI().run()

    except Exception as ex:

        print("Quit")
        print(ex)

    finally:
        print("Cleaning, please wait")
        state.quit = True

        midiThread.join(timeout=5)
        print("Done.")

if __name__ == '__main__x':
    g = Generator()
    print(g.test_list)