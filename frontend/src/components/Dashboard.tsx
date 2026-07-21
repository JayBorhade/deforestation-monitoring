'use client'

import React, { useState, useEffect } from 'react'
import { useAlerts } from '@/hooks/useAlerts'
import { usePredictions } from '@/hooks/usePredictions'
import { Alert } from '@/types'

interface StatCard {
  title: string
  value: string | number
  icon: string
  color: string
}

export const Dashboard: React.FC = () => {
  const { alerts, summary } = useAlerts()
  const { predictions, riskDistribution } = usePredictions()
  const [stats, setStats] = useState<StatCard[]>([])

  useEffect(() => {
    if (summary) {
      setStats([
        {
          title: 'Total Alerts',
          value: summary.total || 0,
          icon: '🚨',
          color: 'bg-red-500',
        },
        {
          title: 'Active Alerts',
          value: summary.active || 0,
          icon: '⚠️',
          color: 'bg-orange-500',
        },
        {
          title: 'Critical Alerts',
          value: summary.critical || 0,
          icon: '🔴',
          color: 'bg-red-600',
        },
        {
          title: 'Risk Predictions',
          value: predictions.length,
          icon: '🏘️',
          color: 'bg-blue-500',
        },
      ])
    }
  }, [summary, predictions])

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat, index) => (
        <div key={index} className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">{stat.title}</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
            </div>
            <div className={`${stat.color} text-white p-3 rounded-lg text-2xl`}>
              {stat.icon}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
