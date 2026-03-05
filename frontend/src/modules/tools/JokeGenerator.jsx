import React, { useState } from 'react';

const jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I've got a great UDP joke, but I'm not sure if you'd get it.",
    "A programmer's wife tells him: \"Go to store. If they have eggs, bring 10.\" He returns with 10 loaves of bread.",
    "What's a programmer's favorite hangout place? Foo Bar.",
    "How many programmers does it take to change a light bulb? None. It's a hardware problem."
];

const JokeGenerator = ({ showSystemDialog, completeTool }) => {
    const [joke, setJoke] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleGenerate = () => {
        setIsLoading(true);
        setTimeout(() => {
            const randomJoke = jokes[Math.floor(Math.random() * jokes.length)];
            setJoke(randomJoke);
            setIsLoading(false);

            completeTool({
                duration: 2,
                score: 50,
                // humor is subjective but we reward them
                metadata: { jokeType: 'programmer_humor' },
                eventCategory: 'TOOL_SUCCESS'
            });
        }, 500);
    };

    return (
        <div className="space-y-6 text-white max-w-md mx-auto text-center flex flex-col items-center">
            <h3 className="text-xl font-black uppercase tracking-widest mb-8">Humor <span className="text-yellow-400">Synthesizer</span></h3>
            
            <div className="w-32 h-32 rounded-full border-4 border-yellow-400/30 flex items-center justify-center mb-8 relative">
                <div className="absolute inset-0 bg-yellow-400/10 rounded-full animate-pulse blur-xl"></div>
                <div className="text-6xl z-10">🤖</div>
            </div>

            <button 
                onClick={handleGenerate}
                className="w-full py-4 bg-white/5 border border-white/20 rounded-xl font-black uppercase tracking-widest hover:bg-white/10 hover:border-yellow-400 transition-all text-yellow-500 shadow-[0_0_15px_rgba(250,204,21,0.2)] hover:shadow-[0_0_20px_rgba(250,204,21,0.5)]"
                disabled={isLoading}
            >
                {isLoading ? 'Compiling Humor...' : 'Generate Syntax Error'}
            </button>

            {joke && !isLoading && (
                <div className="mt-8 p-6 bg-yellow-400/10 border border-yellow-400/30 rounded-xl flex flex-col items-center relative overflow-hidden">
                    <div className="absolute -right-4 -top-8 text-9xl text-yellow-500/10 font-black">"</div>
                    <span className="text-xs font-black uppercase tracking-widest text-gray-400 mb-4 z-10">Humor Payload</span>
                    <div className="text-lg font-black text-yellow-400 drop-shadow-[0_0_10px_rgba(250,204,21,0.5)] leading-relaxed z-10 italic">
                        "{joke}"
                    </div>
                </div>
            )}
        </div>
    );
};

export default JokeGenerator;
