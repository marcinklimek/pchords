mport asyncio
import time
import platform
import tkinter as tk
from tkinter import ttk
from typing import Optional, List
from pathlib import Path

from models import AppState, Config, ChordData
from utils import notes_names_to_index, index_to_note_name
from logger import get_logger

logger = get_logger(__name__)


class UIHandler:


    def __init__(self, config: Config, state: AppState):

        self.config = config
        self.state = state
        self.root: Optional[tk.Tk] = None
        self.canvas: Optional[tk.Canvas] = None
        self.img: Optional[tk.PhotoImage] = None
        
        # UI elements
        self.time_text: Optional[int] = None
        self.title_text: Optional[int] = None
        self.chord_lbl: Optional[int] = None
        self.chord_text: Optional[int] = None
        self.notes_lbl: Optional[int] = None
        self.notes_text: Optional[int] = None
        self.played_lbl: Optional[int] = None
        self.played_text: Optional[int] = None
        
        # State
        self.time_current = "-"
        self.current_chord: Optional[ChordData] = None
        self.notes_to_check: List[int] = []
        self._running = False
        self._tasks: List[asyncio.Task] = []

    async def start(self) -> None:

        try:
            await self._initialize_ui()
            self._running = True
            
            # Start update tasks
            self._tasks.append(asyncio.create_task(self._clock_update_loop()))
            self._tasks.append(asyncio.create_task(self._ui_update_loop()))
            
            logger.info("UI handler started")
            
        except Exception as e:
            logger.error(f"Failed to start UI handler: {e}")
            raise

    async def stop(self) -> None:

        self._running = False
        
        # Cancel all tasks
        for task in self._tasks:
            task.cancel()
        
        # Wait for tasks to complete
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        
        # Close UI
        if self.root:
            self.root.quit()
            self.root.destroy()
        
        logger.info("UI handler stopped")

    async def _initialize_ui(self) -> None:

        # Create main window
        self.root = tk.Tk(className="pchords")
        self.root.title(self.config.window_title)
        self.root.geometry(f'{self.config.window_width}x{self.config.window_height}')
        self.root.resizable(False, False)
        self.root.focus()
        
        # Set font size based on platform
        font_size = self.config.default_font_size
        if platform.system() == 'Darwin':
            font_size = self.config.macos_font_size
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.config.window_width,
            height=self.config.window_height
        )
        self.canvas.pack()
        
        # Load background image
        try:
            if self.config.paper_image.exists():
                self.img = tk.PhotoImage(file=str(self.config.paper_image))
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
            else:
                logger.warning(f"Background image not found: {self.config.paper_image}")
        except Exception as e:
            logger.error(f"Failed to load background image: {e}")
        
        # Create UI text elements
        self._create_text_elements()
        
        # Set up window close handler
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_text_elements(self) -> None:

        # Time display
        self.time_text = self.canvas.create_text(
            870, 40, fill="black", font="Segoe 25", 
            anchor=tk.SW, text=""
        )
        
        # Title
        self.title_text = self.canvas.create_text(
            160, 166, fill="black", font="Segoe 70", 
            anchor=tk.SW, text="PChord"
        )
        
        # Chord label and text
        self.chord_lbl = self.canvas.create_text(
            165, 411, fill="black", font="Segoe 45", 
            anchor=tk.SW, text="Chord"
        )
        self.chord_text = self.canvas.create_text(
            400, 411, fill="black", font="Segoe 45", 
            anchor=tk.SW, text="?"
        )
        
        # Notes label and text
        self.notes_lbl = self.canvas.create_text(
            165, 511, fill="black", font="Segoe 45", 
            anchor=tk.SW, text="Notes"
        )
        self.notes_text = self.canvas.create_text(
            400, 511, fill="black", font="Segoe 45", 
            anchor=tk.SW, text="[?, ?, ?, ?]"
        )
        
        # Played notes label and text
        self.played_lbl = self.canvas.create_text(
            165, 661, fill="black", font="Segoe 45", 
            anchor=tk.SW, text="Played"
        )
        self.played_text = self.canvas.create_text(
            400, 661, fill="black", font="Segoe 45", 
            anchor=tk.SW, text="[?, ?, ?, ?, ?, ?]"
        )

    def _on_closing(self) -> None:

        logger.info("UI window closing")
        asyncio.create_task(self.state.set_quit(True))

    async def _clock_update_loop(self) -> None:

        while self._running:
            try:
                time_str = time.strftime('%H:%M:%S')
                
                if time_str != self.time_current:
                    self.time_current = time_str
                    if self.canvas and self.time_text:
                        self.canvas.itemconfig(self.time_text, text=self.time_current)
                
                await asyncio.sleep(self.config.clock_update_interval / 1000.0)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in clock update loop: {e}")
                await asyncio.sleep(0.1)

    async def _ui_update_loop(self) -> None:

        while self._running:
            try:
                # Check if we should quit
                if await self.state.is_quit():
                    break
                
                # Update played notes display
                played_notes = await self.state.get_played_notes()
                await self._update_played_notes_display(played_notes)
                
                # Check if chord is completed
                if played_notes and self.notes_to_check:
                    if played_notes == self.notes_to_check:
                        logger.info("Chord completed!")
                        # Note: Chord generation should be handled by main application
                
                await asyncio.sleep(self.config.ui_update_interval / 1000.0)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in UI update loop: {e}")
                await asyncio.sleep(0.1)

    async def _update_played_notes_display(self, played_notes: List[int]) -> None:

        if not self.canvas or not self.played_text:
            return
        
        try:
            if played_notes and self.current_chord:
                # Convert indices to note names using current chord scale
                note_names = index_to_note_name(played_notes, self.current_chord.scale)
                display_text = str(note_names)
            else:
                display_text = ""
            
            self.canvas.itemconfig(self.played_text, text=display_text)
            
        except Exception as e:
            logger.error(f"Error updating played notes display: {e}")

    async def update_chord(self, chord: ChordData) -> None:

        try:
            self.current_chord = chord
            self.notes_to_check = notes_names_to_index(chord.notes)
            
            if self.canvas and self.chord_text and self.notes_text:
                self.canvas.itemconfig(self.chord_text, text=chord.name)
                self.canvas.itemconfig(self.notes_text, text=str(chord.notes))
            
            logger.info(f"Updated chord: {chord.name}")
            
        except Exception as e:
            logger.error(f"Error updating chord: {e}")

    def run_mainloop(self) -> None:

        if self.root:
            self.root.mainloop()
