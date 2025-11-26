import Visualizer from '@/components/visualizer/Visualizer'
import Logs from '@/components/logs/Logs'

export default function Home() {
  return (
    <main className="flex h-full w-full flex-col p-4 gap-4">
      <header className="flex justify-between items-center border-b border-cyber-gray pb-2">
        <h1 className="text-2xl font-bold cyber-glow">MIRAGE // SYSTEM MONITOR</h1>
        <div className="text-xs text-cyber-pink animate-pulse">STATUS: ACTIVE</div>
      </header>

      <div className="flex flex-1 gap-4 min-h-0">
        <div className="flex-[2] cyber-border bg-cyber-dark/50 rounded p-2 relative">
          <div className="absolute top-2 left-2 text-xs bg-cyber-black px-2 border border-cyber-gray">VISUALIZER</div>
          <Visualizer />
        </div>
        <div className="flex-1 cyber-border bg-cyber-dark/50 rounded p-2 relative flex flex-col">
          <div className="absolute top-2 left-2 text-xs bg-cyber-black px-2 border border-cyber-gray">LIVE LOGS</div>
          <Logs />
        </div>
      </div>
    </main>
  )
}
