import { useCallback, useEffect, useState } from 'react'
import { AnalysisResult, SatelliteImage } from '@/types'
import {
  getAnalysisResults,
  getSatelliteImages,
  createAnalysisResult,
} from '@/services/api'

export const useAnalysis = () => {
  const [analysisResults, setAnalysisResults] = useState<AnalysisResult[]>([])
  const [satelliteImages, setSatelliteImages] = useState<SatelliteImage[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchAnalysisResults = useCallback(async (skip = 0, limit = 50) => {
    setLoading(true)
    setError(null)
    try {
      const data = await getAnalysisResults(skip, limit)
      setAnalysisResults(data)
    } catch (err: any) {
      setError(err.message || 'Failed to fetch analysis results')
    } finally {
      setLoading(false)
    }
  }, [])

  const fetchSatelliteImages = useCallback(async (skip = 0, limit = 50) => {
    try {
      const data = await getSatelliteImages(skip, limit)
      setSatelliteImages(data)
    } catch (err: any) {
      setError(err.message || 'Failed to fetch satellite images')
    }
  }, [])

  const createAnalysis = useCallback(
    async (analysis: Partial<AnalysisResult>) => {
      try {
        const newAnalysis = await createAnalysisResult(analysis)
        setAnalysisResults((prev) => [newAnalysis, ...prev])
        return newAnalysis
      } catch (err: any) {
        setError(err.message || 'Failed to create analysis')
        throw err
      }
    },
    []
  )

  useEffect(() => {
    fetchAnalysisResults()
    fetchSatelliteImages()
  }, [])

  return {
    analysisResults,
    satelliteImages,
    loading,
    error,
    fetchAnalysisResults,
    fetchSatelliteImages,
    createAnalysis,
  }
}
