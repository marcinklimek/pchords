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
  root_note?: number  // MIDI note number for root note (e.g., C2 = 36)
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
