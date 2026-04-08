import React, { useState } from 'react';

const TranslatorTool = ({ showSystemDialog, completeTool }) => {
    const [text, setText] = useState('');
    const [targetLang, setTargetLang] = useState('es');
    const [result, setResult] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const languages = {
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'ja': 'Japanese',
        'hi': 'Hindi'
    };

    const handleTranslate = () => {
        if (!text) {
            showSystemDialog('TOOL_ERROR', 'error');
            return;
        }

        setIsLoading(true);
        setTimeout(() => {
            // Mock translation
            const translatedMap = {
                es: `[ES] Contexto detectado: "${text}"`,
                fr: `[FR] Traduction: "${text}"`,
                de: `[DE] Verarbeitet: "${text}"`,
                ja: `[JA] 検出されました: "${text}"`,
                hi: `[HI] अनुवादित: "${text}"`
            };
            const translation = translatedMap[targetLang];
            setResult(translation);
            setIsLoading(false);

            completeTool({
                duration: 10,
                score: 50,
                metadata: { from: 'en', to: targetLang, charCount: text.length },
                eventCategory: 'TOOL_SUCCESS'
            });
        }, 800);
    };

    return (
        <div className="space-y-6 text-white max-w-md mx-auto">
            <h3 className="text-xl font-black uppercase tracking-widest text-center mb-8">Linguistic <span className="text-neon-pink">Decrypter</span></h3>
            
            <div className="space-y-4">
                <div>
                    <label className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2 block">Source Data</label>
                    <textarea 
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        className="w-full h-32 bg-black/50 border border-white/10 rounded-xl p-4 text-sm font-bold focus:border-neon-pink focus:outline-none transition-colors resize-none"
                        placeholder="Input raw signal for deciphering..."
                    />
                </div>
                
                <div>
                    <label className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2 block">Target Protocol</label>
                    <select 
                        value={targetLang} 
                        onChange={(e) => setTargetLang(e.target.value)}
                        className="w-full bg-black/50 border border-white/10 rounded-xl p-4 text-center font-bold focus:border-neon-pink focus:outline-none transition-colors appearance-none"
                    >
                        {Object.entries(languages).map(([code, name]) => (
                            <option key={code} value={code}>{name}</option>
                        ))}
                    </select>
                </div>
            </div>

            <button 
                onClick={handleTranslate}
                className="w-full py-4 mt-8 bg-white/5 border border-white/20 rounded-xl font-black uppercase tracking-widest hover:bg-white/10 hover:border-neon-pink transition-all flex justify-center items-center gap-2"
                disabled={isLoading}
            >
                {isLoading ? <span className="animate-pulse">DECRYPTING...</span> : 'Initiate Sequence'}
            </button>

            {result && !isLoading && (
                <div className="mt-8 p-6 bg-neon-pink/10 border border-neon-pink/30 rounded-xl flex flex-col items-center text-center">
                    <span className="text-xs font-black uppercase tracking-widest text-gray-400 mb-4">Decoded Signal</span>
                    <div className="text-lg font-black text-neon-pink drop-shadow-[0_0_10px_rgba(255,0,128,0.5)] leading-relaxed">
                        {result}
                    </div>
                </div>
            )}
        </div>
    );
};

export default TranslatorTool;
