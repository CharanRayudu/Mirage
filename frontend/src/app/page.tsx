"use client";

import { useEffect, useState } from "react";
import TestingPanel from "@/components/TestingPanel";
import AgentGraph from "@/components/AgentGraph"; // Import the new graph component

interface LogEntry {
  timestamp: string;
  level: string;
  agent_id: string;
  request: {
    method: string;
    path?: string;
    jsonrpc?: string;
    id?: number;
    params?: any;
  };
  event?: string;
  exfil_data?: any;
}

export default function Home() {
  const [logs, setLogs] = useState<LogEntry[]>([]);

  // Initial fetch of historical logs
  const fetchLogs = async () => {
    try {
      const res = await fetch("/api/logs"); 
      const data = await res.json();
      setLogs(data); // The graph logic will handle the order
    } catch (error) {
      console.error("Failed to fetch initial logs:", error);
    }
  };

  useEffect(() => {
    fetchLogs();
    const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${wsProtocol}//${window.location.host}/api/ws`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => console.log("WebSocket connection established");
    ws.onmessage = (event) => {
      try {
        const newLog = JSON.parse(event.data);
        setLogs(prevLogs => [...prevLogs, newLog]); // Append new log
      } catch (error) {
        console.error("Failed to parse incoming log:", error);
      }
    };
    ws.onerror = (error) => console.error("WebSocket error:", error);
    ws.onclose = () => console.log("WebSocket connection closed");

    return () => ws.close();
  }, []);

  return (
    <main className="bg-gray-900 text-white min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">MIRAGE - Agent Zoo</h1>
        
        <TestingPanel />

        {/* Replace the table with the new AgentGraph component */}
        <h2 className="text-2xl font-bold mt-12 mb-4">Agent Activity Graph</h2>
        <AgentGraph logs={logs} />
      </div>
    </main>
  );
}
