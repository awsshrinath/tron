from kiteconnect import KiteConnect
from config import API_KEY, ACCESS_TOKEN
from datetime import datetime, timedelta

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

ATR_CACHE = {}

def get_instrument_tokens(stock):
    instrument_map = {
        "RELIANCE": 738561,
        "HDFCBANK": 341249,
        "INFY": 408065,
        "ICICIBANK": 1270529,
        "TCS": 2953217
    }
    return instrument_map.get(stock)

def get_atr(stock, period=14, interval="15minute"):
    if stock in ATR_CACHE:
        return ATR_CACHE[stock]

    to_date = datetime.now()
    from_date = to_date - timedelta(days=10)

    try:
        candles = kite.historical_data(
            instrument_token=get_instrument_tokens(stock),
            from_date=from_date,
            to_date=to_date,
            interval=interval
        )

        trs = []
        for i in range(1, len(candles)):
            high = candles[i]['high']
            low = candles[i]['low']
            prev_close = candles[i - 1]['close']
            tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
            trs.append(tr)

        atr = sum(trs[-period:]) / period
        ATR_CACHE[stock] = atr
        return atr

    except Exception as e:
        print(f"❌ Failed to fetch ATR for {stock}: {e}")
        return None
