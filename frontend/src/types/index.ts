export interface SatelliteImage {
  id: string
  tile_id: string
  source: string
  acquisition_date: string
  cloud_coverage: number
  resolution: number
  is_processed: boolean
  processing_date?: string
  created_at: string
  updated_at: string
}

export interface AnalysisResult {
  id: string
  satellite_image_id: string
  model_version: string
  analysis_type: string
  deforestation_percentage: number
  forest_coverage_percentage: number
  degradation_percentage: number
  confidence_score: number
  is_significant_change: boolean
  change_magnitude?: number
  created_at: string
  updated_at: string
}

export interface Alert {
  id: string
  analysis_result_id: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  alert_type: string
  area_hectares: number
  title: string
  description: string
  status: 'active' | 'resolved' | 'ignored'
  is_acknowledged: boolean
  created_at: string
  updated_at: string
  acknowledged_at?: string
}

export interface Prediction {
  id: string
  model_version: string
  prediction_date: string
  valid_until: string
  risk_score: number
  confidence: number
  risk_level: 'low' | 'medium' | 'high' | 'critical'
  is_active: boolean
  created_at: string
}

export interface HealthCheck {
  status: string
  version: string
  environment: string
}

export interface ApiResponse<T> {
  data?: T
  message?: string
  error?: string
}

export interface DashboardStats {
  total_alerts: number
  active_alerts: number
  critical_alerts: number
  total_area_monitored: number
  deforestation_rate: number
  last_analysis: string
}
