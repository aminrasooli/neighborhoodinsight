from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import socket
import sys

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {"message": "Hello from Simple Server!"}
        self.wfile.write(json.dumps(response).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=8080):
    try:
        server_address = ('127.0.0.1', port)
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        print(f"Server is running at http://127.0.0.1:{port}")
        print("Press Ctrl+C to stop the server")
        httpd.serve_forever()
    except socket.error as e:
        print(f"Error: Could not start server on port {port}")
        print(f"Details: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()
        sys.exit(0)

if __name__ == "__main__":
    print("Starting server...")
    run_server() 