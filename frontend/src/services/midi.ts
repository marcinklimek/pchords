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

    // Note on: command = 144 (0x90), velocity > 0
    // Note off: command = 128 (0x80) or command = 144 with velocity = 0
    if (command === 144 && velocity > 0) {
      this.playedNotes.add(note)
      this.onNoteOnCallback?.(note, velocity)
    } else if (command === 128 || (command === 144 && velocity === 0)) {
      this.playedNotes.delete(note)
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
