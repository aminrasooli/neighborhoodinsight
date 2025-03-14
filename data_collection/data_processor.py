import json
import os
import pandas as pd
import logging
from datetime import datetime
import numpy as np
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(
    filename='data_processing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class NeighborhoodDataProcessor:
    def __init__(self):
        self.collected_data_path = "collected_data"
        self.processed_data_path = "processed_data"
        os.makedirs(self.processed_data_path, exist_ok=True)

    def load_category_files(self, category):
        files = [f for f in os.listdir(self.collected_data_path) if f.startswith(category)]
        data = []
        for file in files:
            try:
                with open(os.path.join(self.collected_data_path, file), 'r') as f:
                    data.extend(json.load(f))
            except Exception as e:
                logging.error(f"Error loading {file}: {str(e)}")
        return data

    def process_real_estate_data(self, data):
        try:
            df = pd.DataFrame(data)
            # Process and clean real estate data
            df = df.drop_duplicates()
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            return df
        except Exception as e:
            logging.error(f"Error processing real estate data: {str(e)}")
            return pd.DataFrame()

    def process_demographic_data(self, data):
        try:
            df = pd.DataFrame(data)
            # Process and clean demographic data
            df = df.drop_duplicates()
            df = df.fillna(method='ffill')
            return df
        except Exception as e:
            logging.error(f"Error processing demographic data: {str(e)}")
            return pd.DataFrame()

    def process_crime_data(self, data):
        try:
            df = pd.DataFrame(data)
            # Process and clean crime data
            df = df.drop_duplicates()
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            return df
        except Exception as e:
            logging.error(f"Error processing crime data: {str(e)}")
            return pd.DataFrame()

    def process_amenities_data(self, data):
        try:
            df = pd.DataFrame(data)
            # Process and clean amenities data
            df = df.drop_duplicates()
            df = df.groupby(['neighborhood', 'category']).agg({
                'count': 'sum',
                'rating': 'mean'
            }).reset_index()
            return df
        except Exception as e:
            logging.error(f"Error processing amenities data: {str(e)}")
            return pd.DataFrame()

    def process_reviews_data(self, data):
        try:
            df = pd.DataFrame(data)
            # Process and clean reviews data
            df = df.drop_duplicates()
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            return df
        except Exception as e:
            logging.error(f"Error processing reviews data: {str(e)}")
            return pd.DataFrame()

    def merge_data(self, dataframes):
        try:
            # Merge all processed dataframes
            merged_data = {}
            for category, df in dataframes.items():
                if not df.empty:
                    merged_data[category] = df.to_dict('records')
            
            # Save merged data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.processed_data_path, f"merged_data_{timestamp}.json")
            with open(output_file, 'w') as f:
                json.dump(merged_data, f, indent=2)
            logging.info(f"Saved merged data to {output_file}")
            
            return merged_data
        except Exception as e:
            logging.error(f"Error merging data: {str(e)}")
            return {}

    def run_processing(self):
        try:
            # Load and process each category
            categories = {
                'real_estate': (self.load_category_files, self.process_real_estate_data),
                'demographics': (self.load_category_files, self.process_demographic_data),
                'crime': (self.load_category_files, self.process_crime_data),
                'amenities': (self.load_category_files, self.process_amenities_data),
                'reviews': (self.load_category_files, self.process_reviews_data)
            }

            processed_data = {}
            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_category = {}
                for category, (loader, processor) in categories.items():
                    data = loader(category)
                    future = executor.submit(processor, data)
                    future_to_category[future] = category

                for future in future_to_category:
                    category = future_to_category[future]
                    try:
                        df = future.result()
                        processed_data[category] = df
                    except Exception as e:
                        logging.error(f"Error processing {category}: {str(e)}")

            # Merge all processed data
            merged_data = self.merge_data(processed_data)
            return merged_data

        except Exception as e:
            logging.error(f"Error in processing pipeline: {str(e)}")
            return {}

if __name__ == "__main__":
    processor = NeighborhoodDataProcessor()
    logging.info("Starting data processing...")
    processor.run_processing() 