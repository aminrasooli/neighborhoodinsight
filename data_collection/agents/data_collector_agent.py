from .base_agent import Agent
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
from datetime import datetime
import os

class DataCollectorAgent(Agent):
    def __init__(self, agent_id: str, name: str, data_sources: list):
        super().__init__(agent_id, name)
        self.data_sources = data_sources
        self.session = None
        self.ua = UserAgent()
        self.collected_data = []
        
    async def initialize(self):
        """Initialize the data collector agent"""
        self.session = aiohttp.ClientSession()
        self.logger.info(f"Initialized {self.name} with {len(self.data_sources)} data sources")
        
    async def process(self):
        """Main processing loop for data collection"""
        for source in self.data_sources:
            try:
                data = await self.collect_from_source(source)
                if data:
                    self.collected_data.extend(data)
                    # Notify the processor agent about new data
                    await self.send_message(
                        "processor_agent",
                        {
                            "type": "new_data",
                            "source": source["name"],
                            "data": data
                        }
                    )
            except Exception as e:
                self.logger.error(f"Error collecting from {source['name']}: {str(e)}")
        
        await asyncio.sleep(300)  # Wait 5 minutes before next collection cycle
        
    async def collect_from_source(self, source: dict) -> list:
        """Collect data from a specific source"""
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        async with self.session.get(source["url"], headers=headers) as response:
            if response.status == 200:
                if source["type"] == "json":
                    return await response.json()
                elif source["type"] == "html":
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    return self.parse_html_data(soup, source["parser"])
            return []
            
    def parse_html_data(self, soup: BeautifulSoup, parser_config: dict) -> list:
        """Parse HTML data based on configuration"""
        data = []
        try:
            elements = soup.select(parser_config["selector"])
            for element in elements:
                item = {}
                for field, selector in parser_config["fields"].items():
                    item[field] = element.select_one(selector).text.strip()
                data.append(item)
        except Exception as e:
            self.logger.error(f"Error parsing HTML: {str(e)}")
        return data
        
    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
        self.logger.info(f"Cleaned up {self.name}") 