from typing import Dict, List, Any
from datetime import datetime
import random

class EducationDataCollector:
    def __init__(self):
        # School data by neighborhood
        self.school_data = {
            "Mission District": {
                "public_schools": [
                    {
                        "name": "Mission High School",
                        "type": "Public",
                        "grades": "9-12",
                        "rating": 7.5,
                        "student_teacher_ratio": "18:1",
                        "total_students": 1050,
                        "test_scores": {
                            "math": 78,
                            "reading": 82,
                            "science": 80
                        },
                        "programs": ["AP", "IB", "STEM", "Arts"]
                    },
                    {
                        "name": "Everett Middle School",
                        "type": "Public",
                        "grades": "6-8",
                        "rating": 7.2,
                        "student_teacher_ratio": "16:1",
                        "total_students": 425,
                        "test_scores": {
                            "math": 75,
                            "reading": 80,
                            "science": 77
                        },
                        "programs": ["STEM", "Music", "ESL"]
                    }
                ],
                "private_schools": [
                    {
                        "name": "Mission Preparatory",
                        "type": "Private",
                        "grades": "K-8",
                        "rating": 8.8,
                        "student_teacher_ratio": "12:1",
                        "total_students": 280,
                        "tuition": 28000,
                        "programs": ["Language Immersion", "Arts", "Technology"]
                    }
                ],
                "district_stats": {
                    "avg_test_scores": 78,
                    "graduation_rate": "88%",
                    "college_acceptance": "82%"
                }
            },
            "Pacific Heights": {
                "public_schools": [
                    {
                        "name": "Pacific Heights Elementary",
                        "type": "Public",
                        "grades": "K-5",
                        "rating": 9.2,
                        "student_teacher_ratio": "15:1",
                        "total_students": 350,
                        "test_scores": {
                            "math": 92,
                            "reading": 94,
                            "science": 90
                        },
                        "programs": ["Gifted", "Arts", "Language"]
                    }
                ],
                "private_schools": [
                    {
                        "name": "Pacific Academy",
                        "type": "Private",
                        "grades": "K-12",
                        "rating": 9.5,
                        "student_teacher_ratio": "10:1",
                        "total_students": 450,
                        "tuition": 45000,
                        "programs": ["IB", "STEM", "Arts", "Athletics"]
                    }
                ],
                "district_stats": {
                    "avg_test_scores": 92,
                    "graduation_rate": "98%",
                    "college_acceptance": "95%"
                }
            },
            "Hayes Valley": {
                "public_schools": [
                    {
                        "name": "Hayes Valley Elementary",
                        "type": "Public",
                        "grades": "K-5",
                        "rating": 8.1,
                        "student_teacher_ratio": "16:1",
                        "total_students": 320,
                        "test_scores": {
                            "math": 85,
                            "reading": 87,
                            "science": 83
                        },
                        "programs": ["STEM", "Arts", "After School"]
                    }
                ],
                "private_schools": [
                    {
                        "name": "Hayes Valley School",
                        "type": "Private",
                        "grades": "6-12",
                        "rating": 8.9,
                        "student_teacher_ratio": "11:1",
                        "total_students": 380,
                        "tuition": 35000,
                        "programs": ["Advanced Math", "Science", "Arts"]
                    }
                ],
                "district_stats": {
                    "avg_test_scores": 85,
                    "graduation_rate": "92%",
                    "college_acceptance": "88%"
                }
            },
            "North Beach": {
                "public_schools": [
                    {
                        "name": "North Beach Elementary",
                        "type": "Public",
                        "grades": "K-5",
                        "rating": 8.5,
                        "student_teacher_ratio": "15:1",
                        "total_students": 280,
                        "test_scores": {
                            "math": 88,
                            "reading": 90,
                            "science": 86
                        },
                        "programs": ["Language", "Arts", "Technology"]
                    }
                ],
                "private_schools": [
                    {
                        "name": "North Beach Academy",
                        "type": "Private",
                        "grades": "K-8",
                        "rating": 9.1,
                        "student_teacher_ratio": "11:1",
                        "total_students": 320,
                        "tuition": 32000,
                        "programs": ["Mandarin", "STEM", "Arts"]
                    }
                ],
                "district_stats": {
                    "avg_test_scores": 88,
                    "graduation_rate": "94%",
                    "college_acceptance": "90%"
                }
            }
        }

        # Special programs and resources
        self.special_programs = {
            "Mission District": [
                {
                    "name": "After School STEM",
                    "participants": 150,
                    "success_rate": "85%"
                },
                {
                    "name": "ESL Support",
                    "participants": 200,
                    "success_rate": "88%"
                }
            ],
            "Pacific Heights": [
                {
                    "name": "Advanced Placement",
                    "participants": 180,
                    "success_rate": "92%"
                }
            ],
            "Hayes Valley": [
                {
                    "name": "Arts Integration",
                    "participants": 160,
                    "success_rate": "90%"
                }
            ],
            "North Beach": [
                {
                    "name": "Bilingual Education",
                    "participants": 140,
                    "success_rate": "89%"
                }
            ]
        }

    def get_education_report(self, neighborhood: str) -> Dict[str, Any]:
        """Get comprehensive education report for a neighborhood"""
        if neighborhood not in self.school_data:
            return None

        return {
            "schools": self.school_data[neighborhood],
            "special_programs": self.special_programs.get(neighborhood, []),
            "last_updated": datetime.now().isoformat()
        }

    def get_school_comparison(self, neighborhoods: List[str]) -> Dict[str, Any]:
        """Compare education metrics across neighborhoods"""
        comparison = {}
        for hood in neighborhoods:
            if hood in self.school_data:
                stats = self.school_data[hood]["district_stats"]
                comparison[hood] = {
                    "avg_test_scores": stats["avg_test_scores"],
                    "graduation_rate": stats["graduation_rate"],
                    "college_acceptance": stats["college_acceptance"],
                    "public_schools": len(self.school_data[hood]["public_schools"]),
                    "private_schools": len(self.school_data[hood]["private_schools"])
                }
        return comparison

    def get_education_score(self, neighborhood: str) -> Dict[str, Any]:
        """Calculate education score for a neighborhood"""
        if neighborhood not in self.school_data:
            return None

        data = self.school_data[neighborhood]
        
        # Calculate component scores
        test_score = float(data["district_stats"]["avg_test_scores"])
        grad_rate = float(data["district_stats"]["graduation_rate"].rstrip("%"))
        college_rate = float(data["district_stats"]["college_acceptance"].rstrip("%"))
        
        # Calculate school quality scores
        public_scores = [school["rating"] * 10 for school in data["public_schools"]]
        private_scores = [school["rating"] * 10 for school in data["private_schools"]]
        
        avg_school_rating = (
            sum(public_scores + private_scores) / 
            len(public_scores + private_scores)
        ) if public_scores or private_scores else 0
        
        # Calculate weighted total (0-100 scale)
        total_score = (
            test_score * 0.3 +
            grad_rate * 0.25 +
            college_rate * 0.25 +
            avg_school_rating * 0.2
        )

        return {
            "total_score": round(total_score, 1),
            "components": {
                "test_scores": round(test_score, 1),
                "graduation_rate": round(grad_rate, 1),
                "college_acceptance": round(college_rate, 1),
                "school_ratings": round(avg_school_rating, 1)
            },
            "interpretation": self._get_education_interpretation(total_score),
            "last_updated": datetime.now().isoformat()
        }

    def _get_education_interpretation(self, score: float) -> str:
        """Generate education quality interpretation based on score"""
        if score >= 90:
            return "Exceptional educational environment with outstanding schools and programs"
        elif score >= 80:
            return "Very strong educational system with high-performing schools"
        elif score >= 70:
            return "Good educational options with room for improvement"
        elif score >= 60:
            return "Adequate educational system with some challenges"
        else:
            return "Educational system needs significant improvement" 