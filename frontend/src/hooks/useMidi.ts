/**
 * React hook for Web MIDI API integration.
 */

import { useState, useEffect, useCallback } from 'react'
import { midiService } from '../services/midi'
import type { MidiDevice } from '../types'

export interface UseMidiReturn {
  isInitialized: boolean
  isConnected: boolean
  devices: MidiDevice[]
  playedNotes: number[]
  initialize: () => Promise<void>
  disconnect: () => void
}

export function useMidi(): UseMidiReturn {
  const [isInitialized, setIsInitialized] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const [devices, setDevices] = useState<MidiDevice[]>([])
  const [playedNotes, setPlayedNotes] = useState<number[]>([])

  const updateDevices = useCallback(() => {
    const connectedDevices = midiService.getConnectedDevices()
    setDevices(connectedDevices)
    setIsConnected(midiService.isConnected())
  }, [])

  const updatePlayedNotes = useCallback(() => {
    const notes = midiService.getPlayedNotes()
    setPlayedNotes(notes)
  }, [])

  const initialize = useCallback(async () => {
    const success = await midiService.initialize()

    if (success) {
      setIsInitialized(true)
      updateDevices()

      // Set up MIDI event listeners
      midiService.onNoteOn(() => {
        updatePlayedNotes()
      })

      midiService.onNoteOff(() => {
        updatePlayedNotes()
      })

      midiService.onStateChange(() => {
        updateDevices()
      })
    }
  }, [updateDevices, updatePlayedNotes])

  const disconnect = useCallback(() => {
    midiService.disconnect()
    setIsInitialized(false)
    setIsConnected(false)
    setDevices([])
    setPlayedNotes([])
  }, [])

  // Auto-initialize on mount
  useEffect(() => {
    initialize()

    return () => {
      disconnect()
    }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  return {
    isInitialized,
    isConnected,
    devices,
    playedNotes,
    initialize,
    disconnect,
  }
}
