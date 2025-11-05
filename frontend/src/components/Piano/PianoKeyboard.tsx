/**
 * Interactive piano keyboard component using react-piano.
 */

import { Piano, KeyboardShortcuts, MidiNumbers } from 'react-piano'
import 'react-piano/dist/styles.css'
import './PianoKeyboard.css'

interface PianoKeyboardProps {
  playedNotes: number[]
  expectedNotes: number[]
  onPlayNote?: (midiNumber: number) => void
  onStopNote?: (midiNumber: number) => void
}

export function PianoKeyboard({
  playedNotes,
  expectedNotes,
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

  // Custom render function for keys
  const renderNoteLabel = ({ midiNumber }: { midiNumber: number }) => {
    const isExpected = expectedMidiNumbers.includes(midiNumber)
    const isPlayed = playedNotes.includes(midiNumber)

    if (!isExpected && !isPlayed) return null

    return (
      <div className="note-indicator">
        {isPlayed && isExpected && '✓'}
        {isPlayed && !isExpected && '✗'}
        {!isPlayed && isExpected && '○'}
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
          <span className="legend-dot expected"></span>
          <span>Expected Note</span>
        </div>
        <div className="legend-item">
          <span className="legend-dot correct"></span>
          <span>Correct</span>
        </div>
        <div className="legend-item">
          <span className="legend-dot incorrect"></span>
          <span>Incorrect</span>
        </div>
      </div>
    </div>
  )
}
