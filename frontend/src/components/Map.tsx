'use client'

import React, { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'
import { MAP_CENTER, MAP_ZOOM } from '@/utils/constants'

const DynamicMap = dynamic(() => import('./DynamicMap'), {
  loading: () => (
    <div className="flex items-center justify-center h-full bg-gray-100">
      <p className="text-gray-500">Loading map...</p>
    </div>
  ),
  ssr: false,
})

export const Map: React.FC = () => {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return (
      <div className="flex items-center justify-center h-full bg-gray-100">
        <p className="text-gray-500">Initializing...</p>
      </div>
    )
  }

  return (
    <div className="w-full h-full">
      <DynamicMap center={MAP_CENTER} zoom={MAP_ZOOM} />
    </div>
  )
}
