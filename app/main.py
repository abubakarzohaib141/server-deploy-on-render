# app/main.py
from __future__ import annotations

import asyncio
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.settings import settings
from app.schemas import ChatRequest, ChatResponse, Message
from app.chatbot import run_sync  # sync function that calls abagentsdk Agent.run(...)

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
# DEV: allow all (works with http-server on port 5500, Next dev, etc.)
# PROD: tighten to Vercel (*.vercel.app) or your own domains.
ENV = os.getenv("ENV", "local").lower()

if ENV != "prod":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,  # must be False when using "*"
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_origin_regex=r"^https:\/\/.*\.vercel\.app$",  # allow Vercel previews/prod
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"ok": True, "name": app.title, "status": "running", "env": ENV}

@app.post("/v1/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    try:
        messages = [m.model_dump() for m in req.messages]
        answer: str = await asyncio.to_thread(run_sync, messages)
        return ChatResponse(message=Message(role="assistant", content=answer))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent Error: {e}")

@app.get("/", include_in_schema=False)
def index():
    return {"ok": True, "routes": ["/health", "POST /v1/chat", "/docs"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
