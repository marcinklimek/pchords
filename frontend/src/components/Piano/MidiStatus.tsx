/**
 * MIDI connection status indicator.
 */

import type { MidiDevice } from '../../types'

interface MidiStatusProps {
  isConnected: boolean
  devices: MidiDevice[]
  onRefresh?: () => void
}

export function MidiStatus({ isConnected, devices, onRefresh }: MidiStatusProps) {
  return (
    <div className="flex items-center gap-4 p-4 bg-gray-800 rounded-lg">
      <div className="flex items-center gap-2">
        <div
          className={`w-3 h-3 rounded-full ${
            isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'
          }`}
        />
        <span className="text-sm font-medium text-gray-300">
          {isConnected ? 'MIDI Connected' : 'No MIDI Device'}
        </span>
      </div>

      {devices.length > 0 && (
        <div className="flex-1">
          <div className="text-sm text-gray-400">
            Devices: {devices.map((d) => d.name).join(', ')}
          </div>
        </div>
      )}

      {onRefresh && (
        <button
          onClick={onRefresh}
          className="px-3 py-1 text-sm bg-gray-700 hover:bg-gray-600 text-white rounded transition-colors"
        >
          Refresh
        </button>
      )}
    </div>
  )
}
