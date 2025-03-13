import requests
import os
from datetime import datetime
from typing import Dict, Any, Optional

class ZillowCollector:
    def __init__(self):
        self.api_key = os.getenv('ZILLOW_API_KEY')
        self.base_url = "https://api.bridgedataoutput.com/api/v2/zestimates"
        
    def get_property_details(self, address: str) -> Optional[Dict[str, Any]]:
        """
        Fetch real estate data for a given address from Zillow
        """
        if not self.api_key:
            raise ValueError("Zillow API key not found in environment variables")
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            params = {
                "address": address,
                "access_token": self.api_key
            }
            
            response = requests.get(
                self.base_url,
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._format_property_data(data)
            else:
                print(f"Error fetching Zillow data: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error in Zillow API call: {str(e)}")
            return None
            
    def _format_property_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the raw Zillow API response into our standard format
        """
        try:
            property_data = raw_data.get('property', {})
            zestimate = property_data.get('zestimate', {})
            
            return {
                "median_price": f"${zestimate.get('amount', 0):,}",
                "price_trend": self._calculate_price_trend(property_data),
                "avg_days_on_market": property_data.get('daysOnZillow', 30),
                "price_per_sqft": self._calculate_price_per_sqft(property_data),
                "market_status": self._determine_market_status(property_data),
                "historical_appreciation": self._calculate_appreciation(property_data),
                "forecast": self._get_forecast(property_data),
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error formatting Zillow data: {str(e)}")
            return None
            
    def _calculate_price_trend(self, property_data: Dict[str, Any]) -> str:
        # Calculate 12-month price trend from historical data
        try:
            historical = property_data.get('historicalZestimates', [])
            if len(historical) >= 12:
                old_price = historical[-12].get('amount', 0)
                current_price = property_data.get('zestimate', {}).get('amount', 0)
                if old_price > 0:
                    change = ((current_price - old_price) / old_price) * 100
                    return f"{change:+.1f}% (Last 12 months)"
            return "Data not available"
        except:
            return "Data not available"
            
    def _calculate_price_per_sqft(self, property_data: Dict[str, Any]) -> str:
        try:
            price = property_data.get('zestimate', {}).get('amount', 0)
            sqft = property_data.get('finishedSqFt', 0)
            if price > 0 and sqft > 0:
                return f"${int(price/sqft):,}"
            return "Data not available"
        except:
            return "Data not available"
            
    def _determine_market_status(self, property_data: Dict[str, Any]) -> str:
        try:
            days_on_market = property_data.get('daysOnZillow', 30)
            if days_on_market < 30:
                return "Hot Market"
            elif days_on_market < 60:
                return "Seller's Market"
            elif days_on_market < 90:
                return "Balanced Market"
            else:
                return "Buyer's Market"
        except:
            return "Market status unknown"
            
    def _calculate_appreciation(self, property_data: Dict[str, Any]) -> str:
        try:
            historical = property_data.get('historicalZestimates', [])
            if len(historical) >= 60:  # 5 years of monthly data
                old_price = historical[-60].get('amount', 0)
                current_price = property_data.get('zestimate', {}).get('amount', 0)
                if old_price > 0:
                    annual_rate = (((current_price / old_price) ** (1/5)) - 1) * 100
                    return f"{annual_rate:.1f}% annually over 5 years"
            return "Insufficient historical data"
        except:
            return "Data not available"
            
    def _get_forecast(self, property_data: Dict[str, Any]) -> str:
        try:
            forecast = property_data.get('zestimate', {}).get('forecast', {})
            if forecast:
                change = forecast.get('percentChange', 0) * 100
                return f"Expected to {'+' if change >= 0 else '-'}{abs(change):.1f}% next year"
            return "Forecast not available"
        except:
            return "Forecast not available" 