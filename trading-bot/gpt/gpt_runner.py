import os
from datetime import datetime
from gpt_helper import analyze_error, summarize_trades, suggest_improvements, ask_gpt
import json

FOLDERS = ["stock_trading", "futures", "oiscalpe"]
REPORT_DIR = "./reports"
CONFIG_DIR = "./gpt/config"
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

def read_file_if_exists(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def generate_gpt_config(error_log, trade_log):
    prompt = f"""
    You are a trading bot strategist. Based on today's trading errors and trades below,
    suggest a JSON configuration to improve tomorrow’s bot performance.

    Errors:
    {error_log}

    Trades:
    {trade_log}

    Include:
    - max_trades (int)
    - use_vwap (true/false)
    - vwap_start_time (HH:MM)
    - atr_multiplier (float)
    - entry_filter_strictness (low, medium, high)

    Output the JSON only.
    """
    response = ask_gpt(prompt)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"error": "Failed to parse GPT config response", "raw": response}

def run_gpt_runner():
    today = datetime.now().strftime("%Y-%m-%d")
    all_trade_logs = ""
    all_error_logs = ""

    for folder in FOLDERS:
        trade_path = os.path.join(folder, "trade_log.csv")
        error_path = os.path.join(folder, "error_log.txt")

        trade_log = read_file_if_exists(trade_path)
        error_log = read_file_if_exists(error_path)

        if trade_log:
            all_trade_logs += f"\n--- Trades from {folder} ---\n" + trade_log + "\n"
        if error_log:
            all_error_logs += f"\n--- Errors from {folder} ---\n" + error_log + "\n"

    print("\n[1] Analyzing all errors...")
    error_analysis = analyze_error(all_error_logs)
    print("[2] Summarizing all trade performance...")
    trade_summary = summarize_trades(all_trade_logs)
    print("[3] Suggesting improvements based on combined data...")
    improvement_suggestions = suggest_improvements(all_error_logs + "\n" + all_trade_logs)
    print("[4] Generating GPT Config for bot...")
    gpt_config = generate_gpt_config(all_error_logs, all_trade_logs)

    with open(f"{REPORT_DIR}/analysis_report_{today}.txt", "w", encoding="utf-8") as f:
        f.write("=== ERROR ANALYSIS ===\n\n" + error_analysis + "\n\n")
        f.write("=== TRADE SUMMARY ===\n\n" + trade_summary + "\n")

    with open(f"{REPORT_DIR}/improvement_ideas_{today}.md", "w", encoding="utf-8") as f:
        f.write("# 📈 Improvement Ideas\n\n")
        f.write(improvement_suggestions)

    with open(f"{CONFIG_DIR}/gpt_config_{today}.json", "w", encoding="utf-8") as f:
        json.dump(gpt_config, f, indent=4)

    print("\n✅ GPT Runner completed. Check the 'reports' and 'gpt/config' folders.")

if __name__ == "__main__":
    run_gpt_runner()
