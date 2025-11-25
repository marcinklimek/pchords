"""
Chord API endpoints.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends

from ..core.models import (
    ChordData,
    ChordSet,
    ChordResponse,
    ChordSetCreateRequest,
    ChordSetUpdateRequest
)
from ..core.generator import ChordGenerator

router = APIRouter(prefix="/api/chords", tags=["chords"])

# Global state (will be replaced with dependency injection in production)
_generator: ChordGenerator = None
_chord_sets: List[ChordSet] = []

def get_generator() -> ChordGenerator:
    """Get the global chord generator."""
    global _generator
    if _generator is None:
        raise HTTPException(status_code=500, detail="Generator not initialized")
    return _generator

async def init_generator(chord_sets: List[ChordSet]):
    """Initialize the chord generator."""
    global _generator, _chord_sets
    _chord_sets = chord_sets
    _generator = ChordGenerator(chord_sets)
    await _generator.start()

@router.get("/next", response_model=ChordResponse)
async def get_next_chord(generator: ChordGenerator = Depends(get_generator)):
    """Get the next random chord to practice."""
    chord = await generator.get_next()
    remaining = await generator.get_remaining_count()
    return ChordResponse(chord=chord, remaining=remaining)

@router.get("/sets", response_model=List[ChordSet])
async def get_chord_sets():
    """Get all chord sets."""
    return _chord_sets

@router.post("/sets", response_model=ChordSet)
async def create_chord_set(request: ChordSetCreateRequest):
    """Create a new chord set."""
    chord_set_id = request.name.lower().replace(" ", "_")

    if any(cs.id == chord_set_id for cs in _chord_sets):
        raise HTTPException(status_code=400, detail="Chord set with this name already exists")

    new_set = ChordSet(
        id=chord_set_id,
        name=request.name,
        enabled=True,
        qualities=request.qualities,
        roots=request.roots,
        voicing_types=request.voicing_types,
        difficulty=request.difficulty
    )

    _chord_sets.append(new_set)
    await init_generator(_chord_sets)
    return new_set

@router.get("/sets/{set_id}", response_model=ChordSet)
async def get_chord_set(set_id: str):
    """Get a specific chord set."""
    for chord_set in _chord_sets:
        if chord_set.id == set_id:
            return chord_set
    raise HTTPException(status_code=404, detail="Chord set not found")

@router.put("/sets/{set_id}", response_model=ChordSet)
async def update_chord_set(set_id: str, request: ChordSetUpdateRequest):
    """Update a chord set."""
    for i, chord_set in enumerate(_chord_sets):
        if chord_set.id == set_id:
            if request.name is not None:
                chord_set.name = request.name
            if request.enabled is not None:
                chord_set.enabled = request.enabled
            if request.qualities is not None:
                chord_set.qualities = request.qualities
            if request.roots is not None:
                chord_set.roots = request.roots
            if request.voicing_types is not None:
                chord_set.voicing_types = request.voicing_types
            if request.difficulty is not None:
                chord_set.difficulty = request.difficulty

            _chord_sets[i] = chord_set
            await init_generator(_chord_sets)
            return chord_set

    raise HTTPException(status_code=404, detail="Chord set not found")

@router.delete("/sets/{set_id}")
async def delete_chord_set(set_id: str):
    """Delete a chord set."""
    global _chord_sets
    _chord_sets = [cs for cs in _chord_sets if cs.id != set_id]
    await init_generator(_chord_sets)
    return {"message": "Chord set deleted successfully"}

@router.post("/regenerate")
async def regenerate_chords(generator: ChordGenerator = Depends(get_generator)):
    """Regenerate all chords."""
    await generator.regenerate()
    remaining = await generator.get_remaining_count()
    return {"message": "Chords regenerated successfully", "count": remaining}
