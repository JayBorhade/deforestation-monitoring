'use client'

import React from 'react'
import { Dashboard, Analytics } from '@/components'

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">Overview of deforestation monitoring metrics</p>
      </div>

      <Dashboard />

      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Analytics</h2>
        <Analytics />
      </div>
    </div>
  )
}
