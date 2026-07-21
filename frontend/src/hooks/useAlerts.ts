import { useCallback, useEffect, useState } from 'react'
import { Alert } from '@/types'
import { getAlerts, createAlert, updateAlert, getAlertsSummary } from '@/services/api'

export const useAlerts = () => {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [summary, setSummary] = useState(null)

  const fetchAlerts = useCallback(async (skip = 0, limit = 50) => {
    setLoading(true)
    setError(null)
    try {
      const data = await getAlerts(skip, limit)
      setAlerts(data)
    } catch (err: any) {
      setError(err.message || 'Failed to fetch alerts')
    } finally {
      setLoading(false)
    }
  }, [])

  const fetchSummary = useCallback(async () => {
    try {
      const data = await getAlertsSummary()
      setSummary(data)
    } catch (err: any) {
      console.error('Failed to fetch alerts summary:', err)
    }
  }, [])

  const addAlert = useCallback(
    async (alert: Partial<Alert>) => {
      try {
        const newAlert = await createAlert(alert)
        setAlerts((prev) => [newAlert, ...prev])
        await fetchSummary()
        return newAlert
      } catch (err: any) {
        setError(err.message || 'Failed to create alert')
        throw err
      }
    },
    [fetchSummary]
  )

  const modifyAlert = useCallback(
    async (alertId: string, updates: Partial<Alert>) => {
      try {
        const updated = await updateAlert(alertId, updates)
        setAlerts((prev) =>
          prev.map((a) => (a.id === alertId ? updated : a))
        )
        await fetchSummary()
        return updated
      } catch (err: any) {
        setError(err.message || 'Failed to update alert')
        throw err
      }
    },
    [fetchSummary]
  )

  useEffect(() => {
    fetchAlerts()
    fetchSummary()
  }, [])

  return {
    alerts,
    loading,
    error,
    summary,
    fetchAlerts,
    addAlert,
    modifyAlert,
    fetchSummary,
  }
}
