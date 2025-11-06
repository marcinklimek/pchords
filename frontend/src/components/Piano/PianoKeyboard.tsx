/**
 * Interactive piano keyboard component using react-piano.
 */

import { Piano, KeyboardShortcuts, MidiNumbers } from 'react-piano'
import 'react-piano/dist/styles.css'
import './PianoKeyboard.css'

interface PianoKeyboardProps {
  playedNotes: number[]
  expectedNotes: number[]
  expectedMidiNotes?: number[]  // Optional: pre-calculated MIDI notes from backend
  rootNoteMidi?: number  // Optional: root note for left hand bass
  onPlayNote?: (midiNumber: number) => void
  onStopNote?: (midiNumber: number) => void
}

export function PianoKeyboard({
  playedNotes,
  expectedNotes,
  expectedMidiNotes,
  rootNoteMidi,
  onPlayNote,
  onStopNote,
}: PianoKeyboardProps) {
  // Define keyboard range (C3 to C6)
  const firstNote = MidiNumbers.fromNote('c3')
  const lastNote = MidiNumbers.fromNote('c6')

  // Convert note indices to MIDI numbers in the keyboard range
  const getExpectedMidiNumbers = (): number[] => {
    // Use pre-calculated MIDI notes if available
    if (expectedMidiNotes && expectedMidiNotes.length > 0) {
      return expectedMidiNotes.filter(
        (midi) => midi >= firstNote && midi <= lastNote
      )
    }

    // Fallback: convert indices across all octaves
    const midiNumbers: number[] = []
    for (let octave = 3; octave < 6; octave++) {
      expectedNotes.forEach((noteIndex) => {
        const midiNumber = octave * 12 + noteIndex + 12 // +12 for MIDI offset
        if (midiNumber >= firstNote && midiNumber <= lastNote) {
          midiNumbers.push(midiNumber)
        }
      })
    }
    return midiNumbers
  }

  const expectedChordNotes = getExpectedMidiNumbers()

  // Debug logging
  console.log('🎹 Piano - Expected note indices:', expectedNotes)
  console.log('🎹 Piano - Expected chord MIDI:', expectedChordNotes)
  console.log('🎹 Piano - Root note MIDI:', rootNoteMidi)
  console.log('🎹 Piano - Currently played:', playedNotes)

  // Check if a MIDI note is a black key (sharp/flat)
  const isBlackKey = (midiNumber: number): boolean => {
    const noteIndex = midiNumber % 12
    // Black keys: C#(1), D#(3), F#(6), G#(8), A#(10)
    return [1, 3, 6, 8, 10].includes(noteIndex)
  }

  // Custom render function for keys
  const renderNoteLabel = ({ midiNumber }: { midiNumber: number }) => {
    const isExpectedChordNote = expectedChordNotes.includes(midiNumber)
    const isRootNote = rootNoteMidi !== undefined && midiNumber === rootNoteMidi
    const isExpected = isExpectedChordNote || isRootNote
    const isPlayed = playedNotes.includes(midiNumber)

    if (!isExpected && !isPlayed) return null

    // Determine state and color
    let indicator = ''
    let colorClass = ''

    if (isPlayed && isExpected) {
      indicator = '✓'
      colorClass = 'correct'
    } else if (isPlayed && !isExpected) {
      indicator = '✗'
      colorClass = 'incorrect'
    } else if (!isPlayed && isExpected) {
      // Different indicator for root note vs chord notes
      indicator = isRootNote ? '■' : '○'
      colorClass = isRootNote ? 'root' : 'expected'
    }

    // Determine key type for positioning
    const keyType = isBlackKey(midiNumber) ? 'black-key' : 'white-key'

    return (
      <div className={`note-indicator ${colorClass} ${keyType}`}>
        {indicator}
      </div>
    )
  }

  return (
    <div className="piano-container">
      <Piano
        noteRange={{ first: firstNote, last: lastNote }}
        playNote={onPlayNote || (() => {})}
        stopNote={onStopNote || (() => {})}
        width={1000}
        activeNotes={playedNotes}
        renderNoteLabel={renderNoteLabel}
        keyboardShortcuts={KeyboardShortcuts.create({
          firstNote: firstNote,
          lastNote: lastNote,
          keyboardConfig: KeyboardShortcuts.HOME_ROW,
        })}
      />

      <div className="piano-legend">
        <div className="legend-item">
          <span className="legend-icon root">■</span>
          <span>Root Note - Left Hand Bass</span>
        </div>
        <div className="legend-item">
          <span className="legend-icon expected">○</span>
          <span>Chord Notes - Right Hand</span>
        </div>
        <div className="legend-item">
          <span className="legend-icon correct">✓</span>
          <span>Correct - Playing Right Note</span>
        </div>
        <div className="legend-item">
          <span className="legend-icon incorrect">✗</span>
          <span>Incorrect - Wrong Note</span>
        </div>
      </div>
    </div>
  )
}
