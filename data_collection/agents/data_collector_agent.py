from .base_agent import MLEnhancedAgent
import aiohttp
import asyncio
import logging
from datetime import datetime
import numpy as np
import pandas as pd
from typing import Dict, List, Any
from ..config import config

class DataCollectorAgent(MLEnhancedAgent):
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name)
        self.session = None
        self.collected_data = {}
        self.collection_stats = pd.DataFrame()
        
    async def initialize(self):
        """Initialize the data collector agent"""
        self.session = aiohttp.ClientSession()
        self.logger.info(f"Initialized {self.name}")
        
    async def process(self):
        """Main processing loop with ML-enhanced data collection"""
        try:
            # Predict optimal collection times
            collection_schedule = await self.predict_collection_schedule()
            
            for source_name, source_config in config.data_sources.items():
                if await self.should_collect_now(source_name, collection_schedule):
                    try:
                        start_time = datetime.now()
                        data = await self.collect_from_source(source_config)
                        
                        if data:
                            # Check for anomalies
                            if len(data) > 0:
                                anomalies = await self.detect_anomalies(
                                    np.array([item.get('value', 0) for item in data])
                                )
                                # Filter out anomalous data
                                data = [d for d, a in zip(data, anomalies) if a == 1]
                            
                            self.collected_data[source_name] = data
                            
                            # Record collection statistics
                            self.collection_stats = pd.concat([
                                self.collection_stats,
                                pd.DataFrame([{
                                    'timestamp': datetime.now(),
                                    'source': source_name,
                                    'success': True,
                                    'response_time': (datetime.now() - start_time).total_seconds()
                                }])
                            ])
                            
                            # Notify processor agent
                            await self.send_message(
                                "processor_agent",
                                {
                                    "type": "new_data",
                                    "source": source_name,
                                    "data": data
                                }
                            )
                            
                            # Learn from success
                            await self.learn_from_experience(1.0)
                            
                    except Exception as e:
                        self.logger.error(f"Error collecting from {source_name}: {str(e)}")
                        # Learn from failure
                        await self.learn_from_experience(0.0)
                        
                        # Record failed collection
                        self.collection_stats = pd.concat([
                            self.collection_stats,
                            pd.DataFrame([{
                                'timestamp': datetime.now(),
                                'source': source_name,
                                'success': False,
                                'response_time': (datetime.now() - start_time).total_seconds()
                            }])
                        ])
            
            # Optimize collection parameters
            await self.optimize_collection_parameters()
            
        except Exception as e:
            self.logger.error(f"Error in process loop: {str(e)}")
        
        await asyncio.sleep(config.collection.interval)
        
    async def predict_collection_schedule(self) -> pd.DataFrame:
        """Predict optimal collection times for each source"""
        try:
            if len(self.collection_stats) < 24:  # Need at least 24 hours of data
                return pd.DataFrame()  # Return empty schedule if not enough data
                
            # Group by source and predict success rate
            schedules = {}
            for source_name, source_config in config.data_sources.items():
                source_stats = self.collection_stats[
                    self.collection_stats['source'] == source_name
                ].copy()
                
                if len(source_stats) > 0:
                    source_stats.set_index('timestamp', inplace=True)
                    forecast = await self.predict_time_series(
                        source_stats['success'].astype(float),
                        forecast_periods=24
                    )
                    schedules[source_name] = forecast
                    
            return schedules
        except Exception as e:
            self.logger.error(f"Error predicting collection schedule: {str(e)}")
            return pd.DataFrame()
            
    async def should_collect_now(self, source_name: str, schedule: dict) -> bool:
        """Determine if we should collect from a source now based on predictions"""
        try:
            if not schedule or source_name not in schedule:
                return True  # Collect if we don't have predictions
                
            forecast = schedule[source_name]
            current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
            
            # Get predicted success probability for current hour
            prediction = forecast[
                forecast['ds'] == current_hour
            ]['yhat'].iloc[0]
            
            # Collect if predicted success probability is above threshold
            return prediction >= 0.5
            
        except Exception as e:
            self.logger.error(f"Error checking collection timing: {str(e)}")
            return True
            
    async def optimize_collection_parameters(self):
        """Optimize collection parameters based on performance"""
        try:
            # Calculate current parameters
            current_params = {
                'request_timeout': 30,
                'retry_delay': 60,
                'batch_size': 100
            }
            
            # Optimize parameters
            optimized = await self.optimize_parameters(current_params)
            
            # Update parameters if optimization successful
            if optimized:
                self.logger.info(f"Updated collection parameters: {optimized}")
                
        except Exception as e:
            self.logger.error(f"Error optimizing parameters: {str(e)}")
            
    async def collect_from_source(self, source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collect data from a specific source with proper authentication"""
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        # Add authentication if required
        if source_config['requires_auth']:
            if source_config.get('auth_header'):
                auth_value = getattr(config.api, f"{source_config['name']}_api_key")
                headers[source_config['auth_header']] = f"{source_config.get('auth_prefix', '')} {auth_value}".strip()
        
        params = source_config.get('params', {})
        if source_config.get('auth_param'):
            params[source_config['auth_param']] = getattr(config.api, f"{source_config['name']}_api_key")
            
        url = source_config['base_url']
        
        for attempt in range(config.rate_limit.max_retries):
            try:
                async with self.session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:  # Rate limit exceeded
                        wait_time = int(response.headers.get('Retry-After', config.rate_limit.delay))
                        self.logger.warning(f"Rate limit exceeded for {source_config['name']}, waiting {wait_time}s")
                        await asyncio.sleep(wait_time)
                    else:
                        self.logger.error(f"Error collecting from {source_config['name']}: {response.status}")
                        return []
                        
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error collecting from {source_config['name']}: {str(e)}")
                if attempt < config.rate_limit.max_retries - 1:
                    await asyncio.sleep(config.rate_limit.delay * (attempt + 1))
                else:
                    return []
                    
        return []
        
    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
        self.logger.info(f"Cleaned up {self.name}") 