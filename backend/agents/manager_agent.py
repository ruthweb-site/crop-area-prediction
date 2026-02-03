"""
Manager Agent - Orchestrates all sub-agents and manages parallel execution.
"""
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base_agent import BaseAgent
from .weather_agent import WeatherAgent
from .soil_agent import SoilAgent
from .satellite_agent import SatelliteAgent
from .prediction_agent import PredictionAgent
from .alert_agent import AlertAgent
from .response_agent import ResponseAgent
import sys
sys.path.append('..')
from config import config

class ManagerAgent(BaseAgent):
    """
    Manager Agent - The orchestrator that coordinates all sub-agents.
    
    This agent:
    1. Parses user queries to understand intent
    2. Assigns tasks to appropriate sub-agents
    3. Manages parallel execution of agents
    4. Aggregates results and returns final response
    """
    
    def __init__(self):
        super().__init__("ManagerAgent")
        
        # Initialize all sub-agents
        self.weather_agent = WeatherAgent()
        self.soil_agent = SoilAgent()
        self.satellite_agent = SatelliteAgent()
        self.prediction_agent = PredictionAgent()
        self.alert_agent = AlertAgent()
        self.response_agent = ResponseAgent()
        
        # Agent registry
        self.agents = {
            "weather": self.weather_agent,
            "soil": self.soil_agent,
            "satellite": self.satellite_agent,
            "prediction": self.prediction_agent,
            "alert": self.alert_agent,
            "response": self.response_agent
        }
    
    def get_capabilities(self) -> list:
        return [
            "parse_user_query",
            "orchestrate_agents",
            "parallel_execution",
            "aggregate_results",
            "error_handling"
        ]
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the full agent orchestration pipeline.
        
        Args:
            task: Contains 'query', 'language', and optionally 'state', 'crop'
            
        Returns:
            Complete response with all agent data aggregated
        """
        self.log_activity(f"Starting orchestration for query: {task.get('query', '')[:50]}...")
        self._record_execution()
        
        start_time = datetime.now()
        
        try:
            # Step 1: Parse the user query
            parsed = self._parse_query(task.get("query", ""))
            
            state = task.get("state") or parsed.get("state", "Maharashtra")
            crop = task.get("crop") or parsed.get("crop", "Rice")
            language = task.get("language", "en")
            
            self.log_activity(f"Parsed: State={state}, Crop={crop}, Language={language}")
            
            # Get coordinates
            state_info = config.INDIAN_STATES.get(state, config.INDIAN_STATES["Maharashtra"])
            lat = state_info["lat"]
            lon = state_info["lon"]
            
            # Step 2: Execute data-fetching agents in parallel
            data_task = {
                "state": state,
                "crop": crop,
                "lat": lat,
                "lon": lon
            }
            
            self.log_activity("Phase 1: Fetching data from Weather, Soil, and Satellite agents...")
            
            weather_data, soil_data, satellite_data = await asyncio.gather(
                self.weather_agent.execute(data_task),
                self.soil_agent.execute(data_task),
                self.satellite_agent.execute(data_task)
            )
            
            self.log_activity("Phase 1 complete. Starting Phase 2...")
            
            # Step 3: Run prediction agent with combined data
            prediction_task = {
                "state": state,
                "crop": crop,
                "weather_data": weather_data,
                "soil_data": soil_data,
                "satellite_data": satellite_data
            }
            
            prediction_data = await self.prediction_agent.execute(prediction_task)
            
            self.log_activity("Prediction complete. Checking alerts...")
            
            # Step 4: Run alert agent
            alert_task = {
                "state": state,
                "crop": crop,
                "weather_data": weather_data,
                "soil_data": soil_data,
                "satellite_data": satellite_data
            }
            
            alert_data = await self.alert_agent.execute(alert_task)
            
            self.log_activity("Alerts processed. Formatting response...")
            
            # Step 5: Format the final response
            response_task = {
                "query": task.get("query", ""),
                "language": language,
                "state": state,
                "crop": crop,
                "weather_data": weather_data,
                "soil_data": soil_data,
                "satellite_data": satellite_data,
                "prediction_data": prediction_data,
                "alert_data": alert_data
            }
            
            formatted_response = await self.response_agent.execute(response_task)
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            self.log_activity(f"Orchestration complete in {execution_time:.2f}s")
            
            # Return complete result
            return {
                "success": True,
                "query": task.get("query", ""),
                "state": state,
                "crop": crop,
                "language": language,
                
                # Raw data from agents
                "raw_data": {
                    "weather": weather_data,
                    "soil": soil_data,
                    "satellite": satellite_data,
                    "prediction": prediction_data,
                    "alerts": alert_data
                },
                
                # Formatted response
                "response": formatted_response,
                
                # Metadata
                "metadata": {
                    "execution_time_seconds": round(execution_time, 2),
                    "agents_used": list(self.agents.keys()),
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            self.log_activity(f"Error during orchestration: {str(e)}", "error")
            return {
                "success": False,
                "error": str(e),
                "query": task.get("query", ""),
                "timestamp": datetime.now().isoformat()
            }
    
    def _parse_query(self, query: str) -> Dict[str, Any]:
        """
        Parse the user query to extract state, crop, and intent.
        
        Uses simple keyword matching for demo. Can be enhanced with NLP.
        """
        query_lower = query.lower()
        
        # Extract state
        state = None
        for s in config.INDIAN_STATES.keys():
            if s.lower() in query_lower:
                state = s
                break
        
        # Extract crop
        crop = None
        all_crops = set()
        for s_data in config.INDIAN_STATES.values():
            all_crops.update(s_data.get("crops", []))
        
        for c in all_crops:
            if c.lower() in query_lower:
                crop = c
                break
        
        # Determine intent
        intent = "yield_prediction"  # Default
        if any(word in query_lower for word in ["weather", "rain", "temperature", "मौसम", "बारिश"]):
            intent = "weather_info"
        elif any(word in query_lower for word in ["soil", "fertilizer", "मिट्टी", "उर्वरक"]):
            intent = "soil_info"
        elif any(word in query_lower for word in ["health", "disease", "pest", "रोग", "कीट"]):
            intent = "health_check"
        elif any(word in query_lower for word in ["irrigation", "water", "सिंचाई", "पानी"]):
            intent = "irrigation_advice"
        
        return {
            "state": state,
            "crop": crop,
            "intent": intent
        }
    
    async def get_quick_weather(self, state: str) -> Dict[str, Any]:
        """Quick weather fetch without full orchestration."""
        state_info = config.INDIAN_STATES.get(state, config.INDIAN_STATES["Maharashtra"])
        return await self.weather_agent.execute({
            "state": state,
            "lat": state_info["lat"],
            "lon": state_info["lon"]
        })
    
    async def get_quick_soil(self, state: str, crop: str) -> Dict[str, Any]:
        """Quick soil analysis without full orchestration."""
        return await self.soil_agent.execute({
            "state": state,
            "crop": crop
        })
    
    def get_all_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        return {
            name: agent.get_status() 
            for name, agent in self.agents.items()
        }
