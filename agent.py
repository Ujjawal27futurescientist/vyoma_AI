import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

# --- LOAD SECRETS ---
try:
    groq_key = st.secrets["GROQ_API_KEY"]
    tavily_key = st.secrets["TAVILY_API_KEY"]
except KeyError:
    load_dotenv()
    groq_key = os.getenv("GROQ_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")

# --- INITIALIZE ---
brain = Groq(api_key=groq_key)
eyes = TavilyClient(api_key=tavily_key)

SYSTEM_PROMPT = """You are Vyoma, an expert investigative AI. You verify facts, check sources, and provide accurate answers.

Format your response EXACTLY like this:

<thinking>
Analyze the search results, check credibility, cross-reference facts
</thinking>

<answer>
Your final answer here
</answer>
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
        "content": f"QUESTION: {user_input}\n\nSEARCH RESULTS:\n{context}"
    })

    response = brain.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=messages
    )
    
    return response.choices[0].message.content