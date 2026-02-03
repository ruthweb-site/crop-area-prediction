"""
Response Agent - Formats and delivers multilingual responses to farmers.
"""
from typing import Dict, Any, List
from datetime import datetime
from .base_agent import BaseAgent
import sys
sys.path.append('..')
from config import config

class ResponseAgent(BaseAgent):
    """Agent responsible for formatting responses and generating recommendations."""
    
    # Multilingual templates
    TRANSLATIONS = {
        "en": {
            "greeting": "Hello! Here's your crop analysis for {crop} in {state}:",
            "yield_good": "Good news! The expected yield is above average.",
            "yield_moderate": "The expected yield is around the historical average.",
            "yield_poor": "Caution: The expected yield may be below average.",
            "risk_low": "Risk Level: Low ✅",
            "risk_medium": "Risk Level: Moderate ⚠️",
            "risk_high": "Risk Level: High 🔴",
            "recommendation": "Recommendation",
            "weather_summary": "Weather Summary",
            "soil_summary": "Soil Conditions",
            "crop_health": "Crop Health",
            "need_action": "Action Required",
            "no_action": "No immediate action needed",
            "units": {
                "temperature": "°C",
                "humidity": "%",
                "rainfall": "mm",
                "yield": "tonnes/ha"
            }
        },
        "hi": {
            "greeting": "नमस्ते! {state} में {crop} के लिए आपका फसल विश्लेषण:",
            "yield_good": "अच्छी खबर! अपेक्षित उपज औसत से अधिक है।",
            "yield_moderate": "अपेक्षित उपज ऐतिहासिक औसत के आसपास है।",
            "yield_poor": "सावधान: अपेक्षित उपज औसत से कम हो सकती है।",
            "risk_low": "जोखिम स्तर: कम ✅",
            "risk_medium": "जोखिम स्तर: मध्यम ⚠️",
            "risk_high": "जोखिम स्तर: उच्च 🔴",
            "recommendation": "सिफारिश",
            "weather_summary": "मौसम सारांश",
            "soil_summary": "मिट्टी की स्थिति",
            "crop_health": "फसल स्वास्थ्य",
            "need_action": "कार्रवाई आवश्यक",
            "no_action": "तत्काल कार्रवाई की आवश्यकता नहीं",
            "units": {
                "temperature": "°से",
                "humidity": "%",
                "rainfall": "मिमी",
                "yield": "टन/हेक्टेयर"
            }
        },
        "mr": {
            "greeting": "नमस्कार! {state} मधील {crop} साठी तुमचे पीक विश्लेषण:",
            "yield_good": "चांगली बातमी! अपेक्षित उत्पादन सरासरीपेक्षा जास्त आहे.",
            "yield_moderate": "अपेक्षित उत्पादन ऐतिहासिक सरासरीच्या आसपास आहे.",
            "yield_poor": "सावधान: अपेक्षित उत्पादन सरासरीपेक्षा कमी असू शकते.",
            "risk_low": "जोखीम पातळी: कमी ✅",
            "risk_medium": "जोखीम पातळी: मध्यम ⚠️",
            "risk_high": "जोखीम पातळी: उच्च 🔴",
            "recommendation": "शिफारस",
            "weather_summary": "हवामान सारांश",
            "soil_summary": "माती स्थिती",
            "crop_health": "पीक आरोग्य",
            "need_action": "कृती आवश्यक",
            "no_action": "तात्काळ कृतीची गरज नाही",
            "units": {
                "temperature": "°से",
                "humidity": "%",
                "rainfall": "मिमी",
                "yield": "टन/हेक्टर"
            }
        }
    }
    
    # State name translations
    STATE_NAMES = {
        "Maharashtra": {"hi": "महाराष्ट्र", "mr": "महाराष्ट्र"},
        "Punjab": {"hi": "पंजाब", "mr": "पंजाब"},
        "Uttar Pradesh": {"hi": "उत्तर प्रदेश", "mr": "उत्तर प्रदेश"},
        "Madhya Pradesh": {"hi": "मध्य प्रदेश", "mr": "मध्य प्रदेश"},
        "Karnataka": {"hi": "कर्नाटक", "mr": "कर्नाटक"},
        "Gujarat": {"hi": "गुजरात", "mr": "गुजरात"},
        "Rajasthan": {"hi": "राजस्थान", "mr": "राजस्थान"},
        "Tamil Nadu": {"hi": "तमिलनाडु", "mr": "तामिळनाडू"},
        "Andhra Pradesh": {"hi": "आंध्र प्रदेश", "mr": "आंध्र प्रदेश"},
        "West Bengal": {"hi": "पश्चिम बंगाल", "mr": "पश्चिम बंगाल"},
    }
    
    # Crop name translations
    CROP_NAMES = {
        "Rice": {"hi": "चावल", "mr": "तांदूळ"},
        "Wheat": {"hi": "गेहूं", "mr": "गहू"},
        "Cotton": {"hi": "कपास", "mr": "कापूस"},
        "Sugarcane": {"hi": "गन्ना", "mr": "ऊस"},
        "Soybean": {"hi": "सोयाबीन", "mr": "सोयाबीन"},
        "Maize": {"hi": "मक्का", "mr": "मका"},
        "Groundnut": {"hi": "मूंगफली", "mr": "भुईमूग"},
    }
    
    def __init__(self):
        super().__init__("ResponseAgent")
    
    def get_capabilities(self) -> list:
        return [
            "format_response",
            "translate_response",
            "generate_charts_data",
            "create_recommendations",
            "format_alerts"
        ]
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute response formatting task.
        
        Args:
            task: Contains all agent data and language preference
            
        Returns:
            Formatted response with charts data and recommendations
        """
        self.log_activity(f"Formatting response in {task.get('language', 'en')}")
        self._record_execution()
        
        language = task.get("language", "en")
        state = task.get("state", "Maharashtra")
        crop = task.get("crop", "Rice")
        weather_data = task.get("weather_data", {})
        soil_data = task.get("soil_data", {})
        satellite_data = task.get("satellite_data", {})
        prediction_data = task.get("prediction_data", {})
        alert_data = task.get("alert_data", {})
        query = task.get("query", "")
        
        # Format the complete response
        response = self._format_complete_response(
            language, state, crop, query,
            weather_data, soil_data, satellite_data,
            prediction_data, alert_data
        )
        
        return response
    
    def _format_complete_response(self, language: str, state: str, crop: str, query: str,
                                  weather: Dict, soil: Dict, satellite: Dict,
                                  prediction: Dict, alerts: Dict) -> Dict[str, Any]:
        """Format the complete response with all components."""
        
        t = self.TRANSLATIONS.get(language, self.TRANSLATIONS["en"])
        
        # Translate names
        translated_state = self._translate_name(state, language, self.STATE_NAMES)
        translated_crop = self._translate_name(crop, language, self.CROP_NAMES)
        
        # Main response text
        greeting = t["greeting"].format(crop=translated_crop, state=translated_state)
        
        # Yield summary
        yield_pred = prediction.get("yield_prediction", {})
        predicted_yield = yield_pred.get("predicted", 0)
        comparison = yield_pred.get("comparison_to_average", 0)
        
        if comparison > 10:
            yield_text = t["yield_good"]
        elif comparison < -10:
            yield_text = t["yield_poor"]
        else:
            yield_text = t["yield_moderate"]
        
        # Risk level
        risk_score = prediction.get("risk_assessment", {}).get("overall_risk_score", 30)
        if risk_score < 30:
            risk_text = t["risk_low"]
        elif risk_score < 60:
            risk_text = t["risk_medium"]
        else:
            risk_text = t["risk_high"]
        
        # Build response
        response = {
            "query": query,
            "language": language,
            "greeting": greeting,
            
            # Main summary text
            "summary": {
                "text": self._build_summary_text(language, translated_crop, translated_state,
                                                 yield_pred, prediction, alerts),
                "yield_message": yield_text,
                "risk_message": risk_text
            },
            
            # Weather card
            "weather_card": self._format_weather_card(weather, language, t),
            
            # Soil card
            "soil_card": self._format_soil_card(soil, language, t),
            
            # Crop health card
            "crop_health_card": self._format_crop_health_card(satellite, language, t),
            
            # Prediction details
            "prediction_details": self._format_prediction_details(prediction, language),
            
            # Alerts
            "alerts_formatted": self._format_alerts(alerts, language),
            
            # Charts data for frontend
            "charts": self._generate_charts_data(weather, soil, satellite, prediction),
            
            # Recommendations
            "recommendations": self._format_recommendations(prediction, soil, alerts, language),
            
            # Irrigation advice
            "irrigation_advice": self._generate_irrigation_advice(weather, soil, crop, language),
            
            # Confidence indicator
            "confidence": {
                "score": prediction.get("confidence", {}).get("score", 70),
                "level": prediction.get("confidence", {}).get("level", "moderate"),
                "display": f"{prediction.get('confidence', {}).get('score', 70)}%"
            },
            
            "timestamp": datetime.now().isoformat()
        }
        
        return response
    
    def _translate_name(self, name: str, language: str, mapping: Dict) -> str:
        """Translate a name to the target language."""
        if language == "en":
            return name
        return mapping.get(name, {}).get(language, name)
    
    def _build_summary_text(self, language: str, crop: str, state: str,
                           yield_pred: Dict, prediction: Dict, alerts: Dict) -> str:
        """Build a natural language summary."""
        predicted = yield_pred.get("predicted", 0)
        unit = yield_pred.get("unit", "tonnes/ha")
        confidence = prediction.get("confidence", {}).get("score", 70)
        risk_level = prediction.get("risk_assessment", {}).get("risk_level", "moderate")
        alert_count = alerts.get("alert_count", 0)
        
        if language == "en":
            summary = f"Based on current weather, soil, and satellite data, the predicted yield for {crop} in {state} is {predicted} {unit}. "
            summary += f"Our confidence in this prediction is {confidence}%. "
            if risk_level in ["low", "moderate"]:
                summary += "Overall conditions look favorable. "
            else:
                summary += f"There are {alert_count} alerts requiring attention. "
        elif language == "hi":
            summary = f"वर्तमान मौसम, मिट्टी और उपग्रह डेटा के आधार पर, {state} में {crop} की अनुमानित उपज {predicted} टन/हेक्टेयर है। "
            summary += f"इस भविष्यवाणी में हमारा विश्वास {confidence}% है। "
            if risk_level in ["low", "moderate"]:
                summary += "समग्र स्थितियां अनुकूल दिखती हैं। "
            else:
                summary += f"{alert_count} अलर्ट हैं जिन पर ध्यान देने की आवश्यकता है। "
        else:  # Marathi
            summary = f"सध्याच्या हवामान, माती आणि उपग्रह डेटावर आधारित, {state} मधील {crop} साठी अंदाजे उत्पादन {predicted} टन/हेक्टर आहे। "
            summary += f"या अंदाजात आमचा विश्वास {confidence}% आहे। "
            if risk_level in ["low", "moderate"]:
                summary += "एकंदर परिस्थिती अनुकूल दिसत आहे। "
            else:
                summary += f"{alert_count} सूचना आहेत ज्यांवर लक्ष देणे आवश्यक आहे। "
        
        return summary
    
    def _format_weather_card(self, weather: Dict, language: str, t: Dict) -> Dict[str, Any]:
        """Format weather data for display card."""
        current = weather.get("current", {})
        units = t.get("units", {})
        
        return {
            "title": t.get("weather_summary", "Weather Summary"),
            "temperature": {
                "value": current.get("temperature", 25),
                "unit": units.get("temperature", "°C"),
                "display": f"{current.get('temperature', 25)}{units.get('temperature', '°C')}"
            },
            "humidity": {
                "value": current.get("humidity", 60),
                "unit": units.get("humidity", "%"),
                "display": f"{current.get('humidity', 60)}{units.get('humidity', '%')}"
            },
            "rainfall_24h": {
                "value": weather.get("rainfall", {}).get("last_24h", 0),
                "unit": units.get("rainfall", "mm"),
                "display": f"{weather.get('rainfall', {}).get('last_24h', 0)}{units.get('rainfall', 'mm')}"
            },
            "description": current.get("description", "Clear"),
            "icon": self._get_weather_icon(current.get("description", "clear"))
        }
    
    def _format_soil_card(self, soil: Dict, language: str, t: Dict) -> Dict[str, Any]:
        """Format soil data for display card."""
        return {
            "title": t.get("soil_summary", "Soil Conditions"),
            "type": soil.get("soil_type", "Unknown"),
            "moisture": {
                "value": soil.get("moisture", {}).get("current", 50),
                "status": soil.get("moisture", {}).get("status", "optimal"),
                "display": f"{soil.get('moisture', {}).get('current', 50)}%"
            },
            "ph": {
                "value": soil.get("ph", {}).get("current", 7.0),
                "status": soil.get("ph", {}).get("status", "optimal"),
                "display": str(soil.get("ph", {}).get("current", 7.0))
            },
            "health_score": soil.get("health_score", 70),
            "npk_summary": self._format_npk_summary(soil.get("npk", {}))
        }
    
    def _format_npk_summary(self, npk: Dict) -> Dict[str, str]:
        """Format NPK summary."""
        return {
            "nitrogen": npk.get("nitrogen", {}).get("status", "adequate"),
            "phosphorus": npk.get("phosphorus", {}).get("status", "adequate"),
            "potassium": npk.get("potassium", {}).get("status", "adequate")
        }
    
    def _format_crop_health_card(self, satellite: Dict, language: str, t: Dict) -> Dict[str, Any]:
        """Format crop health data for display card."""
        return {
            "title": t.get("crop_health", "Crop Health"),
            "ndvi": {
                "value": satellite.get("ndvi", {}).get("current", 0.5),
                "interpretation": satellite.get("ndvi", {}).get("interpretation", "Moderate"),
                "status": satellite.get("ndvi", {}).get("status", "optimal")
            },
            "health_score": satellite.get("health_score", 70),
            "health_status": satellite.get("health_status", "good"),
            "growth_stage": satellite.get("growth_stage", {}).get("current_stage", "Active Growth"),
            "stress_detected": satellite.get("stress_analysis", {}).get("stress_detected", False),
            "coverage": satellite.get("coverage", {})
        }
    
    def _format_prediction_details(self, prediction: Dict, language: str) -> Dict[str, Any]:
        """Format prediction details."""
        yield_pred = prediction.get("yield_prediction", {})
        
        return {
            "yield": {
                "predicted": yield_pred.get("predicted", 0),
                "unit": yield_pred.get("unit", "tonnes/ha"),
                "range": {
                    "lower": yield_pred.get("confidence_interval", {}).get("lower", 0),
                    "upper": yield_pred.get("confidence_interval", {}).get("upper", 0)
                },
                "vs_average": yield_pred.get("comparison_to_average", 0)
            },
            "production": prediction.get("production_forecast", {}),
            "risk": prediction.get("risk_assessment", {}),
            "outlook": prediction.get("outlook", ""),
            "factor_scores": prediction.get("factor_scores", {})
        }
    
    def _format_alerts(self, alerts: Dict, language: str) -> List[Dict]:
        """Format alerts for display."""
        formatted = []
        
        for alert in alerts.get("active_alerts", []):
            formatted.append({
                "type": alert.get("type"),
                "severity": alert.get("severity"),
                "title": alert.get("title"),
                "message": alert.get("message"),
                "action": alert.get("recommended_action"),
                "icon": self._get_alert_icon(alert.get("severity")),
                "color": self._get_alert_color(alert.get("severity"))
            })
        
        return formatted
    
    def _generate_charts_data(self, weather: Dict, soil: Dict, satellite: Dict, prediction: Dict) -> Dict[str, Any]:
        """Generate data for frontend charts."""
        
        # Yield gauge chart
        yield_pred = prediction.get("yield_prediction", {})
        
        # Factor breakdown pie chart
        factors = prediction.get("factor_scores", {})
        
        # Weather forecast line chart
        forecast = weather.get("forecast", [])
        
        return {
            "yield_gauge": {
                "type": "gauge",
                "value": yield_pred.get("predicted", 0),
                "min": 0,
                "max": yield_pred.get("maximum_potential", 5),
                "thresholds": [
                    {"value": yield_pred.get("historical_average", 2.5) * 0.8, "color": "#FF6B6B"},
                    {"value": yield_pred.get("historical_average", 2.5), "color": "#FFD93D"},
                    {"value": yield_pred.get("maximum_potential", 5), "color": "#6BCB77"}
                ]
            },
            "factor_scores": {
                "type": "radar",
                "labels": ["Weather", "Soil", "Crop Health", "Season"],
                "values": [
                    factors.get("weather_impact", 70),
                    factors.get("soil_health", 70),
                    factors.get("crop_condition", 70),
                    factors.get("seasonal_favorability", 70)
                ]
            },
            "weather_forecast": {
                "type": "line",
                "labels": [f.get("datetime", "")[:10] for f in forecast],
                "datasets": [
                    {
                        "label": "Temperature",
                        "data": [f.get("temperature", 25) for f in forecast]
                    },
                    {
                        "label": "Rain Probability",
                        "data": [f.get("rain_probability", 0) for f in forecast]
                    }
                ]
            },
            "soil_nutrients": {
                "type": "bar",
                "labels": ["Nitrogen", "Phosphorus", "Potassium"],
                "values": [
                    soil.get("npk", {}).get("nitrogen", {}).get("current", 200),
                    soil.get("npk", {}).get("phosphorus", {}).get("current", 30) * 5,  # Scale for visualization
                    soil.get("npk", {}).get("potassium", {}).get("current", 180)
                ]
            },
            "risk_breakdown": {
                "type": "doughnut",
                "labels": [f.get("factor") for f in prediction.get("risk_assessment", {}).get("factors", [])],
                "values": [1 for _ in prediction.get("risk_assessment", {}).get("factors", [])]
            }
        }
    
    def _format_recommendations(self, prediction: Dict, soil: Dict, alerts: Dict, language: str) -> List[Dict]:
        """Format actionable recommendations."""
        recommendations = []
        
        # From prediction agent
        for rec in prediction.get("recommendations", []):
            recommendations.append({
                "category": rec.get("category"),
                "priority": rec.get("priority"),
                "action": rec.get("action"),
                "impact": rec.get("expected_impact"),
                "icon": "📋"
            })
        
        # From soil agent
        for rec in soil.get("recommendations", []):
            recommendations.append({
                "category": rec.get("type", "").replace("_", " ").title(),
                "priority": rec.get("priority"),
                "action": rec.get("action"),
                "impact": rec.get("message"),
                "icon": "🌱"
            })
        
        return sorted(recommendations, key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "low"), 3))
    
    def _generate_irrigation_advice(self, weather: Dict, soil: Dict, crop: str, language: str) -> Dict[str, Any]:
        """Generate smart irrigation advice."""
        moisture = soil.get("moisture", {}).get("current", 50)
        status = soil.get("moisture", {}).get("status", "optimal")
        rainfall = weather.get("rainfall", {}).get("last_24h", 0)
        rain_forecast = any(f.get("rain_probability", 0) > 60 for f in weather.get("forecast", [])[:2])
        
        if status == "low" and not rain_forecast:
            advice = {
                "action": "irrigate",
                "urgency": "high",
                "message": {
                    "en": f"Irrigation recommended. Soil moisture is low ({moisture}%) and no rain expected.",
                    "hi": f"सिंचाई की सिफारिश। मिट्टी की नमी कम है ({moisture}%) और बारिश की उम्मीद नहीं है।",
                    "mr": f"सिंचनाची शिफारस. मातीची आर्द्रता कमी आहे ({moisture}%) आणि पावसाची अपेक्षा नाही."
                }.get(language, f"Irrigation recommended. Soil moisture is low ({moisture}%)"),
                "timing": "Early morning (6-8 AM) or evening (5-7 PM)",
                "amount": "25-30mm equivalent"
            }
        elif status == "high" or rainfall > 50:
            advice = {
                "action": "skip",
                "urgency": "low",
                "message": {
                    "en": f"No irrigation needed. Soil moisture adequate ({moisture}%) or recent rainfall.",
                    "hi": f"सिंचाई की जरूरत नहीं। मिट्टी की नमी पर्याप्त ({moisture}%) या हाल ही में बारिश।",
                    "mr": f"सिंचनाची गरज नाही. मातीची आर्द्रता पुरेशी ({moisture}%) किंवा अलीकडील पाऊस."
                }.get(language, f"No irrigation needed."),
                "timing": "N/A",
                "amount": "0mm"
            }
        elif rain_forecast:
            advice = {
                "action": "wait",
                "urgency": "medium",
                "message": {
                    "en": "Rain expected in next 24-48 hours. Wait before irrigating.",
                    "hi": "अगले 24-48 घंटों में बारिश की उम्मीद। सिंचाई से पहले प्रतीक्षा करें।",
                    "mr": "पुढील 24-48 तासांत पावसाची अपेक्षा. सिंचन करण्यापूर्वी प्रतीक्षा करा."
                }.get(language, "Rain expected. Wait before irrigating."),
                "timing": "After rain assessment",
                "amount": "To be determined"
            }
        else:
            advice = {
                "action": "monitor",
                "urgency": "low",
                "message": {
                    "en": f"Soil moisture is adequate ({moisture}%). Continue monitoring.",
                    "hi": f"मिट्टी की नमी पर्याप्त है ({moisture}%)। निगरानी जारी रखें।",
                    "mr": f"मातीची आर्द्रता पुरेशी आहे ({moisture}%). निरीक्षण सुरू ठेवा."
                }.get(language, f"Soil moisture adequate ({moisture}%)."),
                "timing": "Check again in 2-3 days",
                "amount": "N/A"
            }
        
        return advice
    
    def _get_weather_icon(self, description: str) -> str:
        """Get weather emoji icon."""
        description = description.lower()
        if "rain" in description:
            return "🌧️"
        elif "thunder" in description:
            return "⛈️"
        elif "cloud" in description:
            return "☁️"
        elif "sun" in description or "clear" in description:
            return "☀️"
        elif "hot" in description or "heat" in description:
            return "🌡️"
        return "🌤️"
    
    def _get_alert_icon(self, severity: str) -> str:
        """Get alert emoji icon."""
        icons = {
            "critical": "🚨",
            "high": "⚠️",
            "medium": "⚡",
            "low": "ℹ️"
        }
        return icons.get(severity, "📢")
    
    def _get_alert_color(self, severity: str) -> str:
        """Get alert color."""
        colors = {
            "critical": "#FF0000",
            "high": "#FF6600",
            "medium": "#FFCC00",
            "low": "#00CC00"
        }
        return colors.get(severity, "#888888")
