"""
Data models for PChords backend.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class ChordQuality(str, Enum):
    """Available chord qualities."""
    M9 = "M9"
    m9 = "m9"
    NINE = "9"
    SEVEN_SHARP9_SHARP5 = "7#9#5"
    SEVEN_FLAT9_FLAT5 = "7b9b5"
    M7 = "M7"
    SEVEN = "7"
    m7 = "m7"
    m7b5 = "m7b5"
    dim7 = "dim7"
    MAJOR = ""
    MINOR = "m"
    DIM = "dim"
    AUG = "aug"


class ChordScale(str, Enum):
    """Available chord scales."""
    MAJOR = "maj"
    MINOR = "min"


class Difficulty(str, Enum):
    """Practice difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class ChordInversion(str, Enum):
    """Chord inversion types."""
    ROOT = "root"
    FIRST = "first"
    SECOND = "second"
    FROM_3RD = "from_3rd"
    FROM_7TH = "from_7th"


# ============================================================================
# Core Models
# ============================================================================

class ChordData(BaseModel):
    """Represents a single chord."""
    root: str = Field(..., description="Root note (e.g., C, D#, Eb)")
    name: str = Field(..., description="Full chord name")
    notes: List[str] = Field(..., description="List of note names in the chord")
    scale: str = Field(default="", description="Scale type (maj/min)")
    quality: Optional[str] = Field(default=None, description="Chord quality")
    inversion: Optional[str] = Field(default=None, description="Chord inversion type")


class ChordSet(BaseModel):
    """Configuration for a set of chords to practice."""
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Display name")
    enabled: bool = Field(default=True, description="Whether this set is active")
    qualities: List[str] = Field(default_factory=list, description="Chord qualities to include")
    scales: List[str] = Field(default_factory=list, description="Scales to use")
    inversions: List[str] = Field(default_factory=list, description="Inversion types")
    notes_range: Optional[List[int]] = Field(default=None, description="MIDI note range [min, max]")
    exclude_roots: List[str] = Field(default_factory=list, description="Root notes to exclude")
    difficulty: str = Field(default="medium", description="Difficulty level")
    specific_chords: List[ChordData] = Field(default_factory=list, description="Manually defined chords")


class Config(BaseModel):
    """Application configuration."""
    # Window/UI settings
    window_width: int = 998
    window_height: int = 800
    window_title: str = "PChords"

    # MIDI settings
    midi_poll_interval: float = 0.1
    midi_timeout: float = 5.0

    # Chord generation
    chord_sets: List[ChordSet] = Field(default_factory=list)
    active_chord_set_id: Optional[str] = None

    # Database
    database_url: str = "sqlite+aiosqlite:///./pchords.db"


# ============================================================================
# API Request/Response Models
# ============================================================================

class ChordResponse(BaseModel):
    """Response model for chord data."""
    chord: ChordData
    remaining: int = Field(..., description="Number of chords remaining in current set")


class ChordSetCreateRequest(BaseModel):
    """Request to create a new chord set."""
    name: str
    qualities: List[str] = []
    scales: List[str] = ["maj", "min"]
    inversions: List[str] = ["from_3rd", "from_7th"]
    difficulty: str = "medium"


class ChordSetUpdateRequest(BaseModel):
    """Request to update an existing chord set."""
    name: Optional[str] = None
    enabled: Optional[bool] = None
    qualities: Optional[List[str]] = None
    scales: Optional[List[str]] = None
    inversions: Optional[List[str]] = None
    difficulty: Optional[str] = None


class ConfigUpdateRequest(BaseModel):
    """Request to update configuration."""
    active_chord_set_id: Optional[str] = None
    midi_poll_interval: Optional[float] = None


# ============================================================================
# MIDI Models
# ============================================================================

class MidiMessage(BaseModel):
    """MIDI message data."""
    type: str = Field(..., description="Message type (note_on, note_off)")
    note: int = Field(..., ge=0, le=127, description="MIDI note number")
    velocity: int = Field(default=0, ge=0, le=127, description="Note velocity")
    timestamp: float = Field(default_factory=lambda: datetime.now().timestamp())


class MidiStatus(BaseModel):
    """Status of MIDI connections."""
    connected: bool
    input_ports: List[str]
    played_notes: List[int]


# ============================================================================
# Statistics Models
# ============================================================================

class ChordAttempt(BaseModel):
    """Record of a single chord attempt."""
    chord_name: str
    expected_notes: List[str]
    played_notes: List[int]
    success: bool
    time_taken_ms: int
    attempted_at: datetime = Field(default_factory=datetime.now)


class PracticeSession(BaseModel):
    """A practice session."""
    id: Optional[int] = None
    started_at: datetime = Field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None
    chord_set_id: Optional[str] = None
    total_chords: int = 0
    successful_chords: int = 0

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_chords == 0:
            return 0.0
        return (self.successful_chords / self.total_chords) * 100


class ChordStats(BaseModel):
    """Statistics for a specific chord."""
    chord_name: str
    attempts: int = 0
    successes: int = 0
    failures: int = 0
    average_time_ms: float = 0.0
    best_time_ms: Optional[int] = None
    last_practiced: Optional[datetime] = None

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.attempts == 0:
            return 0.0
        return (self.successes / self.attempts) * 100


class OverallStats(BaseModel):
    """Overall practice statistics."""
    total_sessions: int = 0
    total_chords_practiced: int = 0
    total_successes: int = 0
    overall_success_rate: float = 0.0
    average_time_ms: float = 0.0
    most_practiced_chord: Optional[str] = None
    best_chord: Optional[str] = None
    needs_practice: List[str] = []
