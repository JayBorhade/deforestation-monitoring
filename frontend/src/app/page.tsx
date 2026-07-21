import React from 'react'
import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 py-20">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-block bg-green-100 rounded-full px-4 py-2 mb-4">
            <span className="text-green-700 font-medium text-sm">🌍 AI-Powered Monitoring</span>
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Deforestation Monitoring Dashboard
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
            Real-time satellite analysis, predictive hotspot detection, and comprehensive deforestation monitoring powered by AI
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link
              href="/dashboard"
              className="btn btn-lg btn-primary"
            >
              🚀 Go to Dashboard
            </Link>
            <Link
              href="/map"
              className="btn btn-lg bg-blue-500 text-white hover:bg-blue-600"
            >
              🗺️ View Map
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mt-20">
          <div className="card">
            <div className="text-4xl mb-4">🛰️</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Satellite Analysis</h3>
            <p className="text-gray-600">
              Real-time processing of Sentinel-2, Landsat, and other satellite imagery for accurate deforestation detection
            </p>
          </div>

          <div className="card">
            <div className="text-4xl mb-4">🤖</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">AI Detection</h3>
            <p className="text-gray-600">
              Advanced U-Net deep learning models for precise deforestation segmentation and classification
            </p>
          </div>

          <div className="card">
            <div className="text-4xl mb-4">📈</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Predictive Analytics</h3>
            <p className="text-gray-600">
              Machine learning-based hotspot predictions to identify high-risk deforestation areas before they occur
            </p>
          </div>

          <div className="card">
            <div className="text-4xl mb-4">🚨</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Alert System</h3>
            <p className="text-gray-600">
              Automated alerts for significant deforestation events with severity levels and actionable recommendations
            </p>
          </div>

          <div className="card">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Analytics Dashboard</h3>
            <p className="text-gray-600">
              Comprehensive statistics, trends, and visualizations for data-driven decision making
            </p>
          </div>

          <div className="card">
            <div className="text-4xl mb-4">🗺️</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Interactive Maps</h3>
            <p className="text-gray-600">
              Geospatial visualization with GIS layers, zoom controls, and real-time updates
            </p>
          </div>
        </div>

        {/* Stats Section */}
        <div className="grid md:grid-cols-4 gap-6 mt-20 text-center">
          <div>
            <div className="text-4xl font-bold text-green-600 mb-2">150K+</div>
            <p className="text-gray-600">Images Processed</p>
          </div>
          <div>
            <div className="text-4xl font-bold text-blue-600 mb-2">2.5M</div>
            <p className="text-gray-600">Hectares Monitored</p>
          </div>
          <div>
            <div className="text-4xl font-bold text-orange-600 mb-2">95%</div>
            <p className="text-gray-600">Accuracy Rate</p>
          </div>
          <div>
            <div className="text-4xl font-bold text-red-600 mb-2">48hrs</div>
            <p className="text-gray-600">Alert Response Time</p>
          </div>
        </div>
      </div>
    </div>
  )
}
