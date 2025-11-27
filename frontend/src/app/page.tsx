import Visualizer from '@/components/visualizer/Visualizer'
import Logs from '@/components/logs/Logs'
import Card from '@/components/ui/Card'
import { Activity, Terminal } from 'lucide-react'

export default function Home() {
  return (
    <div className="grid grid-cols-12 grid-rows-12 gap-6 h-full w-full">
      {/* Main Visualizer Area */}
      <div className="col-span-8 row-span-8">
        <Card title="NETWORK VISUALIZER" className="h-full" action={<Activity size={16} className="text-cyber-neon" />}>
          <Visualizer />
        </Card>
      </div>

      {/* Stats / Quick Info */}
      <div className="col-span-4 row-span-4 flex flex-col gap-6">
        <Card title="ACTIVE THREATS" className="flex-1 bg-cyber-alert/5 border-cyber-alert/20">
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="text-5xl font-mono font-bold text-cyber-alert glow-text mb-2">0</div>
              <div className="text-xs text-gray-400 tracking-widest">DETECTED INTRUSIONS</div>
            </div>
          </div>
        </Card>
        <Card title="SYSTEM LOAD" className="flex-1">
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="text-5xl font-mono font-bold text-cyber-cyan glow-text mb-2">12%</div>
              <div className="text-xs text-gray-400 tracking-widest">CPU USAGE</div>
            </div>
          </div>
        </Card>
      </div>

      {/* Logs Console */}
      <div className="col-span-4 row-span-8">
        <Card title="LIVE TERMINAL" className="h-full" action={<Terminal size={16} className="text-cyber-neon" />}>
          <Logs />
        </Card>
      </div>

      {/* Bottom Panel (e.g. Timeline or more stats) */}
      <div className="col-span-8 row-span-4">
        <Card title="EVENT TIMELINE" className="h-full">
          <div className="flex items-center justify-center h-full text-gray-500 font-mono text-sm">
            [NO RECENT EVENTS RECORDED]
          </div>
        </Card>
      </div>
    </div>
  )
}
