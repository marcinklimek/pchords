import asyncio
import time
from typing import List, Optional, Callable, Any
import mido
from mido.ports import multi_receive
import rtmidi

from models import AppState, MidiMessage, Config
from validation import validate_played_notes, ValidationError
from logger import get_logger

logger = get_logger(__name__)


class MidiHandler:

    def __init__(self, config: Config, state: AppState):

        self.config = config
        self.state = state
        self.ports: List[mido.ports.BaseInput] = []
        self.played_notes: List[int] = []
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self) -> None:

        try:
            await self._initialize_ports()
            if self.ports:
                self._running = True
                self._task = asyncio.create_task(self._midi_loop())
                logger.info(f"MIDI handler started with {len(self.ports)} ports")
            else:
                logger.warning("No MIDI ports available")
        except Exception as e:
            logger.error(f"Failed to start MIDI handler: {e}")
            raise

    async def stop(self) -> None:

        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        # Close all ports
        for port in self.ports:
            try:
                port.close()
            except Exception as e:
                logger.warning(f"Error closing MIDI port: {e}")
        
        self.ports.clear()
        logger.info("MIDI handler stopped")

    async def _initialize_ports(self) -> None:

        try:
            midi_in = rtmidi.MidiIn()
            port_names = midi_in.get_ports()
            
            logger.info(f"Available MIDI ports: {port_names}")
            
            if not port_names:
                logger.warning("No MIDI input ports found")
                return
            
            # Open all available input ports
            for name in port_names:
                try:
                    port = mido.open_input(name)
                    self.ports.append(port)
                    logger.info(f"Opened MIDI port: {name}")
                except Exception as e:
                    logger.error(f"Failed to open MIDI port {name}: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to initialize MIDI: {e}")
            raise

    async def _midi_loop(self) -> None:

        while self._running:
            try:
                # Process MIDI messages
                for message in multi_receive(self.ports, block=False):
                    await self._process_message(message)
                
                # Update state with current played notes
                if self.played_notes:
                    validated_notes = validate_played_notes(self.played_notes)
                    await self.state.update_played_notes(validated_notes)
                else:
                    await self.state.update_played_notes([])
                
                # Small delay to prevent excessive CPU usage
                await asyncio.sleep(self.config.midi_poll_interval)
                
            except Exception as e:
                logger.error(f"Error in MIDI loop: {e}")
                await asyncio.sleep(0.1)  # Brief pause before retrying

    async def _process_message(self, message: mido.Message) -> None:

        try:
            if message.type == "note_on" and message.velocity > 0:
                # Note pressed
                if message.note not in self.played_notes:
                    self.played_notes.append(message.note)
                    self.played_notes.sort()
                    logger.debug(f"Note on: {message.note}")
                    
            elif message.type == "note_off" or (message.type == "note_on" and message.velocity == 0):
                # Note released
                if message.note in self.played_notes:
                    self.played_notes.remove(message.note)
                    logger.debug(f"Note off: {message.note}")
                    
        except Exception as e:
            logger.error(f"Error processing MIDI message: {e}")

    def get_played_notes(self) -> List[int]:

        return self.played_notes.copy()

    def is_running(self) -> bool:

        return self._running
