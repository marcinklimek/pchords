"""
Chord definitions and generation logic.
"""
from enum import Enum
from typing import List, Dict
from .notes import Note, Interval, NoteName

class ChordQuality(str, Enum):
    MAJOR = "Maj"
    MINOR = "min"
    DIMINISHED = "dim"
    AUGMENTED = "aug"
    MAJOR_7 = "Maj7"
    MINOR_7 = "min7"
    DOMINANT_7 = "7"
    HALF_DIMINISHED = "m7b5"
    DIMINISHED_7 = "dim7"
    MINOR_MAJOR_7 = "mM7"
    SUS4 = "sus4"
    SUS2 = "sus2"
    # Extensions
    MAJOR_9 = "Maj9"
    MINOR_9 = "min9"
    DOMINANT_9 = "9"
    DOMINANT_13 = "13"
    ALT_7 = "7alt"

# Intervals relative to root
CHORD_FORMULAS: Dict[ChordQuality, List[int]] = {
    ChordQuality.MAJOR: [0, 4, 7],
    ChordQuality.MINOR: [0, 3, 7],
    ChordQuality.DIMINISHED: [0, 3, 6],
    ChordQuality.AUGMENTED: [0, 4, 8],
    
    ChordQuality.MAJOR_7: [0, 4, 7, 11],
    ChordQuality.MINOR_7: [0, 3, 7, 10],
    ChordQuality.DOMINANT_7: [0, 4, 7, 10],
    ChordQuality.HALF_DIMINISHED: [0, 3, 6, 10],
    ChordQuality.DIMINISHED_7: [0, 3, 6, 9],
    ChordQuality.MINOR_MAJOR_7: [0, 3, 7, 11],
    
    ChordQuality.SUS4: [0, 5, 7],
    ChordQuality.SUS2: [0, 2, 7],
    
    ChordQuality.MAJOR_9: [0, 4, 7, 11, 14],
    ChordQuality.MINOR_9: [0, 3, 7, 10, 14],
    ChordQuality.DOMINANT_9: [0, 4, 7, 10, 14],
    ChordQuality.DOMINANT_13: [0, 4, 7, 10, 14, 21],
    
    # Altered: Root, 3, b5, b7, #9, b13 (example voicing)
    ChordQuality.ALT_7: [0, 4, 6, 10, 15, 20] 
}

class Chord:
    def __init__(self, root: Note, quality: ChordQuality, inversion: int = 0):
        self.root = root
        self.quality = quality
        self.inversion = inversion
        self.notes = self._generate_notes()

    def _generate_notes(self) -> List[Note]:
        intervals = CHORD_FORMULAS[self.quality]
        notes = [self.root.transpose(interval) for interval in intervals]
        
        # Handle inversion
        if self.inversion > 0:
            # Simple inversion: move bottom notes up an octave
            for _ in range(self.inversion):
                note = notes.pop(0)
                notes.append(note.transpose(12))
                
        return notes

    @property
    def name(self) -> str:
        return f"{self.root.name}{self.quality.value}"

    @property
    def midi_notes(self) -> List[int]:
        return [n.midi for n in self.notes]
