
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from pathlib import Path
import asyncio
from enum import Enum


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class Config:

    # Window settings
    window_width: int = 998
    window_height: int = 800
    window_title: str = "PChords"
    
    # Font settings
    default_font_size: int = 9
    macos_font_size: int = 7
    
    # MIDI settings
    midi_poll_interval: float = 0.1
    midi_timeout: float = 5.0
    
    # UI update intervals
    ui_update_interval: int = 100  # milliseconds
    clock_update_interval: int = 200  # milliseconds
    
    # File paths
    chords_file: Path = Path("chords.json")
    paper_image: Path = Path("bin/paper.png")
    
    # Logging
    log_level: LogLevel = LogLevel.INFO
    log_file: Optional[Path] = None
    
    # Chord generation
    chord_qualities: List[str] = field(default_factory=lambda: ['M9', 'm9'])
    chord_scales: List[str] = field(default_factory=lambda: ['maj', 'min'])


@dataclass
class ChordData:
    root: str
    name: str
    notes: List[str]
    scale: str = ""


@dataclass
class AppState:
    quit: bool = False
    played_notes: List[int] = field(default_factory=list)
    current_chord: Optional[ChordData] = None
    notes_to_check: List[int] = field(default_factory=list)
    
    # Thread safety
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    
    async def update_played_notes(self, notes: List[int]) -> None:
        async with self._lock:
            self.played_notes = notes.copy()
    
    async def get_played_notes(self) -> List[int]:
        async with self._lock:
            return self.played_notes.copy()
    
    async def set_quit(self, value: bool = True) -> None:
        async with self._lock:
            self.quit = value
    
    async def is_quit(self) -> bool:
        async with self._lock:
            return self.quit


@dataclass
class MidiMessage:
    message_type: str
    note: int
    velocity: int = 0
    timestamp: float = 0.0
