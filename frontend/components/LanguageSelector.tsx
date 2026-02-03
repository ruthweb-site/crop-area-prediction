'use client';

interface LanguageSelectorProps {
    language: 'en' | 'hi' | 'mr';
    onLanguageChange: (lang: 'en' | 'hi' | 'mr') => void;
}

const languages = [
    { code: 'en', label: 'EN', fullName: 'English', flag: '🇬🇧' },
    { code: 'hi', label: 'हिं', fullName: 'हिंदी', flag: '🇮🇳' },
    { code: 'mr', label: 'मर', fullName: 'मराठी', flag: '🇮🇳' },
] as const;

export default function LanguageSelector({ language, onLanguageChange }: LanguageSelectorProps) {
    return (
        <div className="flex items-center gap-1 p-1 bg-gray-100 rounded-lg">
            {languages.map((lang) => (
                <button
                    key={lang.code}
                    onClick={() => onLanguageChange(lang.code)}
                    className={`language-btn px-3 py-1.5 rounded-md text-sm font-medium transition-all ${language === lang.code
                            ? 'active shadow-sm'
                            : 'text-gray-600 hover:text-gray-900 hover:bg-white'
                        }`}
                    title={lang.fullName}
                >
                    {lang.label}
                </button>
            ))}
        </div>
    );
}
