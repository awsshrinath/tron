from runner.strategy_factory import load_strategy
import time

class TradeManager:
    def __init__(self, kite, logger):
        self.kite = kite
        self.logger = logger
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

        # Example instrument tokens (you can customize this later)
        # (Later: Read dynamically from strategy or config)
        watchlist = {
            "NIFTY": 256265,       # Nifty Index
            "BANKNIFTY": 260105    # Bank Nifty Index
        }

        while True:
            for symbol, token in watchlist.items():
                candle = market_data_fetcher.fetch_latest_candle(token, interval="5minute")

                if candle:
                    market_data = {
                    symbol: candle
                    }
                    # Now pass real market data to strategy
                    new_trades = self.strategy.find_trade_opportunities(market_data)

                    for trade in new_trades:
                        self.active_trades.append(trade)
                        self.logger.log_event(f"Trade executed (simulated): {trade}")
                else:
                    self.logger.log_event(f"No candle data fetched for {symbol}")

            time.sleep(60)  # Wait 60 seconds before next fetch
