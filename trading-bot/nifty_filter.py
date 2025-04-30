from execution import get_market_data

NIFTY_SYMBOL = "NIFTY 50"

# Simulated VWAP trend check (replace with real VWAP later)
def get_nifty_trend():
    try:
        price, high, low = get_market_data("NIFTY 50")
        vwap = (high + low + price) / 3

        if price > vwap:
            return "UP"
        elif price < vwap:
            return "DOWN"
        else:
            return "FLAT"
    except Exception as e:
        print(f"❌ Failed to get Nifty trend: {e}")
        return None
