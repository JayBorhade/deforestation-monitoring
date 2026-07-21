import { useCallback, useEffect, useState } from 'react'
import { Prediction } from '@/types'
import { getPredictions, getRiskDistribution } from '@/services/api'

export const usePredictions = () => {
  const [predictions, setPredictions] = useState<Prediction[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [riskDistribution, setRiskDistribution] = useState(null)

  const fetchPredictions = useCallback(async (skip = 0, limit = 50) => {
    setLoading(true)
    setError(null)
    try {
      const data = await getPredictions(skip, limit)
      setPredictions(data)
    } catch (err: any) {
      setError(err.message || 'Failed to fetch predictions')
    } finally {
      setLoading(false)
    }
  }, [])

  const fetchRiskDistribution = useCallback(async () => {
    try {
      const data = await getRiskDistribution()
      setRiskDistribution(data)
    } catch (err: any) {
      console.error('Failed to fetch risk distribution:', err)
    }
  }, [])

  useEffect(() => {
    fetchPredictions()
    fetchRiskDistribution()
  }, [])

  return {
    predictions,
    loading,
    error,
    riskDistribution,
    fetchPredictions,
    fetchRiskDistribution,
  }
}
