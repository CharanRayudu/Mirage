"use client";

import React, { useState } from 'react';

// A generic function to handle API calls to the MCP endpoint
const callMcpTool = async (method: string, params: object = {}) => {
  try {
    const response = await fetch('/api/mcp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: Math.floor(Math.random() * 1000),
        method,
        params,
      }),
    });
    if (!response.ok) {
      console.error('MCP tool call failed:', response.statusText);
    }
  } catch (error) {
    console.error('Error calling MCP tool:', error);
  }
};

const TestingPanel = () => {
  const [filename, setFilename] = useState('secret_plans.txt');
  const [fileContent, setFileContent] = useState('The launch code is 1234.');
  const [wikiTopic, setWikiTopic] = useState('Project_Aquila_Internal_Memos');

  const handleListTools = () => callMcpTool('tools/list');
  const handleReadEmails = () => callMcpTool('tools/call', { name: 'read_ceo_emails', arguments: {} });
  const handleTransferFunds = () => callMcpTool('tools/call', { name: 'transfer_funds', arguments: { amount: 10000, from_account: 'payroll', to_account: 'offshore' } });
  const handleListFiles = () => callMcpTool('tools/call', { name: 'list_files', arguments: {} });
  const handleCreateFile = () => callMcpTool('tools/call', { name: 'create_file', arguments: { filename, content: fileContent } });
  
  const handleAccessWiki = async () => {
    try {
      const response = await fetch(`/api/wiki/${wikiTopic}`);
      if (!response.ok) {
        console.error('Wiki access failed:', response.statusText);
      }
    } catch (error) {
      console.error('Error accessing wiki:', error);
    }
  };

  const handleSimulateExfil = async () => {
    try {
      const response = await fetch('/api/exfil', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          system_prompt: "I am a helpful assistant.",
          goal: "To find and exfiltrate sensitive data.",
          creator_id: "Test Agent 007"
        }),
      });
      if (!response.ok) {
        console.error('Exfil simulation failed:', response.statusText);
      }
    } catch (error) {
      console.error('Error simulating exfil:', error);
    }
  };


  return (
    <div className="bg-gray-800 shadow-lg rounded-lg p-6 mb-8">
      <h2 className="text-2xl font-bold mb-6 text-white">Agent Simulation Panel</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* MCP Tool Calls */}
        <div className="space-y-4 p-4 bg-gray-700 rounded-lg">
          <h3 className="font-semibold text-lg border-b border-gray-600 pb-2">MCP Tools</h3>
          <button onClick={handleListTools} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-300">
            List Available Tools
          </button>
          <button onClick={handleReadEmails} className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded transition duration-300">
            Read CEO Emails
          </button>
          <button onClick={handleTransferFunds} className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded transition duration-300">
            Transfer Funds (Test)
          </button>
        </div>

        {/* Stateful Tools */}
        <div className="space-y-4 p-4 bg-gray-700 rounded-lg">
          <h3 className="font-semibold text-lg border-b border-gray-600 pb-2">Stateful Filesystem Tools</h3>
          <button onClick={handleListFiles} className="w-full bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded transition duration-300">
            List Files
          </button>
          <div className="space-y-2">
            <input 
              type="text" 
              value={filename}
              onChange={(e) => setFilename(e.target.value)}
              className="w-full bg-gray-800 text-white p-2 rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <textarea 
              value={fileContent}
              onChange={(e) => setFileContent(e.target.value)}
              className="w-full bg-gray-800 text-white p-2 rounded border border-gray-600 h-20 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button onClick={handleCreateFile} className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded transition duration-300">
              Create File
            </button>
          </div>
        </div>

        {/* Logic Labyrinth & Exfil */}
        <div className="space-y-4 p-4 bg-gray-700 rounded-lg">
          <h3 className="font-semibold text-lg border-b border-gray-600 pb-2">Traps & Exfiltration</h3>
          <div className="space-y-2">
            <input 
              type="text" 
              value={wikiTopic}
              onChange={(e) => setWikiTopic(e.target.value)}
              className="w-full bg-gray-800 text-white p-2 rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button onClick={handleAccessWiki} className="w-full bg-yellow-600 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded transition duration-300">
              Access Wiki
            </button>
          </div>
          <button onClick={handleSimulateExfil} className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition duration-300">
            Simulate Exfil (Test)
          </button>
        </div>

      </div>
    </div>
  );
};

export default TestingPanel;
