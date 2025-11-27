import http.server
import socketserver
import json
import urllib.parse
from app.core.config import settings
from app.mcp.router import list_tools_logic, call_tool_logic

PORT = settings.MCP_SERVER_PORT

class MirageHandler(http.server.SimpleHTTPRequestHandler):


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            body = json.loads(post_data.decode('utf-8'))
        except:
            body = {}
        
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        # CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        if path == "/mcp/tools/call":
            result = call_tool_logic(body)
            if "error" in result and "code" in result:
                # We are sending 200 OK even for errors to simplify, or we could set status
                # But for now, let's just return the error object
                pass
            self.wfile.write(json.dumps(result).encode())
            return

        self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        if path == "/":
            self.wfile.write(json.dumps({"message": "Welcome to MIRAGE (http.server edition)"}).encode())
            return

        if path == "/mcp/tools":
            result = list_tools_logic()
            self.wfile.write(json.dumps(result).encode())
            return

        if path == "/logs":
            from app.core.logger import logger
            self.wfile.write(json.dumps({"logs": logger.get_logs()}).encode())
            return
            
        # 404
        self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

print(f"Starting MIRAGE Backend on port {PORT}")
with socketserver.TCPServer(("", PORT), MirageHandler) as httpd:
    httpd.serve_forever()
