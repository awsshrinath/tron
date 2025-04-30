from runner.strategy_factory import load_strategy
import time
from datetime import datetime

class TradeManager:
    def __init__(self, kite, logger, firestore_client):
        self.kite = kite
        self.logger = logger
        self.firestore = firestore_client
        self.active_trades = []
        self.strategy = None

    def load_strategy(self, strategy_name):
        self.strategy = load_strategy(strategy_name, self.kite, self.logger)
        if self.strategy:
            self.logger.log_event(f"Strategy '{strategy_name}' loaded successfully.")
        else:
            self.logger.log_event(f"Failed to load strategy: {strategy_name}")

    def monitor_and_trade(self, market_data):
        if not self.strategy:
            return

        new_trades = self.strategy.find_trade_opportunities(market_data)
        for trade in new_trades:
            self.active_trades.append(trade)
            self.logger.log_event(f"Trade executed (simulated): {trade}")

def start_trading(self, selected_strategy, market_data_fetcher):
    self.logger.log_event(f"Live Trading Started using Strategy: {selected_strategy}")

    watchlist = {
        "NIFTY": 256265,
        "BANKNIFTY": 260105
    }

    while True:
        for symbol, token in watchlist.items():
            candle = market_data_fetcher.fetch_latest_candle(token, interval="5minute")

            if candle:
                market_data = {
                    symbol: candle
                }

                # Pass market data to strategy
                new_trades = self.strategy.find_trade_opportunities(market_data)

                for trade in new_trades:
                    self.active_trades.append(trade)
                    self.logger.log_event(f"Trade executed (simulated): {trade}")

                    # ✅ Log to Firestore
                    today = datetime.now().strftime("%Y-%m-%d")
                    self.firestore.log_trade(selected_strategy, today, trade)
            else:
                self.logger.log_event(f"No candle data fetched for {symbol}")

        time.sleep(60)  # Wait 60 seconds before next fetch