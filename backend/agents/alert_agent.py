"""
Alert Agent - Detects risks and generates notifications for farmers.
"""
import random
from typing import Dict, Any, List
from datetime import datetime, timedelta
from .base_agent import BaseAgent
import sys
sys.path.append('..')
from config import config

class AlertAgent(BaseAgent):
    """Agent responsible for risk detection and alert generation."""
    
    # Risk thresholds
    THRESHOLDS = {
        "drought": {
            "rainfall_24h_min": 5,  # mm
            "soil_moisture_min": 30,  # %
            "consecutive_dry_days": 7
        },
        "flood": {
            "rainfall_24h_max": 100,  # mm
            "soil_moisture_max": 90  # %
        },
        "heat_wave": {
            "temperature_max": 42,  # °C
            "consecutive_hot_days": 3
        },
        "cold_wave": {
            "temperature_min": 4,  # °C
            "consecutive_cold_days": 2
        },
        "pest_disease": {
            "humidity_range": (70, 90),
            "temperature_range": (25, 35)
        }
    }
    
    # Alert severity levels
    SEVERITY_COLORS = {
        "critical": "#FF0000",
        "high": "#FF6600",
        "medium": "#FFCC00",
        "low": "#00CC00"
    }
    
    def __init__(self):
        super().__init__("AlertAgent")
        self.active_alerts = []
    
    def get_capabilities(self) -> list:
        return [
            "detect_drought_risk",
            "detect_flood_risk",
            "detect_disease_risk",
            "detect_pest_risk",
            "generate_advance_alerts",
            "prioritize_alerts"
        ]
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute alert detection and generation task.
        
        Args:
            task: Contains data from weather, soil, and satellite agents
            
        Returns:
            Alert data including active alerts and 24-48hr forecasts
        """
        self.log_activity(f"Analyzing risks for {task.get('state', 'Unknown')}")
        self._record_execution()
        
        state = task.get("state", "Maharashtra")
        crop = task.get("crop", "Rice")
        weather_data = task.get("weather_data", {})
        soil_data = task.get("soil_data", {})
        satellite_data = task.get("satellite_data", {})
        
        # Detect all types of risks
        alerts = []
        alerts.extend(self._detect_drought_risk(weather_data, soil_data))
        alerts.extend(self._detect_flood_risk(weather_data, soil_data))
        alerts.extend(self._detect_temperature_extremes(weather_data))
        alerts.extend(self._detect_pest_disease_risk(weather_data, soil_data, satellite_data, crop))
        
        # Generate advance alerts (24-48 hours)
        advance_alerts = self._generate_advance_alerts(weather_data, state)
        
        # Prioritize and sort alerts
        sorted_alerts = self._prioritize_alerts(alerts)
        
        return {
            "active_alerts": sorted_alerts,
            "alert_count": len(sorted_alerts),
            "advance_alerts": advance_alerts,
            "risk_summary": self._generate_risk_summary(sorted_alerts, advance_alerts),
            "notification_recommendations": self._generate_notification_recommendations(sorted_alerts),
            "timestamp": datetime.now().isoformat()
        }
    
    def _detect_drought_risk(self, weather: Dict, soil: Dict) -> List[Dict]:
        """Detect drought risk conditions."""
        alerts = []
        
        rainfall = weather.get("rainfall", {}).get("last_24h", 20)
        moisture = soil.get("moisture", {}).get("current", 50)
        
        if rainfall < self.THRESHOLDS["drought"]["rainfall_24h_min"]:
            severity = "high" if rainfall < 2 else "medium"
            alerts.append({
                "type": "drought_risk",
                "severity": severity,
                "title": "Drought Conditions Developing",
                "message": f"Very low rainfall ({rainfall}mm in 24h). Consider irrigation.",
                "affected_component": "water_supply",
                "recommended_action": "Initiate supplemental irrigation immediately",
                "valid_until": (datetime.now() + timedelta(hours=48)).isoformat()
            })
        
        if moisture < self.THRESHOLDS["drought"]["soil_moisture_min"]:
            severity = "high" if moisture < 20 else "medium"
            alerts.append({
                "type": "low_soil_moisture",
                "severity": severity,
                "title": "Critically Low Soil Moisture",
                "message": f"Soil moisture at {moisture}%, crops may experience water stress.",
                "affected_component": "soil",
                "recommended_action": "Apply mulching and irrigate during early morning or evening",
                "valid_until": (datetime.now() + timedelta(hours=24)).isoformat()
            })
        
        return alerts
    
    def _detect_flood_risk(self, weather: Dict, soil: Dict) -> List[Dict]:
        """Detect flood/waterlogging risk."""
        alerts = []
        
        rainfall = weather.get("rainfall", {}).get("last_24h", 20)
        moisture = soil.get("moisture", {}).get("current", 50)
        
        if rainfall > self.THRESHOLDS["flood"]["rainfall_24h_max"]:
            alerts.append({
                "type": "flood_risk",
                "severity": "critical",
                "title": "Heavy Rainfall - Flood Risk",
                "message": f"Extreme rainfall ({rainfall}mm). High risk of waterlogging and flooding.",
                "affected_component": "field",
                "recommended_action": "Clear drainage channels, move equipment to higher ground",
                "valid_until": (datetime.now() + timedelta(hours=24)).isoformat()
            })
        elif rainfall > 70:
            alerts.append({
                "type": "waterlogging_risk",
                "severity": "medium",
                "title": "Waterlogging Possible",
                "message": f"Heavy rainfall ({rainfall}mm) may cause waterlogging in low-lying areas.",
                "affected_component": "field",
                "recommended_action": "Ensure proper drainage in fields",
                "valid_until": (datetime.now() + timedelta(hours=36)).isoformat()
            })
        
        if moisture > self.THRESHOLDS["flood"]["soil_moisture_max"]:
            alerts.append({
                "type": "excess_moisture",
                "severity": "medium",
                "title": "Excess Soil Moisture",
                "message": f"Soil moisture very high ({moisture}%). Risk of root rot and disease.",
                "affected_component": "soil",
                "recommended_action": "Avoid irrigation, improve field drainage",
                "valid_until": (datetime.now() + timedelta(hours=48)).isoformat()
            })
        
        return alerts
    
    def _detect_temperature_extremes(self, weather: Dict) -> List[Dict]:
        """Detect heat wave and cold wave conditions."""
        alerts = []
        
        current = weather.get("current", {})
        temp = current.get("temperature", 25)
        
        if temp > self.THRESHOLDS["heat_wave"]["temperature_max"]:
            alerts.append({
                "type": "heat_wave",
                "severity": "critical",
                "title": "Extreme Heat Warning",
                "message": f"Temperature at {temp}°C. Crops under severe heat stress.",
                "affected_component": "crop",
                "recommended_action": "Provide shade, increase irrigation frequency, spray water on leaves",
                "valid_until": (datetime.now() + timedelta(hours=24)).isoformat()
            })
        elif temp > 38:
            alerts.append({
                "type": "heat_stress",
                "severity": "high",
                "title": "High Temperature Alert",
                "message": f"Temperature at {temp}°C. Crops may experience heat stress.",
                "affected_component": "crop",
                "recommended_action": "Monitor crops closely, consider mulching",
                "valid_until": (datetime.now() + timedelta(hours=24)).isoformat()
            })
        
        if temp < self.THRESHOLDS["cold_wave"]["temperature_min"]:
            alerts.append({
                "type": "cold_wave",
                "severity": "critical",
                "title": "Frost/Cold Wave Warning",
                "message": f"Temperature dropped to {temp}°C. Risk of frost damage.",
                "affected_component": "crop",
                "recommended_action": "Cover sensitive crops, use smoke/fire for frost protection",
                "valid_until": (datetime.now() + timedelta(hours=24)).isoformat()
            })
        
        return alerts
    
    def _detect_pest_disease_risk(self, weather: Dict, soil: Dict, satellite: Dict, crop: str) -> List[Dict]:
        """Detect conditions favorable for pest and disease outbreak."""
        alerts = []
        
        current = weather.get("current", {})
        temp = current.get("temperature", 25)
        humidity = current.get("humidity", 60)
        
        thresh = self.THRESHOLDS["pest_disease"]
        
        # High humidity + warm temperature = disease risk
        if (thresh["humidity_range"][0] <= humidity <= thresh["humidity_range"][1] and
            thresh["temperature_range"][0] <= temp <= thresh["temperature_range"][1]):
            
            # Crop-specific diseases
            disease_info = self._get_crop_disease_info(crop)
            
            alerts.append({
                "type": "disease_risk",
                "severity": "medium",
                "title": f"Disease Risk Alert for {crop}",
                "message": f"Humidity ({humidity}%) and temperature ({temp}°C) favor disease development.",
                "affected_component": "crop",
                "diseases_at_risk": disease_info["diseases"],
                "recommended_action": disease_info["prevention"],
                "valid_until": (datetime.now() + timedelta(hours=48)).isoformat()
            })
        
        # Check satellite stress data
        stress = satellite.get("stress_analysis", {})
        if stress.get("overall_stress_level") == "high":
            alerts.append({
                "type": "crop_stress",
                "severity": "high",
                "title": "Crop Stress Detected",
                "message": "Satellite imagery indicates significant stress in crop canopy.",
                "affected_component": "crop",
                "recommended_action": "Conduct field inspection to identify cause of stress",
                "valid_until": (datetime.now() + timedelta(hours=72)).isoformat()
            })
        
        return alerts
    
    def _get_crop_disease_info(self, crop: str) -> Dict[str, Any]:
        """Get crop-specific disease information."""
        diseases = {
            "Rice": {
                "diseases": ["Blast", "Brown Leaf Spot", "Bacterial Leaf Blight"],
                "prevention": "Apply fungicide spray (Tricyclazole/Carbendazim)"
            },
            "Wheat": {
                "diseases": ["Rust", "Karnal Bunt", "Powdery Mildew"],
                "prevention": "Monitor for rust, apply Propiconazole if detected"
            },
            "Cotton": {
                "diseases": ["Boll Rot", "Wilt", "Grey Mildew"],
                "prevention": "Maintain field hygiene, apply appropriate fungicides"
            },
            "Sugarcane": {
                "diseases": ["Red Rot", "Smut", "Leaf Scald"],
                "prevention": "Use healthy seed material, remove infected plants"
            }
        }
        return diseases.get(crop, {
            "diseases": ["Various fungal diseases"],
            "prevention": "Apply preventive fungicide spray"
        })
    
    def _generate_advance_alerts(self, weather: Dict, state: str) -> List[Dict]:
        """Generate 24-48 hour advance alerts based on forecast."""
        advance_alerts = []
        
        forecast = weather.get("forecast", [])
        
        for i, day in enumerate(forecast[:2]):  # Next 2 days
            hours_ahead = (i + 1) * 24
            
            rain_prob = day.get("rain_probability", 0)
            temp = day.get("temperature", 25)
            
            if rain_prob > 80:
                advance_alerts.append({
                    "type": "rain_forecast",
                    "severity": "medium",
                    "title": f"Heavy Rain Expected in {hours_ahead}h",
                    "message": f"{rain_prob}% chance of rain. Plan field activities accordingly.",
                    "timeframe": f"{hours_ahead} hours",
                    "recommended_action": "Delay pesticide/fertilizer application, ensure drainage"
                })
            
            if temp > 40:
                advance_alerts.append({
                    "type": "heat_forecast",
                    "severity": "high",
                    "title": f"Heat Wave Expected in {hours_ahead}h",
                    "message": f"Temperature expected to reach {temp}°C.",
                    "timeframe": f"{hours_ahead} hours",
                    "recommended_action": "Prepare irrigation, arrange shade protection"
                })
        
        return advance_alerts
    
    def _prioritize_alerts(self, alerts: List[Dict]) -> List[Dict]:
        """Sort alerts by severity and recency."""
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        
        return sorted(alerts, key=lambda x: severity_order.get(x.get("severity", "low"), 4))
    
    def _generate_risk_summary(self, alerts: List[Dict], advance_alerts: List[Dict]) -> Dict[str, Any]:
        """Generate overall risk summary."""
        critical_count = sum(1 for a in alerts if a.get("severity") == "critical")
        high_count = sum(1 for a in alerts if a.get("severity") == "high")
        
        if critical_count > 0:
            overall = "critical"
            message = "Critical conditions detected! Immediate action required."
        elif high_count > 0:
            overall = "high"
            message = "High-risk conditions present. Take precautionary measures."
        elif len(alerts) > 0:
            overall = "medium"
            message = "Some risk factors detected. Monitor situation closely."
        else:
            overall = "low"
            message = "No significant risks detected at this time."
        
        return {
            "overall_risk": overall,
            "message": message,
            "active_alert_count": len(alerts),
            "advance_alert_count": len(advance_alerts),
            "critical_alerts": critical_count,
            "high_alerts": high_count
        }
    
    def _generate_notification_recommendations(self, alerts: List[Dict]) -> List[Dict]:
        """Generate notification recommendations for farmer."""
        recommendations = []
        
        if any(a.get("severity") == "critical" for a in alerts):
            recommendations.append({
                "channel": "SMS",
                "priority": "immediate",
                "message": "Send immediate SMS alert to farmer"
            })
            recommendations.append({
                "channel": "Voice",
                "priority": "high",
                "message": "Consider automated voice call for critical alert"
            })
        
        if any(a.get("severity") in ["high", "critical"] for a in alerts):
            recommendations.append({
                "channel": "App Notification",
                "priority": "high",
                "message": "Send push notification with detailed instructions"
            })
        
        return recommendations
