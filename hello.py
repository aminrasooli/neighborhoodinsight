from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class NeighborhoodHandler(BaseHTTPRequestHandler):
    def _send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path == '/health':
            self._send_json_response({"status": "healthy"})
        else:
            self._send_json_response({
                "message": "Welcome to Neighborhood Insights API",
                "endpoints": {
                    "/health": "Health check",
                    "/insights": "Get neighborhood insights (POST)"
                }
            })

    def do_POST(self):
        if self.path == '/insights':
            # Read the POST data
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                address = data.get('address')
                
                if not address:
                    self._send_json_response({"error": "Address is required"}, 400)
                    return

                # Mock neighborhood insights data
                insights = {
                    "address": address,
                    "crime_analysis": {
                        "risk_level": "Low",
                        "recent_incidents": [
                            {"type": "Theft", "date": "2024-03-01", "severity": "Low"},
                            {"type": "Vandalism", "date": "2024-03-02", "severity": "Low"}
                        ],
                        "trend": "Decreasing"
                    },
                    "real_estate": {
                        "median_price": "$800,000",
                        "price_trend": "+5% (Last 12 months)",
                        "avg_days_on_market": 30,
                        "price_per_sqft": "$450"
                    },
                    "community": {
                        "top_complaints": [
                            "Traffic during rush hour",
                            "Limited parking",
                            "Need more green spaces"
                        ],
                        "positive_aspects": [
                            "Good schools",
                            "Close to public transport",
                            "Active community"
                        ]
                    }
                }
                
                self._send_json_response(insights)
                
            except json.JSONDecodeError:
                self._send_json_response({"error": "Invalid JSON data"}, 400)
            except Exception as e:
                self._send_json_response({"error": "Internal server error"}, 500)
        else:
            self._send_json_response({"error": "Endpoint not found"}, 404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

print('Starting Neighborhood Insights API...')
server = HTTPServer(('localhost', 9000), NeighborhoodHandler)
print('Server running at http://localhost:9000')
print('\nAvailable endpoints:')
print('  GET  /        - API information')
print('  GET  /health  - Health check')
print('  POST /insights - Get neighborhood insights')
print('\nPress Ctrl+C to stop the server')
server.serve_forever() 