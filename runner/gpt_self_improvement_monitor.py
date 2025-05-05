import datetime
import os
from runner.firestore_client import FirestoreClient
from runner.logger import Logger
from runner.openai_manager import ask_gpt
from runner.secret_manager_client import access_secret

logger = Logger("logs/gpt_reflection.log")
firestore_client = FirestoreClient(logger=logger)

def summarize_trades(trades):
    if not trades:
        return "No trades were taken today."

    lines = []
    for trade in trades:
        status = trade.get("status", "open").upper()
        lines.append(
            f"{trade['symbol']} | {trade['strategy']} | Entry: {trade['entry_price']} | "
            f"Exit: {trade.get('exit_price', '-')}, Status: {status}"
        )
    return "\n".join(lines)


def run_gpt_reflection(bot_name):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    trades = firestore_client.fetch_trades(bot_name, today)

    trade_summary = summarize_trades(trades)
    prompt = f"""
You're a trading analyst AI. Review today's trades and suggest improvements.

### TRADE SUMMARY:
{trade_summary}

### TASK:
- Identify patterns in SL/Target hits.
- Suggest strategy improvements.
- Detect overtrading or missed opportunities.
- Suggest SL/target updates or filters.
- Format output cleanly as markdown.
"""
    print("\n[GPT] Reflecting on trades...")
    reflection = ask_gpt(prompt)

    # Save to Firestore
    firestore_client.log_reflection(bot_name, today, reflection)

    # Also log locally
    with open("logs/gpt_reflection.jsonl", "a") as f:
        f.write(
            f'{{"timestamp": "{datetime.datetime.now().isoformat()}", "bot": "{bot_name}", "summary": "{reflection}"}}\n'
        )
    print("[GPT] Reflection complete. Summary saved.")

