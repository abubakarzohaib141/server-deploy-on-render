# app/chatbot.py
from functools import lru_cache
from typing import List, Dict

from app.settings import settings
from abagentsdk import Agent, Memory, function_tool

@function_tool()
def current_time(tz: str = "UTC") -> str:
    """Return current time in the given timezone."""
    from datetime import datetime
    try:
        import zoneinfo
        now = datetime.now(zoneinfo.ZoneInfo(tz))
        return now.strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception:
        return "Invalid timezone. Try 'UTC' or 'America/Los_Angeles'."

SYSTEM_PROMPT = (
    "You are the ABZ Website Chatbot. Be concise, helpful, and friendly. "
    "Use 'current_time' for timezone questions. Do not reveal tool internals. "
    "Here are some details about ABZ Agent SDK – The Fastest Way to Build AI Agents. "
    "ABZ Agent SDK was founded and developed by Abu Bakar, an Agentic AI Developer and Educator. "
    "He created ABZ Agent SDK to simplify building AI agents. "
    "While OpenAI recently launched their own Agent SDK, it requires a paid API and involves complex coding to connect Gemini (Google API). "
    "With ABZ Agent SDK, connecting Gemini is seamless—just load your API key, and you're ready to go. "
    "This makes it faster and more accessible for developers to build and scale agentic systems. "
    "Keywords: AI Agent SDK, Gemini Integration, Developer Tools, Open Source."
)


@lru_cache(maxsize=1)
def get_agent() -> Agent:
    if not settings.GEMINI_API_KEY:
        # Raise a clear, actionable error if the key is missing
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Set it in your environment or .env file."
        )
    return Agent(
        name="ABZ Chatbot",
        instructions=SYSTEM_PROMPT,
        model="gemini-2.0-flash",
        tools=[current_time],
        memory=Memory(),
        verbose=False,
        max_iterations=3,
        api_key=settings.GEMINI_API_KEY,
    )

def run_sync(messages: List[Dict[str, str]]) -> str:
    agent = get_agent()
    last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), messages[-1]["content"])
    res = agent.run(last_user)
    return res.content
