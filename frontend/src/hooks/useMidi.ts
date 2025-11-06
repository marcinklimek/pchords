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
    console.log('📱 Devices updated:', connectedDevices)
    setDevices(connectedDevices)
    setIsConnected(midiService.isConnected())
  }, [])

  const initialize = useCallback(async () => {
    console.log('🔌 Initializing MIDI...')
    const success = await midiService.initialize()

    if (success) {
      console.log('✅ MIDI initialized successfully')
      setIsInitialized(true)
      updateDevices()

      // Set up MIDI event listeners - use direct state setters
      midiService.onNoteOn((note, velocity) => {
        console.log('🎵 Note ON callback fired:', note, velocity)
        const notes = midiService.getPlayedNotes()
        console.log('📝 Updating React state with notes:', notes)
        setPlayedNotes(notes)
      })

      midiService.onNoteOff((note, velocity) => {
        console.log('🔇 Note OFF callback fired:', note, velocity)
        const notes = midiService.getPlayedNotes()
        console.log('📝 Updating React state with notes:', notes)
        setPlayedNotes(notes)
      })

      midiService.onStateChange(() => {
        console.log('🔄 MIDI state changed')
        updateDevices()
      })
    } else {
      console.error('❌ MIDI initialization failed')
    }
  }, [updateDevices])

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
