/**
 * API Client for CropAgent Backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ChatRequest {
    query: string;
    language: 'en' | 'hi' | 'mr';
    state?: string;
    crop?: string;
}

export interface ChatResponse {
    success: boolean;
    query: string;
    state: string;
    crop: string;
    language: string;
    response: any;
    raw_data?: any;
    metadata: {
        execution_time_seconds: number;
        agents_used: string[];
        timestamp: string;
    };
}

export interface StateInfo {
    name: string;
    lat: number;
    lon: number;
    major_crops: string[];
}

class CropAgentAPI {
    private baseUrl: string;

    constructor(baseUrl: string = API_BASE_URL) {
        this.baseUrl = baseUrl;
    }

    async chat(request: ChatRequest): Promise<ChatResponse> {
        const response = await fetch(`${this.baseUrl}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request),
        });

        if (!response.ok) {
            throw new Error(`Chat request failed: ${response.statusText}`);
        }

        return response.json();
    }

    async getWeather(state: string): Promise<any> {
        const response = await fetch(`${this.baseUrl}/api/weather/${encodeURIComponent(state)}`);

        if (!response.ok) {
            throw new Error(`Weather request failed: ${response.statusText}`);
        }

        return response.json();
    }

    async getSoil(state: string, crop: string): Promise<any> {
        const response = await fetch(
            `${this.baseUrl}/api/soil/${encodeURIComponent(state)}/${encodeURIComponent(crop)}`
        );

        if (!response.ok) {
            throw new Error(`Soil request failed: ${response.statusText}`);
        }

        return response.json();
    }

    async getStates(): Promise<{ states: StateInfo[] }> {
        const response = await fetch(`${this.baseUrl}/api/states`);

        if (!response.ok) {
            throw new Error(`States request failed: ${response.statusText}`);
        }

        return response.json();
    }

    async getCrops(state: string): Promise<{ state: string; crops: string[] }> {
        const response = await fetch(`${this.baseUrl}/api/crops/${encodeURIComponent(state)}`);

        if (!response.ok) {
            throw new Error(`Crops request failed: ${response.statusText}`);
        }

        return response.json();
    }

    async getHistory(state?: string, crop?: string, limit: number = 10): Promise<any> {
        const params = new URLSearchParams();
        if (state) params.append('state', state);
        if (crop) params.append('crop', crop);
        params.append('limit', limit.toString());

        const response = await fetch(`${this.baseUrl}/api/history?${params}`);

        if (!response.ok) {
            throw new Error(`History request failed: ${response.statusText}`);
        }

        return response.json();
    }

    async getStats(): Promise<any> {
        const response = await fetch(`${this.baseUrl}/api/stats`);

        if (!response.ok) {
            throw new Error(`Stats request failed: ${response.statusText}`);
        }

        return response.json();
    }

    async healthCheck(): Promise<{ status: string; timestamp: string; agents: number }> {
        const response = await fetch(`${this.baseUrl}/health`);

        if (!response.ok) {
            throw new Error(`Health check failed: ${response.statusText}`);
        }

        return response.json();
    }

    // WebSocket connection for real-time updates
    createWebSocket(onMessage: (data: any) => void, onError?: (error: Event) => void): WebSocket {
        const wsUrl = this.baseUrl.replace('http', 'ws') + '/ws';
        const ws = new WebSocket(wsUrl);

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            onMessage(data);
        };

        ws.onerror = (error) => {
            if (onError) {
                onError(error);
            }
        };

        return ws;
    }
}

// Export a default instance
export const api = new CropAgentAPI();

// Export the class for custom instances
export default CropAgentAPI;
