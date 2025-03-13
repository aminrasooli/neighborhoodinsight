from typing import Dict, List, Any
from datetime import datetime
import random

class AmenitiesDataCollector:
    def __init__(self):
        # Amenities data by neighborhood
        self.amenities_data = {
            "Mission District": {
                "dining": {
                    "restaurants": [
                        {
                            "name": "Foreign Cinema",
                            "cuisine": "California",
                            "price_range": "$$$",
                            "rating": 4.5,
                            "reviews": 2800
                        },
                        {
                            "name": "Tartine Bakery",
                            "cuisine": "Bakery",
                            "price_range": "$$",
                            "rating": 4.7,
                            "reviews": 3500
                        }
                    ],
                    "cafes": 45,
                    "bars": 38,
                    "food_diversity_score": 9.2
                },
                "shopping": {
                    "grocery_stores": [
                        {
                            "name": "Whole Foods Market",
                            "type": "Supermarket",
                            "price_range": "$$$",
                            "organic_options": True
                        },
                        {
                            "name": "Local Mission Market",
                            "type": "Local Market",
                            "price_range": "$$",
                            "organic_options": True
                        }
                    ],
                    "retail_stores": 85,
                    "shopping_centers": 2,
                    "specialty_shops": 35
                },
                "entertainment": {
                    "movie_theaters": 2,
                    "music_venues": 5,
                    "art_galleries": 12,
                    "performance_spaces": 3
                },
                "outdoor_spaces": {
                    "parks": [
                        {
                            "name": "Dolores Park",
                            "size_acres": 16.0,
                            "facilities": ["Playground", "Tennis Courts", "Basketball Courts"],
                            "rating": 4.8
                        }
                    ],
                    "playgrounds": 3,
                    "dog_parks": 2,
                    "green_spaces": 5
                },
                "services": {
                    "gyms": 8,
                    "banks": 6,
                    "post_offices": 1,
                    "libraries": 1,
                    "medical_facilities": 4,
                    "pharmacies": 5
                }
            },
            "Pacific Heights": {
                "dining": {
                    "restaurants": [
                        {
                            "name": "State Bird Provisions",
                            "cuisine": "Contemporary American",
                            "price_range": "$$$$",
                            "rating": 4.6,
                            "reviews": 2200
                        }
                    ],
                    "cafes": 25,
                    "bars": 15,
                    "food_diversity_score": 8.5
                },
                "shopping": {
                    "grocery_stores": [
                        {
                            "name": "Mollie Stone's Markets",
                            "type": "Supermarket",
                            "price_range": "$$$",
                            "organic_options": True
                        }
                    ],
                    "retail_stores": 65,
                    "shopping_centers": 1,
                    "specialty_shops": 28
                },
                "entertainment": {
                    "movie_theaters": 1,
                    "music_venues": 1,
                    "art_galleries": 8,
                    "performance_spaces": 1
                },
                "outdoor_spaces": {
                    "parks": [
                        {
                            "name": "Alta Plaza Park",
                            "size_acres": 12.0,
                            "facilities": ["Tennis Courts", "Playground", "Dog Play Area"],
                            "rating": 4.7
                        }
                    ],
                    "playgrounds": 2,
                    "dog_parks": 1,
                    "green_spaces": 4
                },
                "services": {
                    "gyms": 5,
                    "banks": 4,
                    "post_offices": 1,
                    "libraries": 1,
                    "medical_facilities": 3,
                    "pharmacies": 3
                }
            },
            "Hayes Valley": {
                "dining": {
                    "restaurants": [
                        {
                            "name": "Rich Table",
                            "cuisine": "California",
                            "price_range": "$$$$",
                            "rating": 4.7,
                            "reviews": 1800
                        }
                    ],
                    "cafes": 30,
                    "bars": 22,
                    "food_diversity_score": 8.8
                },
                "shopping": {
                    "grocery_stores": [
                        {
                            "name": "Trader Joe's",
                            "type": "Supermarket",
                            "price_range": "$$",
                            "organic_options": True
                        }
                    ],
                    "retail_stores": 75,
                    "shopping_centers": 0,
                    "specialty_shops": 42
                },
                "entertainment": {
                    "movie_theaters": 0,
                    "music_venues": 2,
                    "art_galleries": 15,
                    "performance_spaces": 2
                },
                "outdoor_spaces": {
                    "parks": [
                        {
                            "name": "Patricia's Green",
                            "size_acres": 0.5,
                            "facilities": ["Public Art", "Seating Areas"],
                            "rating": 4.5
                        }
                    ],
                    "playgrounds": 1,
                    "dog_parks": 1,
                    "green_spaces": 3
                },
                "services": {
                    "gyms": 6,
                    "banks": 3,
                    "post_offices": 0,
                    "libraries": 0,
                    "medical_facilities": 2,
                    "pharmacies": 4
                }
            },
            "North Beach": {
                "dining": {
                    "restaurants": [
                        {
                            "name": "Tony's Pizza Napoletana",
                            "cuisine": "Italian",
                            "price_range": "$$",
                            "rating": 4.8,
                            "reviews": 4200
                        }
                    ],
                    "cafes": 35,
                    "bars": 28,
                    "food_diversity_score": 8.9
                },
                "shopping": {
                    "grocery_stores": [
                        {
                            "name": "North Beach Market",
                            "type": "Local Market",
                            "price_range": "$$",
                            "organic_options": True
                        }
                    ],
                    "retail_stores": 55,
                    "shopping_centers": 0,
                    "specialty_shops": 25
                },
                "entertainment": {
                    "movie_theaters": 1,
                    "music_venues": 4,
                    "art_galleries": 6,
                    "performance_spaces": 2
                },
                "outdoor_spaces": {
                    "parks": [
                        {
                            "name": "Washington Square",
                            "size_acres": 2.26,
                            "facilities": ["Playground", "Benches", "Open Space"],
                            "rating": 4.6
                        }
                    ],
                    "playgrounds": 2,
                    "dog_parks": 1,
                    "green_spaces": 3
                },
                "services": {
                    "gyms": 4,
                    "banks": 5,
                    "post_offices": 1,
                    "libraries": 1,
                    "medical_facilities": 2,
                    "pharmacies": 3
                }
            }
        }

    def get_amenities_report(self, neighborhood: str) -> Dict[str, Any]:
        """Get comprehensive amenities report for a neighborhood"""
        if neighborhood not in self.amenities_data:
            return None

        return {
            "amenities": self.amenities_data[neighborhood],
            "summary": self._generate_summary(neighborhood),
            "last_updated": datetime.now().isoformat()
        }

    def get_amenities_comparison(self, neighborhoods: List[str]) -> Dict[str, Any]:
        """Compare amenities across neighborhoods"""
        comparison = {}
        for hood in neighborhoods:
            if hood in self.amenities_data:
                data = self.amenities_data[hood]
                comparison[hood] = {
                    "restaurants": len(data["dining"]["restaurants"]),
                    "cafes": data["dining"]["cafes"],
                    "bars": data["dining"]["bars"],
                    "retail_stores": data["shopping"]["retail_stores"],
                    "grocery_stores": len(data["shopping"]["grocery_stores"]),
                    "entertainment_venues": (
                        data["entertainment"]["movie_theaters"] +
                        data["entertainment"]["music_venues"] +
                        data["entertainment"]["art_galleries"] +
                        data["entertainment"]["performance_spaces"]
                    ),
                    "parks": len(data["outdoor_spaces"]["parks"]),
                    "essential_services": (
                        data["services"]["gyms"] +
                        data["services"]["banks"] +
                        data["services"]["post_offices"] +
                        data["services"]["libraries"] +
                        data["services"]["medical_facilities"] +
                        data["services"]["pharmacies"]
                    )
                }
        return comparison

    def get_amenities_score(self, neighborhood: str) -> Dict[str, Any]:
        """Calculate amenities score for a neighborhood"""
        if neighborhood not in self.amenities_data:
            return None

        data = self.amenities_data[neighborhood]
        
        # Calculate component scores (0-100 scale)
        dining_score = min(100, (
            len(data["dining"]["restaurants"]) * 15 +
            data["dining"]["cafes"] * 2 +
            data["dining"]["bars"] * 2 +
            data["dining"]["food_diversity_score"] * 5
        ) / 5)
        
        shopping_score = min(100, (
            len(data["shopping"]["grocery_stores"]) * 20 +
            data["shopping"]["retail_stores"] * 0.5 +
            data["shopping"]["shopping_centers"] * 15 +
            data["shopping"]["specialty_shops"] * 1
        ) / 3)
        
        entertainment_score = min(100, (
            data["entertainment"]["movie_theaters"] * 20 +
            data["entertainment"]["music_venues"] * 15 +
            data["entertainment"]["art_galleries"] * 5 +
            data["entertainment"]["performance_spaces"] * 15
        ) / 2)
        
        outdoor_score = min(100, (
            len(data["outdoor_spaces"]["parks"]) * 30 +
            data["outdoor_spaces"]["playgrounds"] * 15 +
            data["outdoor_spaces"]["dog_parks"] * 15 +
            data["outdoor_spaces"]["green_spaces"] * 10
        ) / 2)
        
        services_score = min(100, (
            data["services"]["gyms"] * 10 +
            data["services"]["banks"] * 10 +
            data["services"]["post_offices"] * 15 +
            data["services"]["libraries"] * 15 +
            data["services"]["medical_facilities"] * 20 +
            data["services"]["pharmacies"] * 10
        ) / 2)
        
        # Calculate weighted total
        total_score = (
            dining_score * 0.25 +
            shopping_score * 0.20 +
            entertainment_score * 0.20 +
            outdoor_score * 0.20 +
            services_score * 0.15
        )

        return {
            "total_score": round(total_score, 1),
            "components": {
                "dining": round(dining_score, 1),
                "shopping": round(shopping_score, 1),
                "entertainment": round(entertainment_score, 1),
                "outdoor_spaces": round(outdoor_score, 1),
                "services": round(services_score, 1)
            },
            "interpretation": self._get_amenities_interpretation(total_score),
            "last_updated": datetime.now().isoformat()
        }

    def _generate_summary(self, neighborhood: str) -> str:
        """Generate a summary of neighborhood amenities"""
        data = self.amenities_data[neighborhood]
        return f"{neighborhood} offers {data['dining']['cafes']} cafes, " + \
               f"{data['dining']['bars']} bars, {data['shopping']['retail_stores']} retail stores, " + \
               f"and {len(data['outdoor_spaces']['parks'])} parks. The area has " + \
               f"{data['services']['medical_facilities']} medical facilities and " + \
               f"{data['services']['pharmacies']} pharmacies."

    def _get_amenities_interpretation(self, score: float) -> str:
        """Generate amenities quality interpretation based on score"""
        if score >= 90:
            return "Exceptional variety of amenities with excellent accessibility"
        elif score >= 80:
            return "Very good selection of amenities covering all essential needs"
        elif score >= 70:
            return "Good range of amenities with some specialty options"
        elif score >= 60:
            return "Adequate amenities for basic needs"
        else:
            return "Limited amenities, may require travel to other areas" 