import React from 'react';
import { LayoutDashboard, Terminal, Settings, Activity, ShieldAlert } from 'lucide-react';
import clsx from 'clsx';

interface SidebarProps {
    className?: string;
}

const Sidebar: React.FC<SidebarProps> = ({ className }) => {
    const navItems = [
        { icon: LayoutDashboard, label: 'Dashboard', active: true },
        { icon: Terminal, label: 'Live Logs', active: false },
        { icon: Activity, label: 'Network Graph', active: false },
        { icon: ShieldAlert, label: 'Threat Intel', active: false },
        { icon: Settings, label: 'System Config', active: false },
    ];

    return (
        <aside className={clsx("w-64 h-full flex flex-col glass-panel border-r border-cyber-gray/50", className)}>
            <div className="p-6 border-b border-cyber-gray/30">
                <h1 className="text-2xl font-bold tracking-tighter text-cyber-neon glow-text">
                    MIRAGE<span className="text-cyber-pink">_OS</span>
                </h1>
                <div className="text-xs text-cyber-gray mt-1 tracking-widest">V.2.0.4 [STABLE]</div>
            </div>

            <nav className="flex-1 p-4 space-y-2">
                {navItems.map((item, index) => (
                    <button
                        key={index}
                        className={clsx(
                            "w-full flex items-center gap-3 px-4 py-3 rounded-md transition-all duration-300 group",
                            item.active
                                ? "bg-cyber-neon/10 text-cyber-neon border border-cyber-neon/20 shadow-[0_0_15px_rgba(0,255,157,0.1)]"
                                : "text-gray-400 hover:text-white hover:bg-white/5"
                        )}
                    >
                        <item.icon size={20} className={clsx("transition-transform group-hover:scale-110", item.active && "animate-pulse-slow")} />
                        <span className="font-mono text-sm tracking-wide">{item.label}</span>
                        {item.active && <div className="ml-auto w-1.5 h-1.5 rounded-full bg-cyber-neon shadow-[0_0_5px_#00ff9d]" />}
                    </button>
                ))}
            </nav>

            <div className="p-4 border-t border-cyber-gray/30">
                <div className="bg-black/40 rounded p-3 border border-cyber-gray/20">
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-xs text-gray-500 font-mono">CPU LOAD</span>
                        <span className="text-xs text-cyber-cyan font-mono">34%</span>
                    </div>
                    <div className="w-full h-1 bg-gray-800 rounded-full overflow-hidden">
                        <div className="h-full bg-cyber-cyan w-[34%] shadow-[0_0_10px_#00f2ea]" />
                    </div>

                    <div className="flex justify-between items-center mt-3 mb-2">
                        <span className="text-xs text-gray-500 font-mono">MEMORY</span>
                        <span className="text-xs text-cyber-pink font-mono">62%</span>
                    </div>
                    <div className="w-full h-1 bg-gray-800 rounded-full overflow-hidden">
                        <div className="h-full bg-cyber-pink w-[62%] shadow-[0_0_10px_#bd00ff]" />
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;
