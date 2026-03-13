class PersonalityEngine {
    constructor() {
        this.memoryCache = new Map();

        // Dialog databases
        this.dialogs = {
            GAMES: {
                GAME_WIN: [
                    "Hmph. Not bad for a rookie.",
                    "You won? Must have been a glitch in my sensors.",
                    "I calculate a 0.001% chance of you repeating that.",
                    "Acceptable performance. Barely.",
                    "Don't let it go to your head."
                ],
                GAME_LOSS: [
                    "Pathetic. Even my sub-routines are laughing.",
                    "Did you even try? Honestly.",
                    "I've seen idle processes with better reflexes.",
                    "Recalibrating expectations... to zero.",
                    "Anomaly detected: terminal lack of skill."
                ],
                STREAK_ACTIVE: [
                    "You're on fire. Don't burn yourself.",
                    "A streak? I guess miracles do happen.",
                    "Keep this up and I might actually respect you.",
                    "Statistical anomaly in progress. Continuing observation."
                ]
            },
            TOOLS: {
                CURRENCY_CONVERTED: [
                    "Exchange data processed with optimal efficiency.",
                    "Funds translated. May your market predictions be favorable.",
                    "Conversion complete. Calculating fiscal viability... Just kidding.",
                    "Currency matrix updated. Enjoy your capitalism."
                ],
                BMI_CALCULATED: [
                    "Biometric analysis complete. You are... human.",
                    "Mass-to-height ratio processed.",
                    "Physical metrics logged. Remember to hydrate.",
                    "Health data synthesized successfully."
                ],
                TOOL_USAGE: [
                    "System optimized. Ready for input.",
                    "Executing task with maximum precision.",
                    "Another flawless calculation, if I do say so myself.",
                    "Tool engaged. Processing parameters."
                ]
            }
        };
        this.lastDialogTime = 0;
        this.COOLDOWN = 6000;
    }

    _getRandomLine(category, event) {
        const now = Date.now();
        if (now - this.lastDialogTime < this.COOLDOWN) {
            return null; // Silent if in cooldown
        }
        this.lastDialogTime = now;

        const lines = this.dialogs[category]?.[event] || ["Processing...", "Protocol engaged.", "Action logged."];

        // Prevent repetition via cache
        const cacheKey = `${category}_${event}`;
        const lastSaid = this.memoryCache.get(cacheKey) || [];

        // Filter out recently said lines (keep last 2 in memory)
        const availableLines = lines.filter(line => !lastSaid.includes(line));

        const selected = availableLines.length > 0
            ? availableLines[Math.floor(Math.random() * availableLines.length)]
            : lines[Math.floor(Math.random() * lines.length)]; // Fallback if all used recently

        // Update memory
        lastSaid.push(selected);
        if (lastSaid.length > 2) lastSaid.shift();
        this.memoryCache.set(cacheKey, lastSaid);

        return selected;
    }

    getGameRoast(event) {
        return this._getRandomLine('GAMES', event);
    }

    getSystemDialog(event) {
        return this._getRandomLine('TOOLS', event);
    }
}

// Singleton instance
export const personalityEngine = new PersonalityEngine();
