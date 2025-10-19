from typing import List, Any, Optional, Union
from pathlib import Path
import json
from models import ChordData, Config
from constants import SCALES_LIST, QUALITIES, NOTES_IN_OCTAVE
from logger import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_midi_note(note: int) -> bool:

    return isinstance(note, int) and 0 <= note <= 127


def validate_note_name(note: str) -> bool:

    if not isinstance(note, str):
        return False
    
    # Check if note is in the scales list
    return note in SCALES_LIST


def validate_chord_quality(quality: str) -> bool:

    return isinstance(quality, str) and quality in QUALITIES


def validate_scale(scale: str) -> bool:

    valid_scales = ['maj', 'min', 'major', 'minor']
    return isinstance(scale, str) and scale.lower() in valid_scales


def validate_chord_data(chord_data: Any) -> ChordData:

    if not isinstance(chord_data, (list, dict)):
        raise ValidationError(f"Chord data must be list or dict, got {type(chord_data)}")
    
    try:
        if isinstance(chord_data, list):
            if len(chord_data) < 3:
                raise ValidationError("Chord data list must have at least 3 elements")
            
            root, name, notes = chord_data[0], chord_data[1], chord_data[2]
            scale = chord_data[3] if len(chord_data) > 3 else ""
        else:
            root = chord_data.get('root', '')
            name = chord_data.get('name', '')
            notes = chord_data.get('notes', [])
            scale = chord_data.get('scale', '')
        
        # Validate root note
        if not validate_note_name(root):
            raise ValidationError(f"Invalid root note: {root}")
        
        # Validate notes list
        if not isinstance(notes, list):
            raise ValidationError("Notes must be a list")
        
        for note in notes:
            if not validate_note_name(note):
                raise ValidationError(f"Invalid note in chord: {note}")
        
        # Validate scale if provided
        if scale and not validate_scale(scale):
            raise ValidationError(f"Invalid scale: {scale}")
        
        return ChordData(root=root, name=name, notes=notes, scale=scale)
        
    except (IndexError, KeyError, TypeError) as e:
        raise ValidationError(f"Invalid chord data structure: {e}")


def validate_file_path(file_path: Union[str, Path], must_exist: bool = False) -> Path:

    try:
        path = Path(file_path)
        
        if must_exist and not path.exists():
            raise ValidationError(f"File does not exist: {path}")
        
        return path
        
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Invalid file path: {e}")


def validate_json_file(file_path: Union[str, Path]) -> Any:
 
    try:
        path = validate_file_path(file_path, must_exist=True)
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data
        
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON in file {file_path}: {e}")
    except Exception as e:
        raise ValidationError(f"Failed to read JSON file {file_path}: {e}")


def validate_config(config_data: dict) -> Config:
 
    try:
        # Validate window settings
        window_width = config_data.get('window_width', 998)
        window_height = config_data.get('window_height', 800)
        
        if not isinstance(window_width, int) or window_width <= 0:
            raise ValidationError("window_width must be a positive integer")
        
        if not isinstance(window_height, int) or window_height <= 0:
            raise ValidationError("window_height must be a positive integer")
        
        # Validate file paths
        chords_file = Path(config_data.get('chords_file', 'chords.json'))
        paper_image = Path(config_data.get('paper_image', 'bin/paper.png'))
        
        # Validate log level
        log_level_str = config_data.get('log_level', 'INFO')
        try:
            from models import LogLevel
            log_level = LogLevel(log_level_str.upper())
        except ValueError:
            raise ValidationError(f"Invalid log level: {log_level_str}")
        
        # Validate chord qualities
        chord_qualities = config_data.get('chord_qualities', ['M9', 'm9'])
        if not isinstance(chord_qualities, list):
            raise ValidationError("chord_qualities must be a list")
        
        for quality in chord_qualities:
            if not validate_chord_quality(quality):
                raise ValidationError(f"Invalid chord quality: {quality}")
        
        return Config(
            window_width=window_width,
            window_height=window_height,
            window_title=config_data.get('window_title', 'PChords'),
            default_font_size=config_data.get('default_font_size', 9),
            macos_font_size=config_data.get('macos_font_size', 7),
            midi_poll_interval=config_data.get('midi_poll_interval', 0.1),
            midi_timeout=config_data.get('midi_timeout', 5.0),
            ui_update_interval=config_data.get('ui_update_interval', 100),
            clock_update_interval=config_data.get('clock_update_interval', 200),
            chords_file=chords_file,
            paper_image=paper_image,
            log_level=log_level,
            log_file=Path(config_data['log_file']) if config_data.get('log_file') else None,
            chord_qualities=chord_qualities,
            chord_scales=config_data.get('chord_scales', ['maj', 'min'])
        )
        
    except Exception as e:
        raise ValidationError(f"Configuration validation failed: {e}")


def validate_played_notes(notes: List[int]) -> List[int]:

    if not isinstance(notes, list):
        raise ValidationError("Played notes must be a list")
    
    validated_notes = []
    for note in notes:
        if not validate_midi_note(note):
            logger.warning(f"Invalid MIDI note ignored: {note}")
            continue
        validated_notes.append(note)
    
    return validated_notes
