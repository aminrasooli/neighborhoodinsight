from typing import Dict, List, Any
from datetime import datetime, timedelta
import random

class TransportationDataCollector:
    def __init__(self):
        # Transit data by neighborhood
        self.transit_data = {
            "Mission District": {
                "public_transit": {
                    "subway_stations": [
                        {
                            "name": "16th Street Mission",
                            "lines": ["BART"],
                            "avg_daily_riders": 12000,
                            "accessibility": True
                        },
                        {
                            "name": "24th Street Mission",
                            "lines": ["BART"],
                            "avg_daily_riders": 11000,
                            "accessibility": True
                        }
                    ],
                    "bus_lines": [
                        {
                            "number": "14",
                            "frequency": "8 mins",
                            "coverage": "High",
                            "reliability": "85%"
                        },
                        {
                            "number": "49",
                            "frequency": "10 mins",
                            "coverage": "Medium",
                            "reliability": "82%"
                        }
                    ],
                    "light_rail": [
                        {
                            "line": "J-Church",
                            "frequency": "12 mins",
                            "reliability": "88%"
                        }
                    ]
                },
                "bike_infrastructure": {
                    "bike_lanes_miles": 8.5,
                    "bike_sharing_stations": 12,
                    "bike_parking_spots": 450,
                    "bike_friendly_rating": 8.2
                },
                "walkability": {
                    "walk_score": 95,
                    "pedestrian_friendly_rating": 8.8,
                    "sidewalk_condition": "Good",
                    "street_lighting": "Well-lit"
                },
                "parking": {
                    "street_parking": "Limited",
                    "parking_garages": 3,
                    "avg_monthly_parking": 250,
                    "parking_difficulty": "High"
                }
            },
            "Pacific Heights": {
                "public_transit": {
                    "subway_stations": [],
                    "bus_lines": [
                        {
                            "number": "1",
                            "frequency": "10 mins",
                            "coverage": "Medium",
                            "reliability": "90%"
                        },
                        {
                            "number": "22",
                            "frequency": "12 mins",
                            "coverage": "High",
                            "reliability": "88%"
                        }
                    ],
                    "light_rail": []
                },
                "bike_infrastructure": {
                    "bike_lanes_miles": 4.2,
                    "bike_sharing_stations": 6,
                    "bike_parking_spots": 220,
                    "bike_friendly_rating": 7.0
                },
                "walkability": {
                    "walk_score": 88,
                    "pedestrian_friendly_rating": 8.5,
                    "sidewalk_condition": "Excellent",
                    "street_lighting": "Well-lit"
                },
                "parking": {
                    "street_parking": "Moderate",
                    "parking_garages": 2,
                    "avg_monthly_parking": 300,
                    "parking_difficulty": "Medium"
                }
            },
            "Hayes Valley": {
                "public_transit": {
                    "subway_stations": [],
                    "bus_lines": [
                        {
                            "number": "21",
                            "frequency": "10 mins",
                            "coverage": "High",
                            "reliability": "87%"
                        }
                    ],
                    "light_rail": [
                        {
                            "line": "N-Judah",
                            "frequency": "10 mins",
                            "reliability": "89%"
                        }
                    ]
                },
                "bike_infrastructure": {
                    "bike_lanes_miles": 6.8,
                    "bike_sharing_stations": 8,
                    "bike_parking_spots": 380,
                    "bike_friendly_rating": 8.5
                },
                "walkability": {
                    "walk_score": 92,
                    "pedestrian_friendly_rating": 9.0,
                    "sidewalk_condition": "Excellent",
                    "street_lighting": "Well-lit"
                },
                "parking": {
                    "street_parking": "Limited",
                    "parking_garages": 4,
                    "avg_monthly_parking": 275,
                    "parking_difficulty": "High"
                }
            },
            "North Beach": {
                "public_transit": {
                    "subway_stations": [],
                    "bus_lines": [
                        {
                            "number": "30",
                            "frequency": "12 mins",
                            "coverage": "High",
                            "reliability": "85%"
                        },
                        {
                            "number": "45",
                            "frequency": "15 mins",
                            "coverage": "Medium",
                            "reliability": "83%"
                        }
                    ],
                    "light_rail": []
                },
                "bike_infrastructure": {
                    "bike_lanes_miles": 5.5,
                    "bike_sharing_stations": 7,
                    "bike_parking_spots": 290,
                    "bike_friendly_rating": 7.8
                },
                "walkability": {
                    "walk_score": 98,
                    "pedestrian_friendly_rating": 9.2,
                    "sidewalk_condition": "Good",
                    "street_lighting": "Well-lit"
                },
                "parking": {
                    "street_parking": "Very Limited",
                    "parking_garages": 5,
                    "avg_monthly_parking": 325,
                    "parking_difficulty": "Very High"
                }
            }
        }

        # Commute times to key destinations
        self.commute_times = {
            "Mission District": {
                "downtown": {
                    "public_transit": 15,
                    "driving": 20,
                    "biking": 25,
                    "walking": 45
                },
                "financial_district": {
                    "public_transit": 18,
                    "driving": 22,
                    "biking": 28,
                    "walking": 50
                }
            },
            "Pacific Heights": {
                "downtown": {
                    "public_transit": 25,
                    "driving": 20,
                    "biking": 30,
                    "walking": 55
                },
                "financial_district": {
                    "public_transit": 28,
                    "driving": 25,
                    "biking": 35,
                    "walking": 60
                }
            },
            "Hayes Valley": {
                "downtown": {
                    "public_transit": 20,
                    "driving": 15,
                    "biking": 20,
                    "walking": 40
                },
                "financial_district": {
                    "public_transit": 22,
                    "driving": 18,
                    "biking": 25,
                    "walking": 45
                }
            },
            "North Beach": {
                "downtown": {
                    "public_transit": 15,
                    "driving": 12,
                    "biking": 18,
                    "walking": 35
                },
                "financial_district": {
                    "public_transit": 12,
                    "driving": 10,
                    "biking": 15,
                    "walking": 30
                }
            }
        }

    def get_transportation_report(self, neighborhood: str) -> Dict[str, Any]:
        """Get comprehensive transportation report for a neighborhood"""
        if neighborhood not in self.transit_data:
            return None

        return {
            "transit_options": self.transit_data[neighborhood],
            "commute_times": self.commute_times[neighborhood],
            "last_updated": datetime.now().isoformat()
        }

    def get_transit_comparison(self, neighborhoods: List[str]) -> Dict[str, Any]:
        """Compare transportation metrics across neighborhoods"""
        comparison = {}
        for hood in neighborhoods:
            if hood in self.transit_data:
                data = self.transit_data[hood]
                comparison[hood] = {
                    "walk_score": data["walkability"]["walk_score"],
                    "bike_friendly_rating": data["bike_infrastructure"]["bike_friendly_rating"],
                    "public_transit_options": len(data["public_transit"]["subway_stations"]) + 
                                           len(data["public_transit"]["bus_lines"]) +
                                           len(data["public_transit"]["light_rail"]),
                    "parking_difficulty": data["parking"]["parking_difficulty"]
                }
        return comparison

    def get_transportation_score(self, neighborhood: str) -> Dict[str, Any]:
        """Calculate transportation score for a neighborhood"""
        if neighborhood not in self.transit_data:
            return None

        data = self.transit_data[neighborhood]
        
        # Calculate component scores (0-100 scale)
        walk_score = data["walkability"]["walk_score"]
        bike_score = data["bike_infrastructure"]["bike_friendly_rating"] * 10
        
        # Calculate transit score
        transit_options = len(data["public_transit"]["subway_stations"]) * 20 + \
                         len(data["public_transit"]["bus_lines"]) * 10 + \
                         len(data["public_transit"]["light_rail"]) * 15
        transit_score = min(100, transit_options)
        
        # Calculate parking score (inverse of difficulty)
        parking_difficulty_map = {
            "Very High": 20,
            "High": 40,
            "Medium": 60,
            "Low": 80,
            "Very Low": 100
        }
        parking_score = parking_difficulty_map.get(data["parking"]["parking_difficulty"], 50)
        
        # Calculate weighted total
        total_score = (
            walk_score * 0.35 +
            transit_score * 0.30 +
            bike_score * 0.20 +
            parking_score * 0.15
        )

        return {
            "total_score": round(total_score, 1),
            "components": {
                "walkability": round(walk_score, 1),
                "public_transit": round(transit_score, 1),
                "bike_friendly": round(bike_score, 1),
                "parking": round(parking_score, 1)
            },
            "interpretation": self._get_transportation_interpretation(total_score),
            "last_updated": datetime.now().isoformat()
        }

    def _get_transportation_interpretation(self, score: float) -> str:
        """Generate transportation quality interpretation based on score"""
        if score >= 90:
            return "Exceptional transportation options with excellent accessibility"
        elif score >= 80:
            return "Very good transportation infrastructure with multiple options"
        elif score >= 70:
            return "Good transportation options with some limitations"
        elif score >= 60:
            return "Adequate transportation with room for improvement"
        else:
            return "Limited transportation options, heavily car-dependent" 