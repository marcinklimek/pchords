"""
Utilities for note and MIDI conversion.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from pychord.constants.scales import SHARPED_SCALE, FLATTED_SCALE, SCALE_VAL_DICT

from .constants import NOTES_IN_OCTAVE


def get_key_by_value(elements: Dict[Any, Any], value_to_find: Any) -> Optional[Any]:
    """Find key by value in a dictionary."""
    for key, value in elements.items():
        if value == value_to_find:
            return key
    return None


def midi_to_note(number: int) -> Tuple[int, int]:
    """
    Convert MIDI note number to note and octave.

    Args:
        number: MIDI note number (0-127)

    Returns:
        Tuple of (note_index, octave)

    Reference: http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm
    """
    octave = number // NOTES_IN_OCTAVE
    note = number % NOTES_IN_OCTAVE
    return note, octave


def notes_names_to_index(notes: List[str]) -> List[int]:
    """
    Convert note names to note indices.

    Args:
        notes: List of note names (e.g., ['C', 'E', 'G'])

    Returns:
        List of note indices (0-11)
    """
    conv_notes = []
    for item in notes:
        index = get_key_by_value(SHARPED_SCALE, item)
        if index is not None:
            conv_notes.append(index)
        else:
            index = get_key_by_value(FLATTED_SCALE, item)
            if index is not None:
                conv_notes.append(index)
    return conv_notes


def index_to_note_name(notes: List[int], scale: str) -> List[str]:
    """
    Convert note indices to note names based on scale.

    Args:
        notes: List of note indices (0-11)
        scale: Scale type (e.g., 'maj', 'min')

    Returns:
        List of note names
    """
    if scale not in SCALE_VAL_DICT:
        return []

    scale_notes = SCALE_VAL_DICT[scale]
    conv_notes = []

    for item in notes:
        if 0 <= item < len(scale_notes):
            conv_notes.append(scale_notes[item])

    return conv_notes


def midi_to_index(notes: List[int]) -> List[int]:
    """
    Convert MIDI note numbers to note indices (0-11).

    Args:
        notes: List of MIDI note numbers

    Returns:
        List of note indices
    """
    conv_notes = []
    for item in notes:
        note_index, _ = midi_to_note(item)
        conv_notes.append(note_index)

    return conv_notes


def note_name_to_midi(note_name: str, octave: int = 2) -> int:
    """
    Convert note name to MIDI note number.

    Args:
        note_name: Note name (e.g., 'C', 'D#', 'Eb')
        octave: Octave number (default 2 for left hand bass notes)

    Returns:
        MIDI note number (e.g., C2 = 36, C3 = 48)
    """
    # Get note index from sharped or flatted scale
    note_index = get_key_by_value(SHARPED_SCALE, note_name)
    if note_index is None:
        note_index = get_key_by_value(FLATTED_SCALE, note_name)

    if note_index is None:
        # Fallback to C if note not found
        note_index = 0

    # Convert to MIDI number: octave * 12 + note_index + 12 (MIDI offset)
    # C2 = 2*12 + 0 + 12 = 36
    # C3 = 3*12 + 0 + 12 = 48
    midi_number = octave * 12 + note_index + 12

    return midi_number


def save_json(file_path: Path, file_content: Any) -> None:
    """
    Save content to JSON file.

    Args:
        file_path: Path to save to
        file_content: Content to save
    """
    # Ensure directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(file_content, f, ensure_ascii=False, indent=2)


def load_json(file_path: Path) -> Any:
    """
    Load content from JSON file.

    Args:
        file_path: Path to load from

    Returns:
        Loaded content or empty list if file doesn't exist
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in {file_path}")
