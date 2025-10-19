
"""
Constants for musical scales and chord qualities.
"""
from typing import Tuple, List

SCALES_LIST: Tuple[str, ...] = ('Ab', 'A', 'A#', 'Bb', 'B', 'Cb', 'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#')
QUALITIES: Tuple[str, ...] = ('m9', 'M9', '9', '7#9#5', '7b9b5')
OCTAVES: List[int] = list(range(11))
NOTES_IN_OCTAVE: int = 12
