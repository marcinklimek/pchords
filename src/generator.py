import random
import asyncio
from pathlib import Path
from typing import List, Optional, Tuple
from pychord import Chord

from constants import SCALES_LIST
from models import ChordData, Config
from utils import load_json, save_json
from validation import validate_chord_data, ValidationError
from logger import get_logger

logger = get_logger(__name__)


class Generator:


    def __init__(self, config: Config):
        """
        Initialize chord generator.

        Args:
            config: Application configuration
        """
        self.config = config
        self.chord_list: List[ChordData] = []
        self._lock = asyncio.Lock()

    async def start(self) -> None:
        """
        Start the generator and initialize chord list.
        """
        await self.init_chord_list()

    async def init_chord_list(self, reboot: bool = False) -> None:
        """
        Initialize chord list from file or generate new chords.
        
        Args:
            reboot: Whether to force regeneration of chords
        """
        async with self._lock:
            self.chord_list = []

            if self.config.chords_file.exists() and not reboot:
                try:
                    raw_data = load_json(self.config.chords_file)
                    self.chord_list = [validate_chord_data(chord) for chord in raw_data]
                    logger.info(f"Loaded {len(self.chord_list)} chords from file")
                except (ValidationError, Exception) as e:
                    logger.error(f"Failed to load chords: {e}")
                    self.chord_list = []

            if len(self.chord_list) == 0 or reboot:
                logger.info("Generating new chord list")
                await self.generate_chords()
                await self.save_chords()

            logger.info(f"Chord list initialized with {len(self.chord_list)} chords")

    async def get(self) -> ChordData:
        """
        a random chord from the list.
        """
        
        async with self._lock:
            if len(self.chord_list) == 0:
                logger.info("Chord list empty, regenerating")
                await self.init_chord_list(reboot=True)
            
            if len(self.chord_list) > 0:
                item = random.choice(self.chord_list)
                self.chord_list.remove(item)
                
                # Save updated list
                await self.save_chords()
                
                logger.info(f"Selected chord: {item.name}, {len(self.chord_list)} chords remaining")
                return item
            else:
                # Fallback if generation failed
                logger.error("Failed to generate chords, returning default")
                return ChordData(root="C", name="C Major", notes=["C", "E", "G"], scale="maj")

    async def generate_chords(self) -> None:
        """
        Generate chord data for all configured qualities and scales.
        """
        for quality in self.config.chord_qualities:
            for scale in self.config.chord_scales:
                await self._generate_chords_for_quality_scale(quality, scale)

    async def _generate_chords_for_quality_scale(self, quality: str, scale: str) -> None:
        """
        chords for a specific quality and scale combination.
        """
        for root_note in SCALES_LIST:
            try:
                chord_base = Chord.from_note_index(1, quality, root_note + scale)
                notes = chord_base.components()

                # Generate chord from 3rd
                chord_name = f"{root_note}{chord_base.quality} - From 3rd"
                notes_from_3rd = notes[1:] if len(notes) > 1 else notes
                
                chord_data = ChordData(
                    root=str(chord_base.root),
                    name=chord_name,
                    notes=notes_from_3rd,
                    scale=scale
                )
                self.chord_list.append(chord_data)

                # Generate chord from 7th (if we have enough notes)
                if len(notes) >= 4:
                    chord_name = f"{root_note}{chord_base.quality} - From 7th"
                    notes_from_7th = notes[3:] + notes[1:3]
                    
                    chord_data = ChordData(
                        root=str(chord_base.root),
                        name=chord_name,
                        notes=notes_from_7th,
                        scale=scale
                    )
                    self.chord_list.append(chord_data)
                    
            except Exception as e:
                logger.warning(f"Failed to generate chord for {root_note} {quality} {scale}: {e}")

    async def save_chords(self) -> None:
        """
        Save current chord list to file.
        """
        try:
            # Convert ChordData objects to serializable format
            serializable_data = []
            for chord in self.chord_list:
                serializable_data.append([chord.root, chord.name, chord.notes, chord.scale])
            
            save_json(self.config.chords_file, serializable_data)
            logger.debug(f"Saved {len(self.chord_list)} chords to file")
            
        except Exception as e:
            logger.error(f"Failed to save chords: {e}")
            raise
