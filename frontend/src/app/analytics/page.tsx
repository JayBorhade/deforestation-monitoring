'use client'

import React from 'react'
import { Analytics } from '@/components'

export default function AnalyticsPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Analytics</h1>
        <p className="text-gray-600">Comprehensive deforestation trends and statistics</p>
      </div>

      <Analytics />
    </div>
  )
}
