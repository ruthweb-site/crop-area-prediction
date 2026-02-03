'use client';

import { useState, useEffect } from 'react';
import ChatInterface from '@/components/ChatInterface';
import WeatherWidget from '@/components/WeatherWidget';
import YieldChart from '@/components/YieldChart';
import RiskIndicator from '@/components/RiskIndicator';
import IrrigationAdvisor from '@/components/IrrigationAdvisor';
import LanguageSelector from '@/components/LanguageSelector';
import CropHealthMap from '@/components/CropHealthMap';

// Translations
const translations = {
    en: {
        title: 'CropAgent',
        subtitle: 'AI-Powered Crop Prediction for Indian Farmers',
        welcome: 'Welcome! Ask me about crop yields, weather conditions, or farming advice.',
        dashboard: 'Dashboard',
        chat: 'Chat',
        weather: 'Weather',
        soilHealth: 'Soil Health',
        cropHealth: 'Crop Health',
        alerts: 'Alerts',
        predictions: 'Predictions',
        irrigation: 'Irrigation Advisor',
        selectState: 'Select State',
        selectCrop: 'Select Crop',
        askQuestion: 'Ask a question about your crops...',
    },
    hi: {
        title: 'क्रॉप एजेंट',
        subtitle: 'भारतीय किसानों के लिए AI-आधारित फसल भविष्यवाणी',
        welcome: 'स्वागत है! फसल उपज, मौसम की स्थिति या खेती की सलाह के बारे में पूछें।',
        dashboard: 'डैशबोर्ड',
        chat: 'चैट',
        weather: 'मौसम',
        soilHealth: 'मिट्टी स्वास्थ्य',
        cropHealth: 'फसल स्वास्थ्य',
        alerts: 'अलर्ट',
        predictions: 'भविष्यवाणी',
        irrigation: 'सिंचाई सलाहकार',
        selectState: 'राज्य चुनें',
        selectCrop: 'फसल चुनें',
        askQuestion: 'अपनी फसलों के बारे में प्रश्न पूछें...',
    },
    mr: {
        title: 'क्रॉप एजंट',
        subtitle: 'भारतीय शेतकऱ्यांसाठी AI-आधारित पीक अंदाज',
        welcome: 'स्वागत! पीक उत्पादन, हवामान किंवा शेती सल्ल्याबद्दल विचारा.',
        dashboard: 'डॅशबोर्ड',
        chat: 'चॅट',
        weather: 'हवामान',
        soilHealth: 'माती आरोग्य',
        cropHealth: 'पीक आरोग्य',
        alerts: 'सूचना',
        predictions: 'अंदाज',
        irrigation: 'सिंचन सल्लागार',
        selectState: 'राज्य निवडा',
        selectCrop: 'पीक निवडा',
        askQuestion: 'तुमच्या पिकांबद्दल प्रश्न विचारा...',
    }
};

// Indian states data
const states = [
    { name: 'Maharashtra', crops: ['Rice', 'Cotton', 'Sugarcane', 'Soybean'] },
    { name: 'Tamil Nadu', crops: ['Rice', 'Sugarcane', 'Cotton', 'Groundnut'] },
    { name: 'Uttar Pradesh', crops: ['Wheat', 'Rice', 'Sugarcane', 'Potato'] },
];

export default function Home() {
    const [language, setLanguage] = useState<'en' | 'hi' | 'mr'>('en');
    const [selectedState, setSelectedState] = useState('Maharashtra');
    const [selectedCrop, setSelectedCrop] = useState('Rice');
    const [activeTab, setActiveTab] = useState('dashboard');
    const [chatResponse, setChatResponse] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(false);

    const t = translations[language];
    const currentState = states.find(s => s.name === selectedState);
    const availableCrops = currentState?.crops || ['Rice'];

    // Update crop when state changes
    useEffect(() => {
        if (!availableCrops.includes(selectedCrop)) {
            setSelectedCrop(availableCrops[0]);
        }
    }, [selectedState, availableCrops, selectedCrop]);

    // Auto-fetch dashboard data when state or crop changes
    useEffect(() => {
        const fetchDashboardData = async () => {
            setIsLoading(true);
            try {
                // Fetch prediction data for the selected state and crop
                const response = await fetch('http://localhost:8000/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        query: `What is the yield prediction for ${selectedCrop} in ${selectedState}?`,
                        language,
                        state: selectedState,
                        crop: selectedCrop
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    setChatResponse(data);
                }
            } catch (error) {
                console.error('Dashboard data fetch error:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchDashboardData();
    }, [selectedState, selectedCrop, language]);

    const handleChatSubmit = async (query: string) => {
        setIsLoading(true);
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query,
                    language,
                    state: selectedState,
                    crop: selectedCrop
                })
            });

            if (response.ok) {
                const data = await response.json();
                setChatResponse(data);
            }
        } catch (error) {
            console.error('Chat error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <main className="min-h-screen">
            {/* Header */}
            <header className="glass sticky top-0 z-50 px-4 py-3 md:px-8">
                <div className="max-w-7xl mx-auto flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-crop-500 to-crop-600 flex items-center justify-center">
                            <span className="text-2xl">🌾</span>
                        </div>
                        <div>
                            <h1 className="text-xl font-bold gradient-text">{t.title}</h1>
                            <p className="text-xs text-gray-500 hidden md:block">{t.subtitle}</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-4">
                        {/* State/Crop Selectors */}
                        <div className="hidden md:flex items-center gap-2">
                            <select
                                value={selectedState}
                                onChange={(e) => setSelectedState(e.target.value)}
                                className="px-3 py-2 rounded-lg border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-crop-500"
                            >
                                {states.map(state => (
                                    <option key={state.name} value={state.name}>{state.name}</option>
                                ))}
                            </select>

                            <select
                                value={selectedCrop}
                                onChange={(e) => setSelectedCrop(e.target.value)}
                                className="px-3 py-2 rounded-lg border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-crop-500"
                            >
                                {availableCrops.map(crop => (
                                    <option key={crop} value={crop}>{crop}</option>
                                ))}
                            </select>
                        </div>

                        <LanguageSelector language={language} onLanguageChange={setLanguage} />
                    </div>
                </div>
            </header>

            {/* Mobile State/Crop Selectors */}
            <div className="md:hidden px-4 py-2 flex gap-2">
                <select
                    value={selectedState}
                    onChange={(e) => setSelectedState(e.target.value)}
                    className="flex-1 px-3 py-2 rounded-lg border border-gray-200 text-sm"
                >
                    {states.map(state => (
                        <option key={state.name} value={state.name}>{state.name}</option>
                    ))}
                </select>

                <select
                    value={selectedCrop}
                    onChange={(e) => setSelectedCrop(e.target.value)}
                    className="flex-1 px-3 py-2 rounded-lg border border-gray-200 text-sm"
                >
                    {availableCrops.map(crop => (
                        <option key={crop} value={crop}>{crop}</option>
                    ))}
                </select>
            </div>

            {/* Navigation Tabs */}
            <nav className="px-4 md:px-8 py-2 border-b border-gray-100">
                <div className="max-w-7xl mx-auto flex gap-1 overflow-x-auto">
                    {['dashboard', 'chat'].map(tab => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab)}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${activeTab === tab
                                ? 'bg-crop-500 text-white'
                                : 'text-gray-600 hover:bg-gray-100'
                                }`}
                        >
                            {tab === 'dashboard' ? t.dashboard : t.chat}
                        </button>
                    ))}
                </div>
            </nav>

            {/* Main Content */}
            <div className="max-w-7xl mx-auto px-4 md:px-8 py-6">
                {activeTab === 'dashboard' ? (
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        {/* Left Column - Weather & Soil */}
                        <div className="space-y-6">
                            <WeatherWidget state={selectedState} language={language} />
                            <IrrigationAdvisor
                                state={selectedState}
                                crop={selectedCrop}
                                language={language}
                            />
                        </div>

                        {/* Middle Column - Main Content */}
                        <div className="lg:col-span-2 space-y-6">
                            {/* Quick Stats */}
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div className="stats-card">
                                    <div className="text-3xl mb-2">🌱</div>
                                    <div className="text-2xl font-bold text-crop-600">
                                        {chatResponse?.response?.prediction_details?.yield?.predicted || '2.8'}
                                    </div>
                                    <div className="text-sm text-gray-500">Tonnes/Ha</div>
                                </div>
                                <div className="stats-card">
                                    <div className="text-3xl mb-2">📊</div>
                                    <div className="text-2xl font-bold text-sky-600">
                                        {chatResponse?.response?.confidence?.score || '75'}%
                                    </div>
                                    <div className="text-sm text-gray-500">Confidence</div>
                                </div>
                                <div className="stats-card">
                                    <div className="text-3xl mb-2">🌡️</div>
                                    <div className="text-2xl font-bold text-orange-600">
                                        {chatResponse?.response?.weather_card?.temperature?.value || '28'}°C
                                    </div>
                                    <div className="text-sm text-gray-500">Temperature</div>
                                </div>
                                <div className="stats-card">
                                    <div className="text-3xl mb-2">💧</div>
                                    <div className="text-2xl font-bold text-blue-600">
                                        {chatResponse?.response?.soil_card?.moisture?.value || '55'}%
                                    </div>
                                    <div className="text-sm text-gray-500">Soil Moisture</div>
                                </div>
                            </div>

                            {/* Yield Chart */}
                            <YieldChart data={chatResponse?.response?.charts} crop={selectedCrop} />

                            {/* Risk & Recommendations */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <RiskIndicator
                                    riskScore={chatResponse?.raw_data?.prediction?.risk_assessment?.overall_risk_score || 25}
                                    riskLevel={chatResponse?.raw_data?.prediction?.risk_assessment?.risk_level || 'low'}
                                    factors={chatResponse?.raw_data?.prediction?.risk_assessment?.factors || []}
                                    language={language}
                                />

                                {/* Alerts Card */}
                                <div className="bg-white rounded-2xl p-6 shadow-lg">
                                    <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                                        <span>🔔</span> {t.alerts}
                                    </h3>
                                    <div className="space-y-3">
                                        {(chatResponse?.response?.alerts_formatted || []).length > 0 ? (
                                            chatResponse.response.alerts_formatted.slice(0, 3).map((alert: any, i: number) => (
                                                <div key={i} className={`p-3 rounded-lg ${alert.severity === 'critical' ? 'bg-red-50 border-l-4 border-red-500' :
                                                    alert.severity === 'high' ? 'bg-orange-50 border-l-4 border-orange-500' :
                                                        'bg-yellow-50 border-l-4 border-yellow-500'
                                                    }`}>
                                                    <div className="flex items-center gap-2 font-medium">
                                                        <span>{alert.icon}</span>
                                                        {alert.title}
                                                    </div>
                                                    <p className="text-sm text-gray-600 mt-1">{alert.message}</p>
                                                </div>
                                            ))
                                        ) : (
                                            <div className="text-center py-4 text-gray-400">
                                                <span className="text-4xl mb-2 block">✅</span>
                                                <p>No active alerts</p>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>

                            {/* Map */}
                            <CropHealthMap
                                state={selectedState}
                                healthScore={chatResponse?.raw_data?.satellite?.health_score || 75}
                            />
                        </div>
                    </div>
                ) : (
                    /* Chat Tab */
                    <ChatInterface
                        language={language}
                        state={selectedState}
                        crop={selectedCrop}
                        onSubmit={handleChatSubmit}
                        response={chatResponse}
                        isLoading={isLoading}
                        translations={t}
                    />
                )}
            </div>

            {/* Footer */}
            <footer className="mt-12 py-6 border-t border-gray-100">
                <div className="max-w-7xl mx-auto px-4 md:px-8 text-center text-sm text-gray-500">
                    <p>🌾 CropAgent - Empowering Indian Farmers with AI</p>
                    <p className="mt-1">Built with ❤️ for sustainable agriculture</p>
                </div>
            </footer>
        </main>
    );
}
