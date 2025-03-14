from abc import ABC, abstractmethod
import logging
from typing import Dict, Any
import asyncio
from datetime import datetime

class Agent(ABC):
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.state = {}
        self.messages = []
        self.is_active = True
        self.last_activity = datetime.now()
        
        # Set up logging for this agent
        self.logger = logging.getLogger(f"agent.{name}")
        
    @abstractmethod
    async def initialize(self):
        """Initialize the agent's resources and connections"""
        pass
    
    @abstractmethod
    async def process(self):
        """Main processing loop for the agent"""
        pass
    
    @abstractmethod
    async def cleanup(self):
        """Cleanup resources when agent is stopping"""
        pass
    
    async def send_message(self, target_agent_id: str, message: Dict[str, Any]):
        """Send a message to another agent"""
        self.messages.append({
            'timestamp': datetime.now(),
            'from': self.agent_id,
            'to': target_agent_id,
            'content': message
        })
        self.logger.info(f"Sent message to {target_agent_id}")
    
    async def receive_message(self) -> Dict[str, Any]:
        """Receive and process the next message in the queue"""
        if self.messages:
            message = self.messages.pop(0)
            self.logger.info(f"Received message from {message['from']}")
            return message
        return None
    
    def update_state(self, new_state: Dict[str, Any]):
        """Update the agent's internal state"""
        self.state.update(new_state)
        self.last_activity = datetime.now()
    
    def get_state(self) -> Dict[str, Any]:
        """Get the current state of the agent"""
        return self.state.copy()
    
    async def run(self):
        """Main run loop for the agent"""
        try:
            await self.initialize()
            while self.is_active:
                await self.process()
                await asyncio.sleep(1)  # Prevent CPU overuse
        except Exception as e:
            self.logger.error(f"Error in agent {self.name}: {str(e)}")
        finally:
            await self.cleanup() 