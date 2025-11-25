"""
Voicing logic for chords.
"""
from enum import Enum
from typing import List
from .notes import Note
from .chords import Chord, ChordQuality

class VoicingType(str, Enum):
    CLOSE = "Close"
    DROP_2 = "Drop 2"
    DROP_3 = "Drop 3"
    SHELL_3_7 = "Shell (3-7)"
    SHELL_7_3 = "Shell (7-3)"
    ROOTLESS_A = "Rootless A" # 3-5-7-9
    ROOTLESS_B = "Rootless B" # 7-9-3-5

class VoicingGenerator:
    @staticmethod
    def create_voicing(chord: Chord, voicing_type: VoicingType) -> List[Note]:
        """
        Transform a base chord into a specific voicing.
        """
        # Start with base notes (Root, 3, 5, 7)
        # We need to ensure we have the right intervals. 
        # For simplicity, we'll assume the chord object has [R, 3, 5, 7] roughly in order
        # or we regenerate them based on quality.
        
        base_notes = chord.notes
        if len(base_notes) < 3:
            return base_notes # Can't do much with triads for some voicings
            
        if voicing_type == VoicingType.CLOSE:
            return base_notes
            
        elif voicing_type == VoicingType.DROP_2:
            # Drop the 2nd note from the top down an octave
            if len(base_notes) < 4: return base_notes
            notes = list(base_notes)
            # Standard close position is R 3 5 7. 
            # Drop 2 takes the 2nd from top (5) and drops it.
            # But we need to be careful about the input inversion.
            # Let's assume input is close position.
            second_from_top = notes.pop(-2)
            notes.insert(0, second_from_top.transpose(-12))
            return notes
            
        elif voicing_type == VoicingType.DROP_3:
            # Drop the 3rd note from the top down an octave
            if len(base_notes) < 4: return base_notes
            notes = list(base_notes)
            third_from_top = notes.pop(-3)
            notes.insert(0, third_from_top.transpose(-12))
            return notes
            
        elif voicing_type == VoicingType.SHELL_3_7:
            # Root + 3 + 7
            # We need to identify 3rd and 7th.
            # Based on formulas: index 1 is usually 3rd, index 3 is 7th (for 7th chords)
            if len(base_notes) < 4: return base_notes
            return [base_notes[0], base_notes[1], base_notes[3]]
            
        elif voicing_type == VoicingType.SHELL_7_3:
             # Root + 7 + 3 (Spread)
            if len(base_notes) < 4: return base_notes
            root = base_notes[0]
            third = base_notes[1]
            seventh = base_notes[3]
            # Move 7th down or 3rd up to invert
            return [root, seventh.transpose(-12), third]

        elif voicing_type == VoicingType.ROOTLESS_A:
            # 3 5 7 9 (Left hand rootless)
            # We need to generate the 9th.
            # This requires knowledge of the scale or generic extension.
            # For now, let's just add a Major 9th (14 semitones) to root
            root = base_notes[0]
            ninth = root.transpose(14)
            
            # Remove root, add 9 at top
            notes = base_notes[1:] + [ninth]
            return notes

        return base_notes
