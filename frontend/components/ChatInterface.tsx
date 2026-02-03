'use client';

import { useState, useRef, useEffect } from 'react';

interface ChatInterfaceProps {
    language: 'en' | 'hi' | 'mr';
    state: string;
    crop: string;
    onSubmit: (query: string) => void;
    response: any;
    isLoading: boolean;
    translations: any;
}

interface Message {
    id: number;
    type: 'user' | 'agent';
    content: string;
    timestamp: Date;
    data?: any;
}

const exampleQueries = {
    en: [
        "Will rice yield be good in Maharashtra this season?",
        "What's the weather forecast for Punjab?",
        "Should I irrigate my cotton fields today?",
        "Is there any disease risk for wheat in UP?",
    ],
    hi: [
        "क्या महाराष्ट्र में इस सीजन चावल की उपज अच्छी होगी?",
        "पंजाब के लिए मौसम का पूर्वानुमान क्या है?",
        "क्या मुझे आज अपने कपास के खेतों में सिंचाई करनी चाहिए?",
        "यूपी में गेहूं के लिए कोई बीमारी का खतरा है?",
    ],
    mr: [
        "महाराष्ट्रात या हंगामात तांदळाचे उत्पादन चांगले होईल का?",
        "पंजाबसाठी हवामानाचा अंदाज काय आहे?",
        "मी आज माझ्या कापूस शेतात सिंचन करावे का?",
        "उत्तर प्रदेशात गव्हाला रोगाचा धोका आहे का?",
    ]
};

export default function ChatInterface({
    language,
    state,
    crop,
    onSubmit,
    response,
    isLoading,
    translations
}: ChatInterfaceProps) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    // Scroll to bottom when new messages arrive
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Add welcome message on mount
    useEffect(() => {
        setMessages([
            {
                id: 0,
                type: 'agent',
                content: translations.welcome,
                timestamp: new Date()
            }
        ]);
    }, [translations.welcome]);

    // Update messages when response arrives
    useEffect(() => {
        if (response && response.success) {
            const agentMessage: Message = {
                id: Date.now(),
                type: 'agent',
                content: response.response?.summary?.text || 'Analysis complete.',
                timestamp: new Date(),
                data: response
            };
            setMessages(prev => [...prev, agentMessage]);
        }
    }, [response]);

    const handleSubmit = async (e?: React.FormEvent) => {
        e?.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage: Message = {
            id: Date.now(),
            type: 'user',
            content: input,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        onSubmit(input);
        setInput('');
    };

    const handleExampleClick = (query: string) => {
        setInput(query);
        inputRef.current?.focus();
    };

    return (
        <div className="flex flex-col h-[calc(100vh-200px)] max-h-[700px]">
            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((message) => (
                    <div
                        key={message.id}
                        className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}
                    >
                        <div className={`max-w-[80%] ${message.type === 'user' ? 'chat-bubble-user' : 'chat-bubble-agent'
                            } px-4 py-3`}>
                            {/* Avatar */}
                            <div className="flex items-start gap-3">
                                {message.type === 'agent' && (
                                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-crop-400 to-crop-600 flex items-center justify-center flex-shrink-0">
                                        <span>🌾</span>
                                    </div>
                                )}

                                <div className="flex-1">
                                    <p className="text-sm md:text-base">{message.content}</p>

                                    {/* Additional data display */}
                                    {message.data && (
                                        <div className="mt-4 space-y-3">
                                            {/* Yield info */}
                                            {message.data.response?.prediction_details?.yield && (
                                                <div className="bg-crop-50 rounded-lg p-3 border border-crop-200">
                                                    <div className="text-sm font-medium text-crop-700 mb-2">
                                                        📊 Yield Prediction
                                                    </div>
                                                    <div className="grid grid-cols-2 gap-2 text-sm">
                                                        <div>
                                                            <span className="text-gray-500">Predicted: </span>
                                                            <span className="font-semibold">
                                                                {message.data.response.prediction_details.yield.predicted} t/ha
                                                            </span>
                                                        </div>
                                                        <div>
                                                            <span className="text-gray-500">vs Avg: </span>
                                                            <span className={`font-semibold ${message.data.response.prediction_details.yield.vs_average > 0
                                                                    ? 'text-green-600' : 'text-red-600'
                                                                }`}>
                                                                {message.data.response.prediction_details.yield.vs_average > 0 ? '+' : ''}
                                                                {message.data.response.prediction_details.yield.vs_average}%
                                                            </span>
                                                        </div>
                                                    </div>
                                                </div>
                                            )}

                                            {/* Recommendations */}
                                            {message.data.response?.recommendations?.length > 0 && (
                                                <div className="bg-blue-50 rounded-lg p-3 border border-blue-200">
                                                    <div className="text-sm font-medium text-blue-700 mb-2">
                                                        💡 Recommendations
                                                    </div>
                                                    <ul className="text-sm space-y-1">
                                                        {message.data.response.recommendations.slice(0, 3).map((rec: any, i: number) => (
                                                            <li key={i} className="flex items-start gap-2">
                                                                <span className={`px-1.5 py-0.5 rounded text-xs ${rec.priority === 'high' ? 'bg-red-100 text-red-700' :
                                                                        rec.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                                                                            'bg-green-100 text-green-700'
                                                                    }`}>
                                                                    {rec.priority}
                                                                </span>
                                                                <span>{rec.action}</span>
                                                            </li>
                                                        ))}
                                                    </ul>
                                                </div>
                                            )}

                                            {/* Irrigation advice */}
                                            {message.data.response?.irrigation_advice && (
                                                <div className={`rounded-lg p-3 border ${message.data.response.irrigation_advice.action === 'irrigate'
                                                        ? 'bg-blue-50 border-blue-200'
                                                        : 'bg-gray-50 border-gray-200'
                                                    }`}>
                                                    <div className="text-sm font-medium mb-1">
                                                        💧 Irrigation Advice
                                                    </div>
                                                    <p className="text-sm">
                                                        {message.data.response.irrigation_advice.message}
                                                    </p>
                                                </div>
                                            )}
                                        </div>
                                    )}

                                    <div className="text-xs opacity-60 mt-2">
                                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </div>
                                </div>

                                {message.type === 'user' && (
                                    <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center flex-shrink-0">
                                        <span>👤</span>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                ))}

                {/* Loading indicator */}
                {isLoading && (
                    <div className="flex justify-start animate-fade-in">
                        <div className="chat-bubble-agent px-4 py-3">
                            <div className="flex items-center gap-3">
                                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-crop-400 to-crop-600 flex items-center justify-center">
                                    <span>🌾</span>
                                </div>
                                <div className="typing-indicator">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Example Queries */}
            {messages.length <= 1 && (
                <div className="px-4 py-3 border-t border-gray-100">
                    <p className="text-sm text-gray-500 mb-2">Try asking:</p>
                    <div className="flex flex-wrap gap-2">
                        {exampleQueries[language].map((query, i) => (
                            <button
                                key={i}
                                onClick={() => handleExampleClick(query)}
                                className="text-sm px-3 py-1.5 bg-gray-100 hover:bg-gray-200 rounded-full transition-colors"
                            >
                                {query.length > 40 ? query.substring(0, 40) + '...' : query}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Input Area */}
            <form onSubmit={handleSubmit} className="p-4 border-t border-gray-100">
                <div className="flex gap-2">
                    <input
                        ref={inputRef}
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder={translations.askQuestion}
                        disabled={isLoading}
                        className="flex-1 px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-crop-500 focus:border-transparent disabled:bg-gray-100"
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className="px-6 py-3 bg-gradient-to-r from-crop-500 to-crop-600 text-white rounded-xl font-medium hover:from-crop-600 hover:to-crop-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {isLoading ? (
                            <div className="spinner" />
                        ) : (
                            <span>➤</span>
                        )}
                    </button>
                </div>

                {/* Context info */}
                <div className="mt-2 text-xs text-gray-400 flex items-center gap-2">
                    <span>📍 {state}</span>
                    <span>•</span>
                    <span>🌱 {crop}</span>
                </div>
            </form>
        </div>
    );
}
