import json
from typing import Dict, List, Any
from datetime import datetime

class SFNeighborhoodData:
    def __init__(self):
        # Define SF neighborhoods and their characteristics
        self.neighborhoods = {
            "Mission District": {
                "boundaries": {
                    "north": "Market St",
                    "south": "Cesar Chavez St",
                    "east": "Potrero Ave",
                    "west": "Dolores St"
                },
                "characteristics": {
                    "culture": "Latino/Hispanic influence, artistic community",
                    "known_for": ["Street art", "Mexican restaurants", "Cultural diversity"],
                    "housing_type": "Mix of Victorian homes and modern apartments"
                },
                "price_ranges": {
                    "median_home": 1450000,
                    "median_rent": 3200,
                    "price_trend": "+4.2% YoY"
                }
            },
            "Pacific Heights": {
                "boundaries": {
                    "north": "Broadway",
                    "south": "California St",
                    "east": "Van Ness Ave",
                    "west": "Presidio Ave"
                },
                "characteristics": {
                    "culture": "Affluent, traditional",
                    "known_for": ["Luxury homes", "City views", "High-end shopping"],
                    "housing_type": "Large mansions and luxury apartments"
                },
                "price_ranges": {
                    "median_home": 4200000,
                    "median_rent": 5500,
                    "price_trend": "+3.8% YoY"
                }
            },
            "Hayes Valley": {
                "boundaries": {
                    "north": "McAllister St",
                    "south": "Market St",
                    "east": "Van Ness Ave",
                    "west": "Webster St"
                },
                "characteristics": {
                    "culture": "Modern, trendy",
                    "known_for": ["Boutique shopping", "Restaurants", "Arts scene"],
                    "housing_type": "Mix of Victorian and modern developments"
                },
                "price_ranges": {
                    "median_home": 1250000,
                    "median_rent": 3400,
                    "price_trend": "+5.1% YoY"
                }
            },
            "North Beach": {
                "boundaries": {
                    "north": "Bay St",
                    "south": "Broadway",
                    "east": "The Embarcadero",
                    "west": "Columbus Ave"
                },
                "characteristics": {
                    "culture": "Italian-American, bohemian",
                    "known_for": ["Italian restaurants", "Beat Generation history", "Cafes"],
                    "housing_type": "Historic apartments and condos"
                },
                "price_ranges": {
                    "median_home": 1350000,
                    "median_rent": 3100,
                    "price_trend": "+3.5% YoY"
                }
            }
        }

        # Crime data by neighborhood
        self.crime_data = {
            "Mission District": {
                "risk_level": "Medium",
                "safety_score": 6.5,
                "common_incidents": ["Property theft", "Vehicle break-ins", "Graffiti"],
                "trend": "Improving",
                "police_presence": "High",
                "neighborhood_watch": True
            },
            "Pacific Heights": {
                "risk_level": "Low",
                "safety_score": 9.2,
                "common_incidents": ["Package theft", "Car break-ins"],
                "trend": "Stable",
                "police_presence": "Medium",
                "neighborhood_watch": True
            },
            "Hayes Valley": {
                "risk_level": "Low-Medium",
                "safety_score": 7.8,
                "common_incidents": ["Property theft", "Bicycle theft"],
                "trend": "Improving",
                "police_presence": "Medium",
                "neighborhood_watch": True
            },
            "North Beach": {
                "risk_level": "Low",
                "safety_score": 8.1,
                "common_incidents": ["Tourist-related theft", "Noise complaints"],
                "trend": "Stable",
                "police_presence": "High",
                "neighborhood_watch": True
            }
        }

        # School data by neighborhood
        self.education_data = {
            "Mission District": {
                "public_schools": [
                    {"name": "Mission High School", "rating": 7.2},
                    {"name": "Everett Middle School", "rating": 6.8},
                    {"name": "Marshall Elementary", "rating": 7.5}
                ],
                "private_schools": [
                    {"name": "St. Peter's School", "rating": 8.4},
                    {"name": "Children's Day School", "rating": 8.9}
                ],
                "avg_test_scores": 78
            },
            "Pacific Heights": {
                "public_schools": [
                    {"name": "Sherman Elementary", "rating": 8.9},
                    {"name": "Roosevelt Middle School", "rating": 8.5}
                ],
                "private_schools": [
                    {"name": "Town School for Boys", "rating": 9.2},
                    {"name": "Convent & Stuart Hall", "rating": 9.4}
                ],
                "avg_test_scores": 92
            },
            "Hayes Valley": {
                "public_schools": [
                    {"name": "John Muir Elementary", "rating": 7.1},
                    {"name": "Creative Arts Charter", "rating": 8.2}
                ],
                "private_schools": [
                    {"name": "French American International", "rating": 9.1}
                ],
                "avg_test_scores": 84
            },
            "North Beach": {
                "public_schools": [
                    {"name": "Garfield Elementary", "rating": 8.1},
                    {"name": "Francisco Middle School", "rating": 7.4}
                ],
                "private_schools": [
                    {"name": "St. Peter & Paul School", "rating": 8.7}
                ],
                "avg_test_scores": 82
            }
        }

        # Transportation and amenities data
        self.amenities_data = {
            "Mission District": {
                "transit": {
                    "bart_stations": ["16th St Mission", "24th St Mission"],
                    "muni_lines": ["14", "49", "J"],
                    "transit_score": 95
                },
                "amenities": {
                    "restaurants": 450,
                    "bars": 85,
                    "cafes": 120,
                    "grocery_stores": 25,
                    "parks": 8,
                    "gyms": 15
                },
                "walkability": 96
            },
            "Pacific Heights": {
                "transit": {
                    "bart_stations": [],
                    "muni_lines": ["1", "2", "3", "22"],
                    "transit_score": 82
                },
                "amenities": {
                    "restaurants": 180,
                    "bars": 25,
                    "cafes": 45,
                    "grocery_stores": 12,
                    "parks": 5,
                    "gyms": 8
                },
                "walkability": 88
            },
            "Hayes Valley": {
                "transit": {
                    "bart_stations": [],
                    "muni_lines": ["6", "7", "21", "N"],
                    "transit_score": 93
                },
                "amenities": {
                    "restaurants": 220,
                    "bars": 45,
                    "cafes": 65,
                    "grocery_stores": 15,
                    "parks": 6,
                    "gyms": 12
                },
                "walkability": 95
            },
            "North Beach": {
                "transit": {
                    "bart_stations": [],
                    "muni_lines": ["8", "30", "45"],
                    "transit_score": 89
                },
                "amenities": {
                    "restaurants": 280,
                    "bars": 55,
                    "cafes": 75,
                    "grocery_stores": 18,
                    "parks": 7,
                    "gyms": 10
                },
                "walkability": 94
            }
        }

    def get_neighborhood_data(self, neighborhood: str) -> Dict[str, Any]:
        """Get comprehensive data for a specific neighborhood"""
        if neighborhood not in self.neighborhoods:
            return None

        return {
            "name": neighborhood,
            "basic_info": self.neighborhoods[neighborhood],
            "crime_stats": self.crime_data[neighborhood],
            "education": self.education_data[neighborhood],
            "amenities": self.amenities_data[neighborhood],
            "last_updated": datetime.now().isoformat()
        }

    def get_all_neighborhoods(self) -> List[str]:
        """Get list of all available neighborhoods"""
        return list(self.neighborhoods.keys())

    def get_neighborhood_comparison(self, neighborhoods: List[str]) -> Dict[str, Any]:
        """Compare multiple neighborhoods"""
        comparison = {}
        for hood in neighborhoods:
            if hood in self.neighborhoods:
                comparison[hood] = {
                    "median_home_price": self.neighborhoods[hood]["price_ranges"]["median_home"],
                    "safety_score": self.crime_data[hood]["safety_score"],
                    "transit_score": self.amenities_data[hood]["transit"]["transit_score"],
                    "walkability": self.amenities_data[hood]["walkability"]
                }
        return comparison

    def get_price_ranges(self) -> Dict[str, Dict[str, int]]:
        """Get price ranges for all neighborhoods"""
        return {hood: data["price_ranges"] for hood, data in self.neighborhoods.items()} 