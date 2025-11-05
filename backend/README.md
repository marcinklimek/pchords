# PChords Backend

FastAPI backend for PChords - Piano Chord Practice Tool.

## Features

- 🎵 REST API for chord management
- 🔌 WebSocket for real-time MIDI communication
- 📊 Chord set configuration and management
- 🎹 Support for multiple chord types and inversions

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Running the Server

```bash
# Development mode (with auto-reload)
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Or using the script
python -m backend.main
```

The server will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Chords

- `GET /api/chords/next` - Get next random chord
- `GET /api/chords/sets` - List all chord sets
- `POST /api/chords/sets` - Create new chord set
- `GET /api/chords/sets/{id}` - Get specific chord set
- `PUT /api/chords/sets/{id}` - Update chord set
- `DELETE /api/chords/sets/{id}` - Delete chord set
- `POST /api/chords/regenerate` - Regenerate all chords

### MIDI

- `WS /ws/midi` - WebSocket for real-time MIDI events
- `GET /ws/midi/status` - Get current MIDI status

## WebSocket Protocol

### Client → Server

```json
{
  "type": "midi_event",
  "note": 60,
  "velocity": 100,
  "timestamp": 1234567890.123
}
```

### Server → Client

```json
{
  "type": "state_update",
  "data": {
    "played_notes": [60, 64, 67],
    "connected": true
  }
}
```

## Project Structure

```
backend/
├── api/
│   ├── chords.py       # Chord endpoints
│   └── midi.py         # MIDI WebSocket
├── core/
│   ├── models.py       # Pydantic models
│   └── generator.py    # Chord generation logic
├── utils/
│   ├── constants.py    # Musical constants
│   └── converters.py   # Note conversion utilities
├── main.py             # FastAPI application
└── requirements.txt    # Dependencies
```

## Default Chord Sets

1. **Beginners** - Basic major and minor chords
2. **Jazz - 9th Chords** - M9, m9 chords with inversions
3. **Jazz - Altered** - Altered dominant chords (disabled by default)

## Development

```bash
# Run tests
pytest

# Format code
black backend/

# Type checking
mypy backend/
```
