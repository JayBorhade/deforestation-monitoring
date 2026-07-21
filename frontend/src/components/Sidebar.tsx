'use client'

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

interface NavItem {
  label: string
  href: string
  icon: string
}

const navItems: NavItem[] = [
  { label: 'Dashboard', href: '/dashboard', icon: '📊' },
  { label: 'Map', href: '/map', icon: '🗺️' },
  { label: 'Analytics', href: '/analytics', icon: '📈' },
  { label: 'Alerts', href: '/alerts', icon: '🚨' },
]

export const Sidebar: React.FC = () => {
  const pathname = usePathname()

  return (
    <aside className="w-64 bg-white border-r border-gray-100 h-full">
      <nav className="space-y-2 p-4">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition ${
              pathname === item.href
                ? 'bg-green-100 text-green-700 font-medium'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  )
}
