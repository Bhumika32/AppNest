"""
app/tools/currency/service.py

Currency conversion logic using Frankfurter API (reliable and free).

API Provider:
- https://www.frankfurter.app

Enhancements:
- Provides common currency symbols (₹, $, €, £, ¥, etc.)
- Falls back to currency code if symbol not available
"""

import requests


class CurrencyService:
    """Service class for currency conversion."""

    BASE_URL = "https://api.frankfurter.app"

    # Common currency symbols map (extend anytime)
    CURRENCY_SYMBOLS = {
            # Americas
            "USD": "$", "CAD": "C$", "MXN": "$", "BRL": "R$",
            "ARS": "$", "CLP": "$", "COP": "$", "PEN": "S/",

            # Europe
            "EUR": "€", "GBP": "£", "CHF": "CHF", "NOK": "kr", "SEK": "kr",
            "DKK": "kr", "PLN": "zł", "CZK": "Kč", "HUF": "Ft", "RON": "lei",
            "RUB": "₽", "TRY": "₺", "ISK": "kr",

            # Asia
            "INR": "₹", "JPY": "¥", "CNY": "¥", "KRW": "₩",
            "SGD": "S$", "HKD": "HK$", "TWD": "NT$", "THB": "฿",
            "IDR": "Rp", "MYR": "RM", "PHP": "₱", "VND": "₫",
            "ILS": "₪", "AED": "د.إ", "SAR": "﷼",

            # Oceania
            "AUD": "A$", "NZD": "NZ$",

            # Africa
            "ZAR": "R", "EGP": "E£", "NGN": "₦", "KES": "KSh",
        }

    @staticmethod
    def get_symbol(code: str) -> str:
        """
        Return currency symbol if available, otherwise return code itself.

        Example:
            INR -> ₹
            USD -> $
            Unknown -> <CODE>
        """
        return CurrencyService.CURRENCY_SYMBOLS.get(code.upper(), "")

    @staticmethod
    def get_supported_symbols() -> dict:
        """
        Fetch supported currencies.

        Returns:
            dict: {"USD": "United States Dollar", "INR": "Indian Rupee", ...}
        """
        url = f"{CurrencyService.BASE_URL}/currencies"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()

    @staticmethod
    def convert(amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert currency using live exchange rates.

        Returns:
            float: converted amount
        """
        url = f"{CurrencyService.BASE_URL}/latest"
        params = {"amount": amount, "from": from_currency, "to": to_currency}

        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()

        data = res.json()
        rates = data.get("rates", {})

        if to_currency not in rates:
            raise ValueError("Conversion failed. Invalid currency selection.")

        return round(float(rates[to_currency]), 4)