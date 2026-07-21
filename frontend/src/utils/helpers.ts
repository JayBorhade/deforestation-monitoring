import { Alert, Prediction } from '@/types'
import { format, parseISO } from 'date-fns'
import { DATE_FORMAT, DATETIME_FORMAT } from './constants'

export const formatDate = (date: string | Date): string => {
  try {
    const parsed = typeof date === 'string' ? parseISO(date) : date
    return format(parsed, DATE_FORMAT)
  } catch (error) {
    return 'N/A'
  }
}

export const formatDateTime = (date: string | Date): string => {
  try {
    const parsed = typeof date === 'string' ? parseISO(date) : date
    return format(parsed, DATETIME_FORMAT)
  } catch (error) {
    return 'N/A'
  }
}

export const formatNumber = (num: number, decimals = 2): string => {
  return num.toFixed(decimals)
}

export const formatPercentage = (num: number, decimals = 1): string => {
  return `${num.toFixed(decimals)}%`
}

export const formatArea = (hectares: number): string => {
  if (hectares >= 1000) {
    return `${(hectares / 1000).toFixed(2)} km²`
  }
  return `${hectares.toFixed(2)} ha`
}

export const getSeverityColor = (severity: string): string => {
  const colors: Record<string, string> = {
    low: '#10b981',
    medium: '#f59e0b',
    high: '#ef4444',
    critical: '#991b1b',
  }
  return colors[severity] || '#9ca3af'
}

export const getRiskColor = (riskLevel: string): string => {
  const colors: Record<string, string> = {
    low: '#10b981',
    medium: '#f59e0b',
    high: '#ef4444',
    critical: '#991b1b',
  }
  return colors[riskLevel] || '#9ca3af'
}

export const getStatusBadgeClass = (status: string): string => {
  switch (status) {
    case 'active':
      return 'bg-red-100 text-red-800'
    case 'resolved':
      return 'bg-green-100 text-green-800'
    case 'ignored':
      return 'bg-gray-100 text-gray-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

export const getSeverityBadgeClass = (severity: string): string => {
  switch (severity) {
    case 'critical':
      return 'bg-red-100 text-red-800'
    case 'high':
      return 'bg-orange-100 text-orange-800'
    case 'medium':
      return 'bg-yellow-100 text-yellow-800'
    case 'low':
      return 'bg-green-100 text-green-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

export const getRiskBadgeClass = (riskLevel: string): string => {
  switch (riskLevel) {
    case 'critical':
      return 'bg-red-100 text-red-800'
    case 'high':
      return 'bg-orange-100 text-orange-800'
    case 'medium':
      return 'bg-yellow-100 text-yellow-800'
    case 'low':
      return 'bg-green-100 text-green-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

export const getAlertCountByStatus = (alerts: Alert[]): Record<string, number> => {
  return alerts.reduce(
    (acc, alert) => {
      acc[alert.status] = (acc[alert.status] || 0) + 1
      return acc
    },
    {} as Record<string, number>
  )
}

export const getAlertCountBySeverity = (alerts: Alert[]): Record<string, number> => {
  return alerts.reduce(
    (acc, alert) => {
      acc[alert.severity] = (acc[alert.severity] || 0) + 1
      return acc
    },
    {} as Record<string, number>
  )
}

export const getPredictionCountByRisk = (predictions: Prediction[]): Record<string, number> => {
  return predictions.reduce(
    (acc, prediction) => {
      acc[prediction.risk_level] = (acc[prediction.risk_level] || 0) + 1
      return acc
    },
    {} as Record<string, number>
  )
}
