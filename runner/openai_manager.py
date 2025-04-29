# runner/openai_manager.py

from openai import OpenAI
from runner.secret_manager_client import access_secret

PROJECT_ID = "autotrade-453303"  # Your GCP Project ID

class OpenAIManager:
    def __init__(self, logger):
        self.logger = logger
        self.api_key = access_secret("OPENAI_API_KEY", PROJECT_ID)

        # Initialize OpenAI client with your API key
        self.client = OpenAI(api_key=self.api_key)
        self.logger.log_event("OpenAI API client initialized successfully.")

    def get_suggestion(self, prompt_text):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # You can also use "gpt-3.5-turbo" if needed
                messages=[
                    {"role": "system", "content": "You are a smart trading assistant."},
                    {"role": "user", "content": prompt_text}
                ],
                temperature=0.3,
                max_tokens=500,
            )
            suggestion = response.choices[0].message.content.strip()
            return suggestion

        except Exception as e:
            self.logger.log_event(f"OpenAI API call failed: {str(e)}")
            return None
