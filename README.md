# 🌾 CropAgent - Agentic AI for Indian Farmers

An intelligent multi-agent system that predicts crop area, yield, and health using live data from weather, soil, and satellite sources.

![CropAgent Banner](https://via.placeholder.com/800x200/22c55e/ffffff?text=CropAgent+-+AI+for+Indian+Farmers)

## 🚀 Features

- **6 Specialized AI Agents** working together:
  - 🌦️ **Weather Agent** - Live weather data from OpenWeatherMap
  - 🌱 **Soil Agent** - Soil moisture, pH, and NPK analysis
  - 🛰️ **Satellite Agent** - NDVI-based crop health monitoring
  - 📊 **Prediction Agent** - ML-based yield forecasting
  - 🚨 **Alert Agent** - Drought, flood, and disease risk detection
  - 💬 **Response Agent** - Multilingual response formatting

- **Manager Agent** orchestrates all sub-agents automatically
- **Memory Layer** stores past predictions and learns over time
- **Multilingual Support** - Hindi, English, and Marathi
- **Interactive Dashboard** with charts, maps, and confidence scores
- **Climate Risk Forecasting** with 24-48 hour advance alerts
- **Smart Irrigation Advisor** based on real-time soil + weather data

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

## 🛠️ Installation

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional)
# Create a .env file with:
# OPENWEATHERMAP_API_KEY=your_api_key_here

# Run the server
python main.py
# Or use uvicorn:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🎯 Usage

### Example Query

Ask the chatbot:
> "Will rice yield be good in Maharashtra this season?"

The system will:
1. **Manager Agent** parses the query and assigns tasks
2. **Weather, Soil, and Satellite Agents** fetch data in parallel
3. **Prediction Agent** combines data to generate yield forecast
4. **Alert Agent** checks for any risks
5. **Response Agent** formats the answer in your preferred language

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Main chat endpoint for queries |
| `/api/weather/{state}` | GET | Get weather for a state |
| `/api/soil/{state}/{crop}` | GET | Get soil analysis |
| `/api/states` | GET | List supported states |
| `/api/crops/{state}` | GET | Get crops for a state |
| `/api/history` | GET | Get prediction history |
| `/api/stats` | GET | Get system statistics |
| `/health` | GET | Health check |

### Sample API Request

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Will rice yield be good in Maharashtra this season?",
    "language": "en",
    "state": "Maharashtra",
    "crop": "Rice"
  }'
```

## 🗂️ Project Structure

```
CropAgent/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Configuration
│   ├── requirements.txt        # Python dependencies
│   ├── agents/
│   │   ├── base_agent.py       # Base agent class
│   │   ├── manager_agent.py    # Orchestrator
│   │   ├── weather_agent.py    # Weather data
│   │   ├── soil_agent.py       # Soil data
│   │   ├── satellite_agent.py  # Satellite imagery
│   │   ├── prediction_agent.py # Yield prediction
│   │   ├── alert_agent.py      # Risk alerts
│   │   └── response_agent.py   # Response formatting
│   ├── memory/
│   │   └── memory.py           # Memory layer
│   └── data/
│       ├── indian_regions.py   # Region data
│       └── crop_data.py        # Crop information
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx            # Dashboard
│   │   ├── layout.tsx          # Root layout
│   │   └── globals.css         # Global styles
│   ├── components/
│   │   ├── ChatInterface.tsx
│   │   ├── WeatherWidget.tsx
│   │   ├── CropHealthMap.tsx
│   │   ├── YieldChart.tsx
│   │   ├── RiskIndicator.tsx
│   │   ├── IrrigationAdvisor.tsx
│   │   └── LanguageSelector.tsx
│   ├── locales/
│   │   ├── en.json
│   │   ├── hi.json
│   │   └── mr.json
│   ├── lib/
│   │   └── api.ts              # API client
│   └── package.json
│
└── README.md
```

## 🌐 Supported Regions

| State | Major Crops |
|-------|-------------|
| Maharashtra | Rice, Cotton, Sugarcane, Soybean |
| Punjab | Wheat, Rice, Cotton, Maize |
| Uttar Pradesh | Wheat, Rice, Sugarcane, Potato |
| Madhya Pradesh | Wheat, Soybean, Gram, Rice |
| Karnataka | Rice, Ragi, Sugarcane, Cotton |
| Gujarat | Cotton, Groundnut, Wheat, Rice |
| Rajasthan | Wheat, Bajra, Mustard, Gram |
| Tamil Nadu | Rice, Sugarcane, Cotton, Groundnut |
| Andhra Pradesh | Rice, Cotton, Chilli, Groundnut |
| West Bengal | Rice, Jute, Potato, Wheat |

## 🔧 Configuration

Create a `.env` file in the backend directory:

```env
OPENWEATHERMAP_API_KEY=your_api_key_here
DATABASE_PATH=cropagent.db
AGENT_TIMEOUT=30
MAX_RETRIES=3
```

## 🌟 Key Technologies

- **Backend**: Python, FastAPI, AsyncIO
- **Frontend**: Next.js 14, React, TypeScript
- **Charts**: Chart.js, react-chartjs-2
- **Maps**: Leaflet, react-leaflet
- **Styling**: TailwindCSS
- **Database**: SQLite (via aiosqlite)

## 📊 Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Query                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Manager Agent                            │
│           (Parses query, orchestrates agents)                │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Weather Agent │   │  Soil Agent   │   │Satellite Agent│
│   🌦️ Live     │   │   🌱 NPK      │   │   🛰️ NDVI    │
│   Weather     │   │   Analysis    │   │   Analysis    │
└───────────────┘   └───────────────┘   └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Prediction Agent                           │
│              (Combines data, generates forecast)             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Alert Agent                             │
│       (Detects drought, flood, disease risks)                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Response Agent                            │
│      (Formats multilingual response with charts)             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Dashboard/Chat                           │
│              (Visual results for farmer)                     │
└─────────────────────────────────────────────────────────────┘
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- OpenWeatherMap for weather data API
- Indian Agricultural Research databases
- Open-source satellite imagery references

---

Built with ❤️ for Indian Farmers 🌾
