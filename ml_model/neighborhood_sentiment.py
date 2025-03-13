import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from typing import Dict, Any, List
import re

class NeighborhoodSentimentAnalyzer:
    def __init__(self):
        # Initialize the TF-IDF vectorizer for text analysis
        self.vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Initialize a simple Random Forest classifier
        self.classifier = RandomForestClassifier(
            n_estimators=50,
            max_depth=5,
            random_state=42
        )
        
        # Train the model with some initial data
        self._train_initial_model()
        
    def _train_initial_model(self):
        """Train the model with some initial example data"""
        # Example training data (positive and negative neighborhood aspects)
        positive_examples = [
            "good schools nearby",
            "friendly neighbors",
            "safe streets",
            "clean parks",
            "active community",
            "great public transport",
            "quiet neighborhood",
            "lots of restaurants",
            "well maintained",
            "family friendly"
        ]
        
        negative_examples = [
            "high crime rate",
            "noisy traffic",
            "poor maintenance",
            "limited parking",
            "unsafe at night",
            "far from shops",
            "bad schools",
            "unfriendly neighbors",
            "dirty streets",
            "abandoned buildings"
        ]
        
        # Create training data
        X_train = positive_examples + negative_examples
        y_train = [1] * len(positive_examples) + [0] * len(negative_examples)
        
        # Fit the vectorizer and transform the training data
        X_train_vectorized = self.vectorizer.fit_transform(X_train)
        
        # Train the classifier
        self.classifier.fit(X_train_vectorized, y_train)
    
    def analyze_sentiment(self, text_data: List[str]) -> float:
        """Analyze sentiment of neighborhood reviews and comments"""
        try:
            # Vectorize the input text
            X = self.vectorizer.transform(text_data)
            
            # Get prediction probabilities
            probabilities = self.classifier.predict_proba(X)
            
            # Calculate average positive sentiment score (0-100)
            avg_positive_score = np.mean(probabilities[:, 1]) * 100
            return round(avg_positive_score, 2)
            
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            return 50.0  # Return neutral score on error

class EnhancedNeighborhoodScorer:
    def __init__(self):
        self.sentiment_analyzer = NeighborhoodSentimentAnalyzer()
        self.weights = {
            'sentiment': 0.35,      # Increased weight for community sentiment
            'safety': 0.25,         # Safety is still important
            'real_estate': 0.15,    # Reduced weight
            'amenities': 0.15,      # Maintained
            'education': 0.10       # Slightly reduced
        }
    
    def calculate_score(self, neighborhood_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate enhanced neighborhood score with focus on community sentiment"""
        try:
            # Gather all text data for sentiment analysis
            text_data = self._gather_text_data(neighborhood_data)
            
            # Get sentiment score
            sentiment_score = self.sentiment_analyzer.analyze_sentiment(text_data)
            
            # Calculate other component scores (converted to 0-100 scale)
            safety_score = self._calculate_safety_score(neighborhood_data.get('crime_analysis', {}))
            real_estate_score = self._calculate_real_estate_score(neighborhood_data.get('real_estate', {}))
            amenities_score = self._calculate_amenities_score(neighborhood_data.get('community', {}).get('amenities', {}))
            education_score = self._calculate_education_score(neighborhood_data.get('community', {}).get('education', {}))
            
            # Calculate weighted final score
            final_score = (
                sentiment_score * self.weights['sentiment'] +
                safety_score * self.weights['safety'] +
                real_estate_score * self.weights['real_estate'] +
                amenities_score * self.weights['amenities'] +
                education_score * self.weights['education']
            )
            
            return {
                "overall_score": round(final_score, 2),
                "component_scores": {
                    "community_sentiment": round(sentiment_score, 2),
                    "safety": round(safety_score, 2),
                    "real_estate": round(real_estate_score, 2),
                    "amenities": round(amenities_score, 2),
                    "education": round(education_score, 2)
                },
                "interpretation": self._interpret_score(final_score),
                "sentiment_analysis": {
                    "analyzed_comments": len(text_data),
                    "sentiment_score": round(sentiment_score, 2),
                    "confidence": "high" if len(text_data) > 5 else "medium"
                },
                "recommendations": self._generate_recommendations(
                    sentiment_score, safety_score, real_estate_score,
                    amenities_score, education_score
                )
            }
        except Exception as e:
            print(f"Error calculating neighborhood score: {str(e)}")
            return None
    
    def _gather_text_data(self, neighborhood_data: Dict[str, Any]) -> List[str]:
        """Gather all relevant text data for sentiment analysis"""
        text_data = []
        
        # Add positive aspects
        text_data.extend(neighborhood_data.get('community', {}).get('positive_aspects', []))
        
        # Add complaints (negative aspects)
        text_data.extend(neighborhood_data.get('community', {}).get('top_complaints', []))
        
        # Add crime descriptions
        for incident in neighborhood_data.get('crime_analysis', {}).get('recent_incidents', []):
            text_data.append(f"{incident.get('type', '')} {incident.get('severity', '')}")
        
        return text_data
    
    def _calculate_safety_score(self, crime_data: Dict[str, Any]) -> float:
        """Calculate safety score (0-100)"""
        try:
            risk_levels = {"Low": 90, "Medium": 60, "High": 30}
            risk_score = risk_levels.get(crime_data.get('risk_level', 'Medium'), 60)
            
            safety_score = float(crime_data.get('safety_score', 7.0)) * 10
            
            incidents = len(crime_data.get('recent_incidents', []))
            incident_score = 100 - (incidents * 10)  # Deduct 10 points per incident
            
            return max(0, min(100, (risk_score + safety_score + incident_score) / 3))
        except Exception as e:
            print(f"Error in safety score calculation: {str(e)}")
            return 50.0

    def _calculate_real_estate_score(self, real_estate_data: Dict[str, Any]) -> float:
        """Calculate real estate score (0-100)"""
        try:
            # Extract price trend
            trend_str = real_estate_data.get('price_trend', '+0%')
            trend_match = re.search(r'([+-]?\d+\.?\d*)', trend_str)
            price_trend = float(trend_match.group(1)) if trend_match else 0
            
            # Convert trend to score (0-100)
            trend_score = min(100, max(0, 50 + price_trend * 5))
            
            # Market status score
            market_scores = {
                "Hot Market": 90,
                "Seller's Market": 80,
                "Balanced Market": 70,
                "Buyer's Market": 60
            }
            market_score = market_scores.get(real_estate_data.get('market_status', 'Balanced Market'), 70)
            
            return (trend_score + market_score) / 2
        except Exception as e:
            print(f"Error in real estate score calculation: {str(e)}")
            return 50.0

    def _calculate_amenities_score(self, amenities_data: Dict[str, Any]) -> float:
        """Calculate amenities score (0-100)"""
        try:
            walkability = float(amenities_data.get('walkability_score', 70))
            transit = float(amenities_data.get('transit_score', 70))
            
            nearby = amenities_data.get('nearby', {})
            amenities_count = sum(nearby.values())
            diversity_score = min(100, amenities_count * 2)
            
            return (walkability + transit + diversity_score) / 3
        except Exception as e:
            print(f"Error in amenities score calculation: {str(e)}")
            return 50.0

    def _calculate_education_score(self, education_data: Dict[str, Any]) -> float:
        """Calculate education score (0-100)"""
        try:
            base_score = float(education_data.get('schools_rating', 7.0)) * 10
            
            schools = education_data.get('nearby_schools', [])
            if schools:
                avg_rating = sum(school.get('rating', 7.0) for school in schools) / len(schools) * 10
                return (base_score + avg_rating) / 2
            
            return base_score
        except Exception as e:
            print(f"Error in education score calculation: {str(e)}")
            return 50.0

    def _interpret_score(self, score: float) -> str:
        """Provide detailed interpretation of the overall score"""
        if score >= 90:
            return "Exceptional neighborhood with outstanding community feedback and amenities"
        elif score >= 80:
            return "Excellent neighborhood with very positive community sentiment"
        elif score >= 70:
            return "Very good neighborhood with strong community aspects"
        elif score >= 60:
            return "Good neighborhood with room for community improvement"
        elif score >= 50:
            return "Average neighborhood with mixed community feedback"
        else:
            return "Below average neighborhood with significant community concerns"

    def _generate_recommendations(self, sentiment: float, safety: float,
                                real_estate: float, amenities: float,
                                education: float) -> List[str]:
        """Generate specific recommendations based on scores"""
        recommendations = []
        
        if sentiment < 60:
            recommendations.append("Consider engaging with community forums to understand resident concerns")
        if safety < 60:
            recommendations.append("Review recent community safety initiatives and neighborhood watch programs")
        if real_estate < 60:
            recommendations.append("Monitor market trends and upcoming development projects")
        if amenities < 60:
            recommendations.append("Research planned infrastructure improvements and new business developments")
        if education < 60:
            recommendations.append("Look into supplementary educational programs and resources")
            
        return recommendations if recommendations else ["Neighborhood scores well across all categories - continue monitoring community feedback"] 