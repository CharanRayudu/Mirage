import './globals.css'
import type { Metadata } from 'next'
import { Inter, JetBrains_Mono } from 'next/font/google'
import Sidebar from '@/components/layout/Sidebar'
import Header from '@/components/layout/Header'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const jetbrainsMono = JetBrains_Mono({ subsets: ['latin'], variable: '--font-jetbrains-mono' })

export const metadata: Metadata = {
  title: 'MIRAGE // Agent Zoo',
  description: 'Semantic Honeypot Dashboard',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${jetbrainsMono.variable} bg-cyber-black text-white h-screen w-screen overflow-hidden flex`}>
        <Sidebar />
        <div className="flex-1 flex flex-col h-full relative">
          <div className="absolute inset-0 bg-cyber-grid opacity-20 pointer-events-none" />
          <div className="absolute inset-0 bg-gradient-radial from-cyber-neon/5 to-transparent opacity-50 pointer-events-none" />
          <Header />
          <main className="flex-1 overflow-hidden relative z-0 p-6">
            {children}
          </main>
          <div className="scanline-overlay absolute inset-0 z-50 pointer-events-none opacity-30" />
        </div>
      </body>
    </html>
  )
}
