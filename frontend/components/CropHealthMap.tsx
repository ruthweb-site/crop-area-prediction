'use client';

import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';

// Dynamic import to avoid SSR issues with Leaflet
const MapContainer = dynamic(
    () => import('react-leaflet').then((mod) => mod.MapContainer),
    { ssr: false }
);
const TileLayer = dynamic(
    () => import('react-leaflet').then((mod) => mod.TileLayer),
    { ssr: false }
);
const Circle = dynamic(
    () => import('react-leaflet').then((mod) => mod.Circle),
    { ssr: false }
);
const Popup = dynamic(
    () => import('react-leaflet').then((mod) => mod.Popup),
    { ssr: false }
);

interface CropHealthMapProps {
    state: string;
    healthScore: number;
}

// State coordinates
const stateCoordinates: Record<string, [number, number]> = {
    'Maharashtra': [19.7515, 75.7139],
    'Punjab': [31.1471, 75.3412],
    'Uttar Pradesh': [26.8467, 80.9462],
    'Madhya Pradesh': [22.9734, 78.6569],
    'Karnataka': [15.3173, 75.7139],
    'Gujarat': [22.2587, 71.1924],
    'Rajasthan': [27.0238, 74.2179],
    'Tamil Nadu': [11.1271, 78.6569],
    'Andhra Pradesh': [15.9129, 79.7400],
    'West Bengal': [22.9868, 87.8550],
};

// Generate mock health data for districts
const generateDistrictData = (state: string, baseHealth: number) => {
    const districtCounts: Record<string, number> = {
        'Maharashtra': 8,
        'Punjab': 6,
        'Uttar Pradesh': 10,
        'Madhya Pradesh': 8,
        'Karnataka': 6,
        'Gujarat': 6,
        'Rajasthan': 7,
        'Tamil Nadu': 6,
        'Andhra Pradesh': 6,
        'West Bengal': 5,
    };

    const count = districtCounts[state] || 5;
    const center = stateCoordinates[state] || [20.5937, 78.9629];

    const districts = [];
    for (let i = 0; i < count; i++) {
        const latOffset = (Math.random() - 0.5) * 4;
        const lonOffset = (Math.random() - 0.5) * 4;
        const health = Math.max(30, Math.min(100, baseHealth + (Math.random() - 0.5) * 40));

        districts.push({
            id: i,
            name: `District ${i + 1}`,
            position: [center[0] + latOffset, center[1] + lonOffset] as [number, number],
            health: Math.round(health),
            area: Math.round(50000 + Math.random() * 100000),
        });
    }

    return districts;
};

const getHealthColor = (health: number): string => {
    if (health >= 80) return '#22c55e'; // Green
    if (health >= 60) return '#84cc16'; // Lime
    if (health >= 40) return '#eab308'; // Yellow
    if (health >= 20) return '#f97316'; // Orange
    return '#ef4444'; // Red
};

export default function CropHealthMap({ state, healthScore }: CropHealthMapProps) {
    const [isClient, setIsClient] = useState(false);
    const [districts, setDistricts] = useState<any[]>([]);

    useEffect(() => {
        setIsClient(true);
        setDistricts(generateDistrictData(state, healthScore));
    }, [state, healthScore]);

    const center = stateCoordinates[state] || [20.5937, 78.9629];

    if (!isClient) {
        return (
            <div className="bg-white rounded-2xl p-6 shadow-lg">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                    <span>🗺️</span> Crop Health Map
                </h3>
                <div className="h-80 bg-gray-100 rounded-xl flex items-center justify-center">
                    <div className="text-gray-400">Loading map...</div>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-2xl p-6 shadow-lg">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold flex items-center gap-2">
                    <span>🗺️</span> Crop Health Map - {state}
                </h3>

                {/* Legend */}
                <div className="flex items-center gap-4 text-sm">
                    <div className="flex items-center gap-1">
                        <div className="w-3 h-3 rounded-full bg-green-500" />
                        <span className="text-gray-500">Excellent</span>
                    </div>
                    <div className="flex items-center gap-1">
                        <div className="w-3 h-3 rounded-full bg-yellow-500" />
                        <span className="text-gray-500">Moderate</span>
                    </div>
                    <div className="flex items-center gap-1">
                        <div className="w-3 h-3 rounded-full bg-red-500" />
                        <span className="text-gray-500">Poor</span>
                    </div>
                </div>
            </div>

            <div className="map-container rounded-xl overflow-hidden">
                <MapContainer
                    center={center}
                    zoom={6}
                    style={{ height: '100%', width: '100%' }}
                    scrollWheelZoom={false}
                >
                    <TileLayer
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />

                    {districts.map((district) => (
                        <Circle
                            key={district.id}
                            center={district.position}
                            radius={30000 + district.area / 10}
                            pathOptions={{
                                color: getHealthColor(district.health),
                                fillColor: getHealthColor(district.health),
                                fillOpacity: 0.5,
                                weight: 2,
                            }}
                        >
                            <Popup>
                                <div className="text-sm">
                                    <div className="font-semibold mb-1">{district.name}</div>
                                    <div className="flex items-center gap-2">
                                        <span>Health Score:</span>
                                        <span
                                            className="font-bold"
                                            style={{ color: getHealthColor(district.health) }}
                                        >
                                            {district.health}%
                                        </span>
                                    </div>
                                    <div className="text-gray-500 text-xs mt-1">
                                        Area: {(district.area / 1000).toFixed(0)}k hectares
                                    </div>
                                </div>
                            </Popup>
                        </Circle>
                    ))}
                </MapContainer>
            </div>

            {/* Summary */}
            <div className="mt-4 grid grid-cols-3 gap-4 text-center">
                <div className="bg-green-50 rounded-lg p-3">
                    <div className="text-2xl font-bold text-green-600">
                        {districts.filter(d => d.health >= 70).length}
                    </div>
                    <div className="text-xs text-gray-500">Healthy Areas</div>
                </div>
                <div className="bg-yellow-50 rounded-lg p-3">
                    <div className="text-2xl font-bold text-yellow-600">
                        {districts.filter(d => d.health >= 40 && d.health < 70).length}
                    </div>
                    <div className="text-xs text-gray-500">Moderate Areas</div>
                </div>
                <div className="bg-red-50 rounded-lg p-3">
                    <div className="text-2xl font-bold text-red-600">
                        {districts.filter(d => d.health < 40).length}
                    </div>
                    <div className="text-xs text-gray-500">Stressed Areas</div>
                </div>
            </div>
        </div>
    );
}
