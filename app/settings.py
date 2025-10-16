# app/settings.py
import os
from dotenv import load_dotenv

# Load .env from the repo root (or current working dir)
load_dotenv()

class Settings:
    APP_NAME: str = "ABZ Agent API"
    # ENV controls CORS behavior in main.py ("prod" vs anything else)
    ENV: str = os.getenv("ENV", "dev")

    # ✅ Define GEMINI_API_KEY so the attribute always exists
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")

    def as_dict(self):
        # helper for debugging/health
        return {
            "APP_NAME": self.APP_NAME,
            "ENV": self.ENV,
            "HAS_GEMINI_KEY": bool(self.GEMINI_API_KEY),
        }

settings = Settings()
