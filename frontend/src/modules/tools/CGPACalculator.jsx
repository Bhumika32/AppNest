import React, { useState } from 'react';

const CGPACalculator = ({ showSystemDialog, completeTool }) => {
    const [courses, setCourses] = useState([{ id: 1, credits: '3', grade: 'A' }]);
    const [result, setResult] = useState(null);

    const grades = {
        'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'P': 4, 'F': 0
    };

    const addCourse = () => {
        setCourses([...courses, { id: Date.now(), credits: '3', grade: 'A' }]);
    };

    const updateCourse = (id, field, value) => {
        setCourses(courses.map(c => c.id === id ? { ...c, [field]: value } : c));
    };

    const removeCourse = (id) => {
        if (courses.length > 1) {
            setCourses(courses.filter(c => c.id !== id));
        }
    };

    const calculateCGPA = () => {
        let totalCredits = 0;
        let totalPoints = 0;

        for (const course of courses) {
            const cred = parseFloat(course.credits);
            const pt = grades[course.grade];
            
            if (isNaN(cred)) {
                showSystemDialog('TOOL_ERROR', 'error');
                return;
            }

            totalCredits += cred;
            totalPoints += (cred * pt);
        }

        if (totalCredits === 0) return;

        const cgpa = (totalPoints / totalCredits).toFixed(2);
        setResult(cgpa);

        completeTool({
            duration: 15,
            score: 50,
            metadata: { cgpa, totalCredits },
            eventCategory: 'TOOL_SUCCESS'
        });
    };

    return (
        <div className="space-y-6 text-white max-w-sm mx-auto">
            <h3 className="text-xl font-black uppercase tracking-widest text-center mb-8">Academic <span className="text-neon-green">Evaluator</span></h3>
            
            <div className="space-y-4 max-h-60 overflow-y-auto pr-2 custom-scrollbar">
                {courses.map((course, index) => (
                    <div key={course.id} className="flex gap-2 items-end bg-black/30 p-3 rounded-xl border border-white/5">
                        <div className="flex-1">
                            <label className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-1 block">Course {index + 1} Credits</label>
                            <input 
                                type="number" 
                                value={course.credits}
                                onChange={(e) => updateCourse(course.id, 'credits', e.target.value)}
                                className="w-full bg-black/50 border border-white/10 rounded-lg p-2 text-center font-bold focus:border-neon-green focus:outline-none transition-colors"
                            />
                        </div>
                        <div className="flex-1">
                            <label className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-1 block">Grade</label>
                            <select 
                                value={course.grade} 
                                onChange={(e) => updateCourse(course.id, 'grade', e.target.value)}
                                className="w-full bg-black/50 border border-white/10 rounded-lg p-2 text-center font-bold focus:border-neon-green focus:outline-none transition-colors appearance-none"
                            >
                                {Object.keys(grades).map(g => <option key={g} value={g}>{g}</option>)}
                            </select>
                        </div>
                        <button 
                            onClick={() => removeCourse(course.id)}
                            className="bg-red-500/10 text-red-500 border border-red-500/20 p-2 rounded-lg hover:bg-red-500/20 transition-colors"
                        >
                            ✕
                        </button>
                    </div>
                ))}
            </div>

            <button 
                onClick={addCourse}
                className="w-full py-2 bg-white/5 border border-white/10 text-xs rounded-lg font-bold uppercase tracking-widest hover:bg-white/10 transition-all text-gray-400 hover:text-white"
            >
                + Add Course Parameter
            </button>

            <button 
                onClick={calculateCGPA}
                className="w-full py-4 mt-8 bg-white/5 border border-white/20 rounded-xl font-black uppercase tracking-widest hover:bg-white/10 hover:border-neon-green transition-all"
            >
                Compute Aggregates
            </button>

            {result && (
                <div className="mt-8 p-6 bg-neon-green/10 border border-neon-green/30 rounded-xl text-center">
                    <span className="text-xs font-black uppercase tracking-widest text-gray-400">Final Index</span>
                    <div className="text-5xl font-black text-neon-green mt-2 drop-shadow-[0_0_10px_rgba(0,255,0,0.5)]">
                        {result}
                    </div>
                </div>
            )}
        </div>
    );
};

export default CGPACalculator;
