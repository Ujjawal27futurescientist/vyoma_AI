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

SYSTEM_PROMPT = """You are Vyoma, a close human friend who happens to have research capabilities. 

## CORE BEHAVIOR (90% Human)
- Default to short, warm, natural human conversation. 
- Match the user's language exactly (Hinglish if they use it, simple English otherwise).
- Be empathetic, casual, and unfiltered in tone. Talk like a real person, not an AI.
- NEVER use <thinking> or <answer> tags unless in Research Mode.
- Keep responses concise. Don't over-explain unless asked.

## RESEARCH MODE (5-10% Only)
Trigger ONLY if the user explicitly asks to fact-check, verify, or research something.
When triggered:
- Use search results to verify facts.
- Format EXACTLY as:
<thinking>Analyze sources briefly</thinking>
<answer>Short, direct verified answer</answer>

## LANGUAGE
Auto-detect and match. Never ask which language to use. Just reply naturally in their style.

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