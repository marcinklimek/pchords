"""
Chord generator for PChords backend.
"""
import random
import asyncio
from typing import List, Optional
from .models import ChordData, ChordSet, ChordQuality, VoicingType
from .theory.notes import Note, NoteName
from .theory.chords import Chord
from .theory.voicings import VoicingGenerator

class ChordGenerator:
    """Generates and manages chords for practice."""

    def __init__(self, chord_sets: List[ChordSet]):
        self.chord_sets = chord_sets
        self.chord_queue: List[ChordData] = []
        self._lock = asyncio.Lock()

    async def start(self) -> None:
        """Start the generator."""
        await self.regenerate()

    async def get_next(self) -> ChordData:
        """Get the next chord to practice."""
        async with self._lock:
            if not self.chord_queue:
                await self._generate_batch()
            
            if not self.chord_queue:
                 # Fallback
                return self._create_fallback_chord()
                
            return self.chord_queue.pop(0)

    async def get_remaining_count(self) -> int:
        async with self._lock:
            return len(self.chord_queue)

    async def regenerate(self, chord_sets: Optional[List[ChordSet]] = None) -> None:
        """Regenerate the chord queue."""
        if chord_sets:
            self.chord_sets = chord_sets
        
        async with self._lock:
            self.chord_queue = []
            await self._generate_batch()

    async def _generate_batch(self) -> None:
        """Generate a batch of chords based on active sets."""
        new_chords = []
        
        for chord_set in self.chord_sets:
            if not chord_set.enabled:
                continue
                
            # Determine roots to use
            roots = chord_set.roots if chord_set.roots else [n.value for n in NoteName]
            
            for root_name in roots:
                for quality in chord_set.qualities:
                    for voicing_type in chord_set.voicing_types:
                        try:
                            # Create base chord
                            root = Note(root_name, octave=4) # Middle C octave for base
                            base_chord = Chord(root, quality)
                            
                            # Apply voicing
                            voiced_notes = VoicingGenerator.create_voicing(base_chord, voicing_type)
                            
                            # Create ChordData
                            chord_data = ChordData(
                                root=root_name,
                                quality=quality.value,
                                name=f"{root_name}{quality.value} ({voicing_type.value})",
                                notes=[n.name for n in voiced_notes],
                                midi_notes=[n.midi for n in voiced_notes],
                                voicing_type=voicing_type.value
                            )
                            new_chords.append(chord_data)
                        except Exception as e:
                            print(f"Error generating chord {root_name} {quality}: {e}")
                            continue

        random.shuffle(new_chords)
        self.chord_queue.extend(new_chords)

    def _create_fallback_chord(self) -> ChordData:
        return ChordData(
            root="C",
            quality="Maj",
            name="C Major",
            notes=["C", "E", "G"],
            midi_notes=[60, 64, 67],
            voicing_type="Close"
        )
