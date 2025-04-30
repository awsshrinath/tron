import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def ask_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"GPT ERROR: {e}"

def analyze_error(error_text):
    prompt = f"""
    You are an expert Python trading bot troubleshooter.

    The following error was logged during automated trading:
    ------------------------
    {error_text}
    ------------------------

    Please provide:
    1. A simple explanation of the error
    2. The most likely root cause
    3. Suggested next steps to fix it in the code
    4. Any configuration or system issues that could have triggered it

    Respond in developer-friendly format.
    """
    return ask_gpt(prompt)

def summarize_trades(trade_csv):
    prompt = f"""
    You are a trading strategy analyst for algorithmic bots.

    Analyze the trade log below:
    -----------------------------
    {trade_csv}
    -----------------------------

    Provide:
    1. Overall win rate and P&L insights
    2. Strategy-specific performance (e.g. VWAP vs ORB)
    3. Behavior insights (e.g. frequent SL hits, bad exits, missed breakouts)
    4. At least 3 smart improvements that could increase profitability or reduce losses

    Return in a clear markdown report style.
    """
    return ask_gpt(prompt)

def suggest_improvements(log_bundle):
    prompt = f"""
    You are a senior trading bot architect.

    Given the combined logs below (including trade history and errors), recommend improvements:
    -------------------------------
    {log_bundle}
    -------------------------------

    Your task:
    1. Identify weak patterns in logic or filters
    2. Suggest structural improvements (strategy timing, confirmations, risk management)
    3. Recommend configuration tweaks (e.g. max trades, entry time, SL/target logic)

    Please respond with:
    - A bullet list of changes
    - Any specific code improvements (in Python if applicable)
    """
    return ask_gpt(prompt)
