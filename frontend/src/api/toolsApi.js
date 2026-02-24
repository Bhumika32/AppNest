import axios from './axios';

/**
 * Tools API Service
 * Handles all tool-related API calls
 */

const toolsApi = {
  // General
  listTools: () =>
    axios.get('/tools/'),

  // BMI Calculator
  calculateBMI: (weightKg, heightCm) =>
    axios.post('/tools/bmi/calculate', {
      weight_kg: weightKg,
      height_cm: heightCm,
    }),

  getBMICategories: () =>
    axios.get('/tools/bmi/categories'),

  // Currency Converter
  convertCurrency: (amount, fromCurrency, toCurrency) =>
    axios.post('/tools/currency/convert', {
      amount,
      from_currency: fromCurrency,
      to_currency: toCurrency,
    }),

  getSupportedCurrencies: () =>
    axios.get('/tools/currency/supported'),

  // Weather
  getWeather: (city) =>
    axios.post('/tools/weather/get', { city }),

  // Age Calculator
  calculateAge: (name, dob, funMode = true, roastMode = false) =>
    axios.post('/tools/age/calculate', {
      name,
      dob,
      fun_mode: funMode,
      roast_mode: roastMode,
    }),

  // Rashi Generator
  calculateRashi: (name, birthPlace, birthTime, birthDate, birthLat, birthLon) =>
    axios.post('/tools/rashi/calculate', {
      name,
      birth_place: birthPlace,
      birth_time: birthTime,
      birth_date: birthDate,
      birth_lat: birthLat,
      birth_lon: birthLon,
    }),

  // Unit Converter
  convertUnits: (value, fromUnit, toUnit, category) =>
    axios.post('/tools/unit-converter/convert', {
      value,
      from_unit: fromUnit,
      to_unit: toUnit,
      category,
    }),

  getConverterUnits: (category) =>
    axios.get(`/tools/unit-converter/units?category=${category}`),

  // Tool Roasts
  getToolRoast: (toolName) =>
    axios.get(`/roast/tool/${toolName}`),
};

export default toolsApi;
