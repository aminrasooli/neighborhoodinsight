import numpy as np
from typing import Dict, Any
import re

class NeighborhoodScorer:
    def __init__(self):
        # Initialize feature weights
        self.weights = {
            'safety': 0.3,
            'real_estate': 0.25,
            'education': 0.2,
            'amenities': 0.15,
            'community': 0.1
        }
        
    def calculate_score(self, neighborhood_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate an overall neighborhood score based on various factors
        Returns a dictionary with overall score and component scores
        """
        try:
            # Calculate component scores
            safety_score = self._calculate_safety_score(neighborhood_data.get('crime_analysis', {}))
            real_estate_score = self._calculate_real_estate_score(neighborhood_data.get('real_estate', {}))
            education_score = self._calculate_education_score(neighborhood_data.get('community', {}).get('education', {}))
            amenities_score = self._calculate_amenities_score(neighborhood_data.get('community', {}).get('amenities', {}))
            community_score = self._calculate_community_score(neighborhood_data.get('community', {}))
            
            # Calculate weighted average for final score
            final_score = (
                safety_score * self.weights['safety'] +
                real_estate_score * self.weights['real_estate'] +
                education_score * self.weights['education'] +
                amenities_score * self.weights['amenities'] +
                community_score * self.weights['community']
            )
            
            return {
                "overall_score": round(final_score, 2),
                "component_scores": {
                    "safety": round(safety_score, 2),
                    "real_estate": round(real_estate_score, 2),
                    "education": round(education_score, 2),
                    "amenities": round(amenities_score, 2),
                    "community": round(community_score, 2)
                },
                "interpretation": self._interpret_score(final_score),
                "recommendations": self._generate_recommendations(
                    safety_score, real_estate_score, education_score,
                    amenities_score, community_score
                )
            }
        except Exception as e:
            print(f"Error calculating neighborhood score: {str(e)}")
            return None

    def _calculate_safety_score(self, crime_data: Dict[str, Any]) -> float:
        """Calculate safety score based on crime data"""
        try:
            # Convert risk level to numeric score
            risk_levels = {"Low": 9, "Medium": 6, "High": 3}
            risk_score = risk_levels.get(crime_data.get('risk_level', 'Medium'), 6)
            
            # Use safety score if available
            safety_score = float(crime_data.get('safety_score', 7.0))
            
            # Count recent incidents
            incidents = len(crime_data.get('recent_incidents', []))
            incident_score = 10 - min(incidents, 5)  # Deduct points for incidents, max 5
            
            # Combine scores
            return (risk_score + safety_score + incident_score) / 3
            
        except Exception as e:
            print(f"Error in safety score calculation: {str(e)}")
            return 5.0  # Default middle score

    def _calculate_real_estate_score(self, real_estate_data: Dict[str, Any]) -> float:
        """Calculate real estate score based on market data"""
        try:
            # Extract price trend percentage
            trend_str = real_estate_data.get('price_trend', '+0%')
            trend_match = re.search(r'([+-]?\d+\.?\d*)', trend_str)
            price_trend = float(trend_match.group(1)) if trend_match else 0
            
            # Convert market status to score
            market_scores = {
                "Hot Market": 9,
                "Seller's Market": 8,
                "Balanced Market": 7,
                "Buyer's Market": 6
            }
            market_score = market_scores.get(real_estate_data.get('market_status', 'Balanced Market'), 7)
            
            # Calculate appreciation score
            appreciation_str = real_estate_data.get('historical_appreciation', '0%')
            appreciation_match = re.search(r'(\d+\.?\d*)', appreciation_str)
            appreciation = float(appreciation_match.group(1)) if appreciation_match else 0
            appreciation_score = min(10, appreciation + 5)  # Score from 0-10
            
            # Combine scores
            return (market_score + appreciation_score + min(10, price_trend + 5)) / 3
            
        except Exception as e:
            print(f"Error in real estate score calculation: {str(e)}")
            return 5.0

    def _calculate_education_score(self, education_data: Dict[str, Any]) -> float:
        """Calculate education score based on schools data"""
        try:
            # Use overall schools rating
            base_score = float(education_data.get('schools_rating', 7.0))
            
            # Calculate average school ratings
            schools = education_data.get('nearby_schools', [])
            if schools:
                avg_rating = sum(school.get('rating', 7.0) for school in schools) / len(schools)
                return (base_score + avg_rating) / 2
            
            return base_score
            
        except Exception as e:
            print(f"Error in education score calculation: {str(e)}")
            return 5.0

    def _calculate_amenities_score(self, amenities_data: Dict[str, Any]) -> float:
        """Calculate amenities score based on nearby facilities"""
        try:
            # Use walkability and transit scores
            walkability = float(amenities_data.get('walkability_score', 70)) / 10
            transit = float(amenities_data.get('transit_score', 70)) / 10
            
            # Calculate amenities diversity score
            nearby = amenities_data.get('nearby', {})
            amenities_count = sum(nearby.values())
            diversity_score = min(10, amenities_count / 10)
            
            return (walkability + transit + diversity_score) / 3
            
        except Exception as e:
            print(f"Error in amenities score calculation: {str(e)}")
            return 5.0

    def _calculate_community_score(self, community_data: Dict[str, Any]) -> float:
        """Calculate community score based on various factors"""
        try:
            # Count positive aspects and complaints
            positives = len(community_data.get('positive_aspects', []))
            complaints = len(community_data.get('top_complaints', []))
            
            # Calculate base score
            base_score = 7.0  # Start with above average
            
            # Add points for positives, subtract for complaints
            score = base_score + (positives * 0.5) - (complaints * 0.3)
            
            # Ensure score is between 0 and 10
            return max(0, min(10, score))
            
        except Exception as e:
            print(f"Error in community score calculation: {str(e)}")
            return 5.0

    def _interpret_score(self, score: float) -> str:
        """Provide interpretation of the overall score"""
        if score >= 9:
            return "Exceptional neighborhood with outstanding features across all categories"
        elif score >= 8:
            return "Excellent neighborhood with strong performance in most areas"
        elif score >= 7:
            return "Very good neighborhood with above-average characteristics"
        elif score >= 6:
            return "Good neighborhood with some room for improvement"
        elif score >= 5:
            return "Average neighborhood with mixed characteristics"
        else:
            return "Below average neighborhood with significant room for improvement"

    def _generate_recommendations(self, safety: float, real_estate: float,
                                education: float, amenities: float,
                                community: float) -> list:
        """Generate specific recommendations based on component scores"""
        recommendations = []
        
        if safety < 6:
            recommendations.append("Consider reviewing local safety measures and community watch programs")
        if real_estate < 6:
            recommendations.append("Market conditions suggest potential for future value appreciation")
        if education < 6:
            recommendations.append("Research additional educational resources and programs in the area")
        if amenities < 6:
            recommendations.append("Look into upcoming development projects that might improve local amenities")
        if community < 6:
            recommendations.append("Explore community engagement opportunities to enhance neighborhood connection")
            
        return recommendations if recommendations else ["No specific recommendations - neighborhood scores well across all categories"] 