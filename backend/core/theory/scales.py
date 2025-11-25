"""
Scale definitions and harmonization logic.
"""
from enum import Enum
from typing import List, Dict
from .notes import Note
from .chords import Chord, ChordQuality

class ScaleType(str, Enum):
    MAJOR = "Major"
    NATURAL_MINOR = "Natural Minor"
    HARMONIC_MINOR = "Harmonic Minor"
    MELODIC_MINOR = "Melodic Minor"
    DORIAN = "Dorian"
    PHRYGIAN = "Phrygian"
    LYDIAN = "Lydian"
    MIXOLYDIAN = "Mixolydian"
    AEOLIAN = "Aeolian"
    LOCRIAN = "Locrian"

SCALE_INTERVALS: Dict[ScaleType, List[int]] = {
    ScaleType.MAJOR: [0, 2, 4, 5, 7, 9, 11],
    ScaleType.NATURAL_MINOR: [0, 2, 3, 5, 7, 8, 10],
    ScaleType.HARMONIC_MINOR: [0, 2, 3, 5, 7, 8, 11],
    ScaleType.MELODIC_MINOR: [0, 2, 3, 5, 7, 9, 11],
    ScaleType.DORIAN: [0, 2, 3, 5, 7, 9, 10],
    ScaleType.PHRYGIAN: [0, 1, 3, 5, 7, 8, 10],
    ScaleType.LYDIAN: [0, 2, 4, 6, 7, 9, 11],
    ScaleType.MIXOLYDIAN: [0, 2, 4, 5, 7, 9, 10],
    ScaleType.AEOLIAN: [0, 2, 3, 5, 7, 8, 10],
    ScaleType.LOCRIAN: [0, 1, 3, 5, 6, 8, 10],
}

# Diatonic chords for Major scale (Triads)
MAJOR_SCALE_TRIADS = [
    ChordQuality.MAJOR,
    ChordQuality.MINOR,
    ChordQuality.MINOR,
    ChordQuality.MAJOR,
    ChordQuality.MAJOR,
    ChordQuality.MINOR,
    ChordQuality.DIMINISHED
]

# Diatonic chords for Major scale (7ths)
MAJOR_SCALE_SEVENTHS = [
    ChordQuality.MAJOR_7,
    ChordQuality.MINOR_7,
    ChordQuality.MINOR_7,
    ChordQuality.MAJOR_7,
    ChordQuality.DOMINANT_7,
    ChordQuality.MINOR_7,
    ChordQuality.HALF_DIMINISHED
]

class Scale:
    def __init__(self, root: Note, scale_type: ScaleType):
        self.root = root
        self.scale_type = scale_type
        self.notes = self._generate_notes()

    def _generate_notes(self) -> List[Note]:
        intervals = SCALE_INTERVALS[self.scale_type]
        return [self.root.transpose(interval) for interval in intervals]

    def get_diatonic_chord(self, degree: int, sevenths: bool = True) -> Chord:
        """
        Get the diatonic chord for a given degree (1-based).
        Currently only supports Major scale logic fully.
        """
        if self.scale_type != ScaleType.MAJOR:
            # TODO: Implement harmonization for other scales
            raise NotImplementedError("Harmonization only supported for Major scale currently")
            
        index = (degree - 1) % 7
        root_note = self.notes[index]
        
        if sevenths:
            quality = MAJOR_SCALE_SEVENTHS[index]
        else:
            quality = MAJOR_SCALE_TRIADS[index]
            
        return Chord(root_note, quality)
