import BMICalculator from "../modules/tools/BMICalculator";
import CurrencyConverter from "../modules/tools/CurrencyConverter";
import AgeCalculator from "../modules/tools/AgeCalculator";
import WeatherTool from "../modules/tools/WeatherTool";
import UnitConverter from "../modules/tools/UnitConverter";
import TranslatorTool from "../modules/tools/TranslatorTool";
import RashiGenerator from "../modules/tools/RashiGenerator";
import CGPACalculator from "../modules/tools/CGPACalculator";
import JokeGenerator from "../modules/tools/JokeGenerator";

import TicTacToeGame from "../modules/games/TicTacToeGame";
import SnakeGame from "../modules/games/SnakeGame";
import FlappyBirdGame from "../modules/games/FlappyBirdGame";
import BrickBreakerGame from "../modules/games/BrickBreakerGame";

// Unified Module Registry aligned with backend component_key values
export const moduleRegistry = {
    // Tools
    "BMICalculator": BMICalculator,
    "CurrencyConverter": CurrencyConverter,
    "AgeCalculator": AgeCalculator,
    "WeatherTool": WeatherTool,
    "UnitConverter": UnitConverter,
    "TranslatorTool": TranslatorTool,
    "RashiGenerator": RashiGenerator,
    "CGPACalculator": CGPACalculator,
    "JokeGenerator": JokeGenerator,

    // Games
    "TicTacToeGame": TicTacToeGame,
    "SnakeGame": SnakeGame,
    "FlappyBirdGame": FlappyBirdGame,
    "BrickBreakerGame": BrickBreakerGame
};

export const getModuleComponent = (slug) => {
    // Note: ModuleLoader uses moduleData.component_key to index this registry
    return moduleRegistry[slug] || null;
};
