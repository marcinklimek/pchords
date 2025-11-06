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

function PracticeScreen() {
  const { isConnected, devices, playedNotes, initialize } = useMidi()
  const { data: chordResponse, isLoading, refetch } = useNextChord()

  const [expectedNoteIndices, setExpectedNoteIndices] = useState<number[]>([])
  const [expectedMidiNotes, setExpectedMidiNotes] = useState<number[]>([])
  const [rootNoteMidi, setRootNoteMidi] = useState<number | undefined>(undefined)

  // Convert note names to MIDI note indices (0-11) and extract MIDI numbers
  useEffect(() => {
    if (chordResponse?.chord) {
      const chord = chordResponse.chord
      const noteNames = chord.notes

      // Use MIDI numbers if available, otherwise convert note names
      if (chord.notes_midi && chord.notes_midi.length > 0) {
        // Use pre-calculated MIDI numbers from backend
        setExpectedMidiNotes(chord.notes_midi)
        const indices = chord.notes_midi.map((midi) => midi % 12)
        setExpectedNoteIndices(indices)
        console.log('🎵 New chord:', chord.name)
        console.log('📝 Expected MIDI notes:', chord.notes_midi, '→ indices:', indices)
      } else {
        // Fallback: convert note names to indices (0-11)
        const noteToIndex: { [key: string]: number } = {
          C: 0, 'C#': 1, Db: 1,
          D: 2, 'D#': 3, Eb: 3,
          E: 4,
          F: 5, 'F#': 6, Gb: 6,
          G: 7, 'G#': 8, Ab: 8,
          A: 9, 'A#': 10, Bb: 10,
          B: 11,
        }
        const indices = noteNames.map((name) => noteToIndex[name] ?? 0)
        setExpectedNoteIndices(indices)
        setExpectedMidiNotes([])
        console.log('🎵 New chord:', chord.name)
        console.log('📝 Expected notes:', noteNames, '→ indices:', indices)
      }

      // Set root note MIDI number if available
      setRootNoteMidi(chord.root_note)
      if (chord.root_note) {
        console.log('🎹 Root note MIDI:', chord.root_note)
      }
    }
  }, [chordResponse])

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

    // Check if root note is played (if required)
    const rootNoteCorrect = rootNoteMidi === undefined || playedNotes.includes(rootNoteMidi)

    // Both chord notes AND root note must be correct
    const isCorrect = chordNotesCorrect && rootNoteCorrect

    console.log('🎹 Played:', sortedPlayed, 'Expected:', sortedExpected)
    console.log('🎹 Root note:', rootNoteMidi, 'Played:', rootNoteCorrect)
    console.log('✅ Correct:', isCorrect)

    if (isCorrect) {
      console.log('✅ Chord + root note correct! Auto-advancing in 1 second...')
      // Auto-advance to next chord after a short delay
      setTimeout(() => {
        refetch()
      }, 1000)
    }
  }, [playedNotes, expectedNoteIndices, rootNoteMidi, refetch])

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
            expectedMidiNotes={expectedMidiNotes}
            rootNoteMidi={rootNoteMidi}
          />
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
