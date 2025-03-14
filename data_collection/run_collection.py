import subprocess
import time
import logging
import os
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='collection_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_collection_pipeline():
    try:
        # Create necessary directories
        os.makedirs("collected_data", exist_ok=True)
        os.makedirs("processed_data", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        # Start data collection process
        collector_process = subprocess.Popen(
            ["python", "data_scraper.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logging.info("Started data collection process")

        # Initialize processing interval tracking
        last_processing_time = datetime.now()
        processing_interval = 1800  # Process data every 30 minutes

        while True:
            # Check if collector is still running
            if collector_process.poll() is not None:
                logging.error("Data collector process died, restarting...")
                collector_process = subprocess.Popen(
                    ["python", "data_scraper.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

            # Check if it's time to process data
            current_time = datetime.now()
            if (current_time - last_processing_time).total_seconds() >= processing_interval:
                logging.info("Starting data processing cycle")
                try:
                    processor_process = subprocess.Popen(
                        ["python", "data_processor.py"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    processor_process.wait(timeout=600)  # Wait up to 10 minutes for processing
                    last_processing_time = current_time
                    logging.info("Completed data processing cycle")
                except subprocess.TimeoutExpired:
                    logging.error("Data processing timed out")
                except Exception as e:
                    logging.error(f"Error in data processing: {str(e)}")

            # Sleep for a minute before next check
            time.sleep(60)

    except Exception as e:
        logging.error(f"Error in collection pipeline: {str(e)}")
        time.sleep(60)  # Wait before retrying
        run_collection_pipeline()

if __name__ == "__main__":
    logging.info("Starting data collection pipeline...")
    run_collection_pipeline() 