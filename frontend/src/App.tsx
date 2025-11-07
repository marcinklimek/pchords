/**
 * Main PChords application component.
 */

import { useState, useEffect } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Header } from './components/Layout/Header'
import { CurrentChord } from './components/ChordDisplay/CurrentChord'
import { PlayedNotes } from './components/ChordDisplay/PlayedNotes'
import { PianoKeyboard } from './components/Piano/PianoKeyboard'
import { MidiStatus } from './components/Piano/MidiStatus'
import { useMidi } from './hooks/useMidi'
import { useNextChord } from './hooks/useChords'
import { apiClient } from './services/api'

// Create a client
const queryClient = new QueryClient()

type RootNoteMode = 'off' | 'single' | 'octave'

function PracticeScreen() {
  const { isConnected, devices, playedNotes, initialize } = useMidi()
  const { data: chordResponse, isLoading, refetch } = useNextChord()

  const [expectedNoteIndices, setExpectedNoteIndices] = useState<number[]>([])
  const [rootNoteMode, setRootNoteMode] = useState<RootNoteMode>('single')
  const [expectedMidiNumbers, setExpectedMidiNumbers] = useState<number[]>([])

  // Convert note names to MIDI note indices (0-11) and calculate expected MIDI numbers
  useEffect(() => {
    if (chordResponse?.chord) {
      const noteNames = chordResponse.chord.notes
      const indices = noteNames.map((name) => {
        // Simple note name to index conversion
        const notes: { [key: string]: number } = {
          C: 0,
          'C#': 1,
          Db: 1,
          D: 2,
          'D#': 3,
          Eb: 3,
          E: 4,
          F: 5,
          'F#': 6,
          Gb: 6,
          G: 7,
          'G#': 8,
          Ab: 8,
          A: 9,
          'A#': 10,
          Bb: 10,
          B: 11,
        }
        return notes[name] ?? 0
      })
      setExpectedNoteIndices(indices)

      // Add root note MIDI numbers if root note mode is enabled
      const midiNumbers: number[] = []
      if (rootNoteMode !== 'off' && chordResponse.chord.root_note !== undefined) {
        midiNumbers.push(chordResponse.chord.root_note)

        // If octave mode, add root note + 12 (one octave higher)
        if (rootNoteMode === 'octave') {
          midiNumbers.push(chordResponse.chord.root_note + 12)
        }
      }
      setExpectedMidiNumbers(midiNumbers)

      console.log('🎵 New chord:', chordResponse.chord.name)
      console.log('📝 Expected notes:', noteNames, '→ indices:', indices)
      console.log('🎸 Root note MIDI:', midiNumbers, 'mode:', rootNoteMode)
    }
  }, [chordResponse, rootNoteMode])

  // Check if chord is completed
  useEffect(() => {
    if (playedNotes.length === 0) return
    if (expectedNoteIndices.length === 0) return

    // Convert MIDI notes to indices (0-11) and remove duplicates
    const playedIndices = Array.from(new Set(playedNotes.map((note) => note % 12)))

    // Sort both arrays for comparison
    const sortedPlayed = [...playedIndices].sort((a, b) => a - b)
    const sortedExpected = [...expectedNoteIndices].sort((a, b) => a - b)

    // Check if chord notes are correct
    const chordNotesCorrect =
      sortedPlayed.length === sortedExpected.length &&
      sortedPlayed.every((note, index) => note === sortedExpected[index])

    // Check if root notes are correct (if enabled)
    let rootNotesCorrect = true
    if (rootNoteMode !== 'off' && expectedMidiNumbers.length > 0) {
      rootNotesCorrect = expectedMidiNumbers.every((midi) => playedNotes.includes(midi))
    }

    const isCorrect = chordNotesCorrect && rootNotesCorrect

    console.log('🎹 Played indices:', sortedPlayed, 'Expected indices:', sortedExpected)
    console.log('🎸 Root notes correct:', rootNotesCorrect, 'Expected MIDI:', expectedMidiNumbers)
    console.log('✅ Overall correct:', isCorrect)

    if (isCorrect) {
      console.log('✅ Chord correct! Auto-advancing in 1 second...')
      // Auto-advance to next chord after a short delay
      setTimeout(() => {
        refetch()
      }, 1000)
    }
  }, [playedNotes, expectedNoteIndices, expectedMidiNumbers, rootNoteMode, refetch])

  const handleNextChord = () => {
    refetch()
  }

  const handleRegenerateChords = async () => {
    await apiClient.regenerateChords()
    refetch()
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <Header />

      <main className="container mx-auto px-6 py-8">
        {/* MIDI Status */}
        <div className="mb-6">
          <MidiStatus
            isConnected={isConnected}
            devices={devices}
            onRefresh={initialize}
          />
        </div>

        {/* Current Chord Display */}
        <div className="mb-8 bg-gray-800 rounded-xl shadow-2xl p-6">
          <CurrentChord chord={chordResponse?.chord} isLoading={isLoading} />

          {chordResponse && (
            <div className="text-center text-gray-400 mt-4">
              {chordResponse.remaining} chords remaining
            </div>
          )}
        </div>

        {/* Played Notes */}
        <div className="mb-8">
          <PlayedNotes
            playedNotes={playedNotes}
            expectedNotes={expectedNoteIndices}
          />
        </div>

        {/* Piano Keyboard */}
        <div className="mb-8">
          <PianoKeyboard
            playedNotes={playedNotes}
            expectedNotes={expectedNoteIndices}
            expectedRootNotes={expectedMidiNumbers}
          />
        </div>

        {/* Root Note Configuration */}
        <div className="mb-6 bg-gray-800 rounded-xl shadow-2xl p-6">
          <h3 className="text-xl font-semibold text-white mb-4">Root Note Settings</h3>
          <div className="flex gap-4 items-center">
            <label className="text-gray-300">Root Note Mode:</label>
            <select
              value={rootNoteMode}
              onChange={(e) => setRootNoteMode(e.target.value as RootNoteMode)}
              className="px-4 py-2 bg-gray-700 text-white rounded-lg border border-gray-600 focus:outline-none focus:border-primary-500"
            >
              <option value="off">Off - Rootless chords only</option>
              <option value="single">Single - One root note (left hand)</option>
              <option value="octave">Octave - Two root notes (left hand)</option>
            </select>
          </div>
          <p className="text-gray-400 text-sm mt-2">
            Practice left hand bass notes along with right hand chords
          </p>
        </div>

        {/* Control Buttons */}
        <div className="flex justify-center gap-4">
          <button
            onClick={handleNextChord}
            className="px-8 py-3 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-lg transition-colors shadow-lg"
          >
            Next Chord
          </button>

          <button
            onClick={handleRegenerateChords}
            className="px-8 py-3 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors shadow-lg"
          >
            Regenerate All
          </button>
        </div>

        {/* Instructions */}
        {!isConnected && (
          <div className="mt-8 p-6 bg-yellow-900 bg-opacity-30 border border-yellow-700 rounded-lg">
            <h3 className="text-yellow-300 font-semibold mb-2">
              🎹 Connect Your MIDI Keyboard
            </h3>
            <p className="text-yellow-200 text-sm">
              Connect a MIDI keyboard and click "Refresh" to start practicing. You can also use
              your computer keyboard to play notes.
            </p>
          </div>
        )}
      </main>
    </div>
  )
}

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <PracticeScreen />
    </QueryClientProvider>
  )
}
