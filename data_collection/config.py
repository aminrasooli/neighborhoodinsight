import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Dict, Any
import logging

# Load environment variables
load_dotenv()

@dataclass
class APIConfig:
    """API configuration settings"""
    yelp_api_key: str
    google_places_api_key: str
    census_api_key: str
    
    @classmethod
    def from_env(cls) -> 'APIConfig':
        """Create config from environment variables with validation"""
        required_keys = {
            'YELP_API_KEY': 'Yelp',
            'GOOGLE_PLACES_API_KEY': 'Google Places',
            'CENSUS_API_KEY': 'Census'
        }
        
        # Validate required keys
        missing_keys = []
        for key, service in required_keys.items():
            if not os.getenv(key):
                missing_keys.append(f"{service} API key ({key})")
                
        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")
            
        return cls(
            yelp_api_key=os.getenv('YELP_API_KEY'),
            google_places_api_key=os.getenv('GOOGLE_PLACES_API_KEY'),
            census_api_key=os.getenv('CENSUS_API_KEY')
        )

@dataclass
class RateLimitConfig:
    """Rate limiting configuration"""
    delay: int
    max_retries: int
    
    @classmethod
    def from_env(cls) -> 'RateLimitConfig':
        """Create rate limit config from environment variables"""
        return cls(
            delay=int(os.getenv('RATE_LIMIT_DELAY', '2')),
            max_retries=int(os.getenv('MAX_RETRIES', '3'))
        )

@dataclass
class CollectionConfig:
    """Data collection configuration"""
    interval: int
    processing_interval: int
    max_records_per_request: int
    
    @classmethod
    def from_env(cls) -> 'CollectionConfig':
        """Create collection config from environment variables"""
        return cls(
            interval=int(os.getenv('COLLECTION_INTERVAL', '300')),
            processing_interval=int(os.getenv('PROCESSING_INTERVAL', '1800')),
            max_records_per_request=int(os.getenv('MAX_RECORDS_PER_REQUEST', '50'))
        )

@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str
    file_path: str
    
    @classmethod
    def from_env(cls) -> 'LoggingConfig':
        """Create logging config from environment variables"""
        return cls(
            level=os.getenv('LOG_LEVEL', 'INFO'),
            file_path=os.getenv('LOG_FILE_PATH', 'logs/data_collection.log')
        )
        
    def setup_logging(self):
        """Configure logging based on settings"""
        log_dir = os.path.dirname(self.file_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        logging.basicConfig(
            filename=self.file_path,
            level=getattr(logging, self.level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

class Config:
    """Main configuration class"""
    def __init__(self):
        self.api = APIConfig.from_env()
        self.rate_limit = RateLimitConfig.from_env()
        self.collection = CollectionConfig.from_env()
        self.logging = LoggingConfig.from_env()
        
        # Setup logging
        self.logging.setup_logging()
        
    @property
    def data_sources(self) -> Dict[str, Dict[str, Any]]:
        """Return configured data sources"""
        return {
            "real_estate": {
                "name": "real_estate",
                "type": "api",
                "base_url": "https://api.bridgedataoutput.com/api/v2/zestimate",
                "requires_auth": True,
                "auth_header": "Authorization",
                "auth_prefix": "Bearer"
            },
            "demographics": {
                "name": "demographics",
                "type": "api",
                "base_url": "https://api.census.gov/data/2020/acs/acs5",
                "requires_auth": True,
                "auth_param": "key"
            },
            "crime": {
                "name": "crime",
                "type": "api",
                "base_url": "https://data.sfgov.org/resource/cuks-n6tp.json",
                "requires_auth": False,
                "params": {
                    "$limit": "50000",
                    "$order": "incident_datetime DESC"
                }
            },
            "amenities": {
                "name": "amenities",
                "type": "api",
                "base_url": "https://api.yelp.com/v3/businesses/search",
                "requires_auth": True,
                "auth_header": "Authorization",
                "auth_prefix": "Bearer"
            },
            "reviews": {
                "name": "reviews",
                "type": "api",
                "base_url": "https://api.yelp.com/v3/businesses/{id}/reviews",
                "requires_auth": True,
                "auth_header": "Authorization",
                "auth_prefix": "Bearer"
            }
        }

# Create global config instance
config = Config() 