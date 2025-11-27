'use client';
import React, { useEffect, useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import clsx from 'clsx';

export default function Logs() {
    const [logs, setLogs] = useState<string[]>([]);
    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/logs`);
                if (response.ok) {
                    const data = await response.json();
                    // Backend returns [Newest, ..., Oldest]
                    // We want to display [Oldest, ..., Newest] in the terminal
                    const newLogs = Array.isArray(data) ? data : (data.logs || []);
                    setLogs(newLogs.reverse());
                }
            } catch (error) {
                console.error("Failed to fetch logs:", error);
            }
        };

        fetchLogs();
        const interval = setInterval(fetchLogs, 2000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [logs]);

    return (
        <div className="flex-1 overflow-y-auto font-mono text-xs p-2 space-y-1 custom-scrollbar">
            <AnimatePresence initial={false}>
                {logs.map((log, i) => {
                    // Log string from backend already includes timestamp: "[TIMESTAMP] [LEVEL] Message"
                    const logContent = typeof log === 'string' ? log : JSON.stringify(log);
                    const isError = logContent.toLowerCase().includes('error') || logContent.toLowerCase().includes('failed');
                    const isWarning = logContent.toLowerCase().includes('warn');

                    return (
                        <motion.div
                            key={i} // Using index as key is okay here since we replace the whole list
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className={clsx(
                                "border-l-2 pl-2 py-1 transition-colors duration-200",
                                isError ? "border-cyber-alert text-cyber-alert/90 bg-cyber-alert/5" :
                                    isWarning ? "border-yellow-500 text-yellow-500/90" :
                                        "border-cyber-neon/50 text-cyber-neon/80 hover:bg-cyber-neon/5"
                            )}
                        >
                            {logContent}
                        </motion.div>
                    );
                })}
            </AnimatePresence>
            <div ref={bottomRef} />
        </div>
    );
}
