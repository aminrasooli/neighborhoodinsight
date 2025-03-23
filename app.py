from flask import Flask, render_template, jsonify, request
from data_collection.agents.data_collector_agent import DataCollectorAgent
from data_collection.agents.data_processor_agent import DataProcessorAgent
from data_collection.agents.data_analyzer_agent import DataAnalyzerAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize agents
collector = DataCollectorAgent()
processor = DataProcessorAgent()
analyzer = DataAnalyzerAgent()

@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get the current status of all agents."""
    return jsonify({
        'collector': collector.get_status(),
        'processor': processor.get_status(),
        'analyzer': analyzer.get_status()
    })

@app.route('/api/insights')
def get_insights():
    """Get neighborhood insights."""
    neighborhood = request.args.get('neighborhood', 'default')
    timeframe = request.args.get('timeframe', '1y')
    return jsonify(analyzer.get_insights(neighborhood, timeframe))

@app.route('/api/metrics/quality')
def get_quality_metrics():
    """Get data quality metrics."""
    source = request.args.get('source', 'all')
    return jsonify(collector.get_quality_metrics(source))

@app.route('/api/collect', methods=['POST'])
def trigger_collection():
    """Trigger manual data collection."""
    data = request.get_json()
    sources = data.get('sources', ['all'])
    return jsonify(collector.trigger_collection(sources))

@app.route('/api/visualizations')
def get_visualizations():
    """Get available visualizations."""
    return jsonify(analyzer.get_visualizations())

if __name__ == '__main__':
    # Start the agents
    collector.start()
    processor.start()
    analyzer.start()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=3000, debug=True) 