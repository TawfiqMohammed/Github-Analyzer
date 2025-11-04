# Create: backend/tests/test_base_agent.py

import asyncio
from agents.base_agent import BaseAgent
from typing import Dict, Any

class TestAgent(BaseAgent):
    """Simple test agent"""
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        self.start_timer()
        
        self.log("Doing some work...")
        await asyncio.sleep(1)  # Simulate work
        
        self.end_timer()
        
        return {
            **state,
            "test_result": "Success!"
        }

async def test():
    print("Testing Base Agent...")
    
    agent = TestAgent("Test Agent")
    
    result = await agent.execute({"input": "test"})
    
    print(f"\nResult: {result}")
    print("✅ Base Agent works!")

if __name__ == "__main__":
    asyncio.run(test())