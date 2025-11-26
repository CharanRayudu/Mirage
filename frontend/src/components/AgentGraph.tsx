"use client";

import React, { useMemo } from 'react';
import ReactFlow, { MiniMap, Controls, Background, Node, Edge } from 'reactflow';
import 'reactflow/dist/style.css';

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
}

const AgentGraph = ({ logs }: { logs: LogEntry[] }) => {
  const { nodes, edges } = useMemo(() => {
    const graphNodes: Node[] = [];
    const graphEdges: Edge[] = [];
    
    // Group logs by agent
    const logsByAgent: { [key: string]: LogEntry[] } = {};
    logs.forEach(log => {
      if (!logsByAgent[log.agent_id]) {
        logsByAgent[log.agent_id] = [];
      }
      logsByAgent[log.agent_id].push(log);
    });

    let yPos = 0;
    Object.keys(logsByAgent).forEach((agentId, agentIndex) => {
      const agentLogs = logsByAgent[agentId];
      let xPos = 0;
      
      // Create a "start" node for each agent
      const startNodeId = `start-${agentId}`;
      graphNodes.push({
        id: startNodeId,
        position: { x: xPos, y: yPos },
        data: { label: `Agent: ${agentId}` },
        style: { background: '#2d3748', color: 'white', border: '1px solid #4a5568' },
      });

      agentLogs.forEach((log, index) => {
        const nodeId = `${agentId}-${index}`;
        const prevNodeId = index === 0 ? startNodeId : `${agentId}-${index - 1}`;
        
        xPos += 300;

        graphNodes.push({
          id: nodeId,
          position: { x: xPos, y: yPos },
          data: { label: `${log.event || log.request.method}\n${log.request.path || log.request.params?.name || ''}` },
          style: {
            background: log.event === "PROMPT_INJECTION_SUCCESS" ? '#c53030' : log.event === "TARPIT_TRIGGERED" ? '#d69e2e' : '#2b6cb0',
            color: 'white',
            border: '1px solid #4a5568',
            width: 200,
          },
        });

        graphEdges.push({
          id: `e-${prevNodeId}-${nodeId}`,
          source: prevNodeId,
          target: nodeId,
          animated: true,
        });
      });
      yPos += 200; // Offset the next agent's graph vertically
    });

    return { nodes: graphNodes, edges: graphEdges };
  }, [logs]);

  return (
    <div style={{ height: '80vh' }} className="bg-gray-800 rounded-lg shadow-lg">
      <ReactFlow nodes={nodes} edges={edges}>
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
    </div>
  );
};

export default AgentGraph;
