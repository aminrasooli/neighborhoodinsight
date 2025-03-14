from .base_agent import Agent
import pandas as pd
import json
from datetime import datetime
import os
import asyncio

class DataProcessorAgent(Agent):
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name)
        self.processed_data = {}
        self.output_dir = "processed_data"
        os.makedirs(self.output_dir, exist_ok=True)
        
    async def initialize(self):
        """Initialize the data processor agent"""
        self.logger.info(f"Initialized {self.name}")
        
    async def process(self):
        """Main processing loop for data processing"""
        # Check for new messages from collector agents
        message = await self.receive_message()
        if message and message["content"]["type"] == "new_data":
            await self.process_new_data(message["content"])
            
        # Process existing data periodically
        await self.process_existing_data()
        
        await asyncio.sleep(1800)  # Wait 30 minutes before next processing cycle
        
    async def process_new_data(self, data_message: dict):
        """Process newly received data"""
        source = data_message["source"]
        data = data_message["data"]
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Apply processing based on source type
            if source == "real_estate":
                df = self.process_real_estate_data(df)
            elif source == "demographics":
                df = self.process_demographic_data(df)
            elif source == "crime":
                df = self.process_crime_data(df)
            elif source == "amenities":
                df = self.process_amenities_data(df)
            elif source == "reviews":
                df = self.process_reviews_data(df)
                
            # Store processed data
            self.processed_data[source] = df
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/{source}_{timestamp}.json"
            df.to_json(filename, orient='records')
            
            self.logger.info(f"Processed and saved new data from {source}")
            
        except Exception as e:
            self.logger.error(f"Error processing new data from {source}: {str(e)}")
            
    async def process_existing_data(self):
        """Process and merge all existing data"""
        try:
            merged_data = self.merge_all_data()
            if not merged_data.empty:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.output_dir}/merged_data_{timestamp}.json"
                merged_data.to_json(filename, orient='records')
                self.logger.info("Processed and saved merged data")
        except Exception as e:
            self.logger.error(f"Error processing existing data: {str(e)}")
            
    def merge_all_data(self) -> pd.DataFrame:
        """Merge all processed data into a single DataFrame"""
        if not self.processed_data:
            return pd.DataFrame()
            
        # Start with the first dataset
        merged = next(iter(self.processed_data.values()))
        
        # Merge with remaining datasets
        for source, df in self.processed_data.items():
            if source != merged.name:
                merged = pd.merge(merged, df, how='outer', on='neighborhood')
                
        return merged
        
    def process_real_estate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process real estate data"""
        df = df.drop_duplicates()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df.sort_values('timestamp')
        
    def process_demographic_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process demographic data"""
        df = df.drop_duplicates()
        df = df.fillna(method='ffill')
        return df
        
    def process_crime_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process crime data"""
        df = df.drop_duplicates()
        df['crime_rate'] = df['total_crimes'] / df['population']
        return df
        
    def process_amenities_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process amenities data"""
        df = df.drop_duplicates()
        df['total_amenities'] = df[['restaurants', 'parks', 'schools']].sum(axis=1)
        return df
        
    def process_reviews_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process reviews data"""
        df = df.drop_duplicates()
        df['average_rating'] = df['rating'].mean()
        return df
        
    async def cleanup(self):
        """Cleanup resources"""
        self.logger.info(f"Cleaned up {self.name}") 