from .base_agent import MLEnhancedAgent
import pandas as pd
import json
from datetime import datetime
import os
import asyncio
from typing import Dict, Any, List, Optional
import numpy as np
from ..config import config
import hashlib
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
import joblib

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

class DataProcessorAgent(MLEnhancedAgent):
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name)
        self.processed_data = {}
        self.processing_stats = pd.DataFrame()
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)
        self.cluster_model = DBSCAN(eps=0.5, min_samples=5)
        self.feature_importance = {}
        self.model_dir = "models"
        self.output_dir = "processed_data"
        self.version_dir = os.path.join(self.output_dir, "versions")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.version_dir, exist_ok=True)
        
    async def initialize(self):
        """Initialize the data processor agent"""
        await self.load_models()
        self.logger.info(f"Initialized {self.name}")
        
    async def load_models(self):
        """Load saved ML models if they exist"""
        try:
            scaler_path = os.path.join(self.model_dir, "processor_scaler.joblib")
            pca_path = os.path.join(self.model_dir, "processor_pca.joblib")
            cluster_path = os.path.join(self.model_dir, "processor_cluster.joblib")
            
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
            if os.path.exists(pca_path):
                self.pca = joblib.load(pca_path)
            if os.path.exists(cluster_path):
                self.cluster_model = joblib.load(cluster_path)
                
        except Exception as e:
            self.logger.error(f"Error loading models: {str(e)}")
            
    async def save_models(self):
        """Save trained ML models"""
        try:
            joblib.dump(self.scaler, os.path.join(self.model_dir, "processor_scaler.joblib"))
            joblib.dump(self.pca, os.path.join(self.model_dir, "processor_pca.joblib"))
            joblib.dump(self.cluster_model, os.path.join(self.model_dir, "processor_cluster.joblib"))
        except Exception as e:
            self.logger.error(f"Error saving models: {str(e)}")
            
    async def process(self):
        """Main processing loop with ML-enhanced data processing"""
        try:
            for source_name, data in self.processed_data.items():
                if data:
                    start_time = datetime.now()
                    try:
                        # Preprocess data
                        processed_data = await self.preprocess_data(data, source_name)
                        
                        # Apply ML transformations
                        transformed_data = await self.apply_ml_transformations(processed_data)
                        
                        # Detect patterns and anomalies
                        patterns = await self.detect_patterns(transformed_data)
                        
                        # Update processed data
                        self.processed_data[source_name] = {
                            'data': transformed_data,
                            'patterns': patterns,
                            'timestamp': datetime.now()
                        }
                        
                        # Record processing statistics
                        self.processing_stats = pd.concat([
                            self.processing_stats,
                            pd.DataFrame([{
                                'timestamp': datetime.now(),
                                'source': source_name,
                                'success': True,
                                'processing_time': (datetime.now() - start_time).total_seconds(),
                                'data_size': len(transformed_data),
                                'pattern_count': len(patterns)
                            }])
                        ])
                        
                        # Notify analyzer agent
                        await self.send_message(
                            "analyzer_agent",
                            {
                                "type": "processed_data",
                                "source": source_name,
                                "data": transformed_data,
                                "patterns": patterns
                            }
                        )
                        
                        # Learn from success
                        await self.learn_from_experience(1.0)
                        
                    except Exception as e:
                        self.logger.error(f"Error processing data from {source_name}: {str(e)}")
                        # Learn from failure
                        await self.learn_from_experience(0.0)
                        
                        # Record failed processing
                        self.processing_stats = pd.concat([
                            self.processing_stats,
                            pd.DataFrame([{
                                'timestamp': datetime.now(),
                                'source': source_name,
                                'success': False,
                                'processing_time': (datetime.now() - start_time).total_seconds(),
                                'data_size': 0,
                                'pattern_count': 0
                            }])
                        ])
            
            # Optimize processing parameters
            await self.optimize_processing_parameters()
            
            # Save models periodically
            await self.save_models()
            
        except Exception as e:
            self.logger.error(f"Error in process loop: {str(e)}")
            
    async def preprocess_data(self, data: List[Dict[str, Any]], source: str) -> pd.DataFrame:
        """Preprocess data with advanced cleaning and validation"""
        try:
            df = pd.DataFrame(data)
            
            # Handle missing values
            df = self._handle_missing_values(df)
            
            # Remove duplicates
            df = df.drop_duplicates()
            
            # Validate data types
            df = self._validate_data_types(df, source)
            
            # Handle outliers
            df = self._handle_outliers(df)
            
            # Feature engineering
            df = self._engineer_features(df)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error preprocessing data: {str(e)}")
            return pd.DataFrame()
            
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values intelligently"""
        try:
            # Calculate missing value statistics
            missing_stats = df.isnull().mean()
            
            # For columns with low missing rate (< 5%), use median imputation
            low_missing_cols = missing_stats[missing_stats < 0.05].index
            for col in low_missing_cols:
                df[col] = df[col].fillna(df[col].median())
                
            # For columns with high missing rate, create missing indicator
            high_missing_cols = missing_stats[missing_stats >= 0.05].index
            for col in high_missing_cols:
                df[f"{col}_missing"] = df[col].isnull().astype(int)
                df[col] = df[col].fillna(df[col].median())
                
            return df
            
        except Exception as e:
            self.logger.error(f"Error handling missing values: {str(e)}")
            return df
            
    def _validate_data_types(self, df: pd.DataFrame, source: str) -> pd.DataFrame:
        """Validate and convert data types"""
        try:
            schema = DataSchema.SCHEMAS.get(source, {})
            if not schema or 'types' not in schema:
                return df
                
            for col, dtype in schema['types'].items():
                if col in df.columns:
                    try:
                        if dtype == 'datetime':
                            df[col] = pd.to_datetime(df[col])
                        else:
                            df[col] = df[col].astype(dtype)
                    except Exception as e:
                        self.logger.warning(f"Error converting {col} to {dtype}: {str(e)}")
                        
            return df
            
        except Exception as e:
            self.logger.error(f"Error validating data types: {str(e)}")
            return df
            
    def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle outliers using IQR method"""
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            for col in numeric_cols:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Create outlier indicator
                df[f"{col}_outlier"] = ((df[col] < lower_bound) | (df[col] > upper_bound)).astype(int)
                
                # Cap outliers
                df[col] = df[col].clip(lower_bound, upper_bound)
                
            return df
            
        except Exception as e:
            self.logger.error(f"Error handling outliers: {str(e)}")
            return df
            
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer new features"""
        try:
            # Time-based features
            for col in df.select_dtypes(include=['datetime64']).columns:
                df[f"{col}_hour"] = df[col].dt.hour
                df[f"{col}_day"] = df[col].dt.day
                df[f"{col}_month"] = df[col].dt.month
                df[f"{col}_dayofweek"] = df[col].dt.dayofweek
                
            # Numeric interactions
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for i, col1 in enumerate(numeric_cols):
                for col2 in numeric_cols[i+1:]:
                    df[f"{col1}_{col2}_ratio"] = df[col1] / df[col2].replace(0, np.nan)
                    df[f"{col1}_{col2}_sum"] = df[col1] + df[col2]
                    df[f"{col1}_{col2}_product"] = df[col1] * df[col2]
                    
            return df
            
        except Exception as e:
            self.logger.error(f"Error engineering features: {str(e)}")
            return df
            
    async def apply_ml_transformations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply ML transformations to the data"""
        try:
            if len(df) == 0:
                return df
                
            # Select numeric features
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                return df
                
            # Scale features
            scaled_features = self.scaler.fit_transform(df[numeric_cols])
            
            # Apply PCA
            pca_features = self.pca.fit_transform(scaled_features)
            
            # Add PCA components to dataframe
            for i in range(pca_features.shape[1]):
                df[f"pca_component_{i+1}"] = pca_features[:, i]
                
            # Update feature importance
            self.feature_importance = dict(zip(numeric_cols, self.pca.explained_variance_ratio_))
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error applying ML transformations: {str(e)}")
            return df
            
    async def detect_patterns(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect patterns in the data using clustering"""
        try:
            if len(df) < 10:  # Need minimum data points
                return []
                
            # Select features for clustering
            cluster_features = [col for col in df.columns if col.startswith('pca_component_')]
            if not cluster_features:
                return []
                
            # Perform clustering
            clusters = self.cluster_model.fit_predict(df[cluster_features])
            
            # Analyze clusters
            patterns = []
            for cluster_id in set(clusters):
                if cluster_id == -1:  # Skip noise points
                    continue
                    
                cluster_data = df[clusters == cluster_id]
                pattern = {
                    'cluster_id': int(cluster_id),
                    'size': len(cluster_data),
                    'centroid': cluster_data[cluster_features].mean().to_dict(),
                    'std': cluster_data[cluster_features].std().to_dict(),
                    'feature_importance': self.feature_importance
                }
                patterns.append(pattern)
                
            return patterns
            
        except Exception as e:
            self.logger.error(f"Error detecting patterns: {str(e)}")
            return []
            
    async def optimize_processing_parameters(self):
        """Optimize processing parameters based on performance"""
        try:
            # Calculate current parameters
            current_params = {
                'pca_n_components': 0.95,
                'dbscan_eps': 0.5,
                'dbscan_min_samples': 5
            }
            
            # Analyze performance metrics
            recent_stats = self.processing_stats.tail(100)
            if len(recent_stats) > 0:
                success_rate = recent_stats['success'].mean()
                avg_processing_time = recent_stats['processing_time'].mean()
                avg_pattern_count = recent_stats['pattern_count'].mean()
                
                # Adjust parameters based on performance
                if success_rate < 0.8:
                    current_params['pca_n_components'] *= 0.9
                if avg_processing_time > 10:
                    current_params['dbscan_min_samples'] = max(3, current_params['dbscan_min_samples'] - 1)
                if avg_pattern_count < 3:
                    current_params['dbscan_eps'] *= 1.2
                    
            # Optimize parameters
            optimized = await self.optimize_parameters(current_params)
            
            # Update parameters if optimization successful
            if optimized:
                self.pca.n_components = optimized['pca_n_components']
                self.cluster_model.eps = optimized['dbscan_eps']
                self.cluster_model.min_samples = optimized['dbscan_min_samples']
                self.logger.info(f"Updated processing parameters: {optimized}")
                
        except Exception as e:
            self.logger.error(f"Error optimizing parameters: {str(e)}")
            
    async def cleanup(self):
        """Cleanup resources"""
        await self.save_models()
        self.logger.info(f"Cleaned up {self.name}") 