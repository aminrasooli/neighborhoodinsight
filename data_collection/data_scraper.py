import requests
import json
import time
import pandas as pd
from datetime import datetime
import os
from bs4 import BeautifulSoup
import logging
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from tqdm import tqdm

# Set up logging
logging.basicConfig(
    filename='data_collection.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class NeighborhoodDataCollector:
    def __init__(self):
        self.base_path = "collected_data"
        os.makedirs(self.base_path, exist_ok=True)
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        self.ua = UserAgent(software_names=software_names, operating_systems=operating_systems)
        self.session = requests.Session()

    def get_headers(self):
        return {
            'User-Agent': self.ua.random,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9'
        }

    def save_data(self, data, category):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.base_path}/{category}_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        logging.info(f"Saved {len(data)} records to {filename}")

    def collect_real_estate_data(self):
        try:
            data = []
            # Zillow
            zillow_url = "https://www.zillow.com/san-francisco-ca/"
            # Redfin
            redfin_url = "https://www.redfin.com/city/17151/CA/San-Francisco"
            # Trulia
            trulia_url = "https://www.trulia.com/CA/San_Francisco/"
            
            urls = [zillow_url, redfin_url, trulia_url]
            
            for url in urls:
                try:
                    response = self.session.get(url, headers=self.get_headers())
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'lxml')
                        # Extract property listings
                        listings = self.extract_property_data(soup, url)
                        data.extend(listings)
                        time.sleep(2)  # Respect rate limits
                except Exception as e:
                    logging.error(f"Error collecting from {url}: {str(e)}")
            return data
        except Exception as e:
            logging.error(f"Error in real estate collection: {str(e)}")
            return []

    def collect_demographic_data(self):
        try:
            data = []
            # Census API
            census_url = "https://api.census.gov/data/2020/acs/acs5"
            # Data USA API
            datausa_url = "https://datausa.io/api/data?Geography=16000US0667000"
            # City Data
            citydata_url = "http://www.city-data.com/city/San-Francisco-California.html"
            
            urls = [census_url, datausa_url, citydata_url]
            
            for url in urls:
                try:
                    response = self.session.get(url, headers=self.get_headers())
                    if response.status_code == 200:
                        if 'census.gov' in url:
                            data.extend(self.parse_census_data(response.json()))
                        elif 'datausa.io' in url:
                            data.extend(self.parse_datausa_data(response.json()))
                        else:
                            soup = BeautifulSoup(response.text, 'lxml')
                            data.extend(self.extract_demographic_data(soup))
                        time.sleep(2)
                except Exception as e:
                    logging.error(f"Error collecting from {url}: {str(e)}")
            return data
        except Exception as e:
            logging.error(f"Error in demographic collection: {str(e)}")
            return []

    def collect_crime_data(self):
        try:
            data = []
            # SF OpenData Crime Reports
            sfdata_url = "https://data.sfgov.org/resource/wg3w-h783.json"
            # CrimeMapping
            crimemap_url = "https://www.crimemapping.com/map/ca/sanfrancisco"
            
            urls = [sfdata_url, crimemap_url]
            
            for url in urls:
                try:
                    response = self.session.get(url, headers=self.get_headers())
                    if response.status_code == 200:
                        if 'sfgov.org' in url:
                            data.extend(response.json())
                        else:
                            soup = BeautifulSoup(response.text, 'lxml')
                            data.extend(self.extract_crime_data(soup))
                        time.sleep(2)
                except Exception as e:
                    logging.error(f"Error collecting from {url}: {str(e)}")
            return data
        except Exception as e:
            logging.error(f"Error in crime data collection: {str(e)}")
            return []

    def collect_amenities_data(self):
        try:
            data = []
            # Yelp API
            categories = ["restaurants", "education", "parks", "shopping", "transport", "health", "entertainment"]
            base_url = "https://api.yelp.com/v3/businesses/search"
            
            for category in categories:
                try:
                    params = {
                        'location': 'San Francisco, CA',
                        'categories': category,
                        'limit': 50
                    }
                    response = self.session.get(
                        base_url,
                        headers=self.get_headers(),
                        params=params
                    )
                    if response.status_code == 200:
                        data.extend(self.parse_yelp_data(response.json(), category))
                    time.sleep(2)
                except Exception as e:
                    logging.error(f"Error collecting {category}: {str(e)}")
            return data
        except Exception as e:
            logging.error(f"Error in amenities collection: {str(e)}")
            return []

    def collect_reviews_ratings(self):
        try:
            data = []
            # Google Places API
            places_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            # Yelp Reviews
            yelp_url = "https://api.yelp.com/v3/businesses/"
            # Neighborhood Scout
            scout_url = "https://www.neighborhoodscout.com/ca/san-francisco"
            
            urls = [places_url, yelp_url, scout_url]
            
            for url in urls:
                try:
                    response = self.session.get(url, headers=self.get_headers())
                    if response.status_code == 200:
                        if 'googleapis.com' in url:
                            data.extend(self.parse_google_reviews(response.json()))
                        elif 'yelp.com' in url:
                            data.extend(self.parse_yelp_reviews(response.json()))
                        else:
                            soup = BeautifulSoup(response.text, 'lxml')
                            data.extend(self.extract_neighborhood_reviews(soup))
                        time.sleep(2)
                except Exception as e:
                    logging.error(f"Error collecting from {url}: {str(e)}")
            return data
        except Exception as e:
            logging.error(f"Error in reviews collection: {str(e)}")
            return []

    def extract_property_data(self, soup, source_url):
        data = []
        try:
            if 'zillow.com' in source_url:
                # Extract Zillow property cards
                property_cards = soup.find_all('article', {'class': 'list-card'})
                for card in property_cards:
                    try:
                        property_data = {
                            'source': 'Zillow',
                            'price': card.find('div', {'class': 'list-card-price'}).text,
                            'address': card.find('address', {'class': 'list-card-addr'}).text,
                            'details': card.find('ul', {'class': 'list-card-details'}).text,
                            'timestamp': datetime.now().isoformat()
                        }
                        data.append(property_data)
                    except:
                        continue
            elif 'redfin.com' in source_url:
                # Extract Redfin property cards
                property_cards = soup.find_all('div', {'class': 'HomeCard'})
                for card in property_cards:
                    try:
                        property_data = {
                            'source': 'Redfin',
                            'price': card.find('span', {'class': 'homecardV2Price'}).text,
                            'address': card.find('span', {'class': 'homeAddress'}).text,
                            'details': card.find('div', {'class': 'HomeStatsV2'}).text,
                            'timestamp': datetime.now().isoformat()
                        }
                        data.append(property_data)
                    except:
                        continue
        except Exception as e:
            logging.error(f"Error extracting property data: {str(e)}")
        return data

    def parse_census_data(self, data):
        processed_data = []
        try:
            if data and len(data) > 1:
                headers = data[0]
                for row in data[1:]:
                    entry = {
                        'source': 'Census',
                        'timestamp': datetime.now().isoformat(),
                        'data': dict(zip(headers, row))
                    }
                    processed_data.append(entry)
        except Exception as e:
            logging.error(f"Error parsing census data: {str(e)}")
        return processed_data

    def parse_datausa_data(self, data):
        processed_data = []
        try:
            if 'data' in data:
                for entry in data['data']:
                    processed_entry = {
                        'source': 'DataUSA',
                        'timestamp': datetime.now().isoformat(),
                        'data': entry
                    }
                    processed_data.append(processed_entry)
        except Exception as e:
            logging.error(f"Error parsing DataUSA data: {str(e)}")
        return processed_data

    def extract_demographic_data(self, soup):
        data = []
        try:
            # Extract demographic information from city-data
            stats = soup.find_all('section', {'class': 'city-data'})
            for stat in stats:
                try:
                    stat_data = {
                        'source': 'CityData',
                        'category': stat.find('h2').text if stat.find('h2') else 'Unknown',
                        'value': stat.find('div', {'class': 'value'}).text if stat.find('div', {'class': 'value'}) else '',
                        'timestamp': datetime.now().isoformat()
                    }
                    data.append(stat_data)
                except:
                    continue
        except Exception as e:
            logging.error(f"Error extracting demographic data: {str(e)}")
        return data

    def extract_crime_data(self, soup):
        data = []
        try:
            # Extract crime data from CrimeMapping
            incidents = soup.find_all('div', {'class': 'incident'})
            for incident in incidents:
                try:
                    incident_data = {
                        'source': 'CrimeMapping',
                        'type': incident.find('span', {'class': 'type'}).text if incident.find('span', {'class': 'type'}) else '',
                        'location': incident.find('span', {'class': 'location'}).text if incident.find('span', {'class': 'location'}) else '',
                        'date': incident.find('span', {'class': 'date'}).text if incident.find('span', {'class': 'date'}) else '',
                        'timestamp': datetime.now().isoformat()
                    }
                    data.append(incident_data)
                except:
                    continue
        except Exception as e:
            logging.error(f"Error extracting crime data: {str(e)}")
        return data

    def parse_yelp_data(self, data, category):
        processed_data = []
        try:
            if 'businesses' in data:
                for business in data['businesses']:
                    business_data = {
                        'source': 'Yelp',
                        'category': category,
                        'name': business.get('name', ''),
                        'rating': business.get('rating', 0),
                        'review_count': business.get('review_count', 0),
                        'location': business.get('location', {}),
                        'timestamp': datetime.now().isoformat()
                    }
                    processed_data.append(business_data)
        except Exception as e:
            logging.error(f"Error parsing Yelp data: {str(e)}")
        return processed_data

    def parse_google_reviews(self, data):
        processed_data = []
        try:
            if 'results' in data:
                for place in data['results']:
                    place_data = {
                        'source': 'Google Places',
                        'name': place.get('name', ''),
                        'rating': place.get('rating', 0),
                        'reviews': place.get('reviews', []),
                        'timestamp': datetime.now().isoformat()
                    }
                    processed_data.append(place_data)
        except Exception as e:
            logging.error(f"Error parsing Google reviews: {str(e)}")
        return processed_data

    def parse_yelp_reviews(self, data):
        processed_data = []
        try:
            if 'reviews' in data:
                for review in data['reviews']:
                    review_data = {
                        'source': 'Yelp',
                        'rating': review.get('rating', 0),
                        'text': review.get('text', ''),
                        'time_created': review.get('time_created', ''),
                        'timestamp': datetime.now().isoformat()
                    }
                    processed_data.append(review_data)
        except Exception as e:
            logging.error(f"Error parsing Yelp reviews: {str(e)}")
        return processed_data

    def extract_neighborhood_reviews(self, soup):
        data = []
        try:
            # Extract reviews from NeighborhoodScout
            reviews = soup.find_all('div', {'class': 'review'})
            for review in reviews:
                try:
                    review_data = {
                        'source': 'NeighborhoodScout',
                        'rating': review.find('span', {'class': 'rating'}).text if review.find('span', {'class': 'rating'}) else '',
                        'text': review.find('div', {'class': 'review-text'}).text if review.find('div', {'class': 'review-text'}) else '',
                        'timestamp': datetime.now().isoformat()
                    }
                    data.append(review_data)
                except:
                    continue
        except Exception as e:
            logging.error(f"Error extracting neighborhood reviews: {str(e)}")
        return data

    def run_continuous_collection(self):
        while True:
            try:
                with ThreadPoolExecutor(max_workers=5) as executor:
                    # Submit all collection tasks
                    future_to_category = {
                        executor.submit(self.collect_real_estate_data): "real_estate",
                        executor.submit(self.collect_demographic_data): "demographics",
                        executor.submit(self.collect_crime_data): "crime",
                        executor.submit(self.collect_amenities_data): "amenities",
                        executor.submit(self.collect_reviews_ratings): "reviews"
                    }

                    # Process completed tasks
                    for future in future_to_category:
                        category = future_to_category[future]
                        try:
                            data = future.result()
                            if data:
                                self.save_data(data, category)
                        except Exception as e:
                            logging.error(f"Error processing {category}: {str(e)}")

                # Sleep between collection cycles
                time.sleep(300)  # 5 minutes between cycles

            except Exception as e:
                logging.error(f"Error in collection cycle: {str(e)}")
                time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    collector = NeighborhoodDataCollector()
    logging.info("Starting continuous data collection...")
    collector.run_continuous_collection() 