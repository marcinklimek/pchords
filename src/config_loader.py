import json
from pathlib import Path
from typing import Optional

from models import Config
from validation import validate_config, ValidationError
from logger import get_logger

logger = get_logger(__name__)


def load_config(config_path: Optional[Path] = None) -> Config:

    if config_path is None:
        config_path = Path("config.json")
    
    try:
        if config_path.exists():
            logger.info(f"Loading configuration from {config_path}")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            config = validate_config(config_data)
            logger.info("Configuration loaded successfully")
            return config
        else:
            logger.info(f"Configuration file not found: {config_path}, using defaults")
            return Config()
            
    except (ValidationError, json.JSONDecodeError) as e:
        logger.error(f"Invalid configuration file {config_path}: {e}")
        logger.info("Using default configuration")
        return Config()
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        logger.info("Using default configuration")
        return Config()


def save_config(config: Config, config_path: Optional[Path] = None) -> None:

    if config_path is None:
        config_path = Path("config.json")
    
    try:
        config_data = {
            "window_width": config.window_width,
            "window_height": config.window_height,
            "window_title": config.window_title,
            "default_font_size": config.default_font_size,
            "macos_font_size": config.macos_font_size,
            "midi_poll_interval": config.midi_poll_interval,
            "midi_timeout": config.midi_timeout,
            "ui_update_interval": config.ui_update_interval,
            "clock_update_interval": config.clock_update_interval,
            "chords_file": str(config.chords_file),
            "paper_image": str(config.paper_image),
            "log_level": config.log_level.value,
            "log_file": str(config.log_file) if config.log_file else None,
            "chord_qualities": config.chord_qualities,
            "chord_scales": config.chord_scales
        }
        
        # Ensure directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
        
        logger.info(f"Configuration saved to {config_path}")
        
    except Exception as e:
        logger.error(f"Failed to save configuration: {e}")
        raise
