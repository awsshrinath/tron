from datetime import datetime

class GPTSelfImprovementMonitor:
    def __init__(self, logger, firestore_client, openai_manager):
        self.logger = logger
        self.firestore = firestore_client
        self.openai = openai_manager

    def analyze(self, bot_name):
        today = datetime.now().strftime("%Y-%m-%d")

        # 1. Fetch today's trades from Firestore
        trades = self.firestore.fetch_trades(bot_name, today)
        if not trades:
            self.logger.log_event(f"No trades found for {bot_name} on {today}, skipping GPT reflection.")
            return

        # 2. Build prompt for GPT
        prompt = f"""You are an expert trading assistant.
Today’s trades for bot '{bot_name}' on {today} are:\n
{trades}

Please analyze:
- Were entries optimal?
- Did we exit too early or late?
- Any risk or momentum issues?
- Suggestions for tomorrow’s improvement.
"""

        # 3. Send to OpenAI
        reflection = self.openai.get_suggestion(prompt)

        # 4. Save reflection to Firestore
        self.firestore.log_reflection(bot_name, today, reflection)

        # 5. Log event
        self.logger.log_event(f"GPT Reflection Logged for {bot_name}: {reflection}")
