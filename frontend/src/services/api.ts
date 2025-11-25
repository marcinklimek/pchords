/**
 * API client for PChords backend.
 */

import type {
  ChordResponse,
  ChordSet,
  ScaleResponse,
  ProgressionData
} from '../types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`

    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    })

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`)
    }

    return response.json()
  }

  // Chord endpoints
  async getNextChord(): Promise<ChordResponse> {
    return this.request<ChordResponse>('/api/chords/next')
  }

  async getChordSets(): Promise<ChordSet[]> {
    return this.request<ChordSet[]>('/api/chords/sets')
  }

  async getChordSet(id: string): Promise<ChordSet> {
    return this.request<ChordSet>(`/api/chords/sets/${id}`)
  }

  async createChordSet(data: Partial<ChordSet>): Promise<ChordSet> {
    return this.request<ChordSet>('/api/chords/sets', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async updateChordSet(id: string, data: Partial<ChordSet>): Promise<ChordSet> {
    return this.request<ChordSet>(`/api/chords/sets/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async deleteChordSet(id: string): Promise<void> {
    return this.request<void>(`/api/chords/sets/${id}`, {
      method: 'DELETE',
    })
  }

  async regenerateChords(): Promise<{ message: string; count: number }> {
    return this.request<{ message: string; count: number }>('/api/chords/regenerate', {
      method: 'POST',
    })
  }

  // Scale endpoints
  async getScaleTypes(): Promise<string[]> {
    return this.request<string[]>('/api/scales/types')
  }

  async getScale(root: string, type: string): Promise<ScaleResponse> {
    return this.request<ScaleResponse>(`/api/scales/${encodeURIComponent(root)}/${encodeURIComponent(type)}`)
  }

  // Progression endpoints
  async getProgressionTemplates(): Promise<any[]> {
    return this.request<any[]>('/api/progressions/templates')
  }

  async generateProgression(templateId: string, key: string, scaleType: string = 'Major'): Promise<ProgressionData> {
    return this.request<ProgressionData>(`/api/progressions/generate?template_id=${templateId}&key=${encodeURIComponent(key)}&scale_type=${scaleType}`, {
      method: 'POST'
    })
  }
}

export const apiClient = new ApiClient()
