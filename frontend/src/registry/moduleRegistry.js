/**
 * Component Registry for Dynamic Modules
 * Map component_key from DB to actual React components.
 */

import BMICalculator from "../realms/forge/BMICalculator";
import TicTacToeGame from "../realms/arcade/TicTacToeGame";
import CurrencyConverter from "../realms/forge/CurrencyConverter";

export const moduleRegistry = {
    BMICalculator,
    TicTacToeGame,
    CurrencyConverter
};
