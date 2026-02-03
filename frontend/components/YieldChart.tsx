'use client';

import { useEffect, useRef } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    RadialLinearScale,
    Title,
    Tooltip,
    Legend,
    Filler,
} from 'chart.js';
import { Bar, Doughnut, Line } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    RadialLinearScale,
    Title,
    Tooltip,
    Legend,
    Filler
);

interface YieldChartProps {
    data?: any;
    crop: string;
}

export default function YieldChart({ data, crop }: YieldChartProps) {
    // Default data if no response yet
    const yieldData = {
        labels: ['2022', '2023', '2024', '2025', '2026 (Pred)'],
        datasets: [
            {
                label: 'Yield (tonnes/ha)',
                data: [2.5, 2.7, 2.9, 2.8, data?.yield_gauge?.value || 3.1],
                backgroundColor: [
                    'rgba(34, 197, 94, 0.7)',
                    'rgba(34, 197, 94, 0.7)',
                    'rgba(34, 197, 94, 0.7)',
                    'rgba(34, 197, 94, 0.7)',
                    'rgba(14, 165, 233, 0.7)',
                ],
                borderColor: [
                    'rgb(34, 197, 94)',
                    'rgb(34, 197, 94)',
                    'rgb(34, 197, 94)',
                    'rgb(34, 197, 94)',
                    'rgb(14, 165, 233)',
                ],
                borderWidth: 2,
                borderRadius: 8,
            },
        ],
    };

    const factorData = {
        labels: data?.factor_scores?.labels || ['Weather', 'Soil', 'Crop Health', 'Season'],
        datasets: [
            {
                label: 'Factor Score',
                data: data?.factor_scores?.values || [75, 68, 82, 70],
                backgroundColor: [
                    'rgba(14, 165, 233, 0.7)',
                    'rgba(139, 92, 246, 0.7)',
                    'rgba(34, 197, 94, 0.7)',
                    'rgba(245, 158, 11, 0.7)',
                ],
                borderWidth: 0,
            },
        ],
    };

    const forecastData = {
        labels: data?.weather_forecast?.labels || ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'],
        datasets: [
            {
                label: 'Temperature (°C)',
                data: data?.weather_forecast?.datasets?.[0]?.data || [28, 29, 27, 26, 28],
                borderColor: 'rgb(239, 68, 68)',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                fill: true,
                tension: 0.4,
            },
            {
                label: 'Rain Probability (%)',
                data: data?.weather_forecast?.datasets?.[1]?.data || [20, 30, 60, 70, 40],
                borderColor: 'rgb(59, 130, 246)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                fill: true,
                tension: 0.4,
            },
        ],
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom' as const,
                labels: {
                    usePointStyle: true,
                    padding: 20,
                },
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.05)',
                },
            },
            x: {
                grid: {
                    display: false,
                },
            },
        },
    };

    const doughnutOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom' as const,
                labels: {
                    usePointStyle: true,
                    padding: 15,
                    font: {
                        size: 11,
                    },
                },
            },
        },
        cutout: '60%',
    };

    return (
        <div className="bg-white rounded-2xl p-6 shadow-lg">
            <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <span>📈</span> Yield Analysis - {crop}
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Yield Trend Chart */}
                <div>
                    <h4 className="text-sm font-medium text-gray-500 mb-3">Historical & Predicted Yield</h4>
                    <div className="chart-container">
                        <Bar data={yieldData} options={chartOptions} />
                    </div>
                </div>

                {/* Factor Breakdown */}
                <div>
                    <h4 className="text-sm font-medium text-gray-500 mb-3">Factor Breakdown</h4>
                    <div className="chart-container">
                        <Doughnut data={factorData} options={doughnutOptions} />
                    </div>
                </div>
            </div>

            {/* Weather Forecast Line Chart */}
            <div className="mt-6">
                <h4 className="text-sm font-medium text-gray-500 mb-3">5-Day Weather Forecast</h4>
                <div className="chart-container">
                    <Line data={forecastData} options={chartOptions} />
                </div>
            </div>

            {/* Summary Stats */}
            <div className="mt-6 grid grid-cols-3 gap-4">
                <div className="bg-crop-50 rounded-xl p-4 text-center">
                    <div className="text-2xl font-bold text-crop-600">
                        {data?.yield_gauge?.value || '3.1'}
                    </div>
                    <div className="text-sm text-gray-500">Predicted Yield (t/ha)</div>
                </div>
                <div className="bg-sky-50 rounded-xl p-4 text-center">
                    <div className="text-2xl font-bold text-sky-600">
                        +{Math.round((data?.yield_gauge?.value || 3.1) / 2.8 * 100 - 100)}%
                    </div>
                    <div className="text-sm text-gray-500">vs Historical Avg</div>
                </div>
                <div className="bg-amber-50 rounded-xl p-4 text-center">
                    <div className="text-2xl font-bold text-amber-600">
                        {data?.yield_gauge?.max || '4.5'}
                    </div>
                    <div className="text-sm text-gray-500">Max Potential (t/ha)</div>
                </div>
            </div>
        </div>
    );
}
