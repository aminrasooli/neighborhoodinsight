from typing import Dict, List, Any
from datetime import datetime, timedelta
import random

class CrimeDataCollector:
    def __init__(self):
        # Crime statistics by neighborhood
        self.crime_stats = {
            "Mission District": {
                "overall_safety_score": 6.5,
                "risk_level": "Medium",
                "crime_rate_per_1000": 45.2,
                "year_over_year_change": "-8.5%",
                "police_response_time": "8.5 minutes",
                "crime_categories": {
                    "violent_crime": {
                        "incidents": 85,
                        "trend": "Decreasing",
                        "change": "-12%"
                    },
                    "property_crime": {
                        "incidents": 425,
                        "trend": "Stable",
                        "change": "-3%"
                    },
                    "quality_of_life": {
                        "incidents": 310,
                        "trend": "Improving",
                        "change": "-15%"
                    }
                }
            },
            "Pacific Heights": {
                "overall_safety_score": 9.2,
                "risk_level": "Low",
                "crime_rate_per_1000": 12.8,
                "year_over_year_change": "-5.2%",
                "police_response_time": "6.5 minutes",
                "crime_categories": {
                    "violent_crime": {
                        "incidents": 15,
                        "trend": "Stable",
                        "change": "-2%"
                    },
                    "property_crime": {
                        "incidents": 180,
                        "trend": "Decreasing",
                        "change": "-8%"
                    },
                    "quality_of_life": {
                        "incidents": 95,
                        "trend": "Stable",
                        "change": "-4%"
                    }
                }
            },
            "Hayes Valley": {
                "overall_safety_score": 7.8,
                "risk_level": "Low-Medium",
                "crime_rate_per_1000": 28.5,
                "year_over_year_change": "-12.3%",
                "police_response_time": "7.5 minutes",
                "crime_categories": {
                    "violent_crime": {
                        "incidents": 45,
                        "trend": "Decreasing",
                        "change": "-18%"
                    },
                    "property_crime": {
                        "incidents": 285,
                        "trend": "Improving",
                        "change": "-15%"
                    },
                    "quality_of_life": {
                        "incidents": 195,
                        "trend": "Stable",
                        "change": "-5%"
                    }
                }
            },
            "North Beach": {
                "overall_safety_score": 8.1,
                "risk_level": "Low",
                "crime_rate_per_1000": 22.4,
                "year_over_year_change": "-6.8%",
                "police_response_time": "7.0 minutes",
                "crime_categories": {
                    "violent_crime": {
                        "incidents": 35,
                        "trend": "Stable",
                        "change": "-4%"
                    },
                    "property_crime": {
                        "incidents": 245,
                        "trend": "Decreasing",
                        "change": "-10%"
                    },
                    "quality_of_life": {
                        "incidents": 165,
                        "trend": "Improving",
                        "change": "-12%"
                    }
                }
            }
        }

        # Recent incidents (last 30 days)
        self.recent_incidents = {
            "Mission District": [
                {
                    "type": "Vehicle Break-in",
                    "date": "2024-03-10",
                    "time": "23:15",
                    "severity": "Low",
                    "status": "Under Investigation"
                },
                {
                    "type": "Vandalism",
                    "date": "2024-03-08",
                    "time": "02:30",
                    "severity": "Low",
                    "status": "Resolved"
                }
            ],
            "Pacific Heights": [
                {
                    "type": "Package Theft",
                    "date": "2024-03-09",
                    "time": "14:20",
                    "severity": "Low",
                    "status": "Under Investigation"
                }
            ],
            "Hayes Valley": [
                {
                    "type": "Bicycle Theft",
                    "date": "2024-03-10",
                    "time": "16:45",
                    "severity": "Low",
                    "status": "Under Investigation"
                },
                {
                    "type": "Noise Complaint",
                    "date": "2024-03-07",
                    "time": "23:00",
                    "severity": "Low",
                    "status": "Resolved"
                }
            ],
            "North Beach": [
                {
                    "type": "Pickpocketing",
                    "date": "2024-03-09",
                    "time": "18:30",
                    "severity": "Low",
                    "status": "Under Investigation"
                }
            ]
        }

        # Safety initiatives and community programs
        self.safety_initiatives = {
            "Mission District": [
                {
                    "name": "Community Watch Program",
                    "status": "Active",
                    "participants": 250,
                    "effectiveness": "High"
                },
                {
                    "name": "Business District Security Cameras",
                    "status": "Active",
                    "coverage": "80%",
                    "effectiveness": "Medium"
                }
            ],
            "Pacific Heights": [
                {
                    "name": "Neighborhood Security Patrol",
                    "status": "Active",
                    "coverage": "24/7",
                    "effectiveness": "High"
                }
            ],
            "Hayes Valley": [
                {
                    "name": "Community Safety Workshops",
                    "status": "Active",
                    "frequency": "Monthly",
                    "effectiveness": "Medium"
                }
            ],
            "North Beach": [
                {
                    "name": "Tourist Area Safety Program",
                    "status": "Active",
                    "coverage": "Daily",
                    "effectiveness": "High"
                }
            ]
        }

    def get_safety_report(self, neighborhood: str) -> Dict[str, Any]:
        """Get comprehensive safety report for a neighborhood"""
        if neighborhood not in self.crime_stats:
            return None

        return {
            "statistics": self.crime_stats[neighborhood],
            "recent_incidents": self.recent_incidents.get(neighborhood, []),
            "safety_initiatives": self.safety_initiatives.get(neighborhood, []),
            "last_updated": datetime.now().isoformat()
        }

    def get_recent_incidents(self, neighborhood: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get recent incidents in the neighborhood"""
        if neighborhood not in self.recent_incidents:
            return []

        cutoff_date = datetime.now() - timedelta(days=days)
        return [
            incident for incident in self.recent_incidents[neighborhood]
            if datetime.strptime(incident["date"], "%Y-%m-%d") > cutoff_date
        ]

    def get_safety_comparison(self, neighborhoods: List[str]) -> Dict[str, Any]:
        """Compare safety metrics across neighborhoods"""
        comparison = {}
        for hood in neighborhoods:
            if hood in self.crime_stats:
                comparison[hood] = {
                    "safety_score": self.crime_stats[hood]["overall_safety_score"],
                    "risk_level": self.crime_stats[hood]["risk_level"],
                    "crime_rate": self.crime_stats[hood]["crime_rate_per_1000"],
                    "trend": self.crime_stats[hood]["year_over_year_change"]
                }
        return comparison

    def get_safety_score(self, neighborhood: str) -> Dict[str, Any]:
        """Calculate detailed safety score components"""
        if neighborhood not in self.crime_stats:
            return None

        stats = self.crime_stats[neighborhood]
        
        # Calculate component scores
        violent_crime_score = 100 - (stats["crime_categories"]["violent_crime"]["incidents"] / 10)
        property_crime_score = 100 - (stats["crime_categories"]["property_crime"]["incidents"] / 50)
        qol_score = 100 - (stats["crime_categories"]["quality_of_life"]["incidents"] / 40)
        
        # Normalize scores
        violent_crime_score = max(0, min(100, violent_crime_score))
        property_crime_score = max(0, min(100, property_crime_score))
        qol_score = max(0, min(100, qol_score))
        
        # Calculate weighted total
        total_score = (
            violent_crime_score * 0.4 +
            property_crime_score * 0.35 +
            qol_score * 0.25
        )

        return {
            "total_score": round(total_score, 1),
            "components": {
                "violent_crime": round(violent_crime_score, 1),
                "property_crime": round(property_crime_score, 1),
                "quality_of_life": round(qol_score, 1)
            },
            "interpretation": self._get_safety_interpretation(total_score),
            "last_updated": datetime.now().isoformat()
        }

    def _get_safety_interpretation(self, score: float) -> str:
        """Generate safety interpretation based on score"""
        if score >= 90:
            return "Exceptionally safe neighborhood with minimal crime concerns"
        elif score >= 80:
            return "Very safe neighborhood with low crime rates"
        elif score >= 70:
            return "Generally safe neighborhood with moderate crime concerns"
        elif score >= 60:
            return "Moderately safe neighborhood with some crime concerns"
        else:
            return "Higher crime area with significant safety concerns" 