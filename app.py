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

# --- CUSTOM CSS FOR THE PREMIUM DARK LOOK ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .streamlit-expanderHeader {
        background-color: #161b22 !important;
        color: #58a6ff !important;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid #30363d;
    }
    .streamlit-expanderContent {
        background-color: #0d1117;
        border-left: 3px solid #58a6ff;
        font-family: 'Courier New', monospace;
        color: #c9d1d9;
    }
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR BRANDING ---
with st.sidebar:
    try:
        st.image("images/vyoma_logo.png", width=100)
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
    st.markdown("3. ⚖️ **Fact-Check**: Cross-references multiple outlets.")

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