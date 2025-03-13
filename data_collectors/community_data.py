from typing import Dict, List, Any
from datetime import datetime, timedelta
import random

class CommunityDataCollector:
    def __init__(self):
        self.community_feedback = {
            "Mission District": {
                "reviews": [
                    {
                        "text": "Love the vibrant culture and amazing food scene. The murals are incredible!",
                        "rating": 5,
                        "date": "2024-03-10",
                        "category": "Culture"
                    },
                    {
                        "text": "Great restaurants but parking can be challenging during peak hours.",
                        "rating": 4,
                        "date": "2024-03-09",
                        "category": "Infrastructure"
                    },
                    {
                        "text": "Some concerns about property crime, but overall community is very active.",
                        "rating": 3,
                        "date": "2024-03-08",
                        "category": "Safety"
                    }
                ],
                "common_topics": {
                    "positive": [
                        "Cultural diversity",
                        "Food scene",
                        "Public transportation",
                        "Street art",
                        "Community events"
                    ],
                    "concerns": [
                        "Parking availability",
                        "Property crime",
                        "Gentrification",
                        "Housing costs",
                        "Street cleanliness"
                    ]
                }
            },
            "Pacific Heights": {
                "reviews": [
                    {
                        "text": "Beautiful neighborhood with stunning views. Very safe and clean.",
                        "rating": 5,
                        "date": "2024-03-10",
                        "category": "Environment"
                    },
                    {
                        "text": "Excellent schools and peaceful streets. Limited nightlife though.",
                        "rating": 4,
                        "date": "2024-03-09",
                        "category": "Lifestyle"
                    },
                    {
                        "text": "Gorgeous area but very expensive. Some shops are overpriced.",
                        "rating": 4,
                        "date": "2024-03-08",
                        "category": "Cost"
                    }
                ],
                "common_topics": {
                    "positive": [
                        "Safety",
                        "Clean streets",
                        "Views",
                        "School quality",
                        "Architecture"
                    ],
                    "concerns": [
                        "Housing costs",
                        "Limited nightlife",
                        "Parking on hills",
                        "Tourist traffic",
                        "Shop prices"
                    ]
                }
            },
            "Hayes Valley": {
                "reviews": [
                    {
                        "text": "Perfect mix of shops, restaurants, and residential charm.",
                        "rating": 5,
                        "date": "2024-03-10",
                        "category": "Lifestyle"
                    },
                    {
                        "text": "Great location but new construction is changing the character.",
                        "rating": 4,
                        "date": "2024-03-09",
                        "category": "Development"
                    },
                    {
                        "text": "Love the boutiques and cafes. Very walkable area.",
                        "rating": 5,
                        "date": "2024-03-08",
                        "category": "Amenities"
                    }
                ],
                "common_topics": {
                    "positive": [
                        "Shopping",
                        "Restaurants",
                        "Walkability",
                        "Central location",
                        "Parks"
                    ],
                    "concerns": [
                        "New construction",
                        "Rising rents",
                        "Weekend crowds",
                        "Parking",
                        "Traffic"
                    ]
                }
            },
            "North Beach": {
                "reviews": [
                    {
                        "text": "Historic charm with great Italian restaurants and cafes.",
                        "rating": 5,
                        "date": "2024-03-10",
                        "category": "Culture"
                    },
                    {
                        "text": "Tourist crowds can be overwhelming on weekends.",
                        "rating": 3,
                        "date": "2024-03-09",
                        "category": "Tourism"
                    },
                    {
                        "text": "Amazing food scene and nightlife. Very lively atmosphere.",
                        "rating": 4,
                        "date": "2024-03-08",
                        "category": "Entertainment"
                    }
                ],
                "common_topics": {
                    "positive": [
                        "Italian culture",
                        "Restaurants",
                        "Historic charm",
                        "Nightlife",
                        "Location"
                    ],
                    "concerns": [
                        "Tourist crowds",
                        "Noise levels",
                        "Parking",
                        "Housing costs",
                        "Weekend traffic"
                    ]
                }
            }
        }

        # Recent community events and activities
        self.community_events = {
            "Mission District": [
                {
                    "name": "Carnaval San Francisco",
                    "type": "Cultural Festival",
                    "date": "2024-05-25",
                    "description": "Annual two-day festival celebrating Latin American and Caribbean cultures"
                },
                {
                    "name": "Mission Community Market",
                    "type": "Farmers Market",
                    "date": "Weekly",
                    "description": "Local vendors, fresh produce, and community gathering"
                }
            ],
            "Pacific Heights": [
                {
                    "name": "Fillmore Street Fair",
                    "type": "Street Festival",
                    "date": "2024-07-15",
                    "description": "Annual street fair with music, food, and local artisans"
                },
                {
                    "name": "Architecture Walking Tour",
                    "type": "Cultural",
                    "date": "Monthly",
                    "description": "Guided tour of historic mansions and architecture"
                }
            ],
            "Hayes Valley": [
                {
                    "name": "Hayes Valley Art Works",
                    "type": "Art Exhibition",
                    "date": "Ongoing",
                    "description": "Temporary public art space with rotating exhibitions"
                },
                {
                    "name": "Patricia's Green Events",
                    "type": "Community",
                    "date": "Various",
                    "description": "Regular community events in the central park"
                }
            ],
            "North Beach": [
                {
                    "name": "North Beach Festival",
                    "type": "Street Festival",
                    "date": "2024-06-15",
                    "description": "Italian heritage celebration with food, art, and music"
                },
                {
                    "name": "Poetry at City Lights",
                    "type": "Cultural",
                    "date": "Weekly",
                    "description": "Poetry readings at historic City Lights bookstore"
                }
            ]
        }

    def get_community_feedback(self, neighborhood: str) -> Dict[str, Any]:
        """Get community feedback for a specific neighborhood"""
        if neighborhood not in self.community_feedback:
            return None
        
        return {
            "reviews": self.community_feedback[neighborhood]["reviews"],
            "common_topics": self.community_feedback[neighborhood]["common_topics"],
            "events": self.community_events.get(neighborhood, []),
            "last_updated": datetime.now().isoformat()
        }

    def get_recent_reviews(self, neighborhood: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get recent reviews for a neighborhood within specified days"""
        if neighborhood not in self.community_feedback:
            return []

        cutoff_date = datetime.now() - timedelta(days=days)
        return [
            review for review in self.community_feedback[neighborhood]["reviews"]
            if datetime.strptime(review["date"], "%Y-%m-%d") > cutoff_date
        ]

    def get_neighborhood_sentiment(self, neighborhood: str) -> Dict[str, Any]:
        """Calculate sentiment metrics for a neighborhood"""
        if neighborhood not in self.community_feedback:
            return None

        reviews = self.community_feedback[neighborhood]["reviews"]
        total_reviews = len(reviews)
        avg_rating = sum(review["rating"] for review in reviews) / total_reviews

        # Calculate sentiment by category
        categories = {}
        for review in reviews:
            cat = review["category"]
            if cat not in categories:
                categories[cat] = {"count": 0, "total_rating": 0}
            categories[cat]["count"] += 1
            categories[cat]["total_rating"] += review["rating"]

        category_ratings = {
            cat: {"average_rating": data["total_rating"] / data["count"]}
            for cat, data in categories.items()
        }

        return {
            "average_rating": round(avg_rating, 2),
            "total_reviews": total_reviews,
            "category_ratings": category_ratings,
            "positive_topics": self.community_feedback[neighborhood]["common_topics"]["positive"],
            "concern_topics": self.community_feedback[neighborhood]["common_topics"]["concerns"]
        } 