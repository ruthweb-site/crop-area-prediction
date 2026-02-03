'use client';

import { useState, useEffect } from 'react';

interface WeatherWidgetProps {
    state: string;
    language: 'en' | 'hi' | 'mr';
}

interface WeatherData {
    current: {
        temperature: number;
        humidity: number;
        description: string;
        wind_speed: number;
        clouds: number;
    };
    rainfall: {
        last_24h: number;
    };
    forecast: Array<{
        datetime: string;
        temperature: number;
        rain_probability: number;
        description: string;
    }>;
}

const defaultWeather: WeatherData = {
    current: {
        temperature: 28,
        humidity: 65,
        description: 'Partly Cloudy',
        wind_speed: 12,
        clouds: 40
    },
    rainfall: {
        last_24h: 5
    },
    forecast: [
        { datetime: '2026-02-04', temperature: 29, rain_probability: 30, description: 'Sunny' },
        { datetime: '2026-02-05', temperature: 27, rain_probability: 60, description: 'Light Rain' },
        { datetime: '2026-02-06', temperature: 26, rain_probability: 70, description: 'Moderate Rain' },
    ]
};

const weatherIcons: Record<string, string> = {
    'clear': '☀️',
    'sunny': '☀️',
    'clouds': '☁️',
    'cloudy': '☁️',
    'partly cloudy': '⛅',
    'overcast': '☁️',
    'rain': '🌧️',
    'light rain': '🌦️',
    'moderate rain': '🌧️',
    'heavy rain': '⛈️',
    'thunderstorm': '⛈️',
    'hot': '🌡️',
    'hot and sunny': '🌡️',
    'haze': '🌫️',
};

const getWeatherIcon = (description: string): string => {
    const desc = description.toLowerCase();
    for (const [key, icon] of Object.entries(weatherIcons)) {
        if (desc.includes(key)) return icon;
    }
    return '🌤️';
};

const translations = {
    en: {
        weather: 'Weather',
        temperature: 'Temperature',
        humidity: 'Humidity',
        wind: 'Wind',
        rainfall: 'Rainfall (24h)',
        forecast: 'Forecast',
        rainChance: 'Rain',
    },
    hi: {
        weather: 'मौसम',
        temperature: 'तापमान',
        humidity: 'आर्द्रता',
        wind: 'हवा',
        rainfall: 'वर्षा (24 घंटे)',
        forecast: 'पूर्वानुमान',
        rainChance: 'बारिश',
    },
    mr: {
        weather: 'हवामान',
        temperature: 'तापमान',
        humidity: 'आर्द्रता',
        wind: 'वारा',
        rainfall: 'पाऊस (24 तास)',
        forecast: 'अंदाज',
        rainChance: 'पाऊस',
    }
};

export default function WeatherWidget({ state, language }: WeatherWidgetProps) {
    const [weather, setWeather] = useState<WeatherData>(defaultWeather);
    const [isLoading, setIsLoading] = useState(false);
    const t = translations[language];

    useEffect(() => {
        const fetchWeather = async () => {
            setIsLoading(true);
            try {
                const response = await fetch(`http://localhost:8000/api/weather/${encodeURIComponent(state)}`);
                if (response.ok) {
                    const data = await response.json();
                    if (data.weather) {
                        setWeather(data.weather);
                    }
                }
            } catch (error) {
                console.error('Weather fetch error:', error);
                // Keep default weather data on error
            } finally {
                setIsLoading(false);
            }
        };

        fetchWeather();
    }, [state]);

    return (
        <div className="bg-gradient-to-br from-sky-500 to-sky-600 rounded-2xl p-6 text-white shadow-lg card-hover">
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="text-sm font-medium opacity-80">{t.weather}</h3>
                    <p className="text-lg font-semibold">{state}</p>
                </div>
                <div className="weather-icon">
                    {getWeatherIcon(weather.current.description)}
                </div>
            </div>

            {/* Main Temperature */}
            <div className="mb-6">
                <div className="text-5xl font-bold">
                    {Math.round(weather.current.temperature)}°
                </div>
                <p className="text-sm opacity-80 capitalize">{weather.current.description}</p>
            </div>

            {/* Weather Details */}
            <div className="grid grid-cols-3 gap-4 mb-6">
                <div className="text-center">
                    <div className="text-2xl mb-1">💧</div>
                    <div className="text-lg font-semibold">{Math.round(weather.current.humidity)}%</div>
                    <div className="text-xs opacity-70">{t.humidity}</div>
                </div>
                <div className="text-center">
                    <div className="text-2xl mb-1">💨</div>
                    <div className="text-lg font-semibold">{Math.round(weather.current.wind_speed)}</div>
                    <div className="text-xs opacity-70">{t.wind} km/h</div>
                </div>
                <div className="text-center">
                    <div className="text-2xl mb-1">🌧️</div>
                    <div className="text-lg font-semibold">{Math.round(weather.rainfall.last_24h)}</div>
                    <div className="text-xs opacity-70">mm</div>
                </div>
            </div>

            {/* Forecast */}
            <div>
                <h4 className="text-sm font-medium mb-3 opacity-80">{t.forecast}</h4>
                <div className="flex gap-2">
                    {weather.forecast.slice(0, 3).map((day, i) => (
                        <div key={i} className="flex-1 bg-white/20 rounded-lg p-2 text-center">
                            <div className="text-xs opacity-70">
                                {new Date(day.datetime).toLocaleDateString(language, { weekday: 'short' })}
                            </div>
                            <div className="text-lg my-1">{getWeatherIcon(day.description)}</div>
                            <div className="text-sm font-semibold">{Math.round(day.temperature)}°</div>
                            <div className="text-xs opacity-70">{day.rain_probability}%</div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
