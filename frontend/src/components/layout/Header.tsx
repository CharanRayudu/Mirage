import React from 'react';
import { Bell, Wifi, ShieldCheck, Clock } from 'lucide-react';

const Header = () => {
    return (
        <header className="h-16 w-full flex items-center justify-between px-6 glass-panel border-b border-cyber-gray/50 z-10">
            <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-cyber-neon/10 border border-cyber-neon/20">
                    <div className="w-2 h-2 rounded-full bg-cyber-neon animate-pulse" />
                    <span className="text-xs font-mono text-cyber-neon tracking-wider">SYSTEM ONLINE</span>
                </div>
                <div className="h-4 w-[1px] bg-gray-700" />
                <div className="text-xs text-gray-400 font-mono flex items-center gap-2">
                    <ShieldCheck size={14} className="text-cyber-cyan" />
                    <span>SECURITY LEVEL: <span className="text-white">MAXIMUM</span></span>
                </div>
            </div>

            <div className="flex items-center gap-6">
                <div className="flex items-center gap-2 text-gray-400 font-mono text-sm">
                    <Clock size={16} />
                    <span>23:42:15 UTC</span>
                </div>

                <div className="flex items-center gap-4">
                    <button className="relative p-2 text-gray-400 hover:text-white transition-colors">
                        <Bell size={20} />
                        <span className="absolute top-1 right-1 w-2 h-2 bg-cyber-alert rounded-full animate-ping" />
                        <span className="absolute top-1 right-1 w-2 h-2 bg-cyber-alert rounded-full" />
                    </button>
                    <div className="flex items-center gap-2 text-cyber-cyan">
                        <Wifi size={20} />
                        <span className="text-xs font-mono">CONNECTED</span>
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Header;
