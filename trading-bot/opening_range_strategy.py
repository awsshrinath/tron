from execution import get_market_data
from config import RISK_PER_TRADE, MIS_MARGIN
from datetime import datetime

opening_range_highs = {}
opening_range_lows = {}

def opening_range_strategy(stock, capital):
    now = datetime.now().strftime("%H:%M")
    if now < "09:30":
        return None  # Wait till first 15 min candle closes

    price, high, low = get_market_data(stock)

    # Capture opening range only once
    if stock not in opening_range_highs:
        opening_range_highs[stock] = high
        opening_range_lows[stock] = low

    opening_high = opening_range_highs[stock]
    opening_low = opening_range_lows[stock]

    if price > opening_high and (price - low) / (high - low) > 0.7:
        sl_per_share = max(price * 0.007, 6.0)
        leverage = MIS_MARGIN.get(stock, 1)
        print(f"🔍 {stock}: Leverage used: {leverage}x")
        max_trade_cap = capital * 0.33 * leverage
        qty = int(RISK_PER_TRADE / sl_per_share)

        if qty * price > max_trade_cap:
            qty = int(max_trade_cap / price)
        if qty < 1:
            return None

        return {
            "action": "BUY",
            "entry": price,
            "target": price + sl_per_share * 2,
            "sl": price - sl_per_share,
            "qty": qty,
            "reason": "Opening Range Breakout (ORB Strategy)"
        }

    return None
