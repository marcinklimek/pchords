"""
Data models for PChords backend.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

# Import from theory engine
from .theory.notes import NoteName
from .theory.chords import ChordQuality
from .theory.scales import ScaleType
from .theory.voicings import VoicingType

# ============================================================================
# Core Models
# ============================================================================

class ChordData(BaseModel):
    """Represents a single chord for API response."""
    root: str = Field(..., description="Root note name")
    quality: str = Field(..., description="Chord quality")
    name: str = Field(..., description="Full display name")
    notes: List[str] = Field(..., description="List of note names")
    midi_notes: List[int] = Field(..., description="List of MIDI note numbers")
    voicing_type: Optional[str] = Field(None, description="Voicing type used")
    scale_context: Optional[str] = Field(None, description="Scale context if applicable")

class ScaleData(BaseModel):
    """Represents a scale."""
    root: str
    type: str
    name: str
    notes: List[str]
    midi_notes: List[int]
    diatonic_chords: Optional[List[ChordData]] = None

class ProgressionStep(BaseModel):
    """A single step in a chord progression."""
    degree: str = Field(..., description="Roman numeral degree (e.g., II, V)")
    chord: ChordData
    duration_beats: int = Field(4, description="Duration in beats")

class ProgressionData(BaseModel):
    """A full chord progression."""
    id: str
    name: str
    key: str
    scale_type: str
    steps: List[ProgressionStep]
    tempo: int = 120

# ============================================================================
# Configuration Models
# ============================================================================

class ChordSet(BaseModel):
    """Configuration for a set of chords to practice."""
    id: str
    name: str
    enabled: bool = True
    qualities: List[ChordQuality] = []
    roots: List[str] = [] # Specific roots to practice
    voicing_types: List[VoicingType] = [VoicingType.CLOSE]
    difficulty: str = "medium"

class UserProfile(BaseModel):
    """User settings and profile."""
    id: str = "default"
    midi_input_device: Optional[str] = None
    root_note_mode: str = "single" # off, single, octave
    active_chord_set_id: Optional[str] = None
    
# ============================================================================
# API Request/Response Models
# ============================================================================

class ChordResponse(BaseModel):
    """Response model for chord generation."""
    chord: ChordData
    remaining: int

class ScaleResponse(BaseModel):
    """Response model for scale data."""
    scale: ScaleData
    diatonic_chords: List[ChordData]

class ChordSetCreateRequest(BaseModel):
    """Request to create a new chord set."""
    name: str
    qualities: List[ChordQuality] = []
    roots: List[str] = []
    voicing_types: List[VoicingType] = [VoicingType.CLOSE]
    difficulty: str = "medium"

class ChordSetUpdateRequest(BaseModel):
    """Request to update an existing chord set."""
    name: Optional[str] = None
    enabled: Optional[bool] = None
    qualities: Optional[List[ChordQuality]] = None
    roots: Optional[List[str]] = None
    voicing_types: Optional[List[VoicingType]] = None
    difficulty: Optional[str] = None

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

class PracticeSession(BaseModel):
    """A practice session record."""
    id: Optional[int] = None
    started_at: datetime = Field(default_factory=datetime.now)
    total_items: int = 0
    correct_items: int = 0
    mode: str # chords, scales, progression

class Config(BaseModel):
    """Global app config."""
    chord_sets: List[ChordSet] = []
    user_profile: UserProfile = Field(default_factory=UserProfile)
