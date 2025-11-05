# PChords Frontend

Modern web interface for PChords - Piano Chord Practice Tool.

Built with React, TypeScript, and Vite.

## Features

- 🎹 Interactive piano keyboard visualization
- 🎵 Real-time MIDI input using Web MIDI API
- 🎨 Modern dark-themed UI with TailwindCSS
- ⚡ Fast development with Vite
- 📱 Responsive design
- ✨ Visual feedback for correct/incorrect notes

## Prerequisites

- Node.js 18+ and npm
- A modern browser with Web MIDI API support (Chrome, Edge, Opera)
- MIDI keyboard (optional - can use computer keyboard)

## Installation

```bash
# Install dependencies
npm install
```

## Development

```bash
# Start dev server
npm run dev
```

The app will be available at http://localhost:5173

## Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Piano/
│   │   │   ├── PianoKeyboard.tsx      # Interactive keyboard
│   │   │   ├── MidiStatus.tsx         # MIDI connection status
│   │   │   └── PianoKeyboard.css      # Piano styles
│   │   ├── ChordDisplay/
│   │   │   ├── CurrentChord.tsx       # Shows current chord
│   │   │   └── PlayedNotes.tsx        # Shows played notes
│   │   └── Layout/
│   │       └── Header.tsx             # App header
│   ├── hooks/
│   │   ├── useMidi.ts                 # Web MIDI hook
│   │   └── useChords.ts               # Chord management hook
│   ├── services/
│   │   ├── api.ts                     # Backend API client
│   │   └── midi.ts                    # MIDI service
│   ├── types/
│   │   ├── chord.ts                   # Chord types
│   │   └── midi.ts                    # MIDI types
│   ├── App.tsx                        # Main app component
│   ├── main.tsx                       # Entry point
│   └── index.css                      # Global styles
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Key Technologies

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **TanStack Query** - Server state management
- **react-piano** - Piano keyboard component
- **Web MIDI API** - MIDI input handling

## Browser Compatibility

Web MIDI API is supported in:
- ✅ Chrome/Chromium 43+
- ✅ Edge 79+
- ✅ Opera 30+
- ❌ Firefox (requires flag)
- ❌ Safari (not supported)

For best experience, use Chrome or Edge.

## MIDI Setup

1. Connect your MIDI keyboard to your computer
2. Open the app in a supported browser
3. Grant MIDI access permission when prompted
4. Your MIDI device should appear in the status bar
5. Start playing!

## Keyboard Shortcuts

When using computer keyboard (home row):
- `A S D F G H J K` = White keys
- `W E T Y U` = Black keys

## Development Tips

```bash
# Run linter
npm run lint

# Type checking
npx tsc --noEmit

# Format code
npx prettier --write src/
```

## Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

## Troubleshooting

### MIDI not connecting
- Check browser compatibility
- Ensure MIDI device is connected before opening the app
- Try refreshing the page
- Check browser permissions for MIDI access

### Build errors
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Clear Vite cache: `rm -rf node_modules/.vite`

## License

MIT
