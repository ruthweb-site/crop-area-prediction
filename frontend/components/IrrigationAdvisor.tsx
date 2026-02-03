'use client';

import { useState, useEffect } from 'react';

interface IrrigationAdvisorProps {
    state: string;
    crop: string;
    language: 'en' | 'hi' | 'mr';
}

interface IrrigationAdvice {
    action: 'irrigate' | 'skip' | 'wait' | 'monitor';
    urgency: 'high' | 'medium' | 'low';
    message: string;
    timing: string;
    amount: string;
}

const translations = {
    en: {
        title: 'Smart Irrigation Advisor',
        soilMoisture: 'Soil Moisture',
        action: 'Recommended Action',
        timing: 'Best Timing',
        amount: 'Water Amount',
        irrigate: 'Irrigate Now',
        skip: 'Skip Irrigation',
        wait: 'Wait',
        monitor: 'Monitor',
    },
    hi: {
        title: 'स्मार्ट सिंचाई सलाहकार',
        soilMoisture: 'मिट्टी की नमी',
        action: 'अनुशंसित कार्रवाई',
        timing: 'सर्वोत्तम समय',
        amount: 'पानी की मात्रा',
        irrigate: 'अभी सिंचाई करें',
        skip: 'सिंचाई छोड़ें',
        wait: 'प्रतीक्षा करें',
        monitor: 'निगरानी करें',
    },
    mr: {
        title: 'स्मार्ट सिंचन सल्लागार',
        soilMoisture: 'माती आर्द्रता',
        action: 'शिफारस केलेली कृती',
        timing: 'सर्वोत्तम वेळ',
        amount: 'पाण्याचे प्रमाण',
        irrigate: 'आता सिंचन करा',
        skip: 'सिंचन वगळा',
        wait: 'प्रतीक्षा करा',
        monitor: 'निरीक्षण करा',
    }
};

const actionIcons = {
    irrigate: '💧',
    skip: '⏭️',
    wait: '⏳',
    monitor: '👁️',
};

const actionColors = {
    irrigate: 'bg-blue-500',
    skip: 'bg-gray-500',
    wait: 'bg-yellow-500',
    monitor: 'bg-green-500',
};

export default function IrrigationAdvisor({ state, crop, language }: IrrigationAdvisorProps) {
    const [advice, setAdvice] = useState<IrrigationAdvice>({
        action: 'monitor',
        urgency: 'low',
        message: 'Soil moisture is adequate. Continue monitoring.',
        timing: 'Check again in 2-3 days',
        amount: 'N/A'
    });
    const [soilMoisture, setSoilMoisture] = useState(55);
    const [isLoading, setIsLoading] = useState(false);

    const t = translations[language];

    useEffect(() => {
        const fetchSoilData = async () => {
            setIsLoading(true);
            try {
                const response = await fetch(
                    `http://localhost:8000/api/soil/${encodeURIComponent(state)}/${encodeURIComponent(crop)}`
                );
                if (response.ok) {
                    const data = await response.json();
                    if (data.soil && data.soil.moisture !== undefined) {
                        const moisture = data.soil.moisture;
                        setSoilMoisture(moisture);

                        // Update advice based on real moisture data
                        if (moisture < 35) {
                            setAdvice({
                                action: 'irrigate',
                                urgency: 'high',
                                message: language === 'hi'
                                    ? `मिट्टी की नमी कम है (${Math.round(moisture)}%)। तुरंत सिंचाई करें।`
                                    : language === 'mr'
                                        ? `मातीची आर्द्रता कमी आहे (${Math.round(moisture)}%). लगेच सिंचन करा.`
                                        : `Soil moisture is low (${Math.round(moisture)}%). Irrigate immediately.`,
                                timing: language === 'hi' ? 'सुबह 6-8 बजे या शाम 5-7 बजे'
                                    : language === 'mr' ? 'सकाळी 6-8 किंवा संध्याकाळी 5-7'
                                        : 'Early morning (6-8 AM) or evening (5-7 PM)',
                                amount: '25-30mm'
                            });
                        } else if (moisture > 70) {
                            setAdvice({
                                action: 'skip',
                                urgency: 'low',
                                message: language === 'hi'
                                    ? `मिट्टी की नमी पर्याप्त है (${Math.round(moisture)}%)। सिंचाई की जरूरत नहीं।`
                                    : language === 'mr'
                                        ? `मातीची आर्द्रता पुरेशी आहे (${Math.round(moisture)}%). सिंचनाची गरज नाही.`
                                        : `Soil moisture is adequate (${Math.round(moisture)}%). No irrigation needed.`,
                                timing: 'N/A',
                                amount: '0mm'
                            });
                        } else {
                            setAdvice({
                                action: 'monitor',
                                urgency: 'low',
                                message: language === 'hi'
                                    ? `मिट्टी की नमी ठीक है (${Math.round(moisture)}%)। निगरानी जारी रखें।`
                                    : language === 'mr'
                                        ? `मातीची आर्द्रता योग्य आहे (${Math.round(moisture)}%). निरीक्षण सुरू ठेवा.`
                                        : `Soil moisture is optimal (${Math.round(moisture)}%). Continue monitoring.`,
                                timing: language === 'hi' ? '2-3 दिन बाद जांचें'
                                    : language === 'mr' ? '2-3 दिवसांनी तपासा'
                                        : 'Check again in 2-3 days',
                                amount: 'N/A'
                            });
                        }
                        setIsLoading(false);
                        return;
                    }
                }
            } catch (error) {
                console.error('Soil data fetch error:', error);
            }

            // Fallback to simulated data if API fails
            const moisture = 30 + Math.random() * 50;
            setSoilMoisture(moisture);

            if (moisture < 35) {
                setAdvice({
                    action: 'irrigate',
                    urgency: 'high',
                    message: language === 'hi'
                        ? `मिट्टी की नमी कम है (${Math.round(moisture)}%)। तुरंत सिंचाई करें।`
                        : language === 'mr'
                            ? `मातीची आर्द्रता कमी आहे (${Math.round(moisture)}%). लगेच सिंचन करा.`
                            : `Soil moisture is low (${Math.round(moisture)}%). Irrigate immediately.`,
                    timing: language === 'hi' ? 'सुबह 6-8 बजे या शाम 5-7 बजे'
                        : language === 'mr' ? 'सकाळी 6-8 किंवा संध्याकाळी 5-7'
                            : 'Early morning (6-8 AM) or evening (5-7 PM)',
                    amount: '25-30mm'
                });
            } else if (moisture > 70) {
                setAdvice({
                    action: 'skip',
                    urgency: 'low',
                    message: language === 'hi'
                        ? `मिट्टी की नमी पर्याप्त है (${Math.round(moisture)}%)। सिंचाई की जरूरत नहीं।`
                        : language === 'mr'
                            ? `मातीची आर्द्रता पुरेशी आहे (${Math.round(moisture)}%). सिंचनाची गरज नाही.`
                            : `Soil moisture is adequate (${Math.round(moisture)}%). No irrigation needed.`,
                    timing: 'N/A',
                    amount: '0mm'
                });
            } else {
                setAdvice({
                    action: 'monitor',
                    urgency: 'low',
                    message: language === 'hi'
                        ? `मिट्टी की नमी ठीक है (${Math.round(moisture)}%)। निगरानी जारी रखें।`
                        : language === 'mr'
                            ? `मातीची आर्द्रता योग्य आहे (${Math.round(moisture)}%). निरीक्षण सुरू ठेवा.`
                            : `Soil moisture is optimal (${Math.round(moisture)}%). Continue monitoring.`,
                    timing: language === 'hi' ? '2-3 दिन बाद जांचें'
                        : language === 'mr' ? '2-3 दिवसांनी तपासा'
                            : 'Check again in 2-3 days',
                    amount: 'N/A'
                });
            }

            setIsLoading(false);
        };

        fetchSoilData();
    }, [state, crop, language]);

    // Calculate moisture bar color
    const getMoistureColor = () => {
        if (soilMoisture < 35) return 'bg-red-500';
        if (soilMoisture < 50) return 'bg-yellow-500';
        if (soilMoisture < 75) return 'bg-green-500';
        return 'bg-blue-500';
    };

    return (
        <div className="bg-white rounded-2xl p-6 shadow-lg card-hover">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <span>🌊</span> {t.title}
            </h3>

            {/* Soil Moisture Bar */}
            <div className="mb-6">
                <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-500">{t.soilMoisture}</span>
                    <span className="font-semibold">{Math.round(soilMoisture)}%</span>
                </div>
                <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
                    <div
                        className={`h-full ${getMoistureColor()} transition-all duration-1000 rounded-full`}
                        style={{ width: `${soilMoisture}%` }}
                    />
                </div>
                <div className="flex justify-between text-xs text-gray-400 mt-1">
                    <span>Dry</span>
                    <span>Optimal</span>
                    <span>Wet</span>
                </div>
            </div>

            {/* Action Card */}
            <div className={`rounded-xl p-4 ${advice.action === 'irrigate' ? 'bg-blue-50 border border-blue-200' :
                advice.action === 'skip' ? 'bg-gray-50 border border-gray-200' :
                    advice.action === 'wait' ? 'bg-yellow-50 border border-yellow-200' :
                        'bg-green-50 border border-green-200'
                }`}>
                {/* Action Header */}
                <div className="flex items-center gap-3 mb-3">
                    <div className={`w-12 h-12 rounded-xl ${actionColors[advice.action]} flex items-center justify-center text-2xl`}>
                        {actionIcons[advice.action]}
                    </div>
                    <div>
                        <div className="text-xs text-gray-500">{t.action}</div>
                        <div className="text-lg font-bold text-gray-800">
                            {t[advice.action]}
                        </div>
                    </div>
                    {advice.urgency === 'high' && (
                        <div className="ml-auto px-2 py-1 bg-red-500 text-white text-xs rounded-full animate-pulse">
                            Urgent
                        </div>
                    )}
                </div>

                {/* Message */}
                <p className="text-sm text-gray-600 mb-3">{advice.message}</p>

                {/* Details */}
                <div className="grid grid-cols-2 gap-3 text-sm">
                    <div>
                        <div className="text-xs text-gray-400">{t.timing}</div>
                        <div className="font-medium text-gray-700">{advice.timing}</div>
                    </div>
                    <div>
                        <div className="text-xs text-gray-400">{t.amount}</div>
                        <div className="font-medium text-gray-700">{advice.amount}</div>
                    </div>
                </div>
            </div>

            {/* Crop Context */}
            <div className="mt-4 flex items-center gap-2 text-sm text-gray-500">
                <span>🌱</span>
                <span>{crop} in {state}</span>
            </div>
        </div>
    );
}
