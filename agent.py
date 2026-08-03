import os
import streamlit as st
from dotenv import load_dotenv
import requests
from tavily import TavilyClient

# --- LOAD SECRETS (Cloud vs Local) ---
try:
    router_key = st.secrets["OPENROUTER_API_KEY"]
    tavily_key = st.secrets["TAVILY_API_KEY"]
except KeyError:
    load_dotenv()
    router_key = os.getenv("OPENROUTER_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")

# --- INITIALIZE TOOLS ---
eyes = TavilyClient(api_key=tavily_key)

# --- THE CRITICAL THINKING PROMPT ---
SYSTEM_PROMPT = """You are Vyoma, an expert investigative AI with a core directive for absolute factual accuracy. You do not guess; you verify.

You will be given a user's QUESTION and LIVE SEARCH RESULTS from the web. 
Your job is to analyze these results, check for bias, and synthesize a truthful answer.

You MUST format your final response using these exact XML tags:

<thinking>
1. Source Evaluation: Briefly state what sources you found and rate their credibility.
2. Bias Check: Identify if any source has a clear bias.
3. Fact-Checking: Cross-reference the claims. State what is proven fact vs disputed.
4. Synthesis: Explain how you are forming your final answer based ONLY on credible facts.
</thinking>

<answer>
Provide the final, clean, and direct answer to the user. Do not include your internal reasoning here. Always provide citations/links if applicable.
</answer>
"""

def run_investigation(user_input, history):
    # 1. Use Tavily to search the live web
    try:
        results = eyes.search(query=user_input, search_depth="advanced", max_results=4)
        sources = results.get("results", [])
        context = "\n\n".join([f"- {r.get('title')}: {r.get('content')} (Source: {r.get('url')})" for r in sources])
    except Exception as e:
        context = f"(Live search failed: {e})"

    # 2. Build the message history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history[-6:]:
        role = "user" if msg["role"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["content"]})
        
    messages.append({
        "role": "user", 
        "content": f"QUESTION: {user_input}\n\nLIVE SEARCH RESULTS:\n{context}"
    })

    # 3. Direct API call to OpenRouter (NO openai library!)
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {router_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://vyoma.streamlit.app",
        "X-Title": "Vyoma AI"
    }
    payload = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "temperature": 0,
        "messages": messages
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        return f"<answer>Error: {response.text}</answer>"
    
    return response.json()["choices"][0]["message"]["content"]