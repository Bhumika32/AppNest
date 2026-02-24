import React from 'react';
import { motion } from 'framer-motion';

const LoadingSkeleton = ({ className }) => {
    return (
        <div className={`relative overflow-hidden bg-white/5 rounded-xl ${className}`}>
            <motion.div
                animate={{ x: ['-100%', '200%'] }}
                transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
                className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent shadow-[0_0_20px_rgba(255,255,255,0.05)]"
            />
        </div>
    );
};

export const ChartSkeleton = () => (
    <div className="space-y-4 w-full h-[300px]">
        <div className="flex items-end h-full gap-2">
            {[...Array(7)].map((_, i) => (
                <LoadingSkeleton
                    key={i}
                    className="flex-1"
                    style={{ height: `${20 + Math.random() * 60}%` }}
                />
            ))}
        </div>
    </div>
);

export const BountySkeleton = () => (
    <div className="space-y-6">
        {[...Array(3)].map((_, i) => (
            <div key={i} className="space-y-2">
                <div className="flex justify-between">
                    <LoadingSkeleton className="h-3 w-1/2" />
                    <LoadingSkeleton className="h-3 w-12" />
                </div>
                <LoadingSkeleton className="h-2 w-full rounded-full" />
            </div>
        ))}
    </div>
);

export default LoadingSkeleton;
