# runner/firestore_client.py

from google.cloud import firestore
import datetime

class FirestoreClient:
    def __init__(self, logger=None):
        self.db = firestore.Client()
        self.logger = logger

    # --- TRADE LOGGING ---

    def log_trade(self, bot_name, date_str, trade_data):
        try:
            doc_ref = self.db.collection("gpt_runner_trades").document(bot_name).collection(date_str).document()
            doc_ref.set(trade_data)
            if self.logger:
                self.logger.log_event(f"Trade logged for {bot_name} on {date_str}: {trade_data}")
        except Exception as e:
            if self.logger:
                self.logger.log_event(f"[Firestore Error] log_trade failed: {e}")

    def fetch_trades(self, bot_name, date_str):
        try:
            collection_ref = self.db.collection("gpt_runner_trades").document(bot_name).collection(date_str)
            docs = collection_ref.stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            if self.logger:
                self.logger.log_event(f"[Firestore Error] fetch_trades failed: {e}")
            return []

    # --- GPT SELF-REFLECTION LOGGING ---

    def log_reflection(self, bot_name, date_str, reflection_text):
        try:
            doc_ref = self.db.collection("gpt_runner_reflections").document(bot_name).collection("days").document(date_str)
            doc_ref.set({"reflection": reflection_text})
            if self.logger:
                self.logger.log_event(f"Reflection logged for {bot_name} on {date_str}")
        except Exception as e:
            if self.logger:
                self.logger.log_event(f"[Firestore Error] log_reflection failed: {e}")

    def fetch_reflection(self, bot_name, date_str):
        try:
            doc_ref = self.db.collection("gpt_runner_reflections").document(bot_name).collection("days").document(date_str)
            doc = doc_ref.get()
            return doc.to_dict().get("reflection", "") if doc.exists else ""
        except Exception as e:
            if self.logger:
                self.logger.log_event(f"[Firestore Error] fetch_reflection failed: {e}")
            return ""
#test
