import React, { Suspense, lazy } from 'react';
import { useParams, Navigate } from 'react-router-dom';
import { motion } from 'framer-motion';

const FeatureContainer = ({ type }) => {
    const { featureName } = useParams();

    // Dynamically import the feature component
    // Assuming structure: src/features/tools/<name>/ToolPage.jsx or src/features/games/<name>/Game.jsx
    const FeatureComponent = lazy(() => {
        if (type === 'tool') {
            return import(`../../features/tools/${featureName}/ToolPage.jsx`);
        } else {
            return import(`../../features/games/${featureName}/Game.jsx`);
        }
    });

    if (!featureName) return <Navigate to="/dashboard" />;

    return (
        <div className="min-h-screen bg-dark-bg text-white pb-20">
            <Suspense fallback={
                <div className="h-64 flex items-center justify-center">
                    <div className="text-neon-blue font-black animate-pulse uppercase tracking-[0.3em]">
                        Linking Neural Interface...
                    </div>
                </div>
            }>
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <FeatureComponent />
                </motion.div>
            </Suspense>
        </div>
    );
};

export default FeatureContainer;
