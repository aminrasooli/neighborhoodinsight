import asyncio
import logging
from typing import Dict, List
from .base_agent import Agent
from .data_collector_agent import DataCollectorAgent
from .data_processor_agent import DataProcessorAgent

class AgentManager:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: List[asyncio.Task] = []
        
        # Set up logging
        logging.basicConfig(
            filename='agent_system.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('agent_manager')
        
    def register_agent(self, agent: Agent):
        """Register a new agent in the system"""
        self.agents[agent.agent_id] = agent
        self.logger.info(f"Registered agent: {agent.name} ({agent.agent_id})")
        
    async def start_agent(self, agent_id: str):
        """Start a specific agent"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            task = asyncio.create_task(agent.run())
            self.tasks.append(task)
            self.logger.info(f"Started agent: {agent.name}")
            
    async def stop_agent(self, agent_id: str):
        """Stop a specific agent"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            agent.is_active = False
            self.logger.info(f"Stopped agent: {agent.name}")
            
    async def start_all_agents(self):
        """Start all registered agents"""
        for agent_id in self.agents:
            await self.start_agent(agent_id)
            
    async def stop_all_agents(self):
        """Stop all registered agents"""
        for agent_id in self.agents:
            await self.stop_agent(agent_id)
            
    async def run(self):
        """Main run loop for the agent manager"""
        try:
            # Start all agents
            await self.start_all_agents()
            
            # Wait for all tasks to complete
            await asyncio.gather(*self.tasks)
            
        except Exception as e:
            self.logger.error(f"Error in agent manager: {str(e)}")
        finally:
            await self.stop_all_agents()
            
    def get_agent_status(self, agent_id: str) -> dict:
        """Get the current status of a specific agent"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            return {
                'name': agent.name,
                'is_active': agent.is_active,
                'last_activity': agent.last_activity,
                'state': agent.get_state()
            }
        return None
        
    def get_system_status(self) -> dict:
        """Get the current status of all agents in the system"""
        return {
            agent_id: self.get_agent_status(agent_id)
            for agent_id in self.agents
        } 