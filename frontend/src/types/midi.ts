/**
 * MIDI-related TypeScript types.
 */

export interface MidiMessage {
  type: 'note_on' | 'note_off'
  note: number
  velocity: number
  timestamp: number
}

export interface MidiStatus {
  connected: boolean
  input_ports: string[]
  played_notes: number[]
}

export interface MidiDevice {
  id: string
  name: string
  manufacturer: string
  state: 'connected' | 'disconnected'
}

// Web MIDI API types
export interface WebMidiAccess {
  inputs: Map<string, WebMidiInput>
  outputs: Map<string, WebMidiOutput>
  sysexEnabled: boolean
  onstatechange: ((event: MIDIConnectionEvent) => void) | null
}

export interface WebMidiInput {
  id: string
  name: string
  manufacturer: string
  state: 'connected' | 'disconnected'
  type: 'input'
  onmidimessage: ((event: MIDIMessageEvent) => void) | null
  open(): Promise<WebMidiInput>
  close(): Promise<WebMidiInput>
}

export interface WebMidiOutput {
  id: string
  name: string
  manufacturer: string
  state: 'connected' | 'disconnected'
  type: 'output'
  send(data: number[], timestamp?: number): void
  open(): Promise<WebMidiOutput>
  close(): Promise<WebMidiOutput>
}

export interface MIDIMessageEvent extends Event {
  data: Uint8Array
  receivedTime: number
}

export interface MIDIConnectionEvent extends Event {
  port: WebMidiInput | WebMidiOutput
}
