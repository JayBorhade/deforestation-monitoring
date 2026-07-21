export const APP_NAME = process.env.NEXT_PUBLIC_APP_NAME || 'Deforestation Monitoring'
export const APP_VERSION = process.env.NEXT_PUBLIC_APP_VERSION || '0.1.0'

export const SEVERITY_LEVELS = {
  low: { label: 'Low', color: '#10b981', bgColor: '#d1fae5' },
  medium: { label: 'Medium', color: '#f59e0b', bgColor: '#fef3c7' },
  high: { label: 'High', color: '#ef4444', bgColor: '#fee2e2' },
  critical: { label: 'Critical', color: '#991b1b', bgColor: '#fecaca' },
}

export const RISK_LEVELS = {
  low: { label: 'Low Risk', color: '#10b981', bgColor: '#d1fae5' },
  medium: { label: 'Medium Risk', color: '#f59e0b', bgColor: '#fef3c7' },
  high: { label: 'High Risk', color: '#ef4444', bgColor: '#fee2e2' },
  critical: { label: 'Critical Risk', color: '#991b1b', bgColor: '#fecaca' },
}

export const STATUS_COLORS = {
  active: '#ef4444',
  resolved: '#10b981',
  ignored: '#9ca3af',
}

export const MAP_CENTER = {
  lat: 20,
  lng: 0,
}

export const MAP_ZOOM = 4

export const CHART_COLORS = {
  primary: '#10b981',
  secondary: '#059669',
  success: '#10b981',
  warning: '#f59e0b',
  danger: '#ef4444',
  info: '#3b82f6',
  light: '#f3f4f6',
  dark: '#111827',
}

export const DATE_FORMAT = 'MMM dd, yyyy'
export const DATETIME_FORMAT = 'MMM dd, yyyy HH:mm'
