import './globals.css'
import type { Metadata } from 'next'

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
      <body className="bg-cyber-black text-cyber-neon h-screen w-screen overflow-hidden">
        {children}
      </body>
    </html>
  )
}
