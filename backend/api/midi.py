"""
MIDI WebSocket endpoint for real-time communication.
"""

from typing import List, Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import asyncio

from ..core.models import MidiMessage, MidiStatus


router = APIRouter(prefix="/ws", tags=["websocket"])


class ConnectionManager:
    """Manages WebSocket connections."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.midi_state: Dict[str, any] = {
            "played_notes": [],
            "connected": False,
            "input_ports": []
        }

    async def connect(self, websocket: WebSocket):
        """Accept and store a new connection."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove a connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific client."""
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients."""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # Connection might be closed
                pass

    def update_midi_state(self, played_notes: List[int]):
        """Update the MIDI state."""
        self.midi_state["played_notes"] = played_notes

    def get_midi_state(self) -> dict:
        """Get current MIDI state."""
        return self.midi_state.copy()


# Global connection manager
manager = ConnectionManager()


@router.websocket("/midi")
async def midi_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for MIDI communication.

    The client will send MIDI events and receive state updates.

    Message format from client:
    {
        "type": "midi_event",
        "note": 60,
        "velocity": 100,
        "timestamp": 1234567890.123
    }

    Or for status updates:
    {
        "type": "status",
        "connected": true,
        "input_ports": ["Piano 1", "Piano 2"]
    }

    Message format to client:
    {
        "type": "state_update",
        "played_notes": [60, 64, 67]
    }
    """
    await manager.connect(websocket)

    try:
        # Send initial state
        await manager.send_personal_message(
            {
                "type": "state_update",
                "data": manager.get_midi_state()
            },
            websocket
        )

        # Listen for messages
        while True:
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
                message_type = message.get("type")

                if message_type == "midi_event":
                    # Handle MIDI event
                    note = message.get("note")
                    velocity = message.get("velocity", 0)

                    # Update played notes
                    current_notes = manager.midi_state["played_notes"]

                    if velocity > 0 and note not in current_notes:
                        # Note on
                        current_notes.append(note)
                        current_notes.sort()
                    elif velocity == 0 and note in current_notes:
                        # Note off
                        current_notes.remove(note)

                    manager.update_midi_state(current_notes)

                    # Broadcast to all clients
                    await manager.broadcast({
                        "type": "state_update",
                        "data": manager.get_midi_state()
                    })

                elif message_type == "status":
                    # Update connection status
                    manager.midi_state["connected"] = message.get("connected", False)
                    manager.midi_state["input_ports"] = message.get("input_ports", [])

                    # Broadcast status update
                    await manager.broadcast({
                        "type": "status_update",
                        "data": {
                            "connected": manager.midi_state["connected"],
                            "input_ports": manager.midi_state["input_ports"]
                        }
                    })

                elif message_type == "ping":
                    # Respond to ping
                    await manager.send_personal_message(
                        {"type": "pong"},
                        websocket
                    )

            except json.JSONDecodeError:
                # Invalid JSON
                await manager.send_personal_message(
                    {"type": "error", "message": "Invalid JSON"},
                    websocket
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # Broadcast disconnection if this was the last client
        if len(manager.active_connections) == 0:
            manager.midi_state["connected"] = False
            manager.midi_state["played_notes"] = []

    except Exception as e:
        manager.disconnect(websocket)
        print(f"WebSocket error: {e}")


@router.get("/midi/status", response_model=MidiStatus)
async def get_midi_status():
    """
    Get current MIDI status.

    Returns:
        MidiStatus with connection info and played notes
    """
    state = manager.get_midi_state()
    return MidiStatus(
        connected=state["connected"],
        input_ports=state["input_ports"],
        played_notes=state["played_notes"]
    )
