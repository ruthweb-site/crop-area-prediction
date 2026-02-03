"""
Satellite Agent - Analyzes crop coverage and health from satellite imagery.
"""
import random
import math
from typing import Dict, Any, List
from datetime import datetime, timedelta
from .base_agent import BaseAgent
import sys
sys.path.append('..')
from config import config

class SatelliteAgent(BaseAgent):
    """Agent responsible for satellite imagery analysis and crop health assessment."""
    
    # NDVI interpretation thresholds
    NDVI_THRESHOLDS = {
        "water_barren": (-1.0, 0.1),
        "sparse_vegetation": (0.1, 0.2),
        "moderate_vegetation": (0.2, 0.4),
        "dense_vegetation": (0.4, 0.6),
        "very_dense_vegetation": (0.6, 1.0)
    }
    
    # Crop-specific healthy NDVI ranges
    CROP_NDVI_OPTIMAL = {
        "Rice": {"min": 0.4, "max": 0.7, "peak_month": 8},
        "Wheat": {"min": 0.35, "max": 0.65, "peak_month": 2},
        "Cotton": {"min": 0.3, "max": 0.6, "peak_month": 9},
        "Sugarcane": {"min": 0.45, "max": 0.75, "peak_month": 10},
        "Soybean": {"min": 0.35, "max": 0.6, "peak_month": 8},
        "Maize": {"min": 0.4, "max": 0.7, "peak_month": 8},
        "Groundnut": {"min": 0.3, "max": 0.55, "peak_month": 9},
    }
    
    def __init__(self):
        super().__init__("SatelliteAgent")
    
    def get_capabilities(self) -> list:
        return [
            "calculate_ndvi",
            "assess_crop_health",
            "detect_crop_coverage",
            "identify_stress_areas",
            "track_growth_stages",
            "detect_anomalies"
        ]
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute satellite imagery analysis task.
        
        Args:
            task: Contains 'state', 'crop', 'district' for location
            
        Returns:
            Satellite analysis data including NDVI, crop health, and coverage
        """
        self.log_activity(f"Analyzing satellite data for {task.get('state', 'Unknown')}")
        self._record_execution()
        
        state = task.get("state", "Maharashtra")
        crop = task.get("crop", "Rice")
        district = task.get("district")
        lat = task.get("lat")
        lon = task.get("lon")
        
        # Get coordinates from config if not provided
        if not lat or not lon:
            state_data = config.INDIAN_STATES.get(state, config.INDIAN_STATES["Maharashtra"])
            lat = state_data["lat"]
            lon = state_data["lon"]
        
        # Generate realistic satellite analysis data
        satellite_data = self._generate_satellite_analysis(state, crop, lat, lon)
        
        return satellite_data
    
    def _generate_satellite_analysis(self, state: str, crop: str, lat: float, lon: float) -> Dict[str, Any]:
        """Generate realistic satellite imagery analysis data."""
        
        current_month = datetime.now().month
        crop_info = self.CROP_NDVI_OPTIMAL.get(crop, {"min": 0.35, "max": 0.65, "peak_month": 8})
        
        # Calculate NDVI based on growth stage
        months_from_peak = abs(current_month - crop_info["peak_month"])
        if months_from_peak > 6:
            months_from_peak = 12 - months_from_peak
        
        # NDVI varies with growth stage
        growth_factor = 1 - (months_from_peak / 6) * 0.4
        base_ndvi = (crop_info["min"] + crop_info["max"]) / 2
        ndvi = base_ndvi * growth_factor + random.uniform(-0.1, 0.1)
        ndvi = max(0.1, min(0.9, ndvi))  # Clamp to valid range
        
        # Calculate health score based on NDVI and optimal range
        health_score = self._calculate_health_score(ndvi, crop_info)
        
        # Generate coverage data
        coverage = self._generate_coverage_data(state, crop, ndvi)
        
        # Detect stress areas
        stress_analysis = self._detect_stress_areas(ndvi, health_score, state)
        
        # Historical comparison
        historical = self._generate_historical_comparison(crop, ndvi)
        
        return {
            "ndvi": {
                "current": round(ndvi, 3),
                "interpretation": self._interpret_ndvi(ndvi),
                "optimal_range": {"min": crop_info["min"], "max": crop_info["max"]},
                "status": self._get_ndvi_status(ndvi, crop_info)
            },
            "health_score": health_score,
            "health_status": self._get_health_status(health_score),
            "coverage": coverage,
            "stress_analysis": stress_analysis,
            "growth_stage": self._determine_growth_stage(crop, current_month),
            "historical_comparison": historical,
            "imagery_date": (datetime.now() - timedelta(days=random.randint(1, 5))).isoformat(),
            "satellite_source": "Sentinel-2 (simulated)",
            "resolution": "10m",
            "cloud_cover": round(random.uniform(0, 25), 1),
            "coordinates": {"lat": lat, "lon": lon},
            "timestamp": datetime.now().isoformat(),
            "data_source": "simulated"
        }
    
    def _interpret_ndvi(self, ndvi: float) -> str:
        """Interpret NDVI value."""
        for category, (min_val, max_val) in self.NDVI_THRESHOLDS.items():
            if min_val <= ndvi < max_val:
                return category.replace("_", " ").title()
        return "Unknown"
    
    def _get_ndvi_status(self, ndvi: float, crop_info: Dict) -> str:
        """Get NDVI status relative to optimal range."""
        if ndvi < crop_info["min"]:
            return "below_optimal"
        elif ndvi > crop_info["max"]:
            return "above_optimal"
        return "optimal"
    
    def _calculate_health_score(self, ndvi: float, crop_info: Dict) -> int:
        """Calculate crop health score (0-100)."""
        optimal_mid = (crop_info["min"] + crop_info["max"]) / 2
        optimal_range = crop_info["max"] - crop_info["min"]
        
        # Calculate deviation from optimal
        deviation = abs(ndvi - optimal_mid) / optimal_range
        
        # Base score
        base_score = 100 - (deviation * 50)
        
        # Add some randomness
        score = base_score + random.uniform(-5, 5)
        
        return max(0, min(100, int(score)))
    
    def _get_health_status(self, score: int) -> str:
        """Get health status from score."""
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 40:
            return "moderate"
        elif score >= 20:
            return "poor"
        return "critical"
    
    def _generate_coverage_data(self, state: str, crop: str, ndvi: float) -> Dict[str, Any]:
        """Generate crop coverage data."""
        # Simulated total agricultural area (in hectares)
        state_areas = {
            "Maharashtra": 22500000,
            "Punjab": 4200000,
            "Uttar Pradesh": 17500000,
            "Madhya Pradesh": 15000000,
            "Karnataka": 10200000,
            "Gujarat": 9800000,
            "Rajasthan": 21000000,
            "Tamil Nadu": 5800000,
            "Andhra Pradesh": 7500000,
            "West Bengal": 5400000,
        }
        
        total_area = state_areas.get(state, 10000000)
        crop_area = total_area * random.uniform(0.1, 0.25)  # Portion under this crop
        
        # Healthy area based on NDVI
        healthy_percentage = min(95, max(40, ndvi * 100 + random.uniform(10, 20)))
        
        return {
            "total_agricultural_area": round(total_area / 100000, 2),  # In lakh hectares
            "total_agricultural_area_unit": "lakh hectares",
            "crop_area": round(crop_area / 100000, 2),
            "crop_area_unit": "lakh hectares",
            "healthy_area_percentage": round(healthy_percentage, 1),
            "stressed_area_percentage": round(100 - healthy_percentage, 1),
            "fallow_land_percentage": round(random.uniform(5, 15), 1)
        }
    
    def _detect_stress_areas(self, ndvi: float, health_score: int, state: str) -> Dict[str, Any]:
        """Detect crop stress areas."""
        stress_types = []
        
        # Water stress
        if random.random() > 0.6:
            stress_types.append({
                "type": "water_stress",
                "severity": random.choice(["low", "medium", "high"]),
                "affected_area_percentage": round(random.uniform(5, 25), 1),
                "description": "Areas showing signs of water stress"
            })
        
        # Nutrient deficiency
        if random.random() > 0.7:
            stress_types.append({
                "type": "nutrient_deficiency",
                "severity": random.choice(["low", "medium"]),
                "affected_area_percentage": round(random.uniform(3, 15), 1),
                "description": "Possible nutrient deficiency detected"
            })
        
        # Pest/Disease indicators
        if random.random() > 0.8 and health_score < 70:
            stress_types.append({
                "type": "pest_disease_risk",
                "severity": "medium",
                "affected_area_percentage": round(random.uniform(2, 10), 1),
                "description": "Unusual patterns suggesting pest or disease pressure"
            })
        
        return {
            "stress_detected": len(stress_types) > 0,
            "stress_count": len(stress_types),
            "stress_areas": stress_types,
            "overall_stress_level": self._calculate_overall_stress(stress_types)
        }
    
    def _calculate_overall_stress(self, stress_types: List[Dict]) -> str:
        """Calculate overall stress level."""
        if not stress_types:
            return "none"
        
        severity_score = 0
        for stress in stress_types:
            if stress["severity"] == "high":
                severity_score += 3
            elif stress["severity"] == "medium":
                severity_score += 2
            else:
                severity_score += 1
        
        avg_score = severity_score / len(stress_types)
        if avg_score >= 2.5:
            return "high"
        elif avg_score >= 1.5:
            return "medium"
        return "low"
    
    def _determine_growth_stage(self, crop: str, month: int) -> Dict[str, Any]:
        """Determine crop growth stage based on typical calendar."""
        # Simplified growth stage mapping
        growth_stages = {
            "Rice": {
                "Kharif": [
                    (6, 7, "Sowing/Transplanting"),
                    (7, 8, "Tillering"),
                    (8, 9, "Panicle Initiation"),
                    (9, 10, "Flowering"),
                    (10, 11, "Grain Filling"),
                    (11, 12, "Maturity/Harvest")
                ]
            },
            "Wheat": {
                "Rabi": [
                    (11, 12, "Sowing"),
                    (12, 1, "Crown Root Initiation"),
                    (1, 2, "Tillering"),
                    (2, 3, "Jointing"),
                    (3, 4, "Heading/Flowering"),
                    (4, 5, "Grain Filling/Harvest")
                ]
            }
        }
        
        # Default growth stage info
        stage_info = {
            "current_stage": "Active Growth",
            "days_in_stage": random.randint(10, 30),
            "expected_days_remaining": random.randint(15, 45),
            "next_stage": "Maturation"
        }
        
        return stage_info
    
    def _generate_historical_comparison(self, crop: str, current_ndvi: float) -> Dict[str, Any]:
        """Generate historical comparison data."""
        # Generate historical NDVI values (simulated)
        years = [2023, 2024, 2025]
        historical_ndvi = [current_ndvi + random.uniform(-0.15, 0.1) for _ in years]
        
        avg_historical = sum(historical_ndvi) / len(historical_ndvi)
        deviation = ((current_ndvi - avg_historical) / avg_historical) * 100
        
        return {
            "previous_years": [
                {"year": y, "ndvi": round(n, 3)} for y, n in zip(years, historical_ndvi)
            ],
            "historical_average": round(avg_historical, 3),
            "current_vs_average": round(deviation, 1),
            "trend": "improving" if deviation > 5 else "declining" if deviation < -5 else "stable"
        }
