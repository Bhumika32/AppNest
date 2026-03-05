import React, { useState } from 'react';
import { Cloud, Sun, CloudRain, Wind } from 'lucide-react';

// Mock Weather Data
const mockWeather = {
    "Tokyo": { temp: 22, condition: "Sunny", icon: <Sun className="text-yellow-400" size={48} /> },
    "London": { temp: 15, condition: "Rainy", icon: <CloudRain className="text-blue-400" size={48} /> },
    "New York": { temp: 18, condition: "Cloudy", icon: <Cloud className="text-gray-400" size={48} /> },
    "Mumbai": { temp: 32, condition: "Clear", icon: <Sun className="text-yellow-500" size={48} /> },
    "Sydney": { temp: 24, condition: "Windy", icon: <Wind className="text-purple-400" size={48} /> }
};

const WeatherTool = ({ showSystemDialog, completeTool }) => {
    const [city, setCity] = useState('');
    const [weather, setWeather] = useState(null);

    const checkWeather = () => {
        if (!city) {
            showSystemDialog('TOOL_ERROR', 'error');
            return;
        }

        const data = mockWeather[city] || { 
            temp: Math.floor(Math.random() * 35), 
            condition: "Scattered Clouds", 
            icon: <Cloud className="text-gray-400" size={48} /> 
        };

        setWeather({ ...data, city });

        completeTool({
            duration: 5,
            score: 50,
            metadata: { city, temp: data.temp },
            eventCategory: 'TOOL_SUCCESS'
        });
    };

    return (
        <div className="space-y-6 text-white max-w-sm mx-auto">
            <h3 className="text-xl font-black uppercase tracking-widest text-center mb-8">Atmospheric <span className="text-neon-blue">Radar</span></h3>
            
            <div className="space-y-4">
                <div>
                    <label className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2 block">Target Location</label>
                    <input 
                        type="text" 
                        value={city}
                        onChange={(e) => setCity(e.target.value)}
                        className="w-full bg-black/50 border border-white/10 rounded-xl p-4 text-center font-bold focus:border-neon-blue focus:outline-none transition-colors"
                        placeholder="e.g. Tokyo, London..."
                    />
                </div>
            </div>

            <button 
                onClick={checkWeather}
                className="w-full py-4 mt-8 bg-white/5 border border-white/20 rounded-xl font-black uppercase tracking-widest hover:bg-white/10 hover:border-neon-blue transition-all"
            >
                Scan Sector
            </button>

            {weather && (
                <div className="mt-8 p-6 bg-neon-blue/10 border border-neon-blue/30 rounded-xl flex flex-col items-center">
                    <div className="mb-4">{weather.icon}</div>
                    <div className="text-4xl font-black text-neon-blue drop-shadow-[0_0_10px_rgba(0,255,255,0.5)]">
                        {weather.temp}°C
                    </div>
                    <div className="text-sm font-bold uppercase tracking-widest text-gray-300 mt-2">
                        {weather.condition} in {weather.city}
                    </div>
                </div>
            )}
        </div>
    );
};

export default WeatherTool;
