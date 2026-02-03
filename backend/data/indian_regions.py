"""
Indian Regions Data - Geographic, climate, and agricultural information for Indian states.
"""
from typing import Dict, Any, Optional

INDIAN_REGIONS = {
    "Maharashtra": {
        "capital": "Mumbai",
        "coordinates": {"lat": 19.7515, "lon": 75.7139},
        "climate_zone": "tropical_monsoon",
        "avg_rainfall_mm": 1200,
        "primary_soil_types": ["Black (Regur)", "Alluvial", "Laterite"],
        "major_crops": ["Rice", "Cotton", "Sugarcane", "Soybean", "Jowar", "Bajra"],
        "kharif_crops": ["Rice", "Cotton", "Soybean", "Groundnut"],
        "rabi_crops": ["Wheat", "Gram", "Jowar"],
        "districts": {
            "Nagpur": {"lat": 21.1458, "lon": 79.0882, "specialty": "Oranges"},
            "Nashik": {"lat": 20.0059, "lon": 73.7897, "specialty": "Grapes"},
            "Pune": {"lat": 18.5204, "lon": 73.8567, "specialty": "Sugarcane"},
            "Kolhapur": {"lat": 16.7050, "lon": 74.2433, "specialty": "Sugarcane"},
            "Vidarbha": {"lat": 20.6283, "lon": 78.9628, "specialty": "Cotton"}
        },
        "agricultural_area_lakh_hectares": 225,
        "irrigation_coverage_percent": 18
    },
    "Punjab": {
        "capital": "Chandigarh",
        "coordinates": {"lat": 31.1471, "lon": 75.3412},
        "climate_zone": "semi_arid",
        "avg_rainfall_mm": 600,
        "primary_soil_types": ["Alluvial"],
        "major_crops": ["Wheat", "Rice", "Cotton", "Maize", "Sugarcane"],
        "kharif_crops": ["Rice", "Cotton", "Maize"],
        "rabi_crops": ["Wheat", "Gram", "Barley"],
        "districts": {
            "Ludhiana": {"lat": 30.9010, "lon": 75.8573, "specialty": "Wheat"},
            "Amritsar": {"lat": 31.6340, "lon": 74.8723, "specialty": "Rice"},
            "Jalandhar": {"lat": 31.3260, "lon": 75.5762, "specialty": "Vegetables"},
            "Patiala": {"lat": 30.3398, "lon": 76.3869, "specialty": "Wheat"}
        },
        "agricultural_area_lakh_hectares": 42,
        "irrigation_coverage_percent": 98
    },
    "Uttar Pradesh": {
        "capital": "Lucknow",
        "coordinates": {"lat": 26.8467, "lon": 80.9462},
        "climate_zone": "semi_arid",
        "avg_rainfall_mm": 950,
        "primary_soil_types": ["Alluvial"],
        "major_crops": ["Wheat", "Rice", "Sugarcane", "Potato", "Mustard"],
        "kharif_crops": ["Rice", "Maize", "Sugarcane", "Pigeon Pea"],
        "rabi_crops": ["Wheat", "Gram", "Mustard", "Potato"],
        "districts": {
            "Meerut": {"lat": 28.9845, "lon": 77.7064, "specialty": "Sugarcane"},
            "Agra": {"lat": 27.1767, "lon": 78.0081, "specialty": "Wheat"},
            "Varanasi": {"lat": 25.3176, "lon": 82.9739, "specialty": "Rice"},
            "Lucknow": {"lat": 26.8467, "lon": 80.9462, "specialty": "Mango"}
        },
        "agricultural_area_lakh_hectares": 175,
        "irrigation_coverage_percent": 76
    },
    "Madhya Pradesh": {
        "capital": "Bhopal",
        "coordinates": {"lat": 22.9734, "lon": 78.6569},
        "climate_zone": "tropical_wet_dry",
        "avg_rainfall_mm": 1100,
        "primary_soil_types": ["Black (Regur)", "Alluvial", "Red"],
        "major_crops": ["Wheat", "Soybean", "Gram", "Rice", "Cotton"],
        "kharif_crops": ["Soybean", "Rice", "Maize", "Groundnut"],
        "rabi_crops": ["Wheat", "Gram", "Mustard", "Linseed"],
        "districts": {
            "Indore": {"lat": 22.7196, "lon": 75.8577, "specialty": "Soybean"},
            "Jabalpur": {"lat": 23.1815, "lon": 79.9864, "specialty": "Rice"},
            "Bhopal": {"lat": 23.2599, "lon": 77.4126, "specialty": "Wheat"}
        },
        "agricultural_area_lakh_hectares": 150,
        "irrigation_coverage_percent": 40
    },
    "Karnataka": {
        "capital": "Bengaluru",
        "coordinates": {"lat": 15.3173, "lon": 75.7139},
        "climate_zone": "tropical_monsoon",
        "avg_rainfall_mm": 1200,
        "primary_soil_types": ["Red", "Black (Regur)", "Laterite"],
        "major_crops": ["Rice", "Ragi", "Sugarcane", "Cotton", "Coffee"],
        "kharif_crops": ["Rice", "Ragi", "Maize", "Cotton"],
        "rabi_crops": ["Jowar", "Wheat", "Sunflower"],
        "districts": {
            "Belgaum": {"lat": 15.8497, "lon": 74.4977, "specialty": "Sugarcane"},
            "Mysore": {"lat": 12.2958, "lon": 76.6394, "specialty": "Silk"},
            "Hassan": {"lat": 13.0073, "lon": 76.1000, "specialty": "Coffee"},
            "Shimoga": {"lat": 13.9299, "lon": 75.5681, "specialty": "Arecanut"}
        },
        "agricultural_area_lakh_hectares": 102,
        "irrigation_coverage_percent": 34
    },
    "Gujarat": {
        "capital": "Gandhinagar",
        "coordinates": {"lat": 22.2587, "lon": 71.1924},
        "climate_zone": "semi_arid",
        "avg_rainfall_mm": 800,
        "primary_soil_types": ["Black (Regur)", "Alluvial", "Sandy"],
        "major_crops": ["Cotton", "Groundnut", "Wheat", "Rice", "Tobacco"],
        "kharif_crops": ["Cotton", "Groundnut", "Castor", "Bajra"],
        "rabi_crops": ["Wheat", "Gram", "Cumin"],
        "districts": {
            "Ahmedabad": {"lat": 23.0225, "lon": 72.5714, "specialty": "Cotton"},
            "Rajkot": {"lat": 22.3039, "lon": 70.8022, "specialty": "Groundnut"},
            "Surat": {"lat": 21.1702, "lon": 72.8311, "specialty": "Sugarcane"},
            "Kutch": {"lat": 23.7337, "lon": 69.8597, "specialty": "Dates"}
        },
        "agricultural_area_lakh_hectares": 98,
        "irrigation_coverage_percent": 48
    },
    "Rajasthan": {
        "capital": "Jaipur",
        "coordinates": {"lat": 27.0238, "lon": 74.2179},
        "climate_zone": "arid",
        "avg_rainfall_mm": 500,
        "primary_soil_types": ["Desert", "Alluvial", "Red"],
        "major_crops": ["Wheat", "Bajra", "Mustard", "Gram", "Groundnut"],
        "kharif_crops": ["Bajra", "Maize", "Groundnut", "Guar"],
        "rabi_crops": ["Wheat", "Gram", "Mustard", "Barley"],
        "districts": {
            "Jaipur": {"lat": 26.9124, "lon": 75.7873, "specialty": "Vegetables"},
            "Jodhpur": {"lat": 26.2389, "lon": 73.0243, "specialty": "Cumin"},
            "Udaipur": {"lat": 24.5854, "lon": 73.7125, "specialty": "Maize"},
            "Kota": {"lat": 25.2138, "lon": 75.8648, "specialty": "Soybean"}
        },
        "agricultural_area_lakh_hectares": 210,
        "irrigation_coverage_percent": 35
    },
    "Tamil Nadu": {
        "capital": "Chennai",
        "coordinates": {"lat": 11.1271, "lon": 78.6569},
        "climate_zone": "tropical_wet",
        "avg_rainfall_mm": 950,
        "primary_soil_types": ["Red", "Alluvial", "Black (Regur)"],
        "major_crops": ["Rice", "Sugarcane", "Cotton", "Groundnut", "Banana"],
        "kharif_crops": ["Rice", "Cotton", "Groundnut", "Millets"],
        "rabi_crops": ["Rice", "Pulses", "Groundnut"],
        "districts": {
            "Thanjavur": {"lat": 10.7870, "lon": 79.1378, "specialty": "Rice"},
            "Coimbatore": {"lat": 11.0168, "lon": 76.9558, "specialty": "Cotton"},
            "Salem": {"lat": 11.6643, "lon": 78.1460, "specialty": "Tapioca"},
            "Madurai": {"lat": 9.9252, "lon": 78.1198, "specialty": "Banana"}
        },
        "agricultural_area_lakh_hectares": 58,
        "irrigation_coverage_percent": 55
    },
    "Andhra Pradesh": {
        "capital": "Amaravati",
        "coordinates": {"lat": 15.9129, "lon": 79.7400},
        "climate_zone": "tropical_wet_dry",
        "avg_rainfall_mm": 900,
        "primary_soil_types": ["Red", "Black (Regur)", "Alluvial"],
        "major_crops": ["Rice", "Cotton", "Chilli", "Groundnut", "Tobacco"],
        "kharif_crops": ["Rice", "Cotton", "Maize", "Groundnut"],
        "rabi_crops": ["Rice", "Groundnut", "Sunflower"],
        "districts": {
            "Guntur": {"lat": 16.3067, "lon": 80.4365, "specialty": "Chilli"},
            "Krishna": {"lat": 16.6100, "lon": 80.7214, "specialty": "Rice"},
            "Chittoor": {"lat": 13.2172, "lon": 79.1003, "specialty": "Mango"},
            "Anantapur": {"lat": 14.6819, "lon": 77.6006, "specialty": "Groundnut"}
        },
        "agricultural_area_lakh_hectares": 75,
        "irrigation_coverage_percent": 45
    },
    "West Bengal": {
        "capital": "Kolkata",
        "coordinates": {"lat": 22.9868, "lon": 87.8550},
        "climate_zone": "tropical_wet",
        "avg_rainfall_mm": 1600,
        "primary_soil_types": ["Alluvial", "Laterite", "Red"],
        "major_crops": ["Rice", "Jute", "Potato", "Wheat", "Tea"],
        "kharif_crops": ["Rice", "Jute", "Maize"],
        "rabi_crops": ["Wheat", "Potato", "Mustard", "Vegetables"],
        "districts": {
            "Burdwan": {"lat": 23.2324, "lon": 87.8615, "specialty": "Rice"},
            "Hooghly": {"lat": 22.9008, "lon": 88.3957, "specialty": "Potato"},
            "Darjeeling": {"lat": 27.0410, "lon": 88.2663, "specialty": "Tea"},
            "Murshidabad": {"lat": 24.1820, "lon": 88.2714, "specialty": "Silk"}
        },
        "agricultural_area_lakh_hectares": 54,
        "irrigation_coverage_percent": 60
    }
}


def get_region_data(state: str) -> Optional[Dict[str, Any]]:
    """Get detailed data for a specific state."""
    return INDIAN_REGIONS.get(state)


def get_all_states() -> list:
    """Get list of all supported states."""
    return list(INDIAN_REGIONS.keys())


def get_crops_by_season(state: str, season: str) -> list:
    """Get crops for a state by season (kharif/rabi)."""
    region = INDIAN_REGIONS.get(state)
    if not region:
        return []
    
    if season.lower() == "kharif":
        return region.get("kharif_crops", [])
    elif season.lower() == "rabi":
        return region.get("rabi_crops", [])
    return region.get("major_crops", [])
