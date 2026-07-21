'use client'

import React from 'react'
import { AlertsList } from '@/components'

export default function AlertsPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Alerts</h1>
        <p className="text-gray-600">Deforestation alerts and notifications</p>
      </div>

      <AlertsList />
    </div>
  )
}
