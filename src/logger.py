import logging
import sys
from pathlib import Path
from typing import Optional
from models import LogLevel, Config


def setup_logging(config: Config) -> logging.Logger:

    # Create logger
    logger = logging.getLogger("pchords")
    logger.setLevel(getattr(logging, config.log_level.value))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, config.log_level.value))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if config.log_file:
        try:
            # Ensure log directory exists
            config.log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(config.log_file, encoding='utf-8')
            file_handler.setLevel(getattr(logging, config.log_level.value))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Failed to setup file logging: {e}")
    
    return logger


def get_logger(name: str = "pchords") -> logging.Logger:
    return logging.getLogger(name)
