from .base_agent import Agent
import pandas as pd
import json
from datetime import datetime
import os
import asyncio
from typing import Dict, Any, List
import numpy as np
from ..config import config
import hashlib

class DataSchema:
    """Data schema definitions for validation"""
    SCHEMAS = {
        "real_estate": {
            "required_fields": ["price", "address", "bedrooms", "bathrooms", "sqft"],
            "types": {
                "price": float,
                "bedrooms": int,
                "bathrooms": float,
                "sqft": float
            }
        },
        "demographics": {
            "required_fields": ["population", "median_income", "median_age"],
            "types": {
                "population": int,
                "median_income": float,
                "median_age": float
            }
        },
        "crime": {
            "required_fields": ["incident_datetime", "incident_category", "resolution"],
            "types": {
                "incident_datetime": "datetime"
            }
        },
        "amenities": {
            "required_fields": ["name", "rating", "review_count", "categories"],
            "types": {
                "rating": float,
                "review_count": int
            }
        },
        "reviews": {
            "required_fields": ["rating", "text", "time_created"],
            "types": {
                "rating": int,
                "time_created": "datetime"
            }
        }
    }

class DataProcessorAgent(Agent):
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name)
        self.processed_data = {}
        self.output_dir = "processed_data"
        self.version_dir = os.path.join(self.output_dir, "versions")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.version_dir, exist_ok=True)
        
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
        
        await asyncio.sleep(config.collection.processing_interval)
        
    def validate_data(self, data: List[Dict[str, Any]], source: str) -> List[Dict[str, Any]]:
        """Validate data against schema"""
        schema = DataSchema.SCHEMAS.get(source)
        if not schema:
            self.logger.warning(f"No schema defined for source: {source}")
            return data
            
        valid_data = []
        for item in data:
            try:
                # Check required fields
                if not all(field in item for field in schema["required_fields"]):
                    continue
                    
                # Validate and convert types
                for field, field_type in schema["types"].items():
                    if field in item:
                        if field_type == "datetime":
                            try:
                                item[field] = pd.to_datetime(item[field])
                            except:
                                continue
                        else:
                            try:
                                item[field] = field_type(item[field])
                            except:
                                continue
                                
                valid_data.append(item)
                
            except Exception as e:
                self.logger.error(f"Error validating data item: {str(e)}")
                
        return valid_data
        
    def compute_data_hash(self, data: List[Dict[str, Any]]) -> str:
        """Compute hash of data for versioning"""
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(data_str.encode()).hexdigest()
        
    async def process_new_data(self, data_message: dict):
        """Process newly received data"""
        source = data_message["source"]
        data = data_message["data"]
        
        try:
            # Validate data
            valid_data = self.validate_data(data, source)
            if not valid_data:
                self.logger.warning(f"No valid data found for source: {source}")
                return
                
            # Convert to DataFrame
            df = pd.DataFrame(valid_data)
            
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
            
            # Save versioned data
            data_hash = self.compute_data_hash(valid_data)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            version_file = f"{self.version_dir}/{source}_{timestamp}_{data_hash[:8]}.json"
            
            df.to_json(version_file, orient='records')
            
            # Create latest symlink
            latest_file = f"{self.output_dir}/{source}_latest.json"
            if os.path.exists(latest_file):
                os.remove(latest_file)
            os.symlink(version_file, latest_file)
            
            self.logger.info(f"Processed and saved new data from {source}")
            
        except Exception as e:
            self.logger.error(f"Error processing new data from {source}: {str(e)}")
            
    async def process_existing_data(self):
        """Process and merge all existing data"""
        try:
            merged_data = self.merge_all_data()
            if not merged_data.empty:
                # Save versioned merged data
                data_hash = self.compute_data_hash(merged_data.to_dict('records'))
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                version_file = f"{self.version_dir}/merged_{timestamp}_{data_hash[:8]}.json"
                
                merged_data.to_json(version_file, orient='records')
                
                # Create latest symlink
                latest_file = f"{self.output_dir}/merged_latest.json"
                if os.path.exists(latest_file):
                    os.remove(latest_file)
                os.symlink(version_file, latest_file)
                
                self.logger.info("Processed and saved merged data")
        except Exception as e:
            self.logger.error(f"Error processing existing data: {str(e)}")
            
    def merge_all_data(self) -> pd.DataFrame:
        """Merge all processed data sources"""
        try:
            if not self.processed_data:
                return pd.DataFrame()
                
            # Start with real estate data as base
            merged = self.processed_data.get("real_estate", pd.DataFrame())
            if merged.empty:
                return merged
                
            # Merge other data sources based on location
            for source, df in self.processed_data.items():
                if source != "real_estate" and not df.empty:
                    # Implement proper merging logic based on location/neighborhood
                    pass
                    
            return merged
            
        except Exception as e:
            self.logger.error(f"Error merging data: {str(e)}")
            return pd.DataFrame()
            
    def process_real_estate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process real estate data"""
        try:
            # Clean price data
            df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
            
            # Convert area to numeric
            df['sqft'] = df['sqft'].replace('[,]', '', regex=True).astype(float)
            
            # Calculate price per square foot
            df['price_per_sqft'] = df['price'] / df['sqft']
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error processing real estate data: {str(e)}")
            return pd.DataFrame()
            
    def process_demographic_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process demographic data"""
        try:
            # Clean numeric columns
            numeric_cols = ['population', 'median_income', 'median_age']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    
            return df
            
        except Exception as e:
            self.logger.error(f"Error processing demographic data: {str(e)}")
            return pd.DataFrame()
            
    def process_crime_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process crime data"""
        try:
            # Convert datetime columns
            df['incident_datetime'] = pd.to_datetime(df['incident_datetime'])
            
            # Group by category and calculate statistics
            crime_stats = df.groupby('incident_category').agg({
                'incident_datetime': 'count'
            }).reset_index()
            
            crime_stats.columns = ['category', 'count']
            
            return crime_stats
            
        except Exception as e:
            self.logger.error(f"Error processing crime data: {str(e)}")
            return pd.DataFrame()
            
    def process_amenities_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process amenities data"""
        try:
            # Calculate average ratings
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
            
            # Group by category
            amenity_stats = df.groupby('categories').agg({
                'rating': ['mean', 'count']
            }).reset_index()
            
            amenity_stats.columns = ['category', 'avg_rating', 'count']
            
            return amenity_stats
            
        except Exception as e:
            self.logger.error(f"Error processing amenities data: {str(e)}")
            return pd.DataFrame()
            
    def process_reviews_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process reviews data"""
        try:
            # Convert datetime
            df['time_created'] = pd.to_datetime(df['time_created'])
            
            # Calculate sentiment scores (placeholder for now)
            df['sentiment_score'] = df['rating'] / 5.0
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error processing reviews data: {str(e)}")
            return pd.DataFrame()
            
    async def cleanup(self):
        """Cleanup resources"""
        self.logger.info(f"Cleaned up {self.name}") 