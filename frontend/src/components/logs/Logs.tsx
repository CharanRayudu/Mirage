'use client';
import React, { useEffect, useState } from 'react';

export default function Logs() {
    const [logs, setLogs] = useState<string[]>([]);

    useEffect(() => {
        // Mock logs for now
        const interval = setInterval(() => {
            const newLog = `[${new Date().toLocaleTimeString()}] ATTACK DETECTED: Source IP 192.168.1.${Math.floor(Math.random() * 255)}`;
            setLogs((prev) => [newLog, ...prev].slice(0, 50));
        }, 2000);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="flex-1 overflow-y-auto font-mono text-xs p-2 space-y-1 mt-6">
            {logs.map((log, i) => (
                <div key={i} className="border-b border-cyber-gray/30 pb-1 text-cyber-neon/80 hover:bg-cyber-gray/20 transition-colors">
                    {log}
                </div>
            ))}
        </div>
    );
}
