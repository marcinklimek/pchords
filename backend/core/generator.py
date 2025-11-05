"""
Chord generator for PChords backend.
"""

import random
import asyncio
from pathlib import Path
from typing import List, Optional
from pychord import Chord

from .models import ChordData, ChordSet
from ..utils.constants import SCALES_LIST
from ..utils.converters import save_json, load_json


class ChordGenerator:
    """Generates and manages chords for practice."""

    def __init__(self, chord_sets: List[ChordSet]):
        """
        Initialize chord generator.

        Args:
            chord_sets: List of chord sets to use
        """
        self.chord_sets = chord_sets
        self.chord_list: List[ChordData] = []
        self._lock = asyncio.Lock()
        self.chords_file = Path("data/chords.json")

    async def start(self) -> None:
        """Start the generator and initialize chord list."""
        await self.init_chord_list()

    async def init_chord_list(self, reboot: bool = False) -> None:
        """
        Initialize chord list from file or generate new chords.

        Args:
            reboot: Whether to force regeneration of chords
        """
        async with self._lock:
            self.chord_list = []

            # Try to load from file
            if self.chords_file.exists() and not reboot:
                try:
                    raw_data = load_json(self.chords_file)
                    self.chord_list = [
                        ChordData(**chord) if isinstance(chord, dict)
                        else ChordData(
                            root=chord[0],
                            name=chord[1],
                            notes=chord[2],
                            scale=chord[3] if len(chord) > 3 else ""
                        )
                        for chord in raw_data
                    ]
                except Exception:
                    self.chord_list = []

            # Generate if needed
            if len(self.chord_list) == 0 or reboot:
                await self.generate_chords()
                await self.save_chords()

    async def get_next(self) -> ChordData:
        """
        Get a random chord from the list.

        Returns:
            ChordData object
        """
        async with self._lock:
            # Regenerate if empty
            if len(self.chord_list) == 0:
                await self.init_chord_list(reboot=True)

            # Get random chord
            if len(self.chord_list) > 0:
                item = random.choice(self.chord_list)
                self.chord_list.remove(item)
                await self.save_chords()
                return item
            else:
                # Fallback
                return ChordData(
                    root="C",
                    name="C Major",
                    notes=["C", "E", "G"],
                    scale="maj"
                )

    async def get_remaining_count(self) -> int:
        """Get number of remaining chords."""
        async with self._lock:
            return len(self.chord_list)

    async def generate_chords(self) -> None:
        """Generate chord data for all enabled chord sets."""
        for chord_set in self.chord_sets:
            if not chord_set.enabled:
                continue

            # Generate from specific chords if provided
            if chord_set.specific_chords:
                self.chord_list.extend(chord_set.specific_chords)
                continue

            # Generate from qualities and scales
            for quality in chord_set.qualities:
                for scale in chord_set.scales:
                    await self._generate_chords_for_quality_scale(
                        quality, scale, chord_set
                    )

    async def _generate_chords_for_quality_scale(
        self, quality: str, scale: str, chord_set: ChordSet
    ) -> None:
        """
        Generate chords for a specific quality and scale combination.

        Args:
            quality: Chord quality
            scale: Scale type
            chord_set: Chord set configuration
        """
        for root_note in SCALES_LIST:
            # Skip excluded roots
            if root_note in chord_set.exclude_roots:
                continue

            try:
                # Generate base chord
                chord_base = Chord.from_note_index(1, quality, root_note + scale)
                notes = chord_base.components()

                # Determine which inversions to generate
                inversions = chord_set.inversions or ["from_3rd", "from_7th"]

                for inversion_type in inversions:
                    if inversion_type == "from_3rd" and len(notes) > 1:
                        # Chord from 3rd
                        chord_name = f"{root_note}{chord_base.quality} - From 3rd"
                        notes_subset = notes[1:]
                        self.chord_list.append(
                            ChordData(
                                root=str(chord_base.root),
                                name=chord_name,
                                notes=notes_subset,
                                scale=scale,
                                quality=quality,
                                inversion="from_3rd"
                            )
                        )

                    elif inversion_type == "from_7th" and len(notes) >= 4:
                        # Chord from 7th
                        chord_name = f"{root_note}{chord_base.quality} - From 7th"
                        notes_subset = notes[3:] + notes[1:3]
                        self.chord_list.append(
                            ChordData(
                                root=str(chord_base.root),
                                name=chord_name,
                                notes=notes_subset,
                                scale=scale,
                                quality=quality,
                                inversion="from_7th"
                            )
                        )

                    elif inversion_type == "root":
                        # Root position
                        chord_name = f"{root_note}{chord_base.quality}"
                        self.chord_list.append(
                            ChordData(
                                root=str(chord_base.root),
                                name=chord_name,
                                notes=notes,
                                scale=scale,
                                quality=quality,
                                inversion="root"
                            )
                        )

            except Exception as e:
                # Skip chords that fail to generate
                continue

    async def save_chords(self) -> None:
        """Save current chord list to file."""
        try:
            # Convert to serializable format
            serializable_data = [
                {
                    "root": chord.root,
                    "name": chord.name,
                    "notes": chord.notes,
                    "scale": chord.scale,
                    "quality": chord.quality,
                    "inversion": chord.inversion
                }
                for chord in self.chord_list
            ]

            save_json(self.chords_file, serializable_data)
        except Exception:
            pass

    async def regenerate(self, chord_sets: Optional[List[ChordSet]] = None) -> None:
        """
        Regenerate chords with new chord sets.

        Args:
            chord_sets: New chord sets (or use existing if None)
        """
        if chord_sets is not None:
            self.chord_sets = chord_sets

        await self.init_chord_list(reboot=True)
