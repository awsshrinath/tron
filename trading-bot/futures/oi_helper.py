# 🔮 Simulated Open Interest trend

def get_oi_trend(symbol):
    """
    Placeholder logic to simulate OI-based trend.
    In reality, you'd fetch actual futures OI data from NSE or broker API.
    """
    # Simulate logic
    trending_up_symbols = ["NIFTY", "RELIANCE", "ICICIBANK", "BANKNIFTY"]
    trending_down_symbols = ["HDFCBANK", "TCS", "INFY"]

    if symbol.upper() in trending_up_symbols:
        return "LONG"
    elif symbol.upper() in trending_down_symbols:
        return "SHORT"
    else:
        return "SIDEWAYS"
