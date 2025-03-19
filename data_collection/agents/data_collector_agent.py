from .base_agent import MLEnhancedAgent
import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from ..config import config
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

class DataCollectorAgent(MLEnhancedAgent):
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name)
        self.session = None
        self.collected_data = {}
        self.collection_stats = pd.DataFrame()
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.quality_metrics = {}
        self.model_dir = "models"
        os.makedirs(self.model_dir, exist_ok=True)
        
    async def initialize(self):
        """Initialize the data collector agent"""
        self.session = aiohttp.ClientSession()
        await self.load_models()
        self.logger.info(f"Initialized {self.name}")
        
    async def load_models(self):
        """Load saved ML models if they exist"""
        try:
            anomaly_model_path = os.path.join(self.model_dir, "anomaly_detector.joblib")
            scaler_path = os.path.join(self.model_dir, "scaler.joblib")
            
            if os.path.exists(anomaly_model_path):
                self.anomaly_detector = joblib.load(anomaly_model_path)
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                
        except Exception as e:
            self.logger.error(f"Error loading models: {str(e)}")
            
    async def save_models(self):
        """Save trained ML models"""
        try:
            joblib.dump(self.anomaly_detector, os.path.join(self.model_dir, "anomaly_detector.joblib"))
            joblib.dump(self.scaler, os.path.join(self.model_dir, "scaler.joblib"))
        except Exception as e:
            self.logger.error(f"Error saving models: {str(e)}")
            
    def calculate_data_quality(self, data: List[Dict[str, Any]], source: str) -> Dict[str, float]:
        """Calculate data quality metrics"""
        try:
            df = pd.DataFrame(data)
            metrics = {
                "completeness": 1 - df.isnull().mean().mean(),
                "consistency": self._check_data_consistency(df),
                "freshness": self._check_data_freshness(df),
                "validity": self._check_data_validity(df, source)
            }
            return metrics
        except Exception as e:
            self.logger.error(f"Error calculating data quality: {str(e)}")
            return {}
            
    def _check_data_consistency(self, df: pd.DataFrame) -> float:
        """Check data consistency"""
        try:
            # Check for duplicate records
            duplicate_ratio = len(df[df.duplicated()]) / len(df)
            
            # Check for logical consistency (e.g., price > 0)
            if 'price' in df.columns:
                valid_prices = (df['price'] > 0).mean()
            else:
                valid_prices = 1.0
                
            return 1 - (duplicate_ratio + (1 - valid_prices)) / 2
            
        except Exception as e:
            self.logger.error(f"Error checking data consistency: {str(e)}")
            return 0.0
            
    def _check_data_freshness(self, df: pd.DataFrame) -> float:
        """Check data freshness"""
        try:
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                max_age = (datetime.now() - df['timestamp'].max()).days
                return 1 - min(max_age / 30, 1)  # Consider data fresh if less than 30 days old
            return 1.0
        except Exception as e:
            self.logger.error(f"Error checking data freshness: {str(e)}")
            return 0.0
            
    def _check_data_validity(self, df: pd.DataFrame, source: str) -> float:
        """Check data validity against schema"""
        try:
            schema = DataSchema.SCHEMAS.get(source, {})
            if not schema:
                return 1.0
                
            required_fields = schema.get('required_fields', [])
            if not required_fields:
                return 1.0
                
            field_validity = []
            for field in required_fields:
                if field in df.columns:
                    field_type = schema['types'].get(field)
                    if field_type:
                        try:
                            if field_type == 'datetime':
                                pd.to_datetime(df[field])
                            else:
                                df[field].astype(field_type)
                            field_validity.append(1.0)
                        except:
                            field_validity.append(0.0)
                    else:
                        field_validity.append(1.0)
                else:
                    field_validity.append(0.0)
                    
            return np.mean(field_validity) if field_validity else 0.0
            
        except Exception as e:
            self.logger.error(f"Error checking data validity: {str(e)}")
            return 0.0
            
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
                            # Calculate data quality metrics
                            quality_metrics = self.calculate_data_quality(data, source_name)
                            self.quality_metrics[source_name] = quality_metrics
                            
                            # Check for anomalies
                            if len(data) > 0:
                                anomalies = await self.detect_anomalies(
                                    np.array([item.get('value', 0) for item in data])
                                )
                                # Filter out anomalous data
                                data = [d for d, a in zip(data, anomalies) if a == 1]
                                
                                # Retrain anomaly detector
                                await self.retrain_anomaly_detector(data)
                            
                            self.collected_data[source_name] = data
                            
                            # Record collection statistics
                            self.collection_stats = pd.concat([
                                self.collection_stats,
                                pd.DataFrame([{
                                    'timestamp': datetime.now(),
                                    'source': source_name,
                                    'success': True,
                                    'response_time': (datetime.now() - start_time).total_seconds(),
                                    'quality_score': np.mean(list(quality_metrics.values())) if quality_metrics else 0.0
                                }])
                            ])
                            
                            # Notify processor agent
                            await self.send_message(
                                "processor_agent",
                                {
                                    "type": "new_data",
                                    "source": source_name,
                                    "data": data,
                                    "quality_metrics": quality_metrics
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
                                'response_time': (datetime.now() - start_time).total_seconds(),
                                'quality_score': 0.0
                            }])
                        ])
            
            # Optimize collection parameters
            await self.optimize_collection_parameters()
            
            # Save models periodically
            await self.save_models()
            
        except Exception as e:
            self.logger.error(f"Error in process loop: {str(e)}")
        
        await asyncio.sleep(config.collection.interval)
        
    async def retrain_anomaly_detector(self, data: List[Dict[str, Any]]):
        """Retrain the anomaly detector with new data"""
        try:
            if len(data) < 10:  # Need minimum data points
                return
                
            # Extract numeric features
            features = []
            for item in data:
                feature_vector = []
                for key, value in item.items():
                    if isinstance(value, (int, float)):
                        feature_vector.append(value)
                if feature_vector:
                    features.append(feature_vector)
                    
            if not features:
                return
                
            # Scale features
            features_scaled = self.scaler.fit_transform(features)
            
            # Train anomaly detector
            self.anomaly_detector.fit(features_scaled)
            
        except Exception as e:
            self.logger.error(f"Error retraining anomaly detector: {str(e)}")
            
    async def predict_collection_schedule(self) -> pd.DataFrame:
        """Predict optimal collection times for each source"""
        try:
            if len(self.collection_stats) < 24:  # Need at least 24 hours of data
                return pd.DataFrame()
                
            # Group by source and predict success rate
            schedules = {}
            for source_name, source_config in config.data_sources.items():
                source_stats = self.collection_stats[
                    self.collection_stats['source'] == source_name
                ].copy()
                
                if len(source_stats) > 0:
                    source_stats.set_index('timestamp', inplace=True)
                    
                    # Consider quality scores in prediction
                    source_stats['success_weighted'] = source_stats['success'].astype(float) * source_stats['quality_score']
                    
                    forecast = await self.predict_time_series(
                        source_stats['success_weighted'],
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
            
            # Consider data quality in decision
            quality_score = self.quality_metrics.get(source_name, {}).get('validity', 0.5)
            
            # Collect if predicted success probability is above threshold
            return prediction * quality_score >= 0.5
            
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
            
            # Analyze performance metrics
            recent_stats = self.collection_stats.tail(100)
            if len(recent_stats) > 0:
                success_rate = recent_stats['success'].mean()
                avg_response_time = recent_stats['response_time'].mean()
                avg_quality = recent_stats['quality_score'].mean()
                
                # Adjust parameters based on performance
                if success_rate < 0.8:
                    current_params['request_timeout'] *= 1.2
                if avg_response_time > 10:
                    current_params['retry_delay'] *= 1.5
                if avg_quality < 0.7:
                    current_params['batch_size'] = int(current_params['batch_size'] * 0.8)
                    
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
        await self.save_models()
        self.logger.info(f"Cleaned up {self.name}") 