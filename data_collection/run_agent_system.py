import asyncio
import logging
from agents.agent_manager import AgentManager
from agents.data_collector_agent import DataCollectorAgent
from agents.data_processor_agent import DataProcessorAgent

# Define data sources for collector agents
data_sources = [
    {
        "name": "real_estate",
        "url": "https://www.zillow.com/san-francisco-ca/",
        "type": "html",
        "parser": {
            "selector": ".property-card",
            "fields": {
                "price": ".price",
                "beds": ".beds",
                "baths": ".baths",
                "sqft": ".sqft"
            }
        }
    },
    {
        "name": "demographics",
        "url": "https://api.census.gov/data/2020/acs/acs5",
        "type": "json"
    },
    {
        "name": "crime",
        "url": "https://data.sfgov.org/resource/cuks-n6tp.json",
        "type": "json"
    },
    {
        "name": "amenities",
        "url": "https://api.yelp.com/v3/businesses/search",
        "type": "json"
    },
    {
        "name": "reviews",
        "url": "https://api.yelp.com/v3/businesses/",
        "type": "json"
    }
]

async def main():
    # Create agent manager
    manager = AgentManager()
    
    # Create and register agents
    collector_agent = DataCollectorAgent(
        agent_id="collector_1",
        name="Data Collector",
        data_sources=data_sources
    )
    processor_agent = DataProcessorAgent(
        agent_id="processor_1",
        name="Data Processor"
    )
    
    manager.register_agent(collector_agent)
    manager.register_agent(processor_agent)
    
    # Start the agent system
    await manager.run()

if __name__ == "__main__":
    logging.basicConfig(
        filename='agent_system.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Agent system stopped by user")
    except Exception as e:
        logging.error(f"Error in agent system: {str(e)}") 