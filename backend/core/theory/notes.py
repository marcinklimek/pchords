"""
Core Note and Interval definitions.
"""
from enum import Enum, IntEnum
from typing import List, Optional, Union

class NoteName(str, Enum):
    C = "C"
    C_SHARP = "C#"
    D_FLAT = "Db"
    D = "D"
    D_SHARP = "D#"
    E_FLAT = "Eb"
    E = "E"
    F = "F"
    F_SHARP = "F#"
    G_FLAT = "Gb"
    G = "G"
    G_SHARP = "G#"
    A_FLAT = "Ab"
    A = "A"
    A_SHARP = "A#"
    B_FLAT = "Bb"
    B = "B"

class Interval(IntEnum):
    PERFECT_UNISON = 0
    MINOR_SECOND = 1
    MAJOR_SECOND = 2
    MINOR_THIRD = 3
    MAJOR_THIRD = 4
    PERFECT_FOURTH = 5
    TRITONE = 6
    PERFECT_FIFTH = 7
    MINOR_SIXTH = 8
    MAJOR_SIXTH = 9
    MINOR_SEVENTH = 10
    MAJOR_SEVENTH = 11
    OCTAVE = 12
    MINOR_NINTH = 13
    MAJOR_NINTH = 14
    PERFECT_ELEVENTH = 17
    MAJOR_THIRTEENTH = 21

# Standard MIDI mapping
NOTE_TO_OFFSET = {
    "C": 0, "C#": 1, "Db": 1,
    "D": 2, "D#": 3, "Eb": 3,
    "E": 4,
    "F": 5, "F#": 6, "Gb": 6,
    "G": 7, "G#": 8, "Ab": 8,
    "A": 9, "A#": 10, "Bb": 10,
    "B": 11
}

OFFSET_TO_NOTE = {
    0: ["C"],
    1: ["C#", "Db"],
    2: ["D"],
    3: ["D#", "Eb"],
    4: ["E"],
    5: ["F"],
    6: ["F#", "Gb"],
    7: ["G"],
    8: ["G#", "Ab"],
    9: ["A"],
    10: ["A#", "Bb"],
    11: ["B"]
}

class Note:
    def __init__(self, name_or_midi: Union[str, int], octave: Optional[int] = None):
        if isinstance(name_or_midi, int):
            self.midi = name_or_midi
            self.octave = (self.midi // 12) - 1
            # Default to sharp names for simplicity in basic init, context can change this
            self.name = OFFSET_TO_NOTE[self.midi % 12][0]
            self.pitch_class = self.midi % 12
        else:
            self.name = name_or_midi
            self.pitch_class = NOTE_TO_OFFSET[self.name]
            if octave is not None:
                self.octave = octave
                self.midi = (self.octave + 1) * 12 + self.pitch_class
            else:
                self.octave = 4 # Default middle C octave
                self.midi = (self.octave + 1) * 12 + self.pitch_class

    def __repr__(self):
        return f"Note({self.name}{self.octave})"

    def __eq__(self, other):
        if isinstance(other, Note):
            return self.midi == other.midi
        return False

    def transpose(self, semitones: int) -> 'Note':
        return Note(self.midi + semitones)

    @staticmethod
    def from_midi(midi: int) -> 'Note':
        return Note(midi)
