/**
 * MIDI service using Web MIDI API.
 */

import type { MidiDevice, MIDIMessageEvent } from '../types'

export type MidiNoteCallback = (note: number, velocity: number) => void

export class MidiService {
  private midiAccess: MIDIAccess | null = null
  private connectedInputs: Map<string, MIDIInput> = new Map()
  private playedNotes: Set<number> = new Set()

  // Callbacks
  private onNoteOnCallback: MidiNoteCallback | null = null
  private onNoteOffCallback: MidiNoteCallback | null = null
  private onStateChangeCallback: (() => void) | null = null

  async initialize(): Promise<boolean> {
    if (!navigator.requestMIDIAccess) {
      console.error('Web MIDI API is not supported in this browser')
      return false
    }

    try {
      this.midiAccess = await navigator.requestMIDIAccess()

      // Listen for device connection changes
      this.midiAccess.onstatechange = () => {
        this.onStateChangeCallback?.()
      }

      // Connect to all available inputs
      this.connectAllInputs()

      return true
    } catch (error) {
      console.error('Failed to initialize MIDI:', error)
      return false
    }
  }

  private connectAllInputs(): void {
    if (!this.midiAccess) return

    this.midiAccess.inputs.forEach((input) => {
      this.connectInput(input)
    })
  }

  private connectInput(input: MIDIInput): void {
    input.onmidimessage = (event: Event) => {
      this.handleMidiMessage(event as MIDIMessageEvent)
    }

    this.connectedInputs.set(input.id, input)
  }

  private handleMidiMessage(event: MIDIMessageEvent): void {
    const [command, note, velocity] = event.data

    console.log('🎹 MIDI event:', { command, note, velocity })

    // Note on: status byte 0x90-0x9F (144-159), velocity > 0
    // Note off: status byte 0x80-0x8F (128-143) or note on with velocity 0
    const statusByte = command & 0xF0

    if (statusByte === 0x90 && velocity > 0) {
      // Note on
      this.playedNotes.add(note)
      console.log('✅ Note ON:', note, 'Played notes:', Array.from(this.playedNotes))
      this.onNoteOnCallback?.(note, velocity)
    } else if (statusByte === 0x80 || (statusByte === 0x90 && velocity === 0)) {
      // Note off
      this.playedNotes.delete(note)
      console.log('❌ Note OFF:', note, 'Played notes:', Array.from(this.playedNotes))
      this.onNoteOffCallback?.(note, velocity)
    }
  }

  getPlayedNotes(): number[] {
    return Array.from(this.playedNotes).sort()
  }

  getConnectedDevices(): MidiDevice[] {
    if (!this.midiAccess) return []

    const devices: MidiDevice[] = []

    this.midiAccess.inputs.forEach((input) => {
      devices.push({
        id: input.id,
        name: input.name || 'Unknown Device',
        manufacturer: input.manufacturer || 'Unknown',
        state: input.state,
      })
    })

    return devices
  }

  isConnected(): boolean {
    return this.connectedInputs.size > 0
  }

  onNoteOn(callback: MidiNoteCallback): void {
    this.onNoteOnCallback = callback
  }

  onNoteOff(callback: MidiNoteCallback): void {
    this.onNoteOffCallback = callback
  }

  onStateChange(callback: () => void): void {
    this.onStateChangeCallback = callback
  }

  disconnect(): void {
    this.connectedInputs.forEach((input) => {
      input.onmidimessage = null
    })

    this.connectedInputs.clear()
    this.playedNotes.clear()
  }
}

// Singleton instance
export const midiService = new MidiService()
