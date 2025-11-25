import { ChordQuality, VoicingType, ScaleType } from './theory'

export interface ChordData {
  root: string
  quality: string
  name: string
  notes: string[]
  midi_notes: number[]
  voicing_type?: string
  scale_context?: string
}

export interface ChordSet {
  id: string
  name: string
  enabled: boolean
  qualities: ChordQuality[]
  roots: string[]
  voicing_types: VoicingType[]
  difficulty: string
}

export interface ChordResponse {
  chord: ChordData
  remaining: number
}

export interface ScaleData {
  root: string
  type: string
  name: string
  notes: string[]
  midi_notes: number[]
}

export interface ScaleResponse {
  scale: ScaleData
  diatonic_chords: ChordData[]
}

export interface ProgressionStep {
  degree: string
  chord: ChordData
  duration_beats: number
}

export interface ProgressionData {
  id: string
  name: string
  key: string
  scale_type: string
  steps: ProgressionStep[]
  tempo: number
}
