from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import time
from datetime import datetime
import os
from data_collectors.real_estate_collector import RealEstateCollector
from ml_model.neighborhood_sentiment import EnhancedNeighborhoodScorer

def get_neighborhood_insights(address):
    """Generate detailed insights for the given address"""
    # Initialize collectors and scorer
    real_estate = RealEstateCollector()
    scorer = EnhancedNeighborhoodScorer()
    
    # Get real estate data - this will always return data (either scraped or estimated)
    real_estate_data = real_estate.get_property_details(address)
    
    # Prepare comprehensive neighborhood data
    neighborhood_data = {
        "address": address,
        "timestamp": datetime.now().isoformat(),
        "crime_analysis": {
            "risk_level": "Low",
            "recent_incidents": [
                {"type": "Theft", "date": "2024-03-01", "severity": "Low"},
                {"type": "Vandalism", "date": "2024-03-02", "severity": "Low"}
            ],
            "trend": "Decreasing",
            "safety_score": 8.5,
            "comparison": "Safer than 85% of nearby neighborhoods"
        },
        "real_estate": real_estate_data,
        "community": {
            "demographics": {
                "population": "25,000",
                "median_age": 35,
                "households": "10,000"
            },
            "education": {
                "schools_rating": 8.2,
                "nearby_schools": [
                    {"name": "Lincoln Elementary", "rating": 9.1},
                    {"name": "Washington Middle", "rating": 8.5},
                    {"name": "Roosevelt High", "rating": 8.8}
                ]
            },
            "amenities": {
                "walkability_score": 85,
                "transit_score": 78,
                "nearby": {
                    "restaurants": 45,
                    "shopping": 12,
                    "parks": 5,
                    "gyms": 8
                }
            },
            "top_complaints": [
                "Traffic during rush hour",
                "Limited parking",
                "Need more green spaces"
            ],
            "positive_aspects": [
                "Good schools",
                "Close to public transport",
                "Active community",
                "Many local events"
            ],
            "recent_reviews": [
                {
                    "text": "Love the community events and friendly neighbors",
                    "date": "2024-03-01",
                    "rating": 5
                },
                {
                    "text": "Great location but parking is becoming an issue",
                    "date": "2024-03-02",
                    "rating": 4
                },
                {
                    "text": "Schools are excellent, kids love it here",
                    "date": "2024-03-01",
                    "rating": 5
                }
            ]
        }
    }
    
    # Calculate neighborhood score using ML-based sentiment analysis
    score_data = scorer.calculate_score(neighborhood_data)
    if score_data:
        neighborhood_data["ml_insights"] = score_data
    
    return neighborhood_data

class NeighborhoodHandler(BaseHTTPRequestHandler):
    def log_request(self, *args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.command} {self.path}")
        
    def _send_json_response(self, data, status=200):
        try:
            self.send_response(status)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        except Exception as e:
            print(f"Error sending response: {e}")

    def _serve_static_file(self, file_path, content_type):
        try:
            with open(file_path, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self._send_json_response({"error": "File not found"}, 404)
        except Exception as e:
            print(f"Error serving static file: {e}")
            self._send_json_response({"error": "Internal server error"}, 500)

    def do_GET(self):
        try:
            if self.path == '/':
                self._serve_static_file('static/index.html', 'text/html')
            elif self.path == '/styles.css':
                self._serve_static_file('static/styles.css', 'text/css')
            elif self.path == '/app.js':
                self._serve_static_file('static/app.js', 'application/javascript')
            elif self.path == '/health':
                self._send_json_response({
                    "status": "healthy",
                    "timestamp": datetime.now().isoformat()
                })
            else:
                self._send_json_response({"error": "Not found"}, 404)
        except Exception as e:
            print(f"Error handling GET request: {e}")
            self._send_json_response({"error": "Internal server error"}, 500)

    def do_POST(self):
        try:
            if self.path == '/insights':
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                
                try:
                    data = json.loads(post_data.decode())
                    address = data.get('address')
                    
                    if not address:
                        self._send_json_response({"error": "Address is required"}, 400)
                        return

                    # Get comprehensive insights
                    insights = get_neighborhood_insights(address)
                    self._send_json_response(insights)
                    
                except json.JSONDecodeError:
                    self._send_json_response({"error": "Invalid JSON data"}, 400)
            else:
                self._send_json_response({"error": "Endpoint not found"}, 404)
        except Exception as e:
            print(f"Error handling POST request: {e}")
            self._send_json_response({"error": "Internal server error"}, 500)

    def do_OPTIONS(self):
        try:
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
        except Exception as e:
            print(f"Error handling OPTIONS request: {e}")

def run_server(port=4000, max_retries=5):
    server = None
    retries = 0
    
    while retries < max_retries:
        try:
            if server is None:
                server_address = ('', port)  # Empty string means all interfaces
                server = HTTPServer(server_address, NeighborhoodHandler)
                
            print(f"\nStarting Neighborhood Insights API on port {port}")
            print("Available endpoints:")
            print("  GET  /        - Web Interface")
            print("  GET  /health  - Health check")
            print("  POST /insights - Get neighborhood insights")
            print("\nPress Ctrl+C to stop the server")
            
            server.serve_forever()
            
        except KeyboardInterrupt:
            print("\nShutting down server gracefully...")
            if server:
                server.server_close()
            sys.exit(0)
            
        except Exception as e:
            print(f"\nError: {e}")
            print(f"Retrying in 5 seconds... (Attempt {retries + 1}/{max_retries})")
            retries += 1
            time.sleep(5)
            
            if server:
                try:
                    server.server_close()
                except:
                    pass
                server = None
    
    print("\nFailed to start server after maximum retries")
    sys.exit(1)

if __name__ == '__main__':
    # Ensure static directory exists
    os.makedirs('static', exist_ok=True)
    run_server() 