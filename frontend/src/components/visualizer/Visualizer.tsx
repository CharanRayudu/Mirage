'use client';
import React, { useCallback } from 'react';
import ReactFlow, {
    MiniMap,
    Controls,
    Background,
    useNodesState,
    useEdgesState,
    addEdge,
    Connection,
    Edge,
} from 'reactflow';
import 'reactflow/dist/style.css';

const initialNodes = [
    {
        id: '1',
        position: { x: 100, y: 100 },
        data: { label: 'Attacker (IP: 192.168.1.5)' },
        style: {
            background: '#050505',
            color: '#ff0055',
            border: '1px solid #ff0055',
            boxShadow: '0 0 15px rgba(255, 0, 85, 0.3)',
            borderRadius: '8px',
            fontFamily: 'var(--font-mono)',
            width: 180,
        }
    },
    {
        id: '2',
        position: { x: 400, y: 200 },
        data: { label: 'Mirage Gateway' },
        style: {
            background: '#050505',
            color: '#00ff9d',
            border: '1px solid #00ff9d',
            boxShadow: '0 0 15px rgba(0, 255, 157, 0.3)',
            borderRadius: '8px',
            fontFamily: 'var(--font-mono)',
            width: 180,
        }
    },
    {
        id: '3',
        position: { x: 600, y: 100 },
        data: { label: 'Honeypot DB' },
        style: {
            background: '#050505',
            color: '#bd00ff',
            border: '1px solid #bd00ff',
            boxShadow: '0 0 15px rgba(189, 0, 255, 0.3)',
            borderRadius: '8px',
            fontFamily: 'var(--font-mono)',
            width: 180,
        }
    },
];

const initialEdges = [
    {
        id: 'e1-2',
        source: '1',
        target: '2',
        animated: true,
        style: { stroke: '#ff0055', strokeWidth: 2 }
    },
    {
        id: 'e2-3',
        source: '2',
        target: '3',
        animated: true,
        style: { stroke: '#00ff9d', strokeWidth: 2 }
    }
];

export default function Visualizer() {
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

    const onConnect = useCallback(
        (params: Connection | Edge) => setEdges((eds) => addEdge(params, eds)),
        [setEdges],
    );

    return (
        <div style={{ width: '100%', height: '100%' }} className="bg-cyber-black/50 relative">
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                fitView
                className="react-flow-cyber"
            >
                <Controls className="!bg-cyber-black !border-cyber-gray !fill-cyber-neon [&>button]:!border-cyber-gray [&>button:hover]:!bg-cyber-gray" />
                <MiniMap
                    nodeColor={(n) => {
                        if (n.style?.background) return n.style.background as string;
                        return '#fff';
                    }}
                    maskColor="rgba(5, 5, 5, 0.8)"
                    className="!bg-cyber-black !border !border-cyber-gray"
                />
                <Background gap={20} size={1} color="#1a1a1a" />
            </ReactFlow>
        </div>
    );
}
