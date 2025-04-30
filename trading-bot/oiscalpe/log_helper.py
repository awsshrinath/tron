import csv
import os
from datetime import datetime

ENTRY_LOG = "scalp_entry_log.csv"
EXIT_LOG = "scalp_exit_log.csv"

def log_entry(index, symbol, entry, sl, target, direction, reason):
    with open("scalp_entry_log.csv", mode='a', newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["Time", "Index", "Option", "Entry", "SL", "Target", "Direction", "Reason"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            index, symbol, entry, sl, target, direction, reason
        ])

def log_exit(symbol, option_type, strike, entry_price, exit_price, result, reason):
    file_exists = os.path.isfile(EXIT_LOG)
    with open(EXIT_LOG, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow([
                "Timestamp", "Symbol", "Option Type", "Strike", "Entry Price", "Exit Price", "PnL", "Result", "Reason"
            ])
        pnl = round(exit_price - entry_price, 2)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol,
            option_type,
            strike,
            round(entry_price, 2),
            round(exit_price, 2),
            pnl,
            result,
            reason
        ])

