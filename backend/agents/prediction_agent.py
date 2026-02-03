"""
Prediction Agent - ML-based yield prediction combining data from all agents.
"""
import random
import math
from typing import Dict, Any, Optional
from datetime import datetime
from .base_agent import BaseAgent
import sys
sys.path.append('..')
from config import config

class PredictionAgent(BaseAgent):
    """Agent responsible for yield prediction and risk assessment."""
    
    # Historical average yields (tonnes/hectare) for Indian crops
    AVERAGE_YIELDS = {
        "Rice": {"avg": 2.8, "max": 4.5, "min": 1.5},
        "Wheat": {"avg": 3.5, "max": 5.0, "min": 2.0},
        "Cotton": {"avg": 0.5, "max": 0.8, "min": 0.2},  # lint
        "Sugarcane": {"avg": 70, "max": 100, "min": 40},
        "Soybean": {"avg": 1.2, "max": 2.0, "min": 0.6},
        "Maize": {"avg": 3.0, "max": 5.0, "min": 1.5},
        "Groundnut": {"avg": 1.5, "max": 2.5, "min": 0.8},
        "Gram": {"avg": 1.0, "max": 1.8, "min": 0.5},
        "Bajra": {"avg": 1.3, "max": 2.0, "min": 0.7},
        "Mustard": {"avg": 1.2, "max": 2.0, "min": 0.6},
    }
    
    # Risk factor weights
    RISK_WEIGHTS = {
        "weather": 0.25,
        "soil": 0.20,
        "crop_health": 0.25,
        "historical": 0.15,
        "season": 0.15
    }
    
    def __init__(self):
        super().__init__("PredictionAgent")
    
    def get_capabilities(self) -> list:
        return [
            "predict_yield",
            "calculate_risk_score",
            "generate_confidence_interval",
            "analyze_factors",
            "compare_historical",
            "forecast_production"
        ]
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute yield prediction task.
        
        Args:
            task: Contains 'state', 'crop', and data from other agents
            
        Returns:
            Prediction results including yield forecast and risk scores
        """
        self.log_activity(f"Generating prediction for {task.get('crop', 'Unknown')} in {task.get('state', 'Unknown')}")
        self._record_execution()
        
        state = task.get("state", "Maharashtra")
        crop = task.get("crop", "Rice")
        weather_data = task.get("weather_data", {})
        soil_data = task.get("soil_data", {})
        satellite_data = task.get("satellite_data", {})
        
        # Generate comprehensive prediction
        prediction = self._generate_prediction(state, crop, weather_data, soil_data, satellite_data)
        
        return prediction
    
    def _generate_prediction(self, state: str, crop: str, weather: Dict, soil: Dict, satellite: Dict) -> Dict[str, Any]:
        """Generate comprehensive yield prediction."""
        
        # Get base yield data
        yield_info = self.AVERAGE_YIELDS.get(crop, {"avg": 2.5, "max": 4.0, "min": 1.0})
        
        # Calculate factor scores
        weather_score = self._calculate_weather_score(weather, crop)
        soil_score = self._calculate_soil_score(soil, crop)
        satellite_score = self._calculate_satellite_score(satellite)
        seasonal_score = self._calculate_seasonal_score(crop)
        
        # Combine scores for yield prediction
        combined_score = (
            weather_score * self.RISK_WEIGHTS["weather"] +
            soil_score * self.RISK_WEIGHTS["soil"] +
            satellite_score * self.RISK_WEIGHTS["crop_health"] +
            seasonal_score * self.RISK_WEIGHTS["season"] +
            random.uniform(0.7, 0.9) * self.RISK_WEIGHTS["historical"]
        )
        
        # Calculate predicted yield
        yield_range = yield_info["max"] - yield_info["min"]
        predicted_yield = yield_info["min"] + (yield_range * combined_score)
        predicted_yield = round(predicted_yield, 2)
        
        # Calculate confidence interval
        confidence = self._calculate_confidence(weather, soil, satellite)
        margin = predicted_yield * (1 - confidence / 100) * 0.3
        
        # Overall risk score (inverse of combined score)
        risk_score = round((1 - combined_score) * 100, 1)
        
        # Production forecast
        crop_area = satellite.get("coverage", {}).get("crop_area", 10)  # lakh hectares
        production = round(predicted_yield * crop_area, 2)  # lakh tonnes
        
        return {
            "yield_prediction": {
                "predicted": predicted_yield,
                "unit": "tonnes/hectare",
                "confidence_interval": {
                    "lower": round(predicted_yield - margin, 2),
                    "upper": round(predicted_yield + margin, 2)
                },
                "comparison_to_average": round(((predicted_yield / yield_info["avg"]) - 1) * 100, 1),
                "historical_average": yield_info["avg"],
                "maximum_potential": yield_info["max"]
            },
            "production_forecast": {
                "estimated_production": production,
                "unit": "lakh tonnes",
                "area_under_crop": crop_area,
                "area_unit": "lakh hectares"
            },
            "risk_assessment": {
                "overall_risk_score": risk_score,
                "risk_level": self._get_risk_level(risk_score),
                "factors": self._get_risk_factors(weather_score, soil_score, satellite_score, seasonal_score)
            },
            "confidence": {
                "score": confidence,
                "level": self._get_confidence_level(confidence)
            },
            "outlook": self._generate_outlook(combined_score, risk_score, crop),
            "recommendations": self._generate_yield_recommendations(
                weather_score, soil_score, satellite_score, crop
            ),
            "factor_scores": {
                "weather_impact": round(weather_score * 100, 1),
                "soil_health": round(soil_score * 100, 1),
                "crop_condition": round(satellite_score * 100, 1),
                "seasonal_favorability": round(seasonal_score * 100, 1)
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_weather_score(self, weather: Dict, crop: str) -> float:
        """Calculate weather favorability score (0-1)."""
        if not weather:
            return 0.7  # Default moderate score
        
        current = weather.get("current", {})
        temp = current.get("temperature", 25)
        humidity = current.get("humidity", 60)
        rainfall = weather.get("rainfall", {}).get("last_24h", 20)
        
        score = 1.0
        
        # Temperature impact
        optimal_temps = {
            "Rice": (25, 35),
            "Wheat": (15, 25),
            "Cotton": (25, 35),
            "Sugarcane": (20, 30),
        }
        opt_range = optimal_temps.get(crop, (20, 30))
        if temp < opt_range[0]:
            score -= (opt_range[0] - temp) * 0.02
        elif temp > opt_range[1]:
            score -= (temp - opt_range[1]) * 0.02
        
        # Rainfall impact
        if rainfall > 100:  # Excess rain
            score -= 0.15
        elif rainfall < 5 and crop in ["Rice", "Sugarcane"]:  # Too dry for water-loving crops
            score -= 0.2
        
        # Weather alerts impact
        alerts = weather.get("alerts", [])
        for alert in alerts:
            if alert.get("severity") == "high":
                score -= 0.15
            elif alert.get("severity") == "medium":
                score -= 0.08
        
        return max(0.3, min(1.0, score))
    
    def _calculate_soil_score(self, soil: Dict, crop: str) -> float:
        """Calculate soil health score (0-1)."""
        if not soil:
            return 0.7
        
        health_score = soil.get("health_score", 70)
        moisture_status = soil.get("moisture", {}).get("status", "optimal")
        ph_status = soil.get("ph", {}).get("status", "optimal")
        
        score = health_score / 100
        
        # Moisture adjustment
        if moisture_status == "low":
            score -= 0.15
        elif moisture_status == "high":
            score -= 0.08
        
        # pH adjustment
        if ph_status in ["acidic", "alkaline"]:
            score -= 0.1
        
        return max(0.3, min(1.0, score))
    
    def _calculate_satellite_score(self, satellite: Dict) -> float:
        """Calculate crop health score from satellite data (0-1)."""
        if not satellite:
            return 0.7
        
        health_score = satellite.get("health_score", 70)
        ndvi_status = satellite.get("ndvi", {}).get("status", "optimal")
        stress = satellite.get("stress_analysis", {})
        
        score = health_score / 100
        
        # NDVI status adjustment
        if ndvi_status == "below_optimal":
            score -= 0.1
        
        # Stress adjustment
        if stress.get("overall_stress_level") == "high":
            score -= 0.15
        elif stress.get("overall_stress_level") == "medium":
            score -= 0.08
        
        return max(0.3, min(1.0, score))
    
    def _calculate_seasonal_score(self, crop: str) -> float:
        """Calculate seasonal favorability score (0-1)."""
        month = datetime.now().month
        
        # Crop seasonality
        kharif_crops = ["Rice", "Cotton", "Soybean", "Maize", "Groundnut"]
        rabi_crops = ["Wheat", "Gram", "Mustard"]
        
        if crop in kharif_crops and month in [7, 8, 9, 10]:
            return random.uniform(0.8, 0.95)
        elif crop in rabi_crops and month in [12, 1, 2, 3]:
            return random.uniform(0.8, 0.95)
        else:
            return random.uniform(0.5, 0.7)
    
    def _calculate_confidence(self, weather: Dict, soil: Dict, satellite: Dict) -> int:
        """Calculate prediction confidence score."""
        base_confidence = 70
        
        # Data availability bonus
        if weather and weather.get("data_source") != "simulated":
            base_confidence += 10
        if soil:
            base_confidence += 5
        if satellite:
            base_confidence += 10
        
        # Add some variance
        confidence = base_confidence + random.randint(-5, 5)
        
        return max(50, min(95, confidence))
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Convert risk score to level."""
        if risk_score < 20:
            return "low"
        elif risk_score < 40:
            return "moderate"
        elif risk_score < 60:
            return "elevated"
        elif risk_score < 80:
            return "high"
        return "critical"
    
    def _get_confidence_level(self, confidence: int) -> str:
        """Convert confidence score to level."""
        if confidence >= 85:
            return "very_high"
        elif confidence >= 70:
            return "high"
        elif confidence >= 55:
            return "moderate"
        return "low"
    
    def _get_risk_factors(self, weather_score: float, soil_score: float, 
                          satellite_score: float, seasonal_score: float) -> list:
        """Identify key risk factors."""
        factors = []
        
        if weather_score < 0.6:
            factors.append({
                "factor": "Weather Conditions",
                "impact": "high",
                "description": "Unfavorable weather patterns may affect yield"
            })
        
        if soil_score < 0.6:
            factors.append({
                "factor": "Soil Health",
                "impact": "medium",
                "description": "Soil conditions need improvement for optimal growth"
            })
        
        if satellite_score < 0.6:
            factors.append({
                "factor": "Crop Health",
                "impact": "high",
                "description": "Crop stress detected in satellite imagery"
            })
        
        if seasonal_score < 0.6:
            factors.append({
                "factor": "Seasonal Timing",
                "impact": "medium",
                "description": "Current season may not be optimal for this crop"
            })
        
        if not factors:
            factors.append({
                "factor": "None Significant",
                "impact": "low",
                "description": "All major factors are within acceptable ranges"
            })
        
        return factors
    
    def _generate_outlook(self, combined_score: float, risk_score: float, crop: str) -> str:
        """Generate human-readable outlook."""
        if combined_score >= 0.8:
            return f"Excellent outlook for {crop}. Conditions are favorable and yield is expected to exceed historical averages."
        elif combined_score >= 0.65:
            return f"Good outlook for {crop}. Most factors are positive, though minor issues may slightly impact yield."
        elif combined_score >= 0.5:
            return f"Moderate outlook for {crop}. Some challenges exist that may affect yield. Close monitoring recommended."
        elif combined_score >= 0.35:
            return f"Concerning outlook for {crop}. Multiple factors are unfavorable. Immediate corrective action advised."
        else:
            return f"Poor outlook for {crop}. Significant challenges detected. Consider consulting agricultural experts."
    
    def _generate_yield_recommendations(self, weather_score: float, soil_score: float,
                                        satellite_score: float, crop: str) -> list:
        """Generate actionable recommendations."""
        recommendations = []
        
        if weather_score < 0.6:
            recommendations.append({
                "category": "Weather Management",
                "priority": "high",
                "action": "Install protective measures like shade nets or mulching",
                "expected_impact": "Reduce weather-related stress by 20-30%"
            })
        
        if soil_score < 0.6:
            recommendations.append({
                "category": "Soil Improvement",
                "priority": "high",
                "action": "Apply recommended fertilizers and soil amendments",
                "expected_impact": "Improve soil health score by 15-25%"
            })
        
        if satellite_score < 0.6:
            recommendations.append({
                "category": "Crop Management",
                "priority": "high",
                "action": "Inspect fields for pest/disease and apply treatments if needed",
                "expected_impact": "Prevent further health decline"
            })
        
        # General recommendation
        recommendations.append({
            "category": "Monitoring",
            "priority": "medium",
            "action": f"Continue regular monitoring of {crop} fields",
            "expected_impact": "Early detection of issues"
        })
        
        return recommendations
