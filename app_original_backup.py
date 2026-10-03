import re

import streamlit as st
import streamlit.components.v1 as components

from agent import run_investigation


st.set_page_config(
    page_title="Vyoma | AI With A Soul",
    page_icon="vyoma_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)


QUICK_PROMPTS = [
    "Summarize today's top AI news with sources.",
    "Fact-check a claim about climate change.",
    "Compare two companies and verify the data.",
    "Explain quantum computing in simple language.",
]


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg-1: #050816;
            --bg-2: #0d1230;
            --bg-3: #1b1147;
            --panel: rgba(12, 18, 46, 0.68);
            --panel-strong: rgba(9, 14, 38, 0.84);
            --border: rgba(255, 255, 255, 0.14);
            --gold: #ffd76a;
            --gold-strong: #ffb703;
            --cyan: #6ee7ff;
            --violet: #a78bfa;
            --text: #f8faff;
            --muted: #b7c2e1;
            --shadow: 0 28px 80px rgba(0, 0, 0, 0.35);
        }

        .stApp {
            color: var(--text);
            background:
                radial-gradient(circle at 20% 20%, rgba(111, 231, 255, 0.12), transparent 26%),
                radial-gradient(circle at 80% 10%, rgba(167, 139, 250, 0.18), transparent 22%),
                radial-gradient(circle at 50% 90%, rgba(255, 183, 3, 0.12), transparent 24%),
                linear-gradient(135deg, var(--bg-1), var(--bg-2) 45%, var(--bg-3));
            overflow-x: hidden;
        }

        .stApp::before,
        .stApp::after {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
        }

        .stApp::before {
            background-image:
                linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
            background-size: 42px 42px;
            mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.65), transparent 92%);
        }

        .stApp::after {
            background:
                radial-gradient(circle at 10% 30%, rgba(255, 215, 106, 0.16), transparent 18%),
                radial-gradient(circle at 85% 20%, rgba(110, 231, 255, 0.12), transparent 20%),
                radial-gradient(circle at 80% 80%, rgba(167, 139, 250, 0.14), transparent 24%);
            animation: skyDrift 14s ease-in-out infinite alternate;
        }

        @keyframes skyDrift {
            from { transform: translate3d(0, 0, 0) scale(1); }
            to { transform: translate3d(0, -18px, 0) scale(1.03); }
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(7, 11, 31, 0.95), rgba(14, 18, 44, 0.88));
            border-right: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 8px 0 40px rgba(0, 0, 0, 0.24);
        }

        [data-testid="stSidebar"] > div:first-child {
            background: transparent;
        }

        .vyoma-panel {
            position: relative;
            z-index: 1;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.09), rgba(255, 255, 255, 0.04));
            border: 1px solid var(--border);
            border-radius: 24px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(16px);
            padding: 1rem 1.15rem;
            overflow: hidden;
        }

        .vyoma-panel::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), transparent 35%, transparent 70%, rgba(255, 215, 106, 0.08));
            pointer-events: none;
        }

        .hero-shell {
            position: relative;
            z-index: 1;
            padding: 0.6rem 0 0.8rem;
        }

        .hero-copy {
            position: relative;
            z-index: 1;
            margin-bottom: 1rem;
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.45rem 0.9rem;
            border-radius: 999px;
            background: rgba(255, 215, 106, 0.12);
            border: 1px solid rgba(255, 215, 106, 0.25);
            color: #ffe39d;
            font-size: 0.82rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .hero-title {
            font-size: clamp(2.3rem, 5vw, 4.4rem);
            line-height: 0.96;
            font-weight: 800;
            margin: 0.7rem 0 0.8rem;
            letter-spacing: -0.04em;
        }

        .hero-title span {
            background: linear-gradient(90deg, #ffffff, #ffe39d, #8de7ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero-subtitle {
            color: var(--muted);
            font-size: 1.05rem;
            line-height: 1.65;
            max-width: 760px;
            margin-bottom: 1rem;
        }

        .hero-badges {
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
            margin-top: 0.8rem;
        }

        .hero-badge {
            padding: 0.5rem 0.85rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.14);
            color: #f4f7ff;
            font-size: 0.88rem;
        }

        .section-label {
            margin: 1rem 0 0.65rem;
            color: #fdf3c0;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            font-size: 0.82rem;
        }

        .mini-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.95rem;
            margin-top: 0.65rem;
        }

        .feature-card {
            position: relative;
            padding: 1rem;
            min-height: 160px;
            border-radius: 22px;
            background: linear-gradient(180deg, rgba(18, 25, 62, 0.86), rgba(12, 17, 40, 0.7));
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 22px 45px rgba(0, 0, 0, 0.26);
            transform-style: preserve-3d;
            transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease;
        }

        .feature-card:hover {
            transform: perspective(1000px) translateY(-8px) rotateX(6deg) rotateY(-6deg);
            box-shadow: 0 28px 60px rgba(0, 0, 0, 0.34);
            border-color: rgba(255, 215, 106, 0.28);
        }

        .feature-card::after {
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 22px;
            background: radial-gradient(circle at top right, rgba(255, 215, 106, 0.14), transparent 34%);
            pointer-events: none;
        }

        .feature-icon {
            font-size: 1.5rem;
            margin-bottom: 0.55rem;
        }

        .feature-title {
            font-size: 1.02rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
            color: #fff4ca;
        }

        .feature-text {
            color: var(--muted);
            line-height: 1.55;
            font-size: 0.94rem;
        }

        .stats-row {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.9rem;
            margin: 0.8rem 0 1.1rem;
        }

        .stat-card {
            padding: 0.95rem 1rem;
            border-radius: 20px;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.035));
            border: 1px solid rgba(255, 255, 255, 0.11);
            box-shadow: 0 18px 34px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-5px);
        }

        .stat-value {
            font-size: 1.5rem;
            font-weight: 800;
            color: #ffffff;
        }

        .stat-label {
            font-size: 0.9rem;
            color: var(--muted);
            margin-top: 0.2rem;
        }

        .prompt-wrap {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.85rem;
            margin-bottom: 1.1rem;
        }

        .stButton > button {
            width: 100%;
            border-radius: 18px;
            min-height: 74px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.09), rgba(255, 255, 255, 0.04));
            color: #f6f8ff;
            box-shadow: 0 16px 34px rgba(0, 0, 0, 0.22);
            transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
            white-space: normal;
            padding: 0.8rem 1rem;
            font-weight: 600;
        }

        .stButton > button:hover {
            transform: translateY(-4px);
            border-color: rgba(255, 215, 106, 0.35);
            box-shadow: 0 22px 40px rgba(0, 0, 0, 0.28);
            color: #fff5cf;
        }

        .stChatMessage {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.09), rgba(255, 255, 255, 0.035));
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 22px;
            box-shadow: 0 18px 38px rgba(0, 0, 0, 0.22);
            backdrop-filter: blur(16px);
        }

        [data-testid="chatAvatarIcon-user"] {
            color: #111425;
            background: linear-gradient(135deg, #ffe39d, #ffb703);
        }

        [data-testid="chatAvatarIcon-assistant"] {
            color: #06111e;
            background: linear-gradient(135deg, #8de7ff, #c4b5fd);
        }

        [data-testid="stChatInput"] {
            position: sticky;
            bottom: 1rem;
            z-index: 2;
        }

        [data-testid="stChatInput"] textarea {
            min-height: 70px !important;
            background: rgba(8, 12, 31, 0.88) !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 215, 106, 0.28) !important;
            border-radius: 18px !important;
            box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.04), 0 18px 32px rgba(0, 0, 0, 0.24) !important;
        }

        [data-testid="stChatInput"] textarea:focus {
            border-color: rgba(141, 231, 255, 0.72) !important;
            box-shadow: 0 0 0 1px rgba(141, 231, 255, 0.28), 0 0 26px rgba(141, 231, 255, 0.16) !important;
        }

        [data-testid="stExpander"] details {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 215, 106, 0.18);
            border-radius: 18px;
            overflow: hidden;
        }

        .stCodeBlock {
            border-radius: 18px;
        }

        .logo-frame {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 0.7rem;
            perspective: 1200px;
        }

        .logo-frame img {
            border-radius: 50%;
            box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.08), 0 0 40px rgba(255, 183, 3, 0.24);
            transition: transform 0.35s ease, box-shadow 0.35s ease;
        }

        .logo-frame img:hover {
            transform: rotateY(18deg) rotateX(10deg) scale(1.06);
            box-shadow: 0 0 50px rgba(255, 215, 106, 0.36), 0 18px 40px rgba(0, 0, 0, 0.35);
        }

        ::-webkit-scrollbar {
            width: 9px;
            height: 9px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(7, 9, 24, 0.75);
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, rgba(255, 215, 106, 0.72), rgba(141, 231, 255, 0.6));
            border-radius: 999px;
        }

        @media (max-width: 1050px) {
            .mini-grid,
            .stats-row {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 760px) {
            .mini-grid,
            .stats-row,
            .prompt-wrap {
                grid-template-columns: minmax(0, 1fr);
            }

            .hero-title {
                font-size: 2.2rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown('<div class="logo-frame">', unsafe_allow_html=True)
        try:
            st.image("vyoma_logo.png", width=145)
        except Exception:
            st.markdown("## Vyoma AI")
        st.markdown("</div>", unsafe_allow_html=True)

        st.title("Vyoma AI")
        st.caption("AI With A Soul")
        st.markdown("---")
        st.info("Powered by real-time verification and cross-source reasoning.")
        st.markdown("### Why this version feels alive")
        st.markdown("- 3D-inspired motion and glow")
        st.markdown("- Immersive cards and scene depth")
        st.markdown("- Faster exploration with prompt chips")
        st.markdown("- Verified answers with source-aware logic")

        st.markdown("---")
        st.markdown("### Core pipeline")
        st.markdown("1. Live search")
        st.markdown("2. Credibility scoring")
        st.markdown("3. Cross-reference validation")
        st.markdown("4. Soulful answer delivery")


def render_hero_scene() -> None:
    scene = """
    <style>
        body {
            margin: 0;
            background: transparent;
            overflow: hidden;
            font-family: Inter, system-ui, sans-serif;
        }

        .stage {
            position: relative;
            width: 100%;
            height: 360px;
            perspective: 1400px;
            overflow: hidden;
            border-radius: 28px;
            background:
                radial-gradient(circle at 20% 20%, rgba(141, 231, 255, 0.22), transparent 18%),
                radial-gradient(circle at 80% 20%, rgba(255, 215, 106, 0.18), transparent 22%),
                linear-gradient(135deg, rgba(7, 12, 31, 0.96), rgba(24, 18, 63, 0.94));
            border: 1px solid rgba(255, 255, 255, 0.09);
            box-shadow: inset 0 0 60px rgba(255, 255, 255, 0.04), 0 25px 55px rgba(0, 0, 0, 0.25);
        }

        .nebula {
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at 25% 30%, rgba(141, 231, 255, 0.18), transparent 16%),
                radial-gradient(circle at 72% 28%, rgba(167, 139, 250, 0.18), transparent 22%),
                radial-gradient(circle at 50% 75%, rgba(255, 183, 3, 0.14), transparent 18%);
            filter: blur(10px);
        }

        .stars {
            position: absolute;
            inset: 0;
            background-image:
                radial-gradient(circle, rgba(255, 255, 255, 0.95) 0.8px, transparent 1px),
                radial-gradient(circle, rgba(255, 255, 255, 0.7) 0.7px, transparent 1px),
                radial-gradient(circle, rgba(255, 255, 255, 0.55) 0.9px, transparent 1px);
            background-size: 120px 120px, 160px 160px, 220px 220px;
            background-position: 0 0, 35px 50px, 80px 20px;
            opacity: 0.65;
        }

        .grid {
            position: absolute;
            left: -12%;
            right: -12%;
            bottom: -28%;
            height: 58%;
            transform: rotateX(76deg);
            background-image:
                linear-gradient(rgba(141, 231, 255, 0.22) 1px, transparent 1px),
                linear-gradient(90deg, rgba(141, 231, 255, 0.18) 1px, transparent 1px);
            background-size: 38px 38px;
            mask-image: linear-gradient(to top, rgba(0, 0, 0, 1), transparent 75%);
        }

        .scene {
            position: absolute;
            inset: 0;
            transform-style: preserve-3d;
            transition: transform 180ms ease-out;
        }

        .ring {
            position: absolute;
            left: 50%;
            top: 52%;
            width: 280px;
            height: 280px;
            margin-left: -140px;
            margin-top: -140px;
            border-radius: 50%;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transform: translateZ(30px) rotateX(72deg);
            box-shadow: 0 0 30px rgba(110, 231, 255, 0.15);
        }

        .core {
            position: absolute;
            left: 50%;
            top: 48%;
            width: 116px;
            height: 116px;
            margin-left: -58px;
            margin-top: -58px;
            border-radius: 50%;
            background: radial-gradient(circle at 35% 35%, #fff7d1, #ffd76a 36%, #ff8a00 72%, rgba(255, 138, 0, 0.35));
            box-shadow:
                0 0 35px rgba(255, 215, 106, 0.7),
                0 0 90px rgba(255, 138, 0, 0.36),
                inset -20px -18px 30px rgba(0, 0, 0, 0.18);
            transform: translateZ(70px);
            animation: pulse 4s ease-in-out infinite;
        }

        .orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(0.2px);
            box-shadow: 0 0 24px currentColor;
        }

        .orb-one {
            width: 58px;
            height: 58px;
            left: 18%;
            top: 24%;
            color: rgba(141, 231, 255, 0.95);
            background: radial-gradient(circle at 35% 35%, #f7feff, #8de7ff 45%, rgba(141, 231, 255, 0.24));
            transform: translateZ(80px);
            animation: floatOne 8s ease-in-out infinite;
        }

        .orb-two {
            width: 44px;
            height: 44px;
            right: 18%;
            top: 28%;
            color: rgba(167, 139, 250, 0.9);
            background: radial-gradient(circle at 35% 35%, #ffffff, #b794ff 50%, rgba(167, 139, 250, 0.24));
            transform: translateZ(120px);
            animation: floatTwo 10s ease-in-out infinite;
        }

        .orb-three {
            width: 24px;
            height: 24px;
            right: 28%;
            bottom: 26%;
            color: rgba(255, 215, 106, 0.95);
            background: radial-gradient(circle at 35% 35%, #fffdf2, #ffd76a 52%, rgba(255, 215, 106, 0.24));
            transform: translateZ(140px);
            animation: floatThree 6s ease-in-out infinite;
        }

        .hud {
            position: absolute;
            left: 40px;
            bottom: 28px;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            transform: translateZ(100px);
        }

        .chip {
            padding: 10px 14px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: #eef6ff;
            font-size: 12px;
            letter-spacing: 0.04em;
            backdrop-filter: blur(10px);
        }

        .scan {
            position: absolute;
            inset: -10%;
            background: linear-gradient(180deg, transparent 40%, rgba(141, 231, 255, 0.05) 50%, transparent 60%);
            animation: scan 5.4s linear infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: translateZ(70px) scale(1); }
            50% { transform: translateZ(70px) scale(1.08); }
        }

        @keyframes floatOne {
            0%, 100% { transform: translate3d(0, 0, 80px); }
            50% { transform: translate3d(18px, -20px, 130px); }
        }

        @keyframes floatTwo {
            0%, 100% { transform: translate3d(0, 0, 120px); }
            50% { transform: translate3d(-16px, 18px, 165px); }
        }

        @keyframes floatThree {
            0%, 100% { transform: translate3d(0, 0, 140px); opacity: 0.75; }
            50% { transform: translate3d(12px, -16px, 180px); opacity: 1; }
        }

        @keyframes scan {
            from { transform: translateY(-42%); }
            to { transform: translateY(42%); }
        }
    </style>

    <div class="stage" id="stage">
        <div class="nebula"></div>
        <div class="stars"></div>
        <div class="grid"></div>
        <div class="scene" id="scene">
            <div class="ring"></div>
            <div class="core"></div>
            <div class="orb orb-one"></div>
            <div class="orb orb-two"></div>
            <div class="orb orb-three"></div>
            <div class="hud">
                <div class="chip">3D Presence</div>
                <div class="chip">Verified Search</div>
                <div class="chip">Interactive Soul UI</div>
            </div>
        </div>
        <div class="scan"></div>
    </div>

    <script>
        const stage = document.getElementById("stage");
        const scene = document.getElementById("scene");

        stage.addEventListener("mousemove", (event) => {
            const rect = stage.getBoundingClientRect();
            const x = (event.clientX - rect.left) / rect.width;
            const y = (event.clientY - rect.top) / rect.height;
            const rotateY = (x - 0.5) * 18;
            const rotateX = (0.5 - y) * 14;
            scene.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });

        stage.addEventListener("mouseleave", () => {
            scene.style.transform = "rotateX(0deg) rotateY(0deg)";
        });
    </script>
    """
    components.html(scene, height=360)


def render_hero_copy() -> None:
    st.markdown(
        """
        <div class="hero-shell">
            <div class="hero-copy">
                <div class="eyebrow">Vyoma Experience Upgrade</div>
                <div class="hero-title">A more <span>3D, cinematic, interactive</span> AI front end</div>
                <div class="hero-subtitle">
                    This redesigned interface keeps your investigation engine intact while making the product feel premium:
                    spatial depth, hover motion, layered glass surfaces, quick prompt interactions, and a futuristic presence
                    that matches the idea of "AI With A Soul."
                </div>
                <div class="hero-badges">
                    <div class="hero-badge">Realtime verification flow preserved</div>
                    <div class="hero-badge">3D-inspired motion design</div>
                    <div class="hero-badge">Interactive prompt launcher</div>
                    <div class="hero-badge">Streamlit-friendly implementation</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stats() -> None:
    st.markdown(
        """
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-value">3D</div>
                <div class="stat-label">Scene depth and hover perspective</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">Live</div>
                <div class="stat-label">Existing web-backed investigation engine</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">Fast</div>
                <div class="stat-label">Prompt chips shorten time to first question</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">Soul</div>
                <div class="stat-label">Warm visual language and emotional tone</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_cards() -> None:
    st.markdown(
        """
        <div class="section-label">Experience Layers</div>
        <div class="mini-grid">
            <div class="feature-card">
                <div class="feature-icon">🌌</div>
                <div class="feature-title">Spatial Hero</div>
                <div class="feature-text">
                    A built-in animated scene creates depth and makes the first impression feel closer to a product landing page than a plain tool.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">✨</div>
                <div class="feature-title">Glass Conversations</div>
                <div class="feature-text">
                    Chat bubbles, panels, and cards use layered translucency and glow for a polished futuristic feel without hurting readability.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Quick Launch Prompts</div>
                <div class="feature-text">
                    Visitors can tap prompt cards to start a conversation instantly, making the app feel more alive and guided.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quick_prompts() -> None:
    st.markdown('<div class="section-label">Try A Live Prompt</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    columns = [col1, col2]

    for idx, prompt in enumerate(QUICK_PROMPTS):
        with columns[idx % 2]:
            if st.button(prompt, key=f"quick_prompt_{idx}", use_container_width=True):
                st.session_state["queued_prompt"] = prompt


def parse_response(raw_text: str) -> tuple[str, str]:
    thinking_match = re.search(r"<thinking>(.*?)</thinking>", raw_text, re.DOTALL)
    answer_match = re.search(r"<answer>(.*?)</answer>", raw_text, re.DOTALL)

    thinking_text = thinking_match.group(1).strip() if thinking_match else ""
    answer_text = answer_match.group(1).strip() if answer_match else raw_text
    return thinking_text, answer_text


def handle_chat_turn(prompt: str) -> None:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Vyoma is investigating with soul and precision..."):
            history = st.session_state.messages[:-1]
            try:
                raw_ai_response = run_investigation(prompt, history)
            except Exception as exc:
                raw_ai_response = (
                    "<answer>I'm having trouble connecting to my investigation engine right now. "
                    "Please try again in a moment.</answer>"
                )
                st.error(f"Agent Error: {exc}")

        thinking_text, answer_text = parse_response(raw_ai_response)

        if thinking_text:
            with st.expander("View Vyoma's Thinking", expanded=False):
                st.code(thinking_text, language="markdown")

        st.markdown(answer_text)

    st.session_state.messages.append({"role": "assistant", "content": answer_text})


def render_chat_history() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main() -> None:
    inject_global_styles()
    render_sidebar()

    if "queued_prompt" not in st.session_state:
        st.session_state["queued_prompt"] = None

    left, right = st.columns([1.2, 1])

    with left:
        render_hero_copy()
        render_stats()
        render_feature_cards()

    with right:
        render_hero_scene()

    st.markdown('<div class="vyoma-panel">', unsafe_allow_html=True)
    render_quick_prompts()
    render_chat_history()
    st.markdown("</div>", unsafe_allow_html=True)

    typed_prompt = st.chat_input("Talk to Vyoma... ask, verify, compare, or explore.")
    prompt_to_process = typed_prompt or st.session_state.get("queued_prompt")

    if prompt_to_process:
        st.session_state["queued_prompt"] = None
        handle_chat_turn(prompt_to_process)


if __name__ == "__main__":
    main()
