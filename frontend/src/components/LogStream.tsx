"use client";

import React from 'react';
import { Terminal } from 'lucide-react';

interface LogEntry {
  timestamp: string;
  level: string;
  agent_id: string;
  request: {
    method: string;
    path?: string;
    params?: any;
  };
  event?: string;
  exfil_data?: any;
}

const LogStream = ({ logs }: { logs: LogEntry[] }) => {
  const getEventColor = (event?: string) => {
    switch (event) {
      case 'PROMPT_INJECTION_SUCCESS':
        return 'bg-red-500';
      case 'TARPIT_TRIGGERED':
        return 'bg-yellow-500';
      default:
        return 'bg-blue-500';
    }
  };

  return (
    <div className="bg-gray-800 shadow-lg rounded-lg p-6 h-[80vh] overflow-y-auto">
      <h2 className="text-2xl font-bold mb-6 text-white">Live Agent Activity</h2>
      <div className="space-y-4">
        {logs.slice().reverse().map((log, index) => (
          <div key={index} className="flex items-start space-x-4 p-4 bg-gray-700 rounded-lg">
            <div className={`flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center ${getEventColor(log.event)}`}>
              <Terminal className="text-white" />
            </div>
            <div className="flex-grow">
              <div className="flex justify-between items-center">
                <span className="font-semibold text-lg text-white">{log.event || log.request.method}</span>
                <span className="text-sm text-gray-400">{new Date(log.timestamp).toLocaleTimeString()}</span>
              </div>
              <p className="text-gray-300">Agent ID: {log.agent_id}</p>
              <pre className="text-xs text-gray-400 bg-gray-900 p-2 rounded mt-2">
                {JSON.stringify(log.request.params || log.request, null, 2)}
              </pre>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LogStream;
