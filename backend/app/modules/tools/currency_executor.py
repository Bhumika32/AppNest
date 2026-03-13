from app.platform.module_executor import ModuleExecutor

"""
app/services/tools/currency.py

Currency Converter service using Frankfurter API.

Features:
- Live exchange rates
- Multiple currency support
- Currency symbols
- Professional error handling
"""

import requests
from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class CurrencyConversionResult:
    """Structured currency conversion result."""
    amount: float
    from_currency: str
    to_currency: str
    converted_amount: float
    exchange_rate: float
    from_symbol: str
    to_symbol: str


class CurrencyService:
    """Service class for currency conversion."""

    BASE_URL = "https://api.frankfurter.app"

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
        Get currency symbol for currency code.

        Args:
            code: ISO 4217 currency code (e.g., 'USD', 'INR')

        Returns:
            Currency symbol or code if not found
        """
        return CurrencyService.CURRENCY_SYMBOLS.get(code.upper(), code.upper())

    @staticmethod
    def get_supported_currencies() -> Dict[str, str]:
        """
        Fetch all supported currencies from API.

        Returns:
            Dictionary of {code: name}
        """
        try:
            url = f"{CurrencyService.BASE_URL}/currencies"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {}

    @staticmethod
    def convert(
        amount: float,
        from_currency: str,
        to_currency: str
    ) -> CurrencyConversionResult:
        """
        Convert amount from one currency to another.

        Args:
            amount: Amount to convert
            from_currency: Source currency code
            to_currency: Target currency code

        Returns:
            CurrencyConversionResult with conversion details

        Raises:
            ValueError: If conversion fails
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")

        try:
            url = f"{CurrencyService.BASE_URL}/latest"
            params = {
                "amount": amount,
                "from": from_currency.upper(),
                "to": to_currency.upper()
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            rates = data.get("rates", {})

            if to_currency.upper() not in rates:
                raise ValueError(f"Currency conversion failed for {to_currency}")

            converted_amount = float(rates[to_currency.upper()])
            exchange_rate = converted_amount / amount if amount > 0 else 0

            return CurrencyConversionResult(
                amount=amount,
                from_currency=from_currency.upper(),
                to_currency=to_currency.upper(),
                converted_amount=round(converted_amount, 2),
                exchange_rate=round(exchange_rate, 4),
                from_symbol=CurrencyService.get_symbol(from_currency),
                to_symbol=CurrencyService.get_symbol(to_currency)
            )
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Currency conversion API error: {str(e)}")



from app.platform.module_result import ModuleResult

class CurrencyExecutor(ModuleExecutor):
    module_key = "currency-converter"

    def execute(self, payload: dict, user) -> ModuleResult:
        meta = payload.get("metadata", {})
        amount = payload.get("amount") or meta.get("amount")
        from_currency = payload.get("from_currency") or meta.get("from_currency") or meta.get("from")
        to_currency = payload.get("to_currency") or meta.get("to_currency") or meta.get("to")

        if not amount or not from_currency or not to_currency:
            return ModuleResult(
                completed=False,
                status="error",
                error="INVALID_INPUT",
                message="amount, from_currency, and to_currency are required"
            )

        try:
            result = CurrencyService.convert(float(amount), from_currency, to_currency)
            return ModuleResult(
                completed=True,
                status="success",
                data={
                    "amount": result.amount,
                    "from_currency": result.from_currency,
                    "to_currency": result.to_currency,
                    "converted_amount": result.converted_amount,
                    "exchange_rate": result.exchange_rate,
                    "from_symbol": result.from_symbol,
                    "to_symbol": result.to_symbol
                }
            )
        except ValueError as e:
            return ModuleResult(
                completed=False,
                status="error",
                error="INVALID_INPUT",
                message=str(e)
            )
