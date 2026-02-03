"""
Crop Database - Information about major Indian crops.
"""
from typing import Dict, Any, Optional

CROP_DATABASE = {
    "Rice": {
        "hindi_name": "चावल",
        "marathi_name": "तांदूळ",
        "season": "kharif",
        "sowing_months": [6, 7],
        "harvesting_months": [10, 11, 12],
        "water_requirement_mm": 1200,
        "optimal_temperature": {"min": 20, "max": 35},
        "optimal_ph": {"min": 5.5, "max": 7.0},
        "soil_types": ["Alluvial", "Clayey", "Loamy"],
        "npk_requirement": {"N": 120, "P": 60, "K": 60},  # kg/ha
        "yield_potential": {"min": 2.0, "max": 4.5, "avg": 2.8},  # tonnes/ha
        "growth_duration_days": 120,
        "major_diseases": ["Blast", "Brown Leaf Spot", "Bacterial Blight", "Sheath Blight"],
        "major_pests": ["Stem Borer", "Brown Plant Hopper", "Leaf Folder"],
        "irrigation_critical_stages": ["Transplanting", "Tillering", "Flowering"],
        "market_price_range": {"min": 1800, "max": 2200}  # Rs per quintal
    },
    "Wheat": {
        "hindi_name": "गेहूं",
        "marathi_name": "गहू",
        "season": "rabi",
        "sowing_months": [10, 11, 12],
        "harvesting_months": [3, 4, 5],
        "water_requirement_mm": 400,
        "optimal_temperature": {"min": 10, "max": 25},
        "optimal_ph": {"min": 6.0, "max": 7.5},
        "soil_types": ["Alluvial", "Loamy", "Clayey Loam"],
        "npk_requirement": {"N": 120, "P": 60, "K": 40},
        "yield_potential": {"min": 2.5, "max": 5.0, "avg": 3.5},
        "growth_duration_days": 130,
        "major_diseases": ["Rust", "Karnal Bunt", "Powdery Mildew", "Loose Smut"],
        "major_pests": ["Aphids", "Termites", "Army Worm"],
        "irrigation_critical_stages": ["Crown Root", "Tillering", "Flowering", "Grain Filling"],
        "market_price_range": {"min": 1900, "max": 2400}
    },
    "Cotton": {
        "hindi_name": "कपास",
        "marathi_name": "कापूस",
        "season": "kharif",
        "sowing_months": [4, 5, 6],
        "harvesting_months": [10, 11, 12],
        "water_requirement_mm": 700,
        "optimal_temperature": {"min": 25, "max": 35},
        "optimal_ph": {"min": 6.0, "max": 8.0},
        "soil_types": ["Black (Regur)", "Alluvial", "Sandy Loam"],
        "npk_requirement": {"N": 80, "P": 40, "K": 40},
        "yield_potential": {"min": 0.3, "max": 0.8, "avg": 0.5},  # Lint
        "growth_duration_days": 180,
        "major_diseases": ["Wilt", "Root Rot", "Grey Mildew", "Bacterial Blight"],
        "major_pests": ["Bollworm", "Whitefly", "Aphids", "Jassids"],
        "irrigation_critical_stages": ["Flowering", "Boll Formation"],
        "market_price_range": {"min": 5500, "max": 6500}
    },
    "Sugarcane": {
        "hindi_name": "गन्ना",
        "marathi_name": "ऊस",
        "season": "both",
        "sowing_months": [1, 2, 10],
        "harvesting_months": [11, 12, 1, 2, 3, 4],
        "water_requirement_mm": 2000,
        "optimal_temperature": {"min": 20, "max": 35},
        "optimal_ph": {"min": 6.0, "max": 7.5},
        "soil_types": ["Alluvial", "Loamy", "Clayey"],
        "npk_requirement": {"N": 150, "P": 60, "K": 60},
        "yield_potential": {"min": 50, "max": 100, "avg": 70},
        "growth_duration_days": 360,
        "major_diseases": ["Red Rot", "Smut", "Wilt", "Leaf Scald"],
        "major_pests": ["Top Borer", "Root Borer", "Pyrilla", "White Grub"],
        "irrigation_critical_stages": ["Germination", "Tillering", "Grand Growth"],
        "market_price_range": {"min": 2900, "max": 3200}
    },
    "Soybean": {
        "hindi_name": "सोयाबीन",
        "marathi_name": "सोयाबीन",
        "season": "kharif",
        "sowing_months": [6, 7],
        "harvesting_months": [10, 11],
        "water_requirement_mm": 450,
        "optimal_temperature": {"min": 20, "max": 30},
        "optimal_ph": {"min": 6.0, "max": 7.0},
        "soil_types": ["Black (Regur)", "Loamy", "Well-drained"],
        "npk_requirement": {"N": 20, "P": 60, "K": 40},  # N-fixing
        "yield_potential": {"min": 0.8, "max": 2.0, "avg": 1.2},
        "growth_duration_days": 100,
        "major_diseases": ["Yellow Mosaic", "Rust", "Pod Blight", "Charcoal Rot"],
        "major_pests": ["Girdle Beetle", "Stem Fly", "Pod Borer", "Defoliators"],
        "irrigation_critical_stages": ["Flowering", "Pod Formation"],
        "market_price_range": {"min": 3800, "max": 4500}
    },
    "Maize": {
        "hindi_name": "मक्का",
        "marathi_name": "मका",
        "season": "kharif",
        "sowing_months": [6, 7],
        "harvesting_months": [9, 10],
        "water_requirement_mm": 500,
        "optimal_temperature": {"min": 18, "max": 32},
        "optimal_ph": {"min": 5.8, "max": 7.0},
        "soil_types": ["Loamy", "Sandy Loam", "Well-drained"],
        "npk_requirement": {"N": 120, "P": 60, "K": 40},
        "yield_potential": {"min": 2.0, "max": 5.0, "avg": 3.0},
        "growth_duration_days": 100,
        "major_diseases": ["Downy Mildew", "Stalk Rot", "Banded Leaf"],
        "major_pests": ["Fall Armyworm", "Stem Borer", "Shoot Fly"],
        "irrigation_critical_stages": ["Tasseling", "Silking", "Grain Filling"],
        "market_price_range": {"min": 1700, "max": 2000}
    },
    "Groundnut": {
        "hindi_name": "मूंगफली",
        "marathi_name": "भुईमूग",
        "season": "kharif",
        "sowing_months": [6, 7],
        "harvesting_months": [10, 11],
        "water_requirement_mm": 500,
        "optimal_temperature": {"min": 22, "max": 30},
        "optimal_ph": {"min": 5.5, "max": 7.0},
        "soil_types": ["Sandy Loam", "Well-drained", "Light"],
        "npk_requirement": {"N": 20, "P": 40, "K": 60},
        "yield_potential": {"min": 1.0, "max": 2.5, "avg": 1.5},
        "growth_duration_days": 120,
        "major_diseases": ["Tikka", "Collar Rot", "Stem Rot", "Rust"],
        "major_pests": ["White Grub", "Aphids", "Leaf Miner", "Pod Borer"],
        "irrigation_critical_stages": ["Flowering", "Pegging", "Pod Development"],
        "market_price_range": {"min": 4500, "max": 5500}
    },
    "Gram": {
        "hindi_name": "चना",
        "marathi_name": "हरभरा",
        "season": "rabi",
        "sowing_months": [10, 11],
        "harvesting_months": [2, 3, 4],
        "water_requirement_mm": 300,
        "optimal_temperature": {"min": 15, "max": 25},
        "optimal_ph": {"min": 6.0, "max": 7.5},
        "soil_types": ["Loamy", "Clay Loam", "Well-drained"],
        "npk_requirement": {"N": 20, "P": 60, "K": 20},
        "yield_potential": {"min": 0.6, "max": 1.8, "avg": 1.0},
        "growth_duration_days": 100,
        "major_diseases": ["Wilt", "Blight", "Root Rot", "Rust"],
        "major_pests": ["Pod Borer", "Cutworm", "Aphids"],
        "irrigation_critical_stages": ["Branching", "Flowering", "Pod Formation"],
        "market_price_range": {"min": 4800, "max": 5500}
    },
    "Mustard": {
        "hindi_name": "सरसों",
        "marathi_name": "मोहरी",
        "season": "rabi",
        "sowing_months": [10, 11],
        "harvesting_months": [2, 3],
        "water_requirement_mm": 250,
        "optimal_temperature": {"min": 10, "max": 25},
        "optimal_ph": {"min": 6.0, "max": 7.5},
        "soil_types": ["Loamy", "Clay Loam", "Sandy Loam"],
        "npk_requirement": {"N": 60, "P": 40, "K": 40},
        "yield_potential": {"min": 0.8, "max": 2.0, "avg": 1.2},
        "growth_duration_days": 110,
        "major_diseases": ["White Rust", "Alternaria Blight", "Downy Mildew"],
        "major_pests": ["Aphids", "Sawfly", "Painted Bug"],
        "irrigation_critical_stages": ["Flowering", "Siliqua Formation"],
        "market_price_range": {"min": 4500, "max": 5200}
    },
    "Bajra": {
        "hindi_name": "बाजरा",
        "marathi_name": "बाजरी",
        "season": "kharif",
        "sowing_months": [6, 7],
        "harvesting_months": [9, 10],
        "water_requirement_mm": 350,
        "optimal_temperature": {"min": 25, "max": 35},
        "optimal_ph": {"min": 5.5, "max": 7.5},
        "soil_types": ["Sandy", "Sandy Loam", "Light"],
        "npk_requirement": {"N": 80, "P": 40, "K": 40},
        "yield_potential": {"min": 0.8, "max": 2.0, "avg": 1.3},
        "growth_duration_days": 80,
        "major_diseases": ["Downy Mildew", "Ergot", "Smut"],
        "major_pests": ["Stem Borer", "Shoot Fly", "Grey Weevil"],
        "irrigation_critical_stages": ["Flowering", "Grain Development"],
        "market_price_range": {"min": 2000, "max": 2400}
    }
}


def get_crop_info(crop_name: str) -> Optional[Dict[str, Any]]:
    """Get detailed information about a crop."""
    return CROP_DATABASE.get(crop_name)


def get_all_crops() -> list:
    """Get list of all crops in database."""
    return list(CROP_DATABASE.keys())


def get_crops_by_season(season: str) -> list:
    """Get crops for a specific season."""
    season = season.lower()
    return [
        crop for crop, data in CROP_DATABASE.items()
        if data.get("season") == season or data.get("season") == "both"
    ]


def get_disease_info(crop_name: str) -> list:
    """Get major diseases for a crop."""
    crop = CROP_DATABASE.get(crop_name)
    return crop.get("major_diseases", []) if crop else []


def get_pest_info(crop_name: str) -> list:
    """Get major pests for a crop."""
    crop = CROP_DATABASE.get(crop_name)
    return crop.get("major_pests", []) if crop else []
