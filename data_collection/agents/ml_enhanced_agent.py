from .base_agent import Agent
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from prophet import Prophet
import pandas as pd
from datetime import datetime, timedelta
import logging

class MLEnhancedAgent(Agent):
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name)
        self.anomaly_detector = None
        self.time_series_model = None
        self.scaler = StandardScaler()
        self.performance_history = []
        self.learning_rate = 0.01
        
    async def initialize_ml_models(self):
        """Initialize machine learning models"""
        try:
            # Initialize anomaly detection model
            self.anomaly_detector = IsolationForest(
                contamination=0.1,
                random_state=42
            )
            
            # Initialize time series model
            self.time_series_model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=True
            )
            
            self.logger.info(f"Initialized ML models for {self.name}")
        except Exception as e:
            self.logger.error(f"Error initializing ML models: {str(e)}")
    
    async def detect_anomalies(self, data: np.ndarray) -> np.ndarray:
        """Detect anomalies in the data using Isolation Forest"""
        try:
            if self.anomaly_detector is None:
                await self.initialize_ml_models()
                
            # Scale the data
            scaled_data = self.scaler.fit_transform(data.reshape(-1, 1))
            
            # Predict anomalies
            predictions = self.anomaly_detector.fit_predict(scaled_data)
            return predictions
        except Exception as e:
            self.logger.error(f"Error detecting anomalies: {str(e)}")
            return np.zeros(len(data))
    
    async def predict_time_series(self, historical_data: pd.DataFrame, 
                                forecast_periods: int = 24) -> pd.DataFrame:
        """Predict future values using Prophet"""
        try:
            if self.time_series_model is None:
                await self.initialize_ml_models()
                
            # Prepare data for Prophet
            df = pd.DataFrame({
                'ds': historical_data.index,
                'y': historical_data.values
            })
            
            # Fit model and make predictions
            self.time_series_model.fit(df)
            future = self.time_series_model.make_future_dataframe(
                periods=forecast_periods,
                freq='H'
            )
            forecast = self.time_series_model.predict(future)
            return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        except Exception as e:
            self.logger.error(f"Error predicting time series: {str(e)}")
            return pd.DataFrame()
    
    async def learn_from_experience(self, performance_metric: float):
        """Update agent behavior based on performance"""
        try:
            self.performance_history.append({
                'timestamp': datetime.now(),
                'metric': performance_metric
            })
            
            # Analyze recent performance
            recent_performance = [p['metric'] for p in self.performance_history[-10:]]
            avg_performance = np.mean(recent_performance)
            
            # Adjust learning rate based on performance
            if avg_performance < 0.5:
                self.learning_rate *= 1.1  # Increase learning rate
            else:
                self.learning_rate *= 0.9  # Decrease learning rate
                
            self.logger.info(f"Updated learning rate to {self.learning_rate}")
        except Exception as e:
            self.logger.error(f"Error learning from experience: {str(e)}")
    
    async def optimize_parameters(self, parameters: dict) -> dict:
        """Optimize agent parameters using simple gradient descent"""
        try:
            optimized = {}
            for param, value in parameters.items():
                # Simple gradient descent update
                gradient = np.random.normal(0, 0.1)  # Simplified gradient
                new_value = value + self.learning_rate * gradient
                optimized[param] = new_value
            return optimized
        except Exception as e:
            self.logger.error(f"Error optimizing parameters: {str(e)}")
            return parameters 