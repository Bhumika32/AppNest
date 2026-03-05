import BMICalculator from "../modules/tools/BMICalculator";
import CurrencyConverter from "../modules/tools/CurrencyConverter";
import AgeCalculator from "../modules/tools/AgeCalculator";
import WeatherTool from "../modules/tools/WeatherTool";
import RashiGenerator from "../modules/tools/RashiGenerator";
import UnitConverter from "../modules/tools/UnitConverter";
import CGPACalculator from "../modules/tools/CGPACalculator";
import TranslatorTool from "../modules/tools/TranslatorTool";
import JokeGenerator from "../modules/tools/JokeGenerator";

import TicTacToeGame from "../modules/games/TicTacToeGame";
import SnakeGame from "../modules/games/SnakeGame";
import FlappyBirdGame from "../modules/games/FlappyBirdGame";
import BrickBreakerGame from "../modules/games/BrickBreakerGame";

// Unified Module Registry referencing both tools and games dynamically
export const moduleRegistry = {
    // Tools
    "BMICalculator": BMICalculator,
    "CurrencyConverter": CurrencyConverter,
    "AgeCalculator": AgeCalculator,
    "WeatherTool": WeatherTool,
    "RashiGenerator": RashiGenerator,
    "UnitConverter": UnitConverter,
    "CGPACalculator": CGPACalculator,
    "TranslatorTool": TranslatorTool,
    "JokeGenerator": JokeGenerator,

    // Games
    "TicTacToeGame": TicTacToeGame,
    "SnakeGame": SnakeGame,
    "FlappyBirdGame": FlappyBirdGame,
    "BrickBreakerGame": BrickBreakerGame
};

export const getModuleComponent = (slug) => {
    return moduleRegistry[slug] || null;
};
