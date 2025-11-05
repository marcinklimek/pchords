# 🎹 PChords Web - Piano Chord Practice Tool

Modern web-based piano chord practice application with real-time MIDI support.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal.svg)

## 🚀 Features

### Core Features
- 🎵 **Random Chord Generation** - Practice various chord types and inversions
- 🎹 **Real-time MIDI Input** - Connect your MIDI keyboard for instant feedback
- ✅ **Auto-validation** - Automatic chord recognition and progression
- 📊 **Visual Feedback** - Interactive piano keyboard with note highlighting
- ⚙️ **Customizable Practice** - Configure chord sets, qualities, and difficulties

### Modern Web Interface
- 🌐 **Web-based** - No installation required, works in browser
- 🎨 **Beautiful UI** - Modern dark theme with smooth animations
- 📱 **Responsive** - Works on desktop and tablet
- ⚡ **Fast** - Built with Vite for lightning-fast performance
- 🔌 **WebMIDI** - Direct MIDI input in browser (Chrome/Edge)

## 📋 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend                           │
│  React + TypeScript + Vite + TailwindCSS               │
│  - Interactive Piano Keyboard (react-piano)            │
│  - Real-time MIDI (Web MIDI API)                       │
│  - TanStack Query (API integration)                    │
└─────────────────┬───────────────────────────────────────┘
                  │
                  │ HTTP/REST + WebSocket
                  │
┌─────────────────▼───────────────────────────────────────┐
│                      Backend                            │
│  FastAPI + Python 3.11+                                │
│  - REST API (chord management)                         │
│  - WebSocket (real-time updates)                       │
│  - pychord (music theory)                              │
│  - SQLite (statistics - future)                        │
└─────────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **pychord** - Music theory and chord generation
- **SQLAlchemy** - Database ORM (for future features)
- **Pydantic** - Data validation
- **uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **TailwindCSS** - Utility-first CSS
- **TanStack Query** - Server state management
- **react-piano** - Piano keyboard component
- **Web MIDI API** - Browser MIDI support

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn
- MIDI keyboard (optional)

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/marcinklimek/pchords.git
cd pchords
```

#### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

#### 3. Frontend Setup
```bash
cd frontend
npm install
```

### Running the Application

#### Start Backend (Terminal 1)
```bash
cd backend
python -m uvicorn backend.main:app --reload --port 8000
```

Backend will be available at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

#### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

### Using Docker (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Access the application
open http://localhost:5173
```

## 📖 Usage

### Basic Practice Flow

1. **Open the App** - Navigate to http://localhost:5173
2. **Connect MIDI** - Connect your MIDI keyboard (grant browser permission)
3. **Start Practicing** - A random chord will be displayed
4. **Play the Chord** - Play the notes on your keyboard
5. **Auto-advance** - When correct, automatically moves to next chord
6. **Repeat** - Keep practicing!

### Chord Sets

The app comes with default chord sets:

- **Beginners** - Basic major/minor chords (root position)
- **Jazz - 9th Chords** - M9, m9 with inversions (from 3rd, from 7th)
- **Jazz - Altered** - Advanced altered dominants (7#9#5, 7b9b5)

Configure these in Settings or via API.

### Without MIDI Keyboard

You can still use the app without a physical MIDI keyboard:
- Use computer keyboard (home row keys)
- Click piano keys with mouse
- Great for learning and visualization

## 🔧 Configuration

### Backend Configuration

Edit `backend/main.py` to modify default chord sets:

```python
DEFAULT_CHORD_SETS = [
    ChordSet(
        id="my_custom_set",
        name="My Custom Chords",
        enabled=True,
        qualities=["M7", "m7", "7"],
        scales=["maj", "min"],
        inversions=["root", "first", "second"],
        difficulty="medium"
    ),
]
```

### Frontend Configuration

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

## 📡 API Documentation

### REST Endpoints

```
GET  /api/chords/next           # Get next chord
GET  /api/chords/sets           # List chord sets
POST /api/chords/sets           # Create chord set
GET  /api/chords/sets/{id}      # Get chord set
PUT  /api/chords/sets/{id}      # Update chord set
DELETE /api/chords/sets/{id}    # Delete chord set
POST /api/chords/regenerate     # Regenerate all chords
```

### WebSocket

```
WS /ws/midi                     # Real-time MIDI events
GET /ws/midi/status             # MIDI status
```

Full API documentation: http://localhost:8000/docs

## 🏗️ Project Structure

```
pchords/
├── backend/                    # FastAPI backend
│   ├── api/                   # API endpoints
│   │   ├── chords.py         # Chord management
│   │   └── midi.py           # MIDI WebSocket
│   ├── core/                 # Business logic
│   │   ├── models.py         # Data models
│   │   └── generator.py      # Chord generation
│   ├── utils/                # Utilities
│   │   ├── constants.py      # Musical constants
│   │   └── converters.py     # Note conversion
│   ├── main.py               # FastAPI app
│   └── requirements.txt      # Python dependencies
│
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── hooks/            # Custom hooks
│   │   ├── services/         # API & MIDI services
│   │   ├── types/            # TypeScript types
│   │   └── App.tsx           # Main component
│   ├── package.json          # Node dependencies
│   └── vite.config.ts        # Vite config
│
├── src/                       # Original Python/Tkinter app
├── docker-compose.yml        # Docker setup
└── README_WEB.md             # This file
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Build

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## 🎯 Roadmap

### Planned Features
- [ ] **Statistics Dashboard** - Track practice sessions and progress
- [ ] **User Accounts** - Save progress and preferences
- [ ] **Custom Chord Editor** - Define your own chord sequences
- [ ] **Practice Modes** - Timed challenges, progression exercises
- [ ] **Audio Playback** - Hear chords before playing
- [ ] **Mobile Support** - iOS/Android apps
- [ ] **Metronome** - Practice with timing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **pychord** - Python chord library
- **react-piano** - Piano keyboard component
- **FastAPI** - Modern Python web framework
- **Web MIDI API** - Browser MIDI specification

## 📧 Contact

Marcin Klimek - [GitHub](https://github.com/marcinklimek)

Project Link: [https://github.com/marcinklimek/pchords](https://github.com/marcinklimek/pchords)

---

**Happy Practicing! 🎹🎵**
