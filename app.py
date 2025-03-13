from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from data_collection import fetch_crime_data, fetch_real_estate_data, fetch_resident_complaints

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Welcome to Neighborhood Insights API"}), 200

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route("/get_insights", methods=["POST"])
def get_insights():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        address = data.get("address")
        if not address:
            return jsonify({"error": "Address is required"}), 400
        
        # Extract city from address (simple implementation)
        city = address.split(",")[0].strip()
        
        # Fetch all data
        crime_data = fetch_crime_data(city)
        real_estate_trends = fetch_real_estate_data()
        complaints = fetch_resident_complaints()
        
        # Process and analyze the data
        insights = {
            "crime_analysis": {
                "recent_incidents": crime_data.to_dict("records"),
                "risk_level": "Medium",
                "trend": "Decreasing"
            },
            "real_estate_trends": real_estate_trends,
            "resident_complaints": {
                "top_complaints": complaints,
                "total_complaints": len(complaints)
            }
        }
        
        return jsonify(insights)
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    try:
        print("Starting Neighborhood Insights API...")
        print("Server will be available at http://localhost:3000")
        # Use 0.0.0.0 to bind to all interfaces
        app.run(host="0.0.0.0", port=3000)
    except Exception as e:
        print(f"Failed to start server: {str(e)}")
        exit(1) 