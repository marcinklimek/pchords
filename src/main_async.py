import asyncio
import signal
import sys
from pathlib import Path
from typing import Optional

from models import AppState, Config
from generator import Generator
from midi_handler import MidiHandler
from ui_handler import UIHandler
from logger import setup_logging, get_logger
from config_loader import load_config

logger = get_logger(__name__)


class PChordsApp:


    def __init__(self, config: Optional[Config] = None):

        self.config = config or load_config()
        self.state = AppState()
        self.generator: Optional[Generator] = None
        self.midi_handler: Optional[MidiHandler] = None
        self.ui_handler: Optional[UIHandler] = None
        self._running = False

    async def start(self) -> None:

        try:
            # Setup logging
            setup_logging(self.config)
            logger.info("Starting PChords application")
            
            # Initialize components
            self.generator = Generator(self.config)
            self.midi_handler = MidiHandler(self.config, self.state)
            self.ui_handler = UIHandler(self.config, self.state)

            # Start handlers
            await self.generator.start()
            await self.midi_handler.start()
            await self.ui_handler.start()
            
            self._running = True
            logger.info("PChords application started successfully")
            
            # Start main application loop
            await self._main_loop()
            
        except Exception as e:
            logger.error(f"Failed to start application: {e}")
            raise

    async def stop(self) -> None:

        logger.info("Stopping PChords application")
        self._running = False
        
        # Set quit flag
        await self.state.set_quit(True)
        
        # Stop handlers
        if self.midi_handler:
            await self.midi_handler.stop()
        
        if self.ui_handler:
            await self.ui_handler.stop()
        
        logger.info("PChords application stopped")

    async def _main_loop(self) -> None:

        try:
            # Get initial chord
            if self.generator:
                initial_chord = await self.generator.get()
                await self.ui_handler.update_chord(initial_chord)
            
            # Main loop
            while self._running and not await self.state.is_quit():
                try:
                    # Check if current chord is completed
                    played_notes = await self.state.get_played_notes()
                    if played_notes and self.ui_handler.notes_to_check:
                        if played_notes == self.ui_handler.notes_to_check:
                            logger.info("Chord completed! Getting next chord...")
                            
                            # Get next chord
                            if self.generator:
                                next_chord = await self.generator.get()
                                await self.ui_handler.update_chord(next_chord)
                    
                    # Small delay to prevent excessive CPU usage
                    await asyncio.sleep(0.1)
                    
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
                    await asyncio.sleep(0.1)
                    
        except Exception as e:
            logger.error(f"Fatal error in main loop: {e}")
            raise

    def run_ui_mainloop(self) -> None:

        if self.ui_handler:
            self.ui_handler.run_mainloop()


async def main():
    """
    Main entry point.
    """
    app = None
    try:
        # Create application
        app = PChordsApp()
        
        # Setup signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down...")
            if app:
                asyncio.create_task(app.stop())
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start application
        await app.start()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)
    finally:
        if app:
            await app.stop()


def run_application():
    """
    Run the application with proper thread handling for tkinter.
    """
    try:
        # Run the async main function
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Failed to run application: {e}")
        sys.exit(1)


if __name__ == '__main__':
    run_application()
