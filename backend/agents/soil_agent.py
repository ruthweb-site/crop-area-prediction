"""
Soil Agent - Manages soil data including moisture, pH, and NPK nutrients.
"""
import random
from typing import Dict, Any
from datetime import datetime
from .base_agent import BaseAgent
import sys
sys.path.append('..')
from config import config

class SoilAgent(BaseAgent):
    """Agent responsible for soil data analysis and recommendations."""
    
    # Soil types common in India
    SOIL_TYPES = {
        "Alluvial": {"ph_range": (6.5, 8.0), "moisture_retention": "high", "fertility": "high"},
        "Black (Regur)": {"ph_range": (7.0, 8.5), "moisture_retention": "very_high", "fertility": "high"},
        "Red": {"ph_range": (5.5, 7.0), "moisture_retention": "low", "fertility": "medium"},
        "Laterite": {"ph_range": (5.0, 6.5), "moisture_retention": "low", "fertility": "low"},
        "Desert": {"ph_range": (7.0, 9.0), "moisture_retention": "very_low", "fertility": "low"},
        "Mountain": {"ph_range": (5.5, 7.5), "moisture_retention": "medium", "fertility": "medium"},
    }
    
    # Predominant soil types by state
    STATE_SOIL_MAP = {
        "Maharashtra": ["Black (Regur)", "Alluvial", "Laterite"],
        "Punjab": ["Alluvial"],
        "Uttar Pradesh": ["Alluvial"],
        "Madhya Pradesh": ["Black (Regur)", "Alluvial"],
        "Karnataka": ["Red", "Black (Regur)", "Laterite"],
        "Gujarat": ["Black (Regur)", "Alluvial", "Desert"],
        "Rajasthan": ["Desert", "Alluvial"],
        "Tamil Nadu": ["Red", "Alluvial", "Black (Regur)"],
        "Andhra Pradesh": ["Red", "Black (Regur)", "Alluvial"],
        "West Bengal": ["Alluvial", "Laterite"],
    }
    
    def __init__(self):
        super().__init__("SoilAgent")
    
    def get_capabilities(self) -> list:
        return [
            "analyze_soil_moisture",
            "measure_soil_ph",
            "analyze_npk_nutrients",
            "classify_soil_type",
            "recommend_fertilizers",
            "assess_soil_health"
        ]
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute soil analysis task.
        
        Args:
            task: Contains 'state', 'crop' for context
            
        Returns:
            Soil analysis data including moisture, pH, and NPK levels
        """
        self.log_activity(f"Analyzing soil for {task.get('state', 'Unknown')}")
        self._record_execution()
        
        state = task.get("state", "Maharashtra")
        crop = task.get("crop", "Rice")
        season = task.get("season", self._get_current_season())
        
        # Get soil data (simulated with realistic patterns)
        soil_data = self._generate_soil_data(state, crop, season)
        
        # Add recommendations based on soil conditions
        soil_data["recommendations"] = self._generate_recommendations(soil_data, crop)
        
        return soil_data
    
    def _get_current_season(self) -> str:
        """Determine current agricultural season in India."""
        month = datetime.now().month
        if month in [6, 7, 8, 9, 10]:
            return "Kharif"  # Monsoon season crops
        elif month in [11, 12, 1, 2, 3]:
            return "Rabi"  # Winter season crops
        else:
            return "Zaid"  # Summer season crops
    
    def _generate_soil_data(self, state: str, crop: str, season: str) -> Dict[str, Any]:
        """Generate realistic soil data based on state and conditions."""
        
        # Get predominant soil types for the state
        soil_types = self.STATE_SOIL_MAP.get(state, ["Alluvial"])
        primary_soil = soil_types[0]
        soil_info = self.SOIL_TYPES[primary_soil]
        
        # Generate pH based on soil type
        ph_min, ph_max = soil_info["ph_range"]
        ph = round(random.uniform(ph_min, ph_max), 1)
        
        # Generate moisture based on season and soil type
        moisture_base = {
            "very_high": 70,
            "high": 55,
            "medium": 40,
            "low": 25,
            "very_low": 15
        }[soil_info["moisture_retention"]]
        
        # Adjust for season
        if season == "Kharif":
            moisture_base += 15
        elif season == "Zaid":
            moisture_base -= 10
        
        moisture = min(95, max(10, moisture_base + random.uniform(-10, 10)))
        
        # Generate NPK levels
        fertility_multiplier = {"high": 1.2, "medium": 1.0, "low": 0.7}[soil_info["fertility"]]
        
        npk = {
            "nitrogen": round(random.uniform(150, 280) * fertility_multiplier, 1),  # kg/ha
            "phosphorus": round(random.uniform(10, 50) * fertility_multiplier, 1),  # kg/ha
            "potassium": round(random.uniform(100, 250) * fertility_multiplier, 1),  # kg/ha
        }
        
        # Soil health score (0-100)
        health_score = self._calculate_soil_health(ph, moisture, npk, crop)
        
        return {
            "soil_type": primary_soil,
            "all_soil_types": soil_types,
            "moisture": {
                "current": round(moisture, 1),
                "optimal_range": self._get_optimal_moisture(crop),
                "status": self._get_moisture_status(moisture, crop)
            },
            "ph": {
                "current": ph,
                "optimal_range": self._get_optimal_ph(crop),
                "status": self._get_ph_status(ph, crop)
            },
            "npk": {
                "nitrogen": {
                    "current": npk["nitrogen"],
                    "unit": "kg/ha",
                    "status": self._get_nutrient_status(npk["nitrogen"], "nitrogen", crop)
                },
                "phosphorus": {
                    "current": npk["phosphorus"],
                    "unit": "kg/ha", 
                    "status": self._get_nutrient_status(npk["phosphorus"], "phosphorus", crop)
                },
                "potassium": {
                    "current": npk["potassium"],
                    "unit": "kg/ha",
                    "status": self._get_nutrient_status(npk["potassium"], "potassium", crop)
                }
            },
            "health_score": health_score,
            "organic_carbon": round(random.uniform(0.3, 1.5), 2),
            "electrical_conductivity": round(random.uniform(0.1, 2.0), 2),
            "season": season,
            "timestamp": datetime.now().isoformat(),
            "data_source": "simulated"
        }
    
    def _get_optimal_moisture(self, crop: str) -> Dict[str, float]:
        """Get optimal moisture range for crop."""
        crop_moisture = {
            "Rice": {"min": 60, "max": 80},
            "Wheat": {"min": 40, "max": 60},
            "Cotton": {"min": 35, "max": 55},
            "Sugarcane": {"min": 55, "max": 75},
            "Soybean": {"min": 45, "max": 65},
            "Maize": {"min": 40, "max": 60},
            "Groundnut": {"min": 35, "max": 50},
        }
        return crop_moisture.get(crop, {"min": 40, "max": 60})
    
    def _get_optimal_ph(self, crop: str) -> Dict[str, float]:
        """Get optimal pH range for crop."""
        crop_ph = {
            "Rice": {"min": 5.5, "max": 7.0},
            "Wheat": {"min": 6.0, "max": 7.5},
            "Cotton": {"min": 6.0, "max": 8.0},
            "Sugarcane": {"min": 6.0, "max": 7.5},
            "Soybean": {"min": 6.0, "max": 7.0},
            "Maize": {"min": 5.8, "max": 7.0},
            "Groundnut": {"min": 5.5, "max": 7.0},
        }
        return crop_ph.get(crop, {"min": 6.0, "max": 7.5})
    
    def _get_moisture_status(self, moisture: float, crop: str) -> str:
        """Determine moisture status relative to crop needs."""
        optimal = self._get_optimal_moisture(crop)
        if moisture < optimal["min"]:
            return "low"
        elif moisture > optimal["max"]:
            return "high"
        return "optimal"
    
    def _get_ph_status(self, ph: float, crop: str) -> str:
        """Determine pH status relative to crop needs."""
        optimal = self._get_optimal_ph(crop)
        if ph < optimal["min"]:
            return "acidic"
        elif ph > optimal["max"]:
            return "alkaline"
        return "optimal"
    
    def _get_nutrient_status(self, value: float, nutrient: str, crop: str) -> str:
        """Determine nutrient status."""
        thresholds = {
            "nitrogen": {"low": 180, "high": 250},
            "phosphorus": {"low": 20, "high": 40},
            "potassium": {"low": 150, "high": 220}
        }
        t = thresholds.get(nutrient, {"low": 100, "high": 200})
        if value < t["low"]:
            return "deficient"
        elif value > t["high"]:
            return "sufficient"
        return "adequate"
    
    def _calculate_soil_health(self, ph: float, moisture: float, npk: Dict, crop: str) -> int:
        """Calculate overall soil health score."""
        score = 100
        
        # pH impact
        optimal_ph = self._get_optimal_ph(crop)
        if ph < optimal_ph["min"] or ph > optimal_ph["max"]:
            score -= 15
        
        # Moisture impact
        optimal_moisture = self._get_optimal_moisture(crop)
        if moisture < optimal_moisture["min"]:
            score -= 20
        elif moisture > optimal_moisture["max"]:
            score -= 10
        
        # Nutrient impact
        if npk["nitrogen"] < 180:
            score -= 15
        if npk["phosphorus"] < 20:
            score -= 10
        if npk["potassium"] < 150:
            score -= 10
        
        return max(0, min(100, score + random.randint(-5, 5)))
    
    def _generate_recommendations(self, soil_data: Dict, crop: str) -> list:
        """Generate fertilizer and soil management recommendations."""
        recommendations = []
        
        # Moisture recommendations
        moisture_status = soil_data["moisture"]["status"]
        if moisture_status == "low":
            recommendations.append({
                "type": "irrigation",
                "priority": "high",
                "message": f"Soil moisture is low ({soil_data['moisture']['current']}%). Irrigate immediately.",
                "action": "Increase irrigation frequency"
            })
        elif moisture_status == "high":
            recommendations.append({
                "type": "drainage",
                "priority": "medium",
                "message": f"Excess moisture detected ({soil_data['moisture']['current']}%). Improve drainage.",
                "action": "Create drainage channels"
            })
        
        # pH recommendations
        ph_status = soil_data["ph"]["status"]
        if ph_status == "acidic":
            recommendations.append({
                "type": "soil_amendment",
                "priority": "medium",
                "message": f"Soil is acidic (pH {soil_data['ph']['current']}). Apply lime.",
                "action": "Apply agricultural lime @ 2-4 tonnes/ha"
            })
        elif ph_status == "alkaline":
            recommendations.append({
                "type": "soil_amendment",
                "priority": "medium",
                "message": f"Soil is alkaline (pH {soil_data['ph']['current']}). Apply gypsum.",
                "action": "Apply gypsum @ 2-3 tonnes/ha"
            })
        
        # NPK recommendations
        n_status = soil_data["npk"]["nitrogen"]["status"]
        if n_status == "deficient":
            recommendations.append({
                "type": "fertilizer",
                "priority": "high",
                "message": "Nitrogen deficiency detected.",
                "action": f"Apply Urea @ 100-120 kg/ha for {crop}"
            })
        
        p_status = soil_data["npk"]["phosphorus"]["status"]
        if p_status == "deficient":
            recommendations.append({
                "type": "fertilizer",
                "priority": "high",
                "message": "Phosphorus deficiency detected.",
                "action": "Apply DAP @ 50-60 kg/ha"
            })
        
        k_status = soil_data["npk"]["potassium"]["status"]
        if k_status == "deficient":
            recommendations.append({
                "type": "fertilizer",
                "priority": "medium",
                "message": "Potassium levels are low.",
                "action": "Apply MOP @ 40-50 kg/ha"
            })
        
        if not recommendations:
            recommendations.append({
                "type": "maintenance",
                "priority": "low",
                "message": "Soil conditions are optimal for crop growth.",
                "action": "Continue current practices"
            })
        
        return recommendations
