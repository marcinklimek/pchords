/**
 * Chord-related TypeScript types.
 */

export interface ChordData {
  root: string
  name: string
  notes: string[]
  scale: string
  quality?: string
  inversion?: string
  // MIDI data for root note + full chord practice
  root_note?: number  // MIDI number for root note (left hand bass)
  notes_midi?: number[]  // MIDI numbers for chord notes
}

export interface ChordSet {
  id: string
  name: string
  enabled: boolean
  qualities: string[]
  scales: string[]
  inversions: string[]
  notes_range?: [number, number]
  exclude_roots: string[]
  difficulty: 'easy' | 'medium' | 'hard' | 'expert'
  specific_chords: ChordData[]
}

export interface ChordResponse {
  chord: ChordData
  remaining: number
}
