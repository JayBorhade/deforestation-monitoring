'use client'

import React, { useState } from 'react'
import { Alert } from '@/types'
import { useAlerts } from '@/hooks/useAlerts'
import {
  formatDate,
  getSeverityBadgeClass,
  getStatusBadgeClass,
} from '@/utils/helpers'

export const AlertsList: React.FC = () => {
  const { alerts, modifyAlert, loading } = useAlerts()
  const [selectedSeverity, setSelectedSeverity] = useState<string | null>(null)
  const [selectedStatus, setSelectedStatus] = useState<string | null>(null)

  const filteredAlerts = alerts.filter((alert) => {
    if (selectedSeverity && alert.severity !== selectedSeverity) return false
    if (selectedStatus && alert.status !== selectedStatus) return false
    return true
  })

  const handleAcknowledge = async (alert: Alert) => {
    await modifyAlert(alert.id, { is_acknowledged: true })
  }

  const handleResolve = async (alert: Alert) => {
    await modifyAlert(alert.id, { status: 'resolved' as const })
  }

  if (loading) {
    return <div className="text-center py-8">Loading alerts...</div>
  }

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="flex gap-4 mb-6">
        <select
          value={selectedSeverity || ''}
          onChange={(e) => setSelectedSeverity(e.target.value || null)}
          className="px-4 py-2 border border-gray-300 rounded-lg"
        >
          <option value="">All Severities</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>

        <select
          value={selectedStatus || ''}
          onChange={(e) => setSelectedStatus(e.target.value || null)}
          className="px-4 py-2 border border-gray-300 rounded-lg"
        >
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="resolved">Resolved</option>
          <option value="ignored">Ignored</option>
        </select>
      </div>

      {/* Alerts List */}
      {filteredAlerts.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          No alerts found
        </div>
      ) : (
        <div className="space-y-3">
          {filteredAlerts.map((alert) => (
            <div key={alert.id} className="card hover:shadow-lg transition">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {alert.title}
                    </h3>
                    <span
                      className={`badge text-xs font-semibold ${
                        alert.severity === 'critical'
                          ? 'bg-red-100 text-red-800'
                          : alert.severity === 'high'
                          ? 'bg-orange-100 text-orange-800'
                          : alert.severity === 'medium'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-green-100 text-green-800'
                      }`}
                    >
                      {alert.severity.toUpperCase()}
                    </span>
                    <span className={`badge text-xs font-semibold ${getStatusBadgeClass(alert.status)}`}>
                      {alert.status.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm mb-2">{alert.description}</p>
                  <div className="flex items-center gap-4 text-xs text-gray-500">
                    <span>📍 {alert.area_hectares.toFixed(2)} ha</span>
                    <span>📅 {formatDate(alert.created_at)}</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  {!alert.is_acknowledged && (
                    <button
                      onClick={() => handleAcknowledge(alert)}
                      className="btn btn-sm bg-blue-500 text-white hover:bg-blue-600"
                    >
                      Acknowledge
                    </button>
                  )}
                  {alert.status !== 'resolved' && (
                    <button
                      onClick={() => handleResolve(alert)}
                      className="btn btn-sm btn-success"
                    >
                      Resolve
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
