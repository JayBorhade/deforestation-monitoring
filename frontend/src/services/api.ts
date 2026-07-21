import axios, { AxiosInstance, AxiosError } from 'axios'
import {
  SatelliteImage,
  AnalysisResult,
  Alert,
  Prediction,
  HealthCheck,
  DashboardStats,
} from '@/types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api: AxiosInstance = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for adding auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Health Check
export const healthCheck = async (): Promise<HealthCheck> => {
  const response = await api.get('/health')
  return response.data
}

// Satellite Images
export const getSatelliteImages = async (skip = 0, limit = 50): Promise<SatelliteImage[]> => {
  const response = await api.get('/satellite-images', {
    params: { skip, limit },
  })
  return response.data
}

export const getSatelliteImage = async (imageId: string): Promise<SatelliteImage> => {
  const response = await api.get(`/satellite-images/${imageId}`)
  return response.data
}

export const createSatelliteImage = async (data: Partial<SatelliteImage>): Promise<SatelliteImage> => {
  const response = await api.post('/satellite-images', data)
  return response.data
}

// Analysis Results
export const getAnalysisResults = async (skip = 0, limit = 50): Promise<AnalysisResult[]> => {
  const response = await api.get('/analysis-results', {
    params: { skip, limit },
  })
  return response.data
}

export const getAnalysisResult = async (resultId: string): Promise<AnalysisResult> => {
  const response = await api.get(`/analysis-results/${resultId}`)
  return response.data
}

export const createAnalysisResult = async (data: Partial<AnalysisResult>): Promise<AnalysisResult> => {
  const response = await api.post('/analysis-results', data)
  return response.data
}

// Alerts
export const getAlerts = async (
  skip = 0,
  limit = 50,
  severity?: string,
  status?: string
): Promise<Alert[]> => {
  const response = await api.get('/alerts', {
    params: { skip, limit, severity, status_filter: status },
  })
  return response.data
}

export const getAlert = async (alertId: string): Promise<Alert> => {
  const response = await api.get(`/alerts/${alertId}`)
  return response.data
}

export const createAlert = async (data: Partial<Alert>): Promise<Alert> => {
  const response = await api.post('/alerts', data)
  return response.data
}

export const updateAlert = async (
  alertId: string,
  data: Partial<Alert>
): Promise<Alert> => {
  const response = await api.patch(`/alerts/${alertId}`, data)
  return response.data
}

export const getAlertsSummary = async () => {
  const response = await api.get('/alerts/stats/summary')
  return response.data
}

// Predictions
export const getPredictions = async (
  skip = 0,
  limit = 50,
  riskLevel?: string,
  isActive = true
): Promise<Prediction[]> => {
  const response = await api.get('/predictions', {
    params: { skip, limit, risk_level: riskLevel, is_active: isActive },
  })
  return response.data
}

export const getPrediction = async (predictionId: string): Promise<Prediction> => {
  const response = await api.get(`/predictions/${predictionId}`)
  return response.data
}

export const getRiskDistribution = async () => {
  const response = await api.get('/predictions/stats/risk-distribution')
  return response.data
}

export default api
