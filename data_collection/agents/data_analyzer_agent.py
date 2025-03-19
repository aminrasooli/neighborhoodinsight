from .base_agent import MLEnhancedAgent
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import joblib
import os
from ..config import config
import json

class DataAnalyzerAgent(MLEnhancedAgent):
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name)
        self.analyzed_data = {}
        self.analysis_results = {}
        self.visualizations = {}
        self.regression_models = {}
        self.feature_importance = {}
        self.model_dir = "models"
        self.output_dir = "analysis_results"
        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
    async def initialize(self):
        """Initialize the data analyzer agent"""
        await self.load_models()
        self.logger.info(f"Initialized {self.name}")
        
    async def load_models(self):
        """Load saved ML models if they exist"""
        try:
            for source_name in config.data_sources.keys():
                model_path = os.path.join(self.model_dir, f"{source_name}_regression.joblib")
                if os.path.exists(model_path):
                    self.regression_models[source_name] = joblib.load(model_path)
                    
        except Exception as e:
            self.logger.error(f"Error loading models: {str(e)}")
            
    async def save_models(self):
        """Save trained ML models"""
        try:
            for source_name, model in self.regression_models.items():
                model_path = os.path.join(self.model_dir, f"{source_name}_regression.joblib")
                joblib.dump(model, model_path)
        except Exception as e:
            self.logger.error(f"Error saving models: {str(e)}")
            
    async def process(self):
        """Main processing loop with ML-enhanced analysis"""
        try:
            for source_name, data in self.analyzed_data.items():
                if data:
                    start_time = datetime.now()
                    try:
                        # Perform advanced analysis
                        analysis_results = await self.perform_advanced_analysis(data, source_name)
                        
                        # Generate visualizations
                        visualizations = await self.generate_visualizations(data, analysis_results)
                        
                        # Train/update ML models
                        await self.train_ml_models(data, source_name)
                        
                        # Generate insights
                        insights = await self.generate_insights(data, analysis_results)
                        
                        # Update analysis results
                        self.analysis_results[source_name] = {
                            'results': analysis_results,
                            'visualizations': visualizations,
                            'insights': insights,
                            'timestamp': datetime.now()
                        }
                        
                        # Save results
                        await self.save_analysis_results(source_name)
                        
                        # Notify visualization agent
                        await self.send_message(
                            "visualization_agent",
                            {
                                "type": "analysis_results",
                                "source": source_name,
                                "results": analysis_results,
                                "visualizations": visualizations,
                                "insights": insights
                            }
                        )
                        
                        # Learn from success
                        await self.learn_from_experience(1.0)
                        
                    except Exception as e:
                        self.logger.error(f"Error analyzing data from {source_name}: {str(e)}")
                        # Learn from failure
                        await self.learn_from_experience(0.0)
                        
            # Save models periodically
            await self.save_models()
            
        except Exception as e:
            self.logger.error(f"Error in process loop: {str(e)}")
            
    async def perform_advanced_analysis(self, data: Dict[str, Any], source: str) -> Dict[str, Any]:
        """Perform advanced statistical and ML analysis"""
        try:
            df = pd.DataFrame(data['data'])
            patterns = data.get('patterns', [])
            
            analysis = {
                'basic_stats': self._calculate_basic_stats(df),
                'correlations': self._calculate_correlations(df),
                'trends': self._analyze_trends(df),
                'patterns': self._analyze_patterns(patterns),
                'anomalies': self._detect_anomalies(df)
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error performing advanced analysis: {str(e)}")
            return {}
            
    def _calculate_basic_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate basic statistical measures"""
        try:
            stats = {
                'summary': df.describe().to_dict(),
                'missing_values': df.isnull().sum().to_dict(),
                'unique_values': df.nunique().to_dict(),
                'skewness': df.skew().to_dict(),
                'kurtosis': df.kurtosis().to_dict()
            }
            return stats
        except Exception as e:
            self.logger.error(f"Error calculating basic stats: {str(e)}")
            return {}
            
    def _calculate_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate correlations between numeric variables"""
        try:
            numeric_df = df.select_dtypes(include=[np.number])
            correlations = numeric_df.corr().to_dict()
            return correlations
        except Exception as e:
            self.logger.error(f"Error calculating correlations: {str(e)}")
            return {}
            
    def _analyze_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze trends in time series data"""
        try:
            trends = {}
            for col in df.select_dtypes(include=[np.number]).columns:
                if len(df) > 1:
                    # Simple linear regression
                    X = np.arange(len(df)).reshape(-1, 1)
                    y = df[col].values
                    model = LinearRegression()
                    model.fit(X, y)
                    
                    trends[col] = {
                        'slope': float(model.coef_[0]),
                        'intercept': float(model.intercept_),
                        'r2_score': float(r2_score(y, model.predict(X))),
                        'direction': 'increasing' if model.coef_[0] > 0 else 'decreasing'
                    }
            return trends
        except Exception as e:
            self.logger.error(f"Error analyzing trends: {str(e)}")
            return {}
            
    def _analyze_patterns(self, patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze detected patterns"""
        try:
            pattern_analysis = {
                'total_patterns': len(patterns),
                'pattern_sizes': [p['size'] for p in patterns],
                'feature_importance': self._aggregate_feature_importance(patterns)
            }
            return pattern_analysis
        except Exception as e:
            self.logger.error(f"Error analyzing patterns: {str(e)}")
            return {}
            
    def _detect_anomalies(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect anomalies in the data"""
        try:
            anomalies = {}
            for col in df.select_dtypes(include=[np.number]).columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                anomalies[col] = {
                    'count': len(df[(df[col] < lower_bound) | (df[col] > upper_bound)]),
                    'lower_bound': float(lower_bound),
                    'upper_bound': float(upper_bound)
                }
            return anomalies
        except Exception as e:
            self.logger.error(f"Error detecting anomalies: {str(e)}")
            return {}
            
    async def generate_visualizations(self, data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate interactive visualizations"""
        try:
            df = pd.DataFrame(data['data'])
            visualizations = {
                'time_series': self._create_time_series_plots(df),
                'correlation_matrix': self._create_correlation_matrix(df),
                'distribution_plots': self._create_distribution_plots(df),
                'trend_plots': self._create_trend_plots(df, analysis_results['trends']),
                'pattern_plots': self._create_pattern_plots(data.get('patterns', []))
            }
            return visualizations
        except Exception as e:
            self.logger.error(f"Error generating visualizations: {str(e)}")
            return {}
            
    def _create_time_series_plots(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Create time series plots"""
        try:
            plots = {}
            for col in df.select_dtypes(include=[np.number]).columns:
                if 'timestamp' in df.columns:
                    fig = px.line(df, x='timestamp', y=col, title=f'{col} Over Time')
                    plots[col] = fig.to_json()
            return plots
        except Exception as e:
            self.logger.error(f"Error creating time series plots: {str(e)}")
            return {}
            
    def _create_correlation_matrix(self, df: pd.DataFrame) -> str:
        """Create correlation matrix heatmap"""
        try:
            numeric_df = df.select_dtypes(include=[np.number])
            fig = px.imshow(numeric_df.corr(), title='Correlation Matrix')
            return fig.to_json()
        except Exception as e:
            self.logger.error(f"Error creating correlation matrix: {str(e)}")
            return ""
            
    def _create_distribution_plots(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Create distribution plots"""
        try:
            plots = {}
            for col in df.select_dtypes(include=[np.number]).columns:
                fig = px.histogram(df, x=col, title=f'Distribution of {col}')
                plots[col] = fig.to_json()
            return plots
        except Exception as e:
            self.logger.error(f"Error creating distribution plots: {str(e)}")
            return {}
            
    def _create_trend_plots(self, df: pd.DataFrame, trends: Dict[str, Any]) -> Dict[str, Any]:
        """Create trend plots with regression lines"""
        try:
            plots = {}
            for col, trend in trends.items():
                if 'timestamp' in df.columns:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=df['timestamp'], y=df[col], mode='lines+markers', name='Data'))
                    
                    # Add trend line
                    X = np.arange(len(df))
                    y_trend = trend['slope'] * X + trend['intercept']
                    fig.add_trace(go.Scatter(x=df['timestamp'], y=y_trend, mode='lines', name='Trend'))
                    
                    fig.update_layout(title=f'{col} Trend Analysis')
                    plots[col] = fig.to_json()
            return plots
        except Exception as e:
            self.logger.error(f"Error creating trend plots: {str(e)}")
            return {}
            
    def _create_pattern_plots(self, patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create plots for detected patterns"""
        try:
            if not patterns:
                return {}
                
            # Create pattern size distribution plot
            sizes = [p['size'] for p in patterns]
            fig = px.histogram(x=sizes, title='Pattern Size Distribution')
            return {'pattern_sizes': fig.to_json()}
            
        except Exception as e:
            self.logger.error(f"Error creating pattern plots: {str(e)}")
            return {}
            
    async def train_ml_models(self, data: Dict[str, Any], source: str):
        """Train/update ML models for prediction"""
        try:
            df = pd.DataFrame(data['data'])
            
            # Select features and target
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) < 2:
                return
                
            # Use the last numeric column as target
            target = numeric_cols[-1]
            features = numeric_cols[:-1]
            
            # Prepare data
            X = df[features]
            y = df[target]
            
            # Train model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)
            
            # Calculate feature importance
            self.feature_importance[source] = dict(zip(features, model.feature_importances_))
            
            # Store model
            self.regression_models[source] = model
            
        except Exception as e:
            self.logger.error(f"Error training ML models: {str(e)}")
            
    async def generate_insights(self, data: Dict[str, Any], analysis_results: Dict[str, Any]) -> List[str]:
        """Generate insights from analysis results"""
        try:
            insights = []
            
            # Analyze trends
            for col, trend in analysis_results['trends'].items():
                if trend['r2_score'] > 0.7:  # Strong trend
                    insights.append(f"Strong {trend['direction']} trend in {col} (R² = {trend['r2_score']:.2f})")
                    
            # Analyze correlations
            correlations = analysis_results['correlations']
            for col1, corr_dict in correlations.items():
                for col2, corr in corr_dict.items():
                    if abs(corr) > 0.7:  # Strong correlation
                        direction = "positive" if corr > 0 else "negative"
                        insights.append(f"Strong {direction} correlation between {col1} and {col2} ({corr:.2f})")
                        
            # Analyze anomalies
            for col, anomaly in analysis_results['anomalies'].items():
                if anomaly['count'] > 0:
                    insights.append(f"Found {anomaly['count']} anomalies in {col}")
                    
            # Analyze patterns
            pattern_analysis = analysis_results['patterns']
            if pattern_analysis['total_patterns'] > 0:
                insights.append(f"Detected {pattern_analysis['total_patterns']} distinct patterns in the data")
                
            return insights
            
        except Exception as e:
            self.logger.error(f"Error generating insights: {str(e)}")
            return []
            
    async def save_analysis_results(self, source: str):
        """Save analysis results to files"""
        try:
            results = self.analysis_results[source]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save results
            results_file = f"{self.output_dir}/{source}_results_{timestamp}.json"
            with open(results_file, 'w') as f:
                json.dump(results, f)
                
            # Save visualizations
            for viz_type, viz_data in results['visualizations'].items():
                if isinstance(viz_data, dict):
                    for name, viz_json in viz_data.items():
                        viz_file = f"{self.output_dir}/{source}_{viz_type}_{name}_{timestamp}.json"
                        with open(viz_file, 'w') as f:
                            f.write(viz_json)
                else:
                    viz_file = f"{self.output_dir}/{source}_{viz_type}_{timestamp}.json"
                    with open(viz_file, 'w') as f:
                        f.write(viz_data)
                        
        except Exception as e:
            self.logger.error(f"Error saving analysis results: {str(e)}")
            
    async def cleanup(self):
        """Cleanup resources"""
        await self.save_models()
        self.logger.info(f"Cleaned up {self.name}") 