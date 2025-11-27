'use client';
import React, { useEffect, useState } from 'react';

export default function Logs() {
    const [logs, setLogs] = useState<string[]>([]);

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/logs`);
                if (response.ok) {
                    const data = await response.json();
                    setLogs(data.logs || []);
                }
            } catch (error) {
                console.error("Failed to fetch logs:", error);
            }
        };

        // Fetch immediately
        fetchLogs();

        // Poll every 2 seconds
        const interval = setInterval(fetchLogs, 2000);

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
