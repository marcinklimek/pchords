import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from pychord.constants.scales import SHARPED_SCALE, FLATTED_SCALE, SCALE_VAL_DICT
from constants import NOTES_IN_OCTAVE
from logger import get_logger

logger = get_logger(__name__)


def get_key_by_value(elements: Dict[Any, Any], value_to_find: Any) -> Optional[Any]:

    for key, value in elements.items():
        if value == value_to_find:
            return key
    return None


def midi_to_note(number: int) -> Tuple[int, int]:
    """
    Convert MIDI note number to note and octave.
    
    Reference: http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm
    """
    octave = number // NOTES_IN_OCTAVE
    note = number % NOTES_IN_OCTAVE
    return note, octave


def notes_names_to_index(notes: List[str]) -> List[int]:

    conv_notes = []
    for item in notes:
        index = get_key_by_value(SHARPED_SCALE, item)
        if index is not None:
            conv_notes.append(index)
        else:
            index = get_key_by_value(FLATTED_SCALE, item)
            if index is not None:
                conv_notes.append(index)
            else:
                logger.warning(f"Unknown note name: {item}")
    
    return conv_notes


def index_to_note_name(notes: List[int], scale: str) -> List[str]:

    if scale not in SCALE_VAL_DICT:
        logger.error(f"Unknown scale: {scale}")
        return []
    
    scale_notes = SCALE_VAL_DICT[scale]
    conv_notes = []
    
    for item in notes:
        if 0 <= item < len(scale_notes):
            conv_notes.append(scale_notes[item])
        else:
            logger.warning(f"Invalid note index: {item}")
    
    return conv_notes


def midi_to_index(notes: List[int]) -> List[int]:

    conv_notes = []
    for item in notes:
        note_index, _ = midi_to_note(item)
        conv_notes.append(note_index)
    
    return conv_notes


def save_json(file_path: Path, file_content: Any) -> None:

    try:
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(file_content, f, ensure_ascii=False, indent=4)
        
        logger.debug(f"Saved JSON to {file_path}")
        
    except Exception as e:
        logger.error(f"Failed to save JSON to {file_path}: {e}")
        raise


def load_json(file_path: Path) -> Any:

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.debug(f"Loaded JSON from {file_path}")
        return data
        
    except FileNotFoundError:
        logger.warning(f"JSON file not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to load JSON from {file_path}: {e}")
        raise
