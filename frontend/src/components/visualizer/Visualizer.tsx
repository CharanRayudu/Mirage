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
    { id: '1', position: { x: 0, y: 0 }, data: { label: 'Attacker' }, style: { background: '#ff0055', color: '#fff', border: '1px solid #ff0055' } },
    { id: '2', position: { x: 0, y: 100 }, data: { label: 'MCP Server' }, style: { background: '#00ff9d', color: '#000', border: '1px solid #00ff9d' } },
];

const initialEdges = [{ id: 'e1-2', source: '1', target: '2', animated: true, style: { stroke: '#00ff9d' } }];

export default function Visualizer() {
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

    const onConnect = useCallback(
        (params: Connection | Edge) => setEdges((eds) => addEdge(params, eds)),
        [setEdges],
    );

    return (
        <div style={{ width: '100%', height: '100%' }}>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                fitView
            >
                <Controls style={{ filter: 'invert(1)' }} />
                <MiniMap style={{ filter: 'invert(1)' }} />
                <Background gap={12} size={1} color="#222" />
            </ReactFlow>
        </div>
    );
}
