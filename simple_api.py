from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleAPIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        if self.path == '/health':
            self._set_headers()
            response = {"status": "healthy"}
        else:
            self._set_headers()
            response = {
                "message": "Welcome to Neighborhood Insights API",
                "endpoints": {
                    "/health": "Check API health",
                    "/insights": "Get neighborhood insights (POST)"
                }
            }
        
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        if self.path == '/insights':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                address = data.get('address', '')
                
                if not address:
                    self._set_headers(400)
                    response = {"error": "Address is required"}
                else:
                    # Mock response data
                    response = {
                        "address": address,
                        "crime_rate": "Low",
                        "house_prices": "High",
                        "schools": "Excellent"
                    }
                    self._set_headers()
            except json.JSONDecodeError:
                self._set_headers(400)
                response = {"error": "Invalid JSON"}
            
            self.wfile.write(json.dumps(response).encode())
        else:
            self._set_headers(404)
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=3000):
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, SimpleAPIHandler)
    print(f"Server running at http://127.0.0.1:{port}")
    print("Available endpoints:")
    print("  GET  /health - Check API health")
    print("  POST /insights - Get neighborhood insights")
    print("\nPress Ctrl+C to stop the server")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server() 