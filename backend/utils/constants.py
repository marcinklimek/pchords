"""
Constants for musical scales and chord qualities.
"""
from typing import Tuple, List

SCALES_LIST: Tuple[str, ...] = (
    'Ab', 'A', 'A#', 'Bb', 'B', 'Cb', 'C', 'C#',
    'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#'
)

QUALITIES: Tuple[str, ...] = (
    'm9', 'M9', '9', '7#9#5', '7b9b5',
    'M7', '7', 'm7', 'm7b5', 'dim7',
    '', 'm', 'dim', 'aug'
)

OCTAVES: List[int] = list(range(11))
NOTES_IN_OCTAVE: int = 12

# MIDI constants
MIDI_NOTE_MIN: int = 0
MIDI_NOTE_MAX: int = 127
