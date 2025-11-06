/**
 * Hook for managing application settings with localStorage persistence.
 */

import { useState, useEffect } from 'react'

export interface PracticeSettings {
  rootNotePractice: boolean  // Whether to include root note in practice
  // Future settings will be added here
}

const DEFAULT_SETTINGS: PracticeSettings = {
  rootNotePractice: true,
}

const STORAGE_KEY = 'pchords_settings'

export function useSettings() {
  const [settings, setSettings] = useState<PracticeSettings>(() => {
    // Load settings from localStorage on initial render
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored) {
        const parsed = JSON.parse(stored)
        return { ...DEFAULT_SETTINGS, ...parsed }
      }
    } catch (error) {
      console.error('Failed to load settings from localStorage:', error)
    }
    return DEFAULT_SETTINGS
  })

  // Save settings to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(settings))
      console.log('💾 Settings saved:', settings)
    } catch (error) {
      console.error('Failed to save settings to localStorage:', error)
    }
  }, [settings])

  const updateSettings = (updates: Partial<PracticeSettings>) => {
    setSettings((prev) => ({ ...prev, ...updates }))
  }

  const resetSettings = () => {
    setSettings(DEFAULT_SETTINGS)
  }

  return {
    settings,
    updateSettings,
    resetSettings,
  }
}
