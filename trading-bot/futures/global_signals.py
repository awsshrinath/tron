import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from execution import get_market_data  # or whatever module you're importing


# 🧠 You can replace these mock functions with actual API responses later
def get_dow_jones_direction():
    # Simulated logic - in real use, fetch Dow Jones close price
    # Example with Yahoo Finance API / Alpha Vantage / TradingView webhook
    return "UP"  # or "DOWN"

def get_vix_level():
    # Simulated VIX value
    return 12.5  # India VIX value

def get_bank_nifty_direction():
    # You can use the same get_market_data() logic
    # Simulated upward movement
    return "UP"  # or "DOWN"

def get_global_sentiment():
    dow = get_dow_jones_direction()
    vix = get_vix_level()
    banknifty = get_bank_nifty_direction()

    if vix > 16:
        return {
            "allow_trading": False,
            "reason": "VIX too high",
            "direction": None
        }

    if dow == "UP" and banknifty == "UP":
        return {
            "allow_trading": True,
            "direction": "UP"
        }

    elif dow == "DOWN" and banknifty == "DOWN":
        return {
            "allow_trading": True,
            "direction": "DOWN"
        }

    return {
        "allow_trading": False,
        "reason": "Global mismatch",
        "direction": None
    }
