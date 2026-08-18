import streamlit as st
import re
from agent import run_investigation  # Ensure this module exists in your directory

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Vyoma | AI With A Soul",
    page_icon="vyoma_logo.png",  # Fallback to emoji if file missing
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- LIGHT LIVELY CSS (No blur for performance) ---
st.markdown("""
<style>
    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 300% 300%;
        animation: gradientBG 18s ease infinite;
        color: #fff;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Logo Styling: Glow + Vibrate on Hover */
    [data-testid="stImage"] img {
        border-radius: 50%;
        transition: all .4s ease;
        cursor: pointer;
    }
    [data-testid="stImage"] img:hover {
        box-shadow: 0 0 40px rgba(255, 200, 80, .9), 0 0 90px rgba(255, 140, 0, .5);
        animation: vibrate .25s linear infinite;
    }
    @keyframes vibrate {
        0% { transform: translate(0, 0); }
        25% { transform: translate(-2px, 2px); }
        50% { transform: translate(2px, -2px); }
        75% { transform: translate(-2px, -2px); }
        100% { transform: translate(0, 0); }
    }

    /* Chat Bubbles: Light Glass Effect */
    .stChatMessage {
        background: rgba(255, 255, 255, .06);
        border: 1px solid rgba(255, 255, 255, .12);
        border-radius: 18px;
    }

    /* Golden Glowing Input Box */
    [data-testid="stChatInput"] textarea {
        background: rgba(0, 0, 0, .35) !important;
        color: #fff !important;
        border: 1px solid rgba(255, 215, 0, .35) !important;
        border-radius: 14px !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 18px rgba(255, 215, 0, .45) !important;
    }

    /* Thinking Expander Styling */
    [data-testid="stExpander"] details {
        background: rgba(255, 255, 255, .05);
        border: 1px solid rgba(255, 215, 0, .25);
        border-radius: 12px;
    }
    
    /* Custom Scrollbar for Webkit */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0f0c29; }
    ::-webkit-scrollbar-thumb { background: #302b63; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    try:
        st.image("vyoma_logo.png", width=140)
    except Exception:
        st.markdown("## 🌌 Vyoma AI")
    
    st.title("Vyoma AI")
    st.caption("✨ AI With A Soul")
    st.markdown("---")
    
    st.info("**Powered by Real-Time Verification**")
    st.caption("Vyoma does not guess. It searches live sources, evaluates credibility, and cross-references facts before answering.")
    
    st.markdown("---")
    st.markdown("### How Vyoma works:")
    st.markdown("1. 🔍 **Live Search** — real-time web data")
    st.markdown("2. 💛 **Soulful Talk** — feels your mood, matches your language")
    st.markdown("3. ⚖️ **Fact-Check** — cross-references outlets")

# --- HEADER ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    try:
        st.image("vyoma_logo.png", width=170)
    except Exception:
        pass
    st.title("Vyoma")
    st.caption("AI With A Soul — ask anything, feel the difference.")

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Talk to Vyoma… ask anything or fact-check something…"):
    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("💛 Vyoma is thinking…"):
            history = st.session_state.messages[:-1]
            
            try:
                raw_ai_response = run_investigation(prompt, history)
            except Exception as e:
                raw_ai_response = f"<answer>I'm having trouble connecting to my investigation engine right now. Please try again.</answer>"
                st.error(f"Agent Error: {str(e)}")

        # Parse Structured Response (<thinking> and <answer> tags)
        thinking_match = re.search(r'<thinking>(.*?)</thinking>', raw_ai_response, re.DOTALL)
        thinking_text = thinking_match.group(1).strip() if thinking_match else ""
        
        answer_match = re.search(r'<answer>(.*?)</answer>', raw_ai_response, re.DOTALL)
        answer_text = answer_match.group(1).strip() if answer_match else raw_ai_response

        # Render Thinking Process (Collapsible)
        if thinking_text:
            with st.expander("✨ View Vyoma's Thinking", expanded=False):
                st.code(thinking_text, language="markdown")
        
        # Render Final Answer
        st.markdown(answer_text)

    # Append final answer to history (excluding internal thinking tags)
    st.session_state.messages.append({"role": "assistant", "content": answer_text})