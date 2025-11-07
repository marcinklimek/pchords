/**
 * Interactive piano keyboard component using react-piano.
 */

import { Piano, KeyboardShortcuts, MidiNumbers } from 'react-piano'
import 'react-piano/dist/styles.css'
import './PianoKeyboard.css'

interface PianoKeyboardProps {
  playedNotes: number[]
  expectedNotes: number[]
  expectedRootNotes?: number[]  // MIDI numbers for root notes (left hand)
  onPlayNote?: (midiNumber: number) => void
  onStopNote?: (midiNumber: number) => void
}

export function PianoKeyboard({
  playedNotes,
  expectedNotes,
  expectedRootNotes = [],
  onPlayNote,
  onStopNote,
}: PianoKeyboardProps) {
  // Define keyboard range (C3 to C6)
  const firstNote = MidiNumbers.fromNote('c3')
  const lastNote = MidiNumbers.fromNote('c6')

  // Convert note indices to MIDI numbers in the keyboard range
  const getExpectedMidiNumbers = (): number[] => {
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

  const expectedMidiNumbers = getExpectedMidiNumbers()

  // Debug logging
  console.log('🎹 Piano - Expected note indices:', expectedNotes)
  console.log('🎹 Piano - Expected MIDI numbers:', expectedMidiNumbers)
  console.log('🎸 Piano - Expected root notes:', expectedRootNotes)
  console.log('🎹 Piano - Currently played:', playedNotes)

  // Check if a MIDI note is a black key (sharp/flat)
  const isBlackKey = (midiNumber: number): boolean => {
    const noteIndex = midiNumber % 12
    // Black keys: C#(1), D#(3), F#(6), G#(8), A#(10)
    return [1, 3, 6, 8, 10].includes(noteIndex)
  }

  // Custom render function for keys
  const renderNoteLabel = ({ midiNumber }: { midiNumber: number }) => {
    const isExpectedChord = expectedMidiNumbers.includes(midiNumber)
    const isExpectedRoot = expectedRootNotes.includes(midiNumber)
    const isPlayed = playedNotes.includes(midiNumber)

    if (!isExpectedChord && !isExpectedRoot && !isPlayed) return null

    // Determine state and color
    let indicator = ''
    let colorClass = ''
    let shape = 'circle'  // or 'square' for root notes

    // Root note (left hand) - display as square
    if (isExpectedRoot) {
      shape = 'square'
      if (isPlayed) {
        indicator = '✓'
        colorClass = 'correct-root'
      } else {
        indicator = '■'
        colorClass = 'expected-root'
      }
    }
    // Chord note (right hand) - display as circle
    else if (isExpectedChord) {
      shape = 'circle'
      if (isPlayed) {
        indicator = '✓'
        colorClass = 'correct'
      } else {
        indicator = '○'
        colorClass = 'expected'
      }
    }
    // Incorrect note
    else if (isPlayed) {
      indicator = '✗'
      colorClass = 'incorrect'
    }

    // Determine key type for positioning
    const keyType = isBlackKey(midiNumber) ? 'black-key' : 'white-key'

    console.log(`🎹 Indicator for MIDI ${midiNumber}: ${indicator} ${colorClass} ${keyType} ${shape}`)

    return (
      <div className={`note-indicator ${colorClass} ${keyType} ${shape}`}>
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
          <span className="legend-icon expected">○</span>
          <span>Chord Note - Expected</span>
        </div>
        <div className="legend-item">
          <span className="legend-icon expected-root">■</span>
          <span>Root Note - Expected (Left Hand)</span>
        </div>
        <div className="legend-item">
          <span className="legend-icon correct">✓</span>
          <span>Correct Note</span>
        </div>
        <div className="legend-item">
          <span className="legend-icon incorrect">✗</span>
          <span>Incorrect Note</span>
        </div>
      </div>
    </div>
  )
}
