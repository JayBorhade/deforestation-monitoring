import type { Metadata } from 'next'
import '@/styles/globals.css'
import { Header } from '@/components/Header'

export const metadata: Metadata = {
  title: 'Deforestation Monitoring Dashboard',
  description: 'AI-powered satellite monitoring for deforestation detection',
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Header />
        <main className="min-h-screen bg-gray-50">
          {children}
        </main>
      </body>
    </html>
  )
}
