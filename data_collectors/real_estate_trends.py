from typing import Dict, List, Any
from datetime import datetime, timedelta

class RealEstateTrends:
    def __init__(self):
        # Historical price trends (quarterly data for past 2 years)
        self.price_history = {
            "Mission District": {
                "2022-Q1": {"median_price": 1350000, "price_sqft": 1050},
                "2022-Q2": {"median_price": 1380000, "price_sqft": 1075},
                "2022-Q3": {"median_price": 1395000, "price_sqft": 1090},
                "2022-Q4": {"median_price": 1410000, "price_sqft": 1100},
                "2023-Q1": {"median_price": 1425000, "price_sqft": 1115},
                "2023-Q2": {"median_price": 1435000, "price_sqft": 1125},
                "2023-Q3": {"median_price": 1440000, "price_sqft": 1130},
                "2023-Q4": {"median_price": 1450000, "price_sqft": 1135}
            },
            "Pacific Heights": {
                "2022-Q1": {"median_price": 3900000, "price_sqft": 1450},
                "2022-Q2": {"median_price": 3950000, "price_sqft": 1475},
                "2022-Q3": {"median_price": 4000000, "price_sqft": 1490},
                "2022-Q4": {"median_price": 4050000, "price_sqft": 1500},
                "2023-Q1": {"median_price": 4100000, "price_sqft": 1525},
                "2023-Q2": {"median_price": 4150000, "price_sqft": 1550},
                "2023-Q3": {"median_price": 4175000, "price_sqft": 1560},
                "2023-Q4": {"median_price": 4200000, "price_sqft": 1575}
            },
            "Hayes Valley": {
                "2022-Q1": {"median_price": 1150000, "price_sqft": 950},
                "2022-Q2": {"median_price": 1175000, "price_sqft": 975},
                "2022-Q3": {"median_price": 1190000, "price_sqft": 990},
                "2022-Q4": {"median_price": 1200000, "price_sqft": 1000},
                "2023-Q1": {"median_price": 1215000, "price_sqft": 1015},
                "2023-Q2": {"median_price": 1225000, "price_sqft": 1025},
                "2023-Q3": {"median_price": 1235000, "price_sqft": 1035},
                "2023-Q4": {"median_price": 1250000, "price_sqft": 1050}
            },
            "North Beach": {
                "2022-Q1": {"median_price": 1250000, "price_sqft": 1000},
                "2022-Q2": {"median_price": 1275000, "price_sqft": 1025},
                "2022-Q3": {"median_price": 1290000, "price_sqft": 1040},
                "2022-Q4": {"median_price": 1300000, "price_sqft": 1050},
                "2023-Q1": {"median_price": 1315000, "price_sqft": 1065},
                "2023-Q2": {"median_price": 1325000, "price_sqft": 1075},
                "2023-Q3": {"median_price": 1335000, "price_sqft": 1085},
                "2023-Q4": {"median_price": 1350000, "price_sqft": 1100}
            }
        }

        # Market conditions and forecasts
        self.market_analysis = {
            "Mission District": {
                "market_condition": "Seller's Market",
                "inventory_level": "Low",
                "avg_days_on_market": 28,
                "price_cuts": "15%",
                "year_forecast": {
                    "price_trend": "+4.2%",
                    "demand": "Strong",
                    "new_developments": 3
                },
                "property_types": {
                    "single_family": "35%",
                    "condo": "45%",
                    "multi_family": "20%"
                }
            },
            "Pacific Heights": {
                "market_condition": "Balanced",
                "inventory_level": "Medium",
                "avg_days_on_market": 45,
                "price_cuts": "20%",
                "year_forecast": {
                    "price_trend": "+3.8%",
                    "demand": "Stable",
                    "new_developments": 1
                },
                "property_types": {
                    "single_family": "45%",
                    "condo": "50%",
                    "multi_family": "5%"
                }
            },
            "Hayes Valley": {
                "market_condition": "Seller's Market",
                "inventory_level": "Very Low",
                "avg_days_on_market": 21,
                "price_cuts": "10%",
                "year_forecast": {
                    "price_trend": "+5.1%",
                    "demand": "Very Strong",
                    "new_developments": 5
                },
                "property_types": {
                    "single_family": "25%",
                    "condo": "60%",
                    "multi_family": "15%"
                }
            },
            "North Beach": {
                "market_condition": "Seller's Market",
                "inventory_level": "Low",
                "avg_days_on_market": 32,
                "price_cuts": "12%",
                "year_forecast": {
                    "price_trend": "+3.5%",
                    "demand": "Strong",
                    "new_developments": 2
                },
                "property_types": {
                    "single_family": "30%",
                    "condo": "55%",
                    "multi_family": "15%"
                }
            }
        }

    def get_price_trends(self, neighborhood: str) -> Dict[str, Any]:
        """Get historical price trends for a neighborhood"""
        if neighborhood not in self.price_history:
            return None

        history = self.price_history[neighborhood]
        current_quarter = list(history.keys())[-1]
        year_ago_quarter = list(history.keys())[-4]

        yoy_change = {
            "median_price": (
                (history[current_quarter]["median_price"] - history[year_ago_quarter]["median_price"]) /
                history[year_ago_quarter]["median_price"] * 100
            ),
            "price_sqft": (
                (history[current_quarter]["price_sqft"] - history[year_ago_quarter]["price_sqft"]) /
                history[year_ago_quarter]["price_sqft"] * 100
            )
        }

        return {
            "historical_data": history,
            "current_values": history[current_quarter],
            "yoy_change": {k: round(v, 1) for k, v in yoy_change.items()},
            "last_updated": datetime.now().isoformat()
        }

    def get_market_analysis(self, neighborhood: str) -> Dict[str, Any]:
        """Get current market analysis and forecasts"""
        if neighborhood not in self.market_analysis:
            return None

        return {
            **self.market_analysis[neighborhood],
            "last_updated": datetime.now().isoformat()
        }

    def get_market_comparison(self, neighborhoods: List[str]) -> Dict[str, Any]:
        """Compare market conditions across neighborhoods"""
        comparison = {}
        for hood in neighborhoods:
            if hood in self.market_analysis and hood in self.price_history:
                current_quarter = list(self.price_history[hood].keys())[-1]
                comparison[hood] = {
                    "current_median_price": self.price_history[hood][current_quarter]["median_price"],
                    "price_sqft": self.price_history[hood][current_quarter]["price_sqft"],
                    "market_condition": self.market_analysis[hood]["market_condition"],
                    "avg_days_on_market": self.market_analysis[hood]["avg_days_on_market"],
                    "year_forecast": self.market_analysis[hood]["year_forecast"]["price_trend"]
                }
        return comparison

    def get_investment_score(self, neighborhood: str) -> Dict[str, Any]:
        """Calculate investment potential score (0-100)"""
        if neighborhood not in self.market_analysis or neighborhood not in self.price_history:
            return None

        # Get latest data
        market = self.market_analysis[neighborhood]
        history = self.price_history[neighborhood]
        current_quarter = list(history.keys())[-1]
        year_ago_quarter = list(history.keys())[-4]

        # Calculate price appreciation
        price_appreciation = (
            (history[current_quarter]["median_price"] - history[year_ago_quarter]["median_price"]) /
            history[year_ago_quarter]["median_price"] * 100
        )

        # Calculate score components
        appreciation_score = min(100, max(0, price_appreciation * 10))  # 0-100 based on YoY appreciation
        market_score = {
            "Seller's Market": 80,
            "Balanced": 60,
            "Buyer's Market": 40
        }.get(market["market_condition"], 50)
        
        inventory_score = {
            "Very Low": 90,
            "Low": 75,
            "Medium": 60,
            "High": 40,
            "Very High": 25
        }.get(market["inventory_level"], 50)

        # Calculate weighted score
        total_score = (
            appreciation_score * 0.4 +
            market_score * 0.35 +
            inventory_score * 0.25
        )

        return {
            "total_score": round(total_score, 1),
            "components": {
                "appreciation": round(appreciation_score, 1),
                "market_condition": market_score,
                "inventory": inventory_score
            },
            "recommendation": self._get_investment_recommendation(total_score),
            "last_updated": datetime.now().isoformat()
        }

    def _get_investment_recommendation(self, score: float) -> str:
        """Generate investment recommendation based on score"""
        if score >= 80:
            return "Strong investment opportunity with high potential for appreciation"
        elif score >= 70:
            return "Good investment opportunity with steady growth potential"
        elif score >= 60:
            return "Moderate investment opportunity with stable market conditions"
        elif score >= 50:
            return "Cautious investment opportunity with moderate risk"
        else:
            return "High-risk investment opportunity with uncertain market conditions" 