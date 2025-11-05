/**
 * Component for displaying currently played MIDI notes.
 */

interface PlayedNotesProps {
  playedNotes: number[]
  expectedNotes: number[]
}

const NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

function midiToNoteName(midiNote: number): string {
  const octave = Math.floor(midiNote / 12) - 1
  const noteIndex = midiNote % 12
  return `${NOTE_NAMES[noteIndex]}${octave}`
}

function midiToNoteIndex(midiNote: number): number {
  return midiNote % 12
}

export function PlayedNotes({ playedNotes, expectedNotes }: PlayedNotesProps) {
  const playedIndices = playedNotes.map(midiToNoteIndex)
  const isCorrect = playedNotes.length > 0 &&
                    playedIndices.length === expectedNotes.length &&
                    playedIndices.every(note => expectedNotes.includes(note))

  return (
    <div className="p-6 bg-gray-800 rounded-lg">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-semibold text-gray-300">
          Played Notes
        </h3>

        {playedNotes.length > 0 && (
          <div className="flex items-center gap-2">
            {isCorrect ? (
              <span className="px-3 py-1 bg-green-600 text-white rounded-full text-sm font-medium">
                ✓ Correct!
              </span>
            ) : (
              <span className="px-3 py-1 bg-gray-700 text-gray-300 rounded-full text-sm">
                {playedNotes.length} / {expectedNotes.length}
              </span>
            )}
          </div>
        )}
      </div>

      <div className="min-h-[60px] flex items-center">
        {playedNotes.length === 0 ? (
          <p className="text-gray-500 text-center w-full">
            Play notes on your MIDI keyboard...
          </p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {playedNotes.map((note, index) => {
              const noteIndex = midiToNoteIndex(note)
              const isExpected = expectedNotes.includes(noteIndex)

              return (
                <div
                  key={`${note}-${index}`}
                  className={`px-4 py-2 rounded-lg text-lg font-semibold transition-colors ${
                    isExpected
                      ? 'bg-green-600 text-white'
                      : 'bg-red-600 text-white'
                  }`}
                >
                  {midiToNoteName(note)}
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
