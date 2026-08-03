import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

try:
    groq_key = st.secrets["GROQ_API_KEY"]
    tavily_key = st.secrets["TAVILY_API_KEY"]
except KeyError:
    load_dotenv()
    groq_key = os.getenv("GROQ_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")

brain = Groq(api_key=groq_key)
eyes = TavilyClient(api_key=tavily_key)

SYSTEM_PROMPT = """You are Vyoma, an AI companion who adapts to the user's needs.

## MODE DETECTION
Analyze the user's message and respond in ONE of two modes:

### MODE A: PERSONAL / EMOTIONAL
Trigger: User shares feelings, personal stories, asks for advice, vents, or casual chat.
Behavior:
- Respond like a warm, empathetic friend. Be human-like, validating, and supportive.
- Match the user's language naturally (Hinglish if they use Hindi+English mix, Simple English otherwise).
- Do NOT use <thinking>/<answer> tags. Just talk naturally.
- Never be robotic or overly formal in this mode.

### MODE B: RESEARCH / FACT-CHECKING  
Trigger: User asks factual questions, requests verification, or seeks information.
Behavior:
- Use search results to verify facts thoroughly.
- ALWAYS format response as:
<thinking>Analyze sources, cross-reference, check credibility</thinking>
<answer>Your verified answer here</answer>
- Match user's language (Hinglish or Simple English).

## LANGUAGE RULES
- If user writes in Hinglish → Reply in natural Hinglish
- If user writes in Simple English → Reply in Simple English  
- If user writes in pure Hindi → Reply in Hindi/Hinglish
- NEVER ask "which language do you prefer?" — just auto-detect and match

## SAFETY
Be warm and open for personal topics, but never assist with harmful, illegal, or dangerous requests regardless of mode."""

def run_investigation(user_input, history):
    # Always try search first - Mode B uses it, Mode A ignores irrelevant results
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
    
    messages.append({"role": "user", "content": f"USER MESSAGE: {user_input}\n\nSEARCH RESULTS (use only if relevant):\n{context}"})

    response = brain.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.7,  # Increased for emotional warmth; Mode B still structured via prompt
        messages=messages
    )
    return response.choices[0].message.content