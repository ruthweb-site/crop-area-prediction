'use client';

interface RiskIndicatorProps {
    riskScore: number;
    riskLevel: string;
    factors: Array<{
        factor: string;
        impact: string;
        description: string;
    }>;
    language: 'en' | 'hi' | 'mr';
}

const translations = {
    en: {
        riskAssessment: 'Risk Assessment',
        overallRisk: 'Overall Risk',
        low: 'Low',
        moderate: 'Moderate',
        elevated: 'Elevated',
        high: 'High',
        critical: 'Critical',
        riskFactors: 'Risk Factors',
    },
    hi: {
        riskAssessment: 'जोखिम आकलन',
        overallRisk: 'समग्र जोखिम',
        low: 'कम',
        moderate: 'मध्यम',
        elevated: 'बढ़ा हुआ',
        high: 'उच्च',
        critical: 'गंभीर',
        riskFactors: 'जोखिम कारक',
    },
    mr: {
        riskAssessment: 'जोखीम मूल्यांकन',
        overallRisk: 'एकूण जोखीम',
        low: 'कमी',
        moderate: 'मध्यम',
        elevated: 'वाढलेली',
        high: 'उच्च',
        critical: 'गंभीर',
        riskFactors: 'जोखीम घटक',
    }
};

export default function RiskIndicator({ riskScore, riskLevel, factors, language }: RiskIndicatorProps) {
    const t = translations[language];

    const getRiskColor = (level: string) => {
        switch (level.toLowerCase()) {
            case 'low': return 'from-green-400 to-green-600';
            case 'moderate': return 'from-yellow-400 to-yellow-600';
            case 'elevated': return 'from-orange-400 to-orange-600';
            case 'high': return 'from-red-400 to-red-600';
            case 'critical': return 'from-red-600 to-red-800';
            default: return 'from-gray-400 to-gray-600';
        }
    };

    const getRiskBgColor = (level: string) => {
        switch (level.toLowerCase()) {
            case 'low': return 'bg-green-100';
            case 'moderate': return 'bg-yellow-100';
            case 'elevated': return 'bg-orange-100';
            case 'high': return 'bg-red-100';
            case 'critical': return 'bg-red-200';
            default: return 'bg-gray-100';
        }
    };

    const getRiskTextColor = (level: string) => {
        switch (level.toLowerCase()) {
            case 'low': return 'text-green-700';
            case 'moderate': return 'text-yellow-700';
            case 'elevated': return 'text-orange-700';
            case 'high': return 'text-red-700';
            case 'critical': return 'text-red-800';
            default: return 'text-gray-700';
        }
    };

    const getLocalizedLevel = (level: string) => {
        const key = level.toLowerCase() as keyof typeof t;
        return t[key] || level;
    };

    const getImpactColor = (impact: string) => {
        switch (impact.toLowerCase()) {
            case 'high': return 'bg-red-100 text-red-700';
            case 'medium': return 'bg-yellow-100 text-yellow-700';
            case 'low': return 'bg-green-100 text-green-700';
            default: return 'bg-gray-100 text-gray-700';
        }
    };

    // Calculate gauge rotation (0-180 degrees for 0-100 score)
    const gaugeRotation = (riskScore / 100) * 180;

    return (
        <div className="bg-white rounded-2xl p-6 shadow-lg">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <span>⚠️</span> {t.riskAssessment}
            </h3>

            {/* Gauge */}
            <div className="relative flex justify-center mb-6">
                <div className="relative w-40 h-20 overflow-hidden">
                    {/* Background arc */}
                    <div
                        className="absolute w-40 h-40 rounded-full"
                        style={{
                            background: 'conic-gradient(from 180deg, #22c55e 0deg, #22c55e 60deg, #eab308 60deg, #eab308 120deg, #f97316 120deg, #f97316 150deg, #ef4444 150deg, #ef4444 180deg, transparent 180deg)',
                            clipPath: 'polygon(0 50%, 100% 50%, 100% 100%, 0 100%)',
                            transform: 'rotate(180deg)',
                        }}
                    />

                    {/* Center cover */}
                    <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-28 h-14 bg-white rounded-t-full" />

                    {/* Needle */}
                    <div
                        className="absolute bottom-0 left-1/2 origin-bottom h-16 w-1 bg-gray-800 rounded-full transition-transform duration-1000"
                        style={{
                            transform: `translateX(-50%) rotate(${gaugeRotation - 90}deg)`,
                        }}
                    />

                    {/* Center dot */}
                    <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-1/2 w-4 h-4 bg-gray-800 rounded-full" />
                </div>
            </div>

            {/* Risk Score & Level */}
            <div className="text-center mb-6">
                <div className="text-4xl font-bold text-gray-800 mb-1">
                    {Math.round(riskScore)}
                    <span className="text-lg text-gray-400">/100</span>
                </div>
                <div className={`inline-block px-4 py-1 rounded-full ${getRiskBgColor(riskLevel)} ${getRiskTextColor(riskLevel)} font-medium`}>
                    {getLocalizedLevel(riskLevel)}
                </div>
            </div>

            {/* Risk Factors */}
            {factors.length > 0 && (
                <div>
                    <h4 className="text-sm font-medium text-gray-500 mb-3">{t.riskFactors}</h4>
                    <div className="space-y-2">
                        {factors.slice(0, 4).map((factor, i) => (
                            <div key={i} className="flex items-center gap-2 p-2 bg-gray-50 rounded-lg">
                                <span className={`px-2 py-0.5 rounded text-xs font-medium ${getImpactColor(factor.impact)}`}>
                                    {factor.impact}
                                </span>
                                <div className="flex-1">
                                    <div className="text-sm font-medium text-gray-700">{factor.factor}</div>
                                    <div className="text-xs text-gray-500">{factor.description}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Risk scale legend */}
            <div className="mt-4 flex justify-between text-xs text-gray-400">
                <span>0 (Low)</span>
                <span>50 (Moderate)</span>
                <span>100 (Critical)</span>
            </div>
        </div>
    );
}
