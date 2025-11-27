"use client";

import { useEffect, useState } from "react";
import TestingPanel from "@/components/TestingPanel";
import DashboardLayout from "@/components/DashboardLayout";
import LogStream from "@/components/LogStream";

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
      setLogs(data);
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
        setLogs(prevLogs => [...prevLogs, newLog]);
      } catch (error) {
        console.error("Failed to parse incoming log:", error);
      }
    };
    ws.onerror = (error) => console.error("WebSocket error:", error);
    ws.onclose = () => console.log("WebSocket connection closed");

    return () => ws.close();
  }, []);

  return (
    <DashboardLayout>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <LogStream logs={logs} />
        </div>
        <div>
          <TestingPanel />
        </div>
      </div>
    </DashboardLayout>
  );
}
