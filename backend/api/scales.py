"""
Scales API endpoints.
"""
from typing import List
from fastapi import APIRouter, HTTPException

from ..core.models import ScaleData, ScaleResponse, ChordData
from ..core.theory.notes import Note, NoteName
from ..core.theory.scales import Scale, ScaleType
from ..core.theory.chords import ChordQuality

router = APIRouter(prefix="/api/scales", tags=["scales"])

@router.get("/types", response_model=List[str])
async def get_scale_types():
    """Get available scale types."""
    return [s.value for s in ScaleType]

@router.get("/{root}/{scale_type}", response_model=ScaleResponse)
async def get_scale(root: str, scale_type: str):
    """
    Get scale data and diatonic chords.
    
    Args:
        root: Root note (e.g., C, F#)
        scale_type: Scale type (e.g., Major, Dorian)
    """
    try:
        # Validate inputs
        try:
            s_type = ScaleType(scale_type)
        except ValueError:
            # Try case insensitive matching
            found = False
            for s in ScaleType:
                if s.value.lower() == scale_type.lower():
                    s_type = s
                    found = True
                    break
            if not found:
                raise HTTPException(status_code=400, detail=f"Invalid scale type: {scale_type}")

        # Create scale
        root_note = Note(root, octave=4)
        scale = Scale(root_note, s_type)
        
        # Generate diatonic chords (currently only for Major)
        diatonic_chords = []
        if s_type == ScaleType.MAJOR:
            for i in range(1, 8):
                chord = scale.get_diatonic_chord(i, sevenths=True)
                diatonic_chords.append(
                    ChordData(
                        root=chord.root.name,
                        quality=chord.quality.value,
                        name=f"{chord.root.name}{chord.quality.value}",
                        notes=[n.name for n in chord.notes],
                        midi_notes=[n.midi for n in chord.notes],
                        scale_context=f"{root} {s_type.value} - Degree {i}"
                    )
                )
        
        return ScaleResponse(
            scale=ScaleData(
                root=root,
                type=s_type.value,
                name=f"{root} {s_type.value}",
                notes=[n.name for n in scale.notes],
                midi_notes=[n.midi for n in scale.notes]
            ),
            diatonic_chords=diatonic_chords
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
