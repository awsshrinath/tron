import pandas as pd

def generate_weekly_report():
    df = pd.read_csv("trade_log.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Week"] = df["Date"].dt.isocalendar().week
    latest_week = df["Week"].max()
    report = df[df["Week"] == latest_week]
    total_trades = report.shape[0]
    wins = report[report["Result"] == "WIN"].shape[0]
    losses = report[report["Result"] == "LOSS"].shape[0]
    pnl = report["Capital"].iloc[-1] - report["Capital"].iloc[0] if total_trades > 1 else 0
    win_rate = (wins / total_trades) * 100 if total_trades else 0
    print(f"\n📊 Weekly Report (Week {latest_week})")
    print(f"Total Trades: {total_trades}, Wins: {wins}, Losses: {losses}, Win Rate: {win_rate:.2f}%")
    print(f"Net PnL: ₹{pnl:.2f}")
