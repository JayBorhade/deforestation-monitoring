'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { APP_NAME } from '@/utils/constants'

export const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  return (
    <header className="bg-white shadow-sm border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-lg">🌍</span>
          </div>
          <h1 className="text-2xl font-bold text-gray-900">{APP_NAME}</h1>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center space-x-8">
          <Link href="/dashboard" className="text-gray-600 hover:text-green-500 transition">
            Dashboard
          </Link>
          <Link href="/map" className="text-gray-600 hover:text-green-500 transition">
            Map
          </Link>
          <Link href="/analytics" className="text-gray-600 hover:text-green-500 transition">
            Analytics
          </Link>
          <Link href="/alerts" className="text-gray-600 hover:text-green-500 transition">
            Alerts
          </Link>
          <button className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition">
            Settings
          </button>
        </nav>

        {/* Mobile Menu Button */}
        <button
          className="md:hidden p-2"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </button>
      </div>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <nav className="md:hidden bg-gray-50 border-t border-gray-100 px-4 py-4 space-y-4">
          <Link href="/dashboard" className="block text-gray-600 hover:text-green-500">
            Dashboard
          </Link>
          <Link href="/map" className="block text-gray-600 hover:text-green-500">
            Map
          </Link>
          <Link href="/analytics" className="block text-gray-600 hover:text-green-500">
            Analytics
          </Link>
          <Link href="/alerts" className="block text-gray-600 hover:text-green-500">
            Alerts
          </Link>
        </nav>
      )}
    </header>
  )
}
