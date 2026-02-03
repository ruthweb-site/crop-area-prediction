"""
Weather Agent - Fetches live weather data from OpenWeatherMap API.
"""
import httpx
import random
from typing import Dict, Any
from datetime import datetime, timedelta
from .base_agent import BaseAgent
import sys
sys.path.append('..')
from config import config

class WeatherAgent(BaseAgent):
    """Agent responsible for fetching and analyzing weather data."""
    
    def __init__(self):
        super().__init__("WeatherAgent")
        self.api_key = config.OPENWEATHERMAP_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_capabilities(self) -> list:
        return [
            "fetch_current_weather",
            "get_rainfall_data",
            "get_forecast",
            "analyze_weather_patterns",
            "detect_weather_alerts"
        ]
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute weather data fetching task.
        
        Args:
            task: Contains 'state', 'lat', 'lon' for location
            
        Returns:
            Weather data including current conditions and forecast
        """
        self.log_activity(f"Executing weather fetch for {task.get('state', 'Unknown')}")
        self._record_execution()
        
        state = task.get("state", "Maharashtra")
        lat = task.get("lat")
        lon = task.get("lon")
        
        # Get coordinates from config if not provided
        if not lat or not lon:
            state_data = config.INDIAN_STATES.get(state, config.INDIAN_STATES["Maharashtra"])
            lat = state_data["lat"]
            lon = state_data["lon"]
        
        # Try to fetch real data, fall back to simulated
        try:
            if self.api_key != "demo_key":
                weather_data = await self._fetch_real_weather(lat, lon)
            else:
                weather_data = self._generate_simulated_weather(state, lat, lon)
        except Exception as e:
            self.log_activity(f"API error, using simulated data: {e}", "warning")
            weather_data = self._generate_simulated_weather(state, lat, lon)
        
        return weather_data
    
    async def _fetch_real_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """Fetch real weather data from OpenWeatherMap."""
        async with httpx.AsyncClient() as client:
            # Current weather
            current_url = f"{self.base_url}/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
            current_response = await client.get(current_url)
            current_data = current_response.json()
            
            # 5-day forecast
            forecast_url = f"{self.base_url}/forecast?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
            forecast_response = await client.get(forecast_url)
            forecast_data = forecast_response.json()
            
            return self._parse_weather_response(current_data, forecast_data)
    
    def _parse_weather_response(self, current: Dict, forecast: Dict) -> Dict[str, Any]:
        """Parse OpenWeatherMap API response."""
        return {
            "current": {
                "temperature": current.get("main", {}).get("temp", 25),
                "humidity": current.get("main", {}).get("humidity", 60),
                "pressure": current.get("main", {}).get("pressure", 1013),
                "wind_speed": current.get("wind", {}).get("speed", 5),
                "description": current.get("weather", [{}])[0].get("description", "clear sky"),
                "clouds": current.get("clouds", {}).get("all", 20)
            },
            "rainfall": {
                "last_1h": current.get("rain", {}).get("1h", 0),
                "last_3h": current.get("rain", {}).get("3h", 0),
                "last_24h": sum([f.get("rain", {}).get("3h", 0) for f in forecast.get("list", [])[:8]])
            },
            "forecast": self._parse_forecast(forecast),
            "alerts": self._detect_alerts(current),
            "timestamp": datetime.now().isoformat()
        }
    
    def _parse_forecast(self, forecast: Dict) -> list:
        """Parse forecast data."""
        forecasts = []
        for item in forecast.get("list", [])[:5]:
            forecasts.append({
                "datetime": item.get("dt_txt"),
                "temperature": item.get("main", {}).get("temp"),
                "humidity": item.get("main", {}).get("humidity"),
                "rain_probability": item.get("pop", 0) * 100,
                "description": item.get("weather", [{}])[0].get("description")
            })
        return forecasts
    
    def _detect_alerts(self, weather: Dict) -> list:
        """Detect weather alerts based on conditions."""
        alerts = []
        temp = weather.get("main", {}).get("temp", 25)
        wind = weather.get("wind", {}).get("speed", 5)
        rain = weather.get("rain", {}).get("1h", 0)
        
        if temp > 40:
            alerts.append({"type": "heat_wave", "severity": "high", "message": "Extreme heat warning"})
        if temp < 5:
            alerts.append({"type": "cold_wave", "severity": "high", "message": "Cold wave warning"})
        if wind > 20:
            alerts.append({"type": "strong_wind", "severity": "medium", "message": "Strong winds expected"})
        if rain > 50:
            alerts.append({"type": "heavy_rain", "severity": "high", "message": "Heavy rainfall warning"})
        
        return alerts
    
    def _generate_simulated_weather(self, state: str, lat: float, lon: float) -> Dict[str, Any]:
        """Generate realistic simulated weather data for Indian conditions."""
        # Seasonal adjustments based on current month
        month = datetime.now().month
        
        # Base temperature varies by region and season
        base_temp = 25 + (lat - 20) * -0.5  # Cooler in north
        
        # Seasonal adjustment
        if month in [3, 4, 5]:  # Summer
            base_temp += 10
        elif month in [6, 7, 8, 9]:  # Monsoon
            base_temp += 5
        elif month in [11, 12, 1, 2]:  # Winter
            base_temp -= 5
        
        # Add some randomness
        temperature = base_temp + random.uniform(-3, 3)
        humidity = 60 + random.uniform(-20, 30)
        
        # Monsoon season has more rain
        is_monsoon = month in [6, 7, 8, 9]
        rainfall_24h = random.uniform(10, 100) if is_monsoon else random.uniform(0, 20)
        
        return {
            "current": {
                "temperature": round(temperature, 1),
                "humidity": round(humidity, 1),
                "pressure": round(1013 + random.uniform(-10, 10), 1),
                "wind_speed": round(random.uniform(2, 15), 1),
                "description": self._get_weather_description(is_monsoon, temperature),
                "clouds": random.randint(10, 90)
            },
            "rainfall": {
                "last_1h": round(rainfall_24h / 24, 1),
                "last_3h": round(rainfall_24h / 8, 1),
                "last_24h": round(rainfall_24h, 1)
            },
            "forecast": self._generate_forecast(temperature, is_monsoon),
            "alerts": self._generate_alerts(temperature, rainfall_24h, is_monsoon),
            "timestamp": datetime.now().isoformat(),
            "data_source": "simulated"
        }
    
    def _get_weather_description(self, is_monsoon: bool, temp: float) -> str:
        """Get weather description based on conditions."""
        if is_monsoon:
            options = ["light rain", "moderate rain", "heavy rain", "thunderstorm", "overcast clouds"]
        elif temp > 35:
            options = ["clear sky", "few clouds", "haze", "hot and sunny"]
        else:
            options = ["clear sky", "few clouds", "scattered clouds", "partly cloudy"]
        return random.choice(options)
    
    def _generate_forecast(self, current_temp: float, is_monsoon: bool) -> list:
        """Generate 5-day forecast."""
        forecasts = []
        for i in range(5):
            future_date = datetime.now() + timedelta(days=i)
            temp_variation = random.uniform(-3, 3)
            forecasts.append({
                "datetime": future_date.strftime("%Y-%m-%d %H:%M:%S"),
                "temperature": round(current_temp + temp_variation, 1),
                "humidity": round(60 + random.uniform(-15, 25), 1),
                "rain_probability": random.randint(60, 95) if is_monsoon else random.randint(5, 30),
                "description": self._get_weather_description(is_monsoon, current_temp + temp_variation)
            })
        return forecasts
    
    def _generate_alerts(self, temp: float, rainfall: float, is_monsoon: bool) -> list:
        """Generate weather alerts based on conditions."""
        alerts = []
        
        if temp > 40:
            alerts.append({
                "type": "heat_wave",
                "severity": "high",
                "message": "Heat wave conditions expected. Protect crops with shade nets."
            })
        
        if rainfall > 80:
            alerts.append({
                "type": "flood_risk",
                "severity": "high",
                "message": "Heavy rainfall may cause waterlogging. Ensure proper drainage."
            })
        elif rainfall > 50 and is_monsoon:
            alerts.append({
                "type": "heavy_rain",
                "severity": "medium",
                "message": "Moderate to heavy rain expected. Delay pesticide application."
            })
        
        return alerts
