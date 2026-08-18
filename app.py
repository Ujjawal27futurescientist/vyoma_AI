import streamlit as st
import re
from agent import run_investigation

# --- PREMIUM PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Vyoma | Critical Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LIVELY 3D UI STYLES (REPLACES OLD CSS) ---
st.markdown("""
<style>
    /* 1. Animated Deep Space Background */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #ffffff;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. 3D Logo with Glow and Color Shift on Hover */
    .logo-container {
        text-align: center;
        margin-bottom: 2rem;
        padding-top: 20px;
    }
    .logo-container img {
        width: 220px;
        border-radius: 50%;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.4);
        transition: all 0.5s ease;
        cursor: pointer;
    }
    .logo-container img:hover {
        transform: scale(1.1);
        box-shadow: 0 0 60px rgba(255, 215, 0, 1), 0 0 100px rgba(255, 100, 0, 0.6);
        animation: vibrate 0.2s linear infinite, hueShift 2s infinite;
    }
    @keyframes vibrate {
        0% { transform: translate(0, 0) scale(1.1); }
        25% { transform: translate(-2px, 2px) scale(1.1); }
        50% { transform: translate(2px, -2px) scale(1.1); }
        75% { transform: translate(-2px, -2px) scale(1.1); }
        100% { transform: translate(2px, 2px) scale(1.1); }
    }
    @keyframes hueShift {
        0% { filter: hue-rotate(0deg); }
        50% { filter: hue-rotate(45deg); }
        100% { filter: hue-rotate(0deg); }
    }

    /* 3. Glassmorphism Chat Bubbles & Sidebar */
    .stChatMessage, section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* 4. Glowing Input Box */
    .stChatInput > div > div > input {
        background: rgba(0, 0, 0, 0.4);
        color: #fff !important;
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 15px;
        transition: all 0.3s ease;
    }
    .stChatInput > div > div > input:focus {
        border-color: #ffd700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    }

    /* 5. Expander Styling for Analysis Protocol */
    .streamlit-expanderHeader {
        background-color: rgba(255, 215, 0, 0.1) !important;
        color: #ffd700 !important;
        font-weight: bold;
        border-radius: 10px;
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    .streamlit-expanderContent {
        background-color: rgba(0, 0, 0, 0.3);
        border-left: 3px solid #ffd700;
        font-family: 'Courier New', monospace;
        color: #e0e0e0;
        border-radius: 0 0 10px 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- DISPLAY LOGO AT TOP OF MAIN AREA ---
st.markdown('<div class="logo-container"><img src="images/vyoma_logo.png" alt="Vyoma AI"></div>', unsafe_allow_html=True)

# --- SIDEBAR BRANDING ---
with st.sidebar:
    try:
        st.image("images/vyoma_logo.png", width=80)
    except Exception:
        st.markdown("# 🧠")
    st.title("Vyoma AI")
    st.markdown("---")
    st.info("**Powered by Real-Time Verification**")
    st.caption("Vyoma does not guess. It searches live sources, evaluates credibility, and cross-references facts before answering.")
    st.markdown("---")
    st.markdown("### How Vyoma works:")
    st.markdown("1. 🔍 **Live Search**: Accesses real-time web data.")
    st.markdown("2. 🧠 **Critical Analysis**: Evaluates source bias.")
    st.markdown("3. ️ **Fact-Check**: Cross-references multiple outlets.")

# --- MAIN CHAT INTERFACE ---
st.title("🧠 Vyoma Critical Intelligence")
st.caption("Ask any question. Watch Vyoma think. Get the truth.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter a query to be fact-checked..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching live sources and analyzing facts..."):
            history = st.session_state.messages[:-1]
            raw_ai_response = run_investigation(prompt, history)

        thinking_match = re.search(r'<thinking>(.*?)</thinking>', raw_ai_response, re.DOTALL)
        thinking_text = thinking_match.group(1).strip() if thinking_match else "Analysis data unavailable."

        answer_match = re.search(r'<answer>(.*?)</answer>', raw_ai_response, re.DOTALL)
        answer_text = answer_match.group(1).strip() if answer_match else raw_ai_response

        with st.expander("🧠 View Critical Analysis Protocol", expanded=False):
            st.code(thinking_text, language="markdown")

        st.markdown(answer_text)

    st.session_state.messages.append({"role": "assistant", "content": answer_text})