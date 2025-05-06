import os
import datetime
from kiteconnect import KiteConnect

# Setup Kite client
kite = KiteConnect(api_key=os.getenv("ZERODHA_API_KEY"))
kite.set_access_token(os.getenv("ZERODHA_ACCESS_TOKEN"))

# Cache for instrument tokens
token_cache = {}

def get_instrument_tokens(symbol):
    """Fetch instrument token for a futures symbol like NIFTY24APRFUT."""
    if symbol in token_cache:
        return token_cache[symbol]

    try:
        instruments = kite.instruments("NFO")
        for inst in instruments:
            if inst["tradingsymbol"] == symbol:
                token_cache[symbol] = inst["instrument_token"]
                return inst["instrument_token"]
    except Exception as e:
        print(f"❌ Failed to fetch instrument token for {symbol}: {e}")
        return None

def is_volume_strong(symbol):
    """Check if current volume is higher than average of last 5 candles."""
    try:
        token = get_instrument_tokens(symbol)
        if not token:
            return False

        now = datetime.datetime.now()
        start_time = now - datetime.timedelta(minutes=30)

        candles = kite.historical_data(
            instrument_token=token,
            from_date=start_time,
            to_date=now,
            interval="5minute",
            continuous=False
        )

        if len(candles) < 6:
            print(f"⚠️ Not enough candle data for {symbol}")
            return False

        recent = candles[-1]
        previous = candles[-6:-1]
        current_volume = recent['volume']
        avg_volume = sum(c['volume'] for c in previous) / len(previous)

        if current_volume > avg_volume * 1.2:
            print(f"✅ {symbol} volume strong: {current_volume} > {avg_volume:.0f}")
            return True
        else:
            print(f"🔇 {symbol} volume weak: {current_volume} <= {avg_volume:.0f}")
            return False

    except Exception as e:
        print(f"❌ Volume check failed for {symbol}: {e}")
        return False
