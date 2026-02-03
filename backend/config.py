"""
Configuration management for CropAgent backend.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "demo_key")
    
    # Database
    DATABASE_PATH = os.getenv("DATABASE_PATH", "cropagent.db")
    
    # Agent Settings
    AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "30"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    
    # Supported Languages
    SUPPORTED_LANGUAGES = ["en", "hi", "mr"]
    DEFAULT_LANGUAGE = "en"
    
    # Indian States with coordinates
    INDIAN_STATES = {
        "Maharashtra": {"lat": 19.7515, "lon": 75.7139, "crops": ["Rice", "Cotton", "Sugarcane", "Soybean"]},
        "Punjab": {"lat": 31.1471, "lon": 75.3412, "crops": ["Wheat", "Rice", "Cotton", "Maize"]},
        "Uttar Pradesh": {"lat": 26.8467, "lon": 80.9462, "crops": ["Wheat", "Rice", "Sugarcane", "Potato"]},
        "Madhya Pradesh": {"lat": 22.9734, "lon": 78.6569, "crops": ["Wheat", "Soybean", "Gram", "Rice"]},
        "Karnataka": {"lat": 15.3173, "lon": 75.7139, "crops": ["Rice", "Ragi", "Sugarcane", "Cotton"]},
        "Gujarat": {"lat": 22.2587, "lon": 71.1924, "crops": ["Cotton", "Groundnut", "Wheat", "Rice"]},
        "Rajasthan": {"lat": 27.0238, "lon": 74.2179, "crops": ["Wheat", "Bajra", "Mustard", "Gram"]},
        "Tamil Nadu": {"lat": 11.1271, "lon": 78.6569, "crops": ["Rice", "Sugarcane", "Cotton", "Groundnut"]},
        "Andhra Pradesh": {"lat": 15.9129, "lon": 79.7400, "crops": ["Rice", "Cotton", "Chilli", "Groundnut"]},
        "West Bengal": {"lat": 22.9868, "lon": 87.8550, "crops": ["Rice", "Jute", "Potato", "Wheat"]},
    }

config = Config()
