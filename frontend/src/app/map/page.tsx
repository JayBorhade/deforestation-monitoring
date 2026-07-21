'use client'

import React from 'react'
import { Map } from '@/components'

export default function MapPage() {
  return (
    <div className="h-screen">
      <div className="absolute top-24 left-8 z-10 bg-white p-4 rounded-lg shadow-lg max-w-xs">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Deforestation Hotspots</h1>
        <p className="text-gray-600 text-sm">
          Real-time satellite imagery showing deforestation areas and risk zones
        </p>
      </div>
      <Map />
    </div>
  )
}
