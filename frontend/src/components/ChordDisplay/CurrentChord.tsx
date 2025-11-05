/**
 * Component for displaying the current chord to practice.
 */

import type { ChordData } from '../../types'

interface CurrentChordProps {
  chord: ChordData | undefined
  isLoading?: boolean
}

export function CurrentChord({ chord, isLoading }: CurrentChordProps) {
  if (isLoading) {
    return (
      <div className="text-center p-8">
        <div className="animate-pulse">
          <div className="h-16 bg-gray-700 rounded w-64 mx-auto mb-4"></div>
          <div className="h-8 bg-gray-700 rounded w-48 mx-auto"></div>
        </div>
      </div>
    )
  }

  if (!chord) {
    return (
      <div className="text-center p-8 text-gray-400">
        <p className="text-xl">No chord available</p>
        <p className="text-sm mt-2">Click "Next Chord" to begin</p>
      </div>
    )
  }

  return (
    <div className="text-center p-8">
      <h2 className="text-6xl font-bold text-white mb-4">
        {chord.name}
      </h2>

      <div className="flex justify-center items-center gap-4">
        <span className="text-2xl text-gray-400">Notes:</span>
        <div className="flex gap-2">
          {chord.notes.map((note, index) => (
            <div
              key={index}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg text-2xl font-semibold"
            >
              {note}
            </div>
          ))}
        </div>
      </div>

      {chord.quality && (
        <div className="mt-4 text-gray-400 text-sm">
          Quality: {chord.quality} | Scale: {chord.scale}
        </div>
      )}
    </div>
  )
}
