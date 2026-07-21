'use client'

import React, { useState, useEffect } from 'react'
import { Line, Bar, Doughnut } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js'
import { useAlerts } from '@/hooks/useAlerts'
import { usePredictions } from '@/hooks/usePredictions'
import { getAlertCountBySeverity, getPredictionCountByRisk } from '@/utils/helpers'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

export const Analytics: React.FC = () => {
  const { alerts } = useAlerts()
  const { predictions } = usePredictions()
  const [alertData, setAlertData] = useState(null)
  const [riskData, setRiskData] = useState(null)

  useEffect(() => {
    if (alerts.length > 0) {
      const counts = getAlertCountBySeverity(alerts)
      setAlertData({
        labels: ['Low', 'Medium', 'High', 'Critical'],
        datasets: [
          {
            label: 'Alerts by Severity',
            data: [
              counts.low || 0,
              counts.medium || 0,
              counts.high || 0,
              counts.critical || 0,
            ],
            backgroundColor: ['#10b981', '#f59e0b', '#ef4444', '#991b1b'],
          },
        ],
      })
    }
  }, [alerts])

  useEffect(() => {
    if (predictions.length > 0) {
      const counts = getPredictionCountByRisk(predictions)
      setRiskData({
        labels: ['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk'],
        datasets: [
          {
            label: 'Predictions by Risk Level',
            data: [
              counts.low || 0,
              counts.medium || 0,
              counts.high || 0,
              counts.critical || 0,
            ],
            backgroundColor: ['#10b981', '#f59e0b', '#ef4444', '#991b1b'],
            borderColor: ['#059669', '#d97706', '#dc2626', '#7f1d1d'],
            borderWidth: 2,
          },
        ],
      })
    }
  }, [predictions])

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Alerts by Severity</h3>
        <div className="relative h-64">
          {alertData ? (
            <Doughnut data={alertData} options={{ maintainAspectRatio: false }} />
          ) : (
            <p className="text-gray-500 text-center py-8">No data available</p>
          )}
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Predictions</h3>
        <div className="relative h-64">
          {riskData ? (
            <Doughnut data={riskData} options={{ maintainAspectRatio: false }} />
          ) : (
            <p className="text-gray-500 text-center py-8">No data available</p>
          )}
        </div>
      </div>
    </div>
  )
}
