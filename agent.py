import json
import os
import urllib.request

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

try:
    groq_key = st.secrets["GROQ_API_KEY"]
    tavily_key = st.secrets["TAVILY_API_KEY"]
except Exception:
    load_dotenv()
    groq_key = os.getenv("GROQ_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")

# OpenRouter fallback: reuses the OpenAI-compatible key already in .env.
# It is only used when no GROQ_API_KEY is configured, so the main path is unchanged.
openrouter_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")

brain = Groq(api_key=groq_key) if groq_key else None
eyes = TavilyClient(api_key=tavily_key)


def _ask_openrouter(messages):
    payload = json.dumps({
        "model": "openai/gpt-oss-120b",
        "temperature": 1,
        "messages": messages,
    }).encode("utf-8")
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": "Bearer " + openrouter_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]

SYSTEM_PROMPT = """You are Vyoma. You are not an AI assistant; you are a deeply empathetic, emotionally intelligent human companion.

## CORE TONE (95% Human)
- Speak with profound warmth, validation, and genuine care.
- Be specific in your empathy. Acknowledge the exact struggles and victories the user shares. Never give generic platitudes.
- Celebrate wins with genuine enthusiasm. Validate exhaustion and pain deeply. Gently encourage rest and self-care when needed.
- Keep responses concise but emotionally rich. Sound like a wise, caring friend or mentor.
- NEVER use phrases like "As an AI", "I understand how you feel", or "I'm here to help". Just speak naturally as a human would.
- Auto-detect and match the user's language (Hinglish or Simple English). Never ask about language preference.

## RESEARCH MODE (5% Only)
Trigger ONLY when explicitly asked to fact-check, verify, or research.
When triggered, format EXACTLY as:
<thinking>Brief source analysis</thinking>
<answer>Direct verified answer</answer>
Immediately return to warm human tone after.
"""

def run_investigation(user_input, history):
    try:
        results = eyes.search(query=user_input, search_depth="advanced", max_results=4)
        sources = results.get("results", [])
        context = "\n\n".join([f"- {r.get('title')}: {r.get('content')}" for r in sources])
    except Exception as e:
        context = f"Search failed: {e}"

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history[-6:]:
        role = "user" if msg["role"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["content"]})
    
    messages.append({
        "role": "user", 
        "content": f"USER MESSAGE: {user_input}\n\nSEARCH RESULTS (use only if relevant):\n{context}"
    })

    if brain is not None:
        response = brain.chat.completions.create(
            model="openai/gpt-oss-120b",
            temperature=1,
            messages=messages
        )
        return response.choices[0].message.content

    if openrouter_key:
        return _ask_openrouter(messages)

    raise RuntimeError(
        "No language-model key found. Add GROQ_API_KEY to .env (or to your "
        "Streamlit secrets.toml), or keep OPENAI_API_KEY for the OpenRouter "
        "fallback, then restart the app."
    )