"""
CropAgent - Main FastAPI Application
Agentic AI for Indian Farmers - Crop Area, Yield, and Health Prediction
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
from datetime import datetime

from agents import ManagerAgent
from memory.memory import memory
from config import config

# Initialize FastAPI app
app = FastAPI(
    title="CropAgent API",
    description="Agentic AI for Indian Farmers - Predicts crop area, yield, and health using live data",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Manager Agent
manager = ManagerAgent()

# WebSocket connections for real-time updates
active_connections: List[WebSocket] = []


# Request/Response Models
class ChatRequest(BaseModel):
    query: str
    language: str = "en"
    state: Optional[str] = None
    crop: Optional[str] = None


class ChatResponse(BaseModel):
    success: bool
    query: str
    state: str
    crop: str
    language: str
    response: Dict[str, Any]
    raw_data: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any]


class QuickWeatherRequest(BaseModel):
    state: str


class IrrigationRequest(BaseModel):
    state: str
    crop: str


# API Routes

@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "CropAgent API",
        "version": "1.0.0",
        "description": "Agentic AI for Indian Farmers",
        "endpoints": {
            "chat": "/api/chat",
            "weather": "/api/weather/{state}",
            "states": "/api/states",
            "crops": "/api/crops/{state}",
            "history": "/api/history",
            "stats": "/api/stats"
        }
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - processes farmer queries through the agent system.
    
    Example query: "Will rice yield be good in Maharashtra this season?"
    """
    start_time = datetime.now()
    
    try:
        # Execute the full agent pipeline
        result = await manager.execute({
            "query": request.query,
            "language": request.language,
            "state": request.state,
            "crop": request.crop
        })
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
        
        # Calculate response time
        response_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Store query in memory
        await memory.store_query({
            "query": request.query,
            "language": request.language,
            "state": result.get("state"),
            "crop": result.get("crop"),
            "response_time_ms": response_time_ms
        })
        
        # Store prediction in memory
        prediction = result.get("raw_data", {}).get("prediction", {})
        await memory.store_prediction({
            "state": result.get("state"),
            "crop": result.get("crop"),
            "predicted_yield": prediction.get("yield_prediction", {}).get("predicted", 0),
            "risk_score": prediction.get("risk_assessment", {}).get("overall_risk_score", 0),
            "confidence": prediction.get("confidence", {}).get("score", 0),
            "weather_data": result.get("raw_data", {}).get("weather", {}),
            "soil_data": result.get("raw_data", {}).get("soil", {}),
            "satellite_data": result.get("raw_data", {}).get("satellite", {}),
            "full_response": result.get("response", {})
        })
        
        return ChatResponse(
            success=True,
            query=request.query,
            state=result.get("state", ""),
            crop=result.get("crop", ""),
            language=request.language,
            response=result.get("response", {}),
            raw_data=result.get("raw_data"),
            metadata={
                **result.get("metadata", {}),
                "response_time_ms": response_time_ms
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/weather/{state}")
async def get_weather(state: str):
    """Get current weather for a state."""
    if state not in config.INDIAN_STATES:
        raise HTTPException(status_code=404, detail=f"State '{state}' not found")
    
    weather_data = await manager.get_quick_weather(state)
    return {
        "success": True,
        "state": state,
        "weather": weather_data
    }


@app.get("/api/soil/{state}/{crop}")
async def get_soil(state: str, crop: str):
    """Get soil analysis for a state and crop."""
    if state not in config.INDIAN_STATES:
        raise HTTPException(status_code=404, detail=f"State '{state}' not found")
    
    soil_data = await manager.get_quick_soil(state, crop)
    return {
        "success": True,
        "state": state,
        "crop": crop,
        "soil": soil_data
    }


@app.get("/api/states")
async def get_states():
    """Get list of supported Indian states."""
    states = []
    for name, data in config.INDIAN_STATES.items():
        states.append({
            "name": name,
            "lat": data["lat"],
            "lon": data["lon"],
            "major_crops": data["crops"]
        })
    return {"states": states}


@app.get("/api/crops/{state}")
async def get_crops(state: str):
    """Get major crops for a state."""
    if state not in config.INDIAN_STATES:
        raise HTTPException(status_code=404, detail=f"State '{state}' not found")
    
    return {
        "state": state,
        "crops": config.INDIAN_STATES[state]["crops"]
    }


@app.get("/api/history")
async def get_history(state: Optional[str] = None, crop: Optional[str] = None, limit: int = 10):
    """Get prediction history."""
    predictions = await memory.get_recent_predictions(state, crop, limit)
    return {
        "count": len(predictions),
        "predictions": predictions
    }


@app.get("/api/stats")
async def get_stats():
    """Get system statistics."""
    query_stats = await memory.get_query_statistics()
    agent_perf = await memory.get_agent_performance()
    agent_status = manager.get_all_agent_status()
    
    return {
        "query_statistics": query_stats,
        "agent_performance": agent_perf,
        "agent_status": agent_status,
        "system": {
            "supported_languages": config.SUPPORTED_LANGUAGES,
            "supported_states": list(config.INDIAN_STATES.keys())
        }
    }


@app.get("/api/agents/status")
async def get_agent_status():
    """Get status of all agents."""
    return manager.get_all_agent_status()


# WebSocket for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            # Process query through agents
            result = await manager.execute({
                "query": data.get("query", ""),
                "language": data.get("language", "en"),
                "state": data.get("state"),
                "crop": data.get("crop")
            })
            
            # Send response
            await websocket.send_json(result)
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup."""
    await memory.initialize()
    print("🌾 CropAgent API started successfully!")
    print(f"📍 Supported states: {list(config.INDIAN_STATES.keys())}")
    print(f"🌐 Supported languages: {config.SUPPORTED_LANGUAGES}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("🌾 CropAgent API shutting down...")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents": len(manager.agents)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
