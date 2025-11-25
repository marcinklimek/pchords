"""
Progressions API endpoints.
"""
from typing import List
from fastapi import APIRouter, HTTPException

from ..core.models import ProgressionData, ProgressionStep, ChordData
from ..core.theory.notes import Note
from ..core.theory.scales import Scale, ScaleType
from ..core.theory.chords import ChordQuality

router = APIRouter(prefix="/api/progressions", tags=["progressions"])

# Hardcoded progressions for now
PROGRESSIONS = [
    {
        "id": "ii-v-i-major",
        "name": "II-V-I (Major)",
        "degrees": ["ii", "V", "I"],
        "qualities": [ChordQuality.MINOR_7, ChordQuality.DOMINANT_7, ChordQuality.MAJOR_7]
    },
    {
        "id": "i-vi-ii-v",
        "name": "I-vi-ii-V (Turnaround)",
        "degrees": ["I", "vi", "ii", "V"],
        "qualities": [ChordQuality.MAJOR_7, ChordQuality.MINOR_7, ChordQuality.MINOR_7, ChordQuality.DOMINANT_7]
    }
]

@router.get("/templates", response_model=List[dict])
async def get_progression_templates():
    """Get available progression templates."""
    return PROGRESSIONS

@router.post("/generate", response_model=ProgressionData)
async def generate_progression(template_id: str, key: str, scale_type: str = "Major"):
    """
    Generate a progression in a specific key.
    """
    template = next((p for p in PROGRESSIONS if p["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    try:
        root_note = Note(key, octave=4)
        scale = Scale(root_note, ScaleType(scale_type))
        
        steps = []
        for i, degree_str in enumerate(template["degrees"]):
            # Map roman numerals to scale degrees (simplified)
            degree_map = {"I": 1, "ii": 2, "iii": 3, "IV": 4, "V": 5, "vi": 6, "vii": 7}
            degree_idx = degree_map.get(degree_str, 1)
            
            # Get root note for this degree
            # Note: Scale notes are 0-indexed
            step_root = scale.notes[degree_idx - 1]
            quality = template["qualities"][i]
            
            # Create chord
            # TODO: Add voicing logic here
            chord_name = f"{step_root.name}{quality.value}"
            
            # Generate basic notes for now
            # In real implementation, use Chord class
            from ..core.theory.chords import Chord
            chord_obj = Chord(step_root, quality)
            
            chord_data = ChordData(
                root=step_root.name,
                quality=quality.value,
                name=chord_name,
                notes=[n.name for n in chord_obj.notes],
                midi_notes=[n.midi for n in chord_obj.notes],
                scale_context=f"{key} {scale_type}"
            )
            
            steps.append(ProgressionStep(
                degree=degree_str,
                chord=chord_data,
                duration_beats=4
            ))
            
        return ProgressionData(
            id=f"{template_id}-{key}",
            name=f"{template['name']} in {key}",
            key=key,
            scale_type=scale_type,
            steps=steps
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
