/**
 * React hook for chord management using TanStack Query.
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '../services/api'
import type { ChordResponse, ChordSet } from '../types'

export function useNextChord() {
  return useQuery({
    queryKey: ['chord', 'next'],
    queryFn: () => apiClient.getNextChord(),
    // Don't refetch automatically
    refetchOnWindowFocus: false,
    refetchOnMount: false,
  })
}

export function useChordSets() {
  return useQuery({
    queryKey: ['chord-sets'],
    queryFn: () => apiClient.getChordSets(),
  })
}

export function useChordSet(id: string) {
  return useQuery({
    queryKey: ['chord-set', id],
    queryFn: () => apiClient.getChordSet(id),
    enabled: !!id,
  })
}

export function useCreateChordSet() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: Partial<ChordSet>) => apiClient.createChordSet(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chord-sets'] })
    },
  })
}

export function useUpdateChordSet() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<ChordSet> }) =>
      apiClient.updateChordSet(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chord-sets'] })
      queryClient.invalidateQueries({ queryKey: ['chord', 'next'] })
    },
  })
}

export function useDeleteChordSet() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => apiClient.deleteChordSet(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chord-sets'] })
    },
  })
}

export function useRegenerateChords() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: () => apiClient.regenerateChords(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chord', 'next'] })
    },
  })
}
