import React from 'react';
import { Zap } from 'lucide-react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        console.error("Neural Link Failure:", error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return this.props.fallback || (
                <div className="flex flex-col items-center justify-center min-h-screen bg-[#0a0a0c] text-center p-8">
                    <div className="w-24 h-24 bg-red-500/10 rounded-full flex items-center justify-center mb-6 border border-red-500/20 shadow-[0_0_30px_rgba(239,68,68,0.2)]">
                        <Zap size={48} className="text-red-500" />
                    </div>
                    <h1 className="text-3xl font-black mb-4 tracking-tighter uppercase text-white">System <span className="text-red-500">Fracture</span></h1>
                    <p className="text-gray-500 max-w-md mb-8 font-medium leading-relaxed">
                        A critical error has occurred in the neural matrix. Synchronization with the current sector has been lost.
                    </p>
                    <div className="bg-red-500/5 border border-red-500/20 rounded-xl p-4 mb-8 max-w-2xl w-full text-left font-mono">
                        <p className="text-[10px] text-red-400 font-bold uppercase mb-2">Error Log:</p>
                        <p className="text-xs text-gray-400 break-all">{this.state.error?.message}</p>
                    </div>
                    <button
                        onClick={() => window.location.reload()}
                        className="px-8 py-3 bg-red-500 text-white font-black rounded-xl hover:bg-red-600 transition-all uppercase tracking-tighter shadow-lg shadow-red-500/20"
                    >
                        Hard Reset Ecosystem
                    </button>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
