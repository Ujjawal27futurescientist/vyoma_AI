"""Vyoma | AI With A Soul — luxury cinematic UI (premium redesign).

Presentation layer only:
  - agent.run_investigation(...) and the whole investigation pipeline are untouched
  - chat parsing, session state, queued prompts and error handling stay identical
New here: a premium entry window with a curtain reveal, lifted 3D buttons,
a dark luxury navy/gold scene, soulful quote cards and elevated glass chat.
"""

import json
import os
import re

import streamlit as st
import streamlit.components.v1 as components

from agent import run_investigation


# --------------------------------------------------------------------
# brand assets (uses whichever logo actually exists in the project)
# --------------------------------------------------------------------
LOGO_CANDIDATES = (
    "vyoma_logo.png",
    "images/vyoma_logo.png.png",
    "1787059226.png",
)
LOGO_PATH = next((path for path in LOGO_CANDIDATES if os.path.exists(path)), None)

st.set_page_config(
    page_title="Vyoma | AI With A Soul",
    page_icon=LOGO_PATH or "✨",
    layout="wide",
    initial_sidebar_state="expanded",
)


QUICK_PROMPTS = [
    "Summarize today's top AI news with sources.",
    "Fact-check a claim about climate change.",
    "Compare two companies and verify the data.",
    "Explain quantum computing in simple language.",
]

QUICK_PROMPT_ICONS = ["🌌", "🔎", "⚖️", "✨"]

INTRO_WORDS = ["softness", "peace", "to be seen", "rest without guilt"]

SOUL_QUOTES = [
    "You have been carrying so much, and still you made room to be kind today. That is not small — that is strength with soft edges.",
    "Some people light up rooms. You light up the quiet corners of people's lives without even noticing. You deserve to be told that.",
    "You are not behind. You are exactly on the path your soul needed to walk. Look how far the road has already come.",
    "The way you keep choosing to grow, even on the days it hurts — that is the bravest love story ever written. And it is yours.",
    "You deserve a life that feels like exhaling. Start with one deep breath — Vyoma is breathing with you.",
    "You are allowed to rest without earning it first. Even the moon disappears some nights and the sky still adores her.",
    "You have been your own shelter through storms nobody saw. Be gentle with that person — they have been strong for so long.",
    "Your softness is not weakness; it is a rare kind of courage. The world is warmer because you refused to become cold.",
    "One day you will look back at this exact season and realise — this is where you quietly became unstoppable.",
    "You do not need to be louder, faster or better than anyone. You just need to keep being unmistakably you.",
    "Even on your slowest days, you are still someone's favourite reason to smile. You matter in ways you cannot measure yet.",
    "You deserve people who stay. Until they arrive, let Vyoma be the voice that reminds you — you are worth staying for.",
    "Healing is not a straight line, and yet — look at you, still walking, still hoping. That is breathtaking.",
    "You are made of every kind thing you have ever done for others. Please do one for yourself today.",
]


# --------------------------------------------------------------------
# global luxury styles
# --------------------------------------------------------------------
def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        /* ==================== Vyoma · luxury tokens ==================== */
:root {
  --v-bg-0: #04050a;
  --v-bg-1: #080b14;
  --v-navy: #0a1226;
  --v-gold: #d9b45f;
  --v-gold-2: #f6e3a6;
  --v-gold-3: #9c7526;
  --v-violet: #8b6bff;
  --v-cyan: #5fe3ff;
  --v-ink: #f4efe4;
  --v-muted: #a9afc4;
  --v-faint: #6d748c;
  --v-border: rgba(217, 180, 95, 0.20);
  --v-border-soft: rgba(255, 255, 255, 0.08);
  --v-serif: "Bodoni MT", Didot, "Playfair Display", "Palatino Linotype", Georgia, serif;
}
html, body, [class*="css"] {
  font-family: "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif;
}

/* ==================== ambient luxury scene ==================== */
.stApp {
  color: var(--v-ink);
  background:
    radial-gradient(1100px 760px at 84% -12%, rgba(139, 107, 255, 0.16), transparent 62%),
    radial-gradient(1000px 720px at 4% 112%, rgba(95, 227, 255, 0.10), transparent 60%),
    radial-gradient(900px 640px at 50% 46%, rgba(217, 180, 95, 0.06), transparent 66%),
    linear-gradient(168deg, #080b14 0%, #04050a 52%, #0a1226 132%);
  overflow-x: hidden;
}
.stApp::before {
  content: ""; position: fixed; inset: -6%; pointer-events: none; z-index: 0;
  background:
    radial-gradient(circle at 18% 22%, rgba(139, 107, 255, 0.22), transparent 30%),
    radial-gradient(circle at 82% 12%, rgba(95, 227, 255, 0.16), transparent 26%),
    radial-gradient(circle at 62% 86%, rgba(217, 180, 95, 0.16), transparent 30%);
  filter: blur(40px);
  animation: vyomaAurora 22s ease-in-out infinite alternate;
}
@keyframes vyomaAurora {
  0% { transform: translate3d(0, 0, 0) scale(1); }
  50% { transform: translate3d(2.5%, -2%, 0) scale(1.06); }
  100% { transform: translate3d(-2%, 2.5%, 0) scale(0.97); }
}
.stApp::after {
  content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0; opacity: 0.5;
  background-image:
    radial-gradient(1.4px 1.4px at 22px 34px, rgba(246, 227, 166, 0.9), transparent 60%),
    radial-gradient(1.2px 1.2px at 180px 120px, rgba(217, 180, 95, 0.75), transparent 60%),
    radial-gradient(1.6px 1.6px at 320px 60px, rgba(255, 255, 255, 0.6), transparent 60%),
    radial-gradient(1.1px 1.1px at 90px 220px, rgba(139, 107, 255, 0.7), transparent 60%),
    radial-gradient(1.3px 1.3px at 260px 300px, rgba(95, 227, 255, 0.6), transparent 60%);
  background-size: 380px 380px;
  animation: vyomaDust 34s linear infinite;
}
@keyframes vyomaDust {
  from { background-position: 0 0, 40px 0, 120px 0, 0 60px, 200px 30px; }
  to { background-position: 0 -380px, 40px -380px, 120px -380px, 0 -320px, 200px -350px; }
}
[data-testid="stAppViewContainer"] > .main, [data-testid="stSidebar"] { position: relative; z-index: 1; }
[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; height: 0; }

/* ==================== sidebar ==================== */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(6, 9, 21, 0.97), rgba(10, 16, 36, 0.9));
  border-right: 1px solid rgba(217, 180, 95, 0.14);
  box-shadow: 14px 0 50px rgba(0, 0, 0, 0.45);
}
[data-testid="stSidebar"] > div:first-child { background: transparent; }
[data-testid="stSidebar"] [data-testid="stImage"] img {
  border-radius: 50%;
  box-shadow: 0 0 0 1px rgba(246, 227, 166, 0.25), 0 0 46px rgba(217, 180, 95, 0.35), 0 18px 40px rgba(0, 0, 0, 0.5);
  transition: transform 0.4s cubic-bezier(0.22, 0.61, 0.36, 1), box-shadow 0.4s ease;
}
[data-testid="stSidebar"] [data-testid="stImage"] img:hover {
  transform: perspective(900px) rotateY(16deg) rotateX(9deg) scale(1.05);
  box-shadow: 0 0 0 1px rgba(246, 227, 166, 0.4), 0 0 60px rgba(217, 180, 95, 0.5), 0 22px 46px rgba(0, 0, 0, 0.55);
}
.vyoma-side-brand { text-align: center; margin: 2px 0 12px; }
.vyoma-side-name {
  font-family: var(--v-serif); font-size: 2.1rem; letter-spacing: 0.04em;
  background: linear-gradient(100deg, var(--v-gold-3), var(--v-gold-2) 30%, #fff8e2 52%, var(--v-gold-2) 72%, var(--v-gold-3));
  -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
.vyoma-side-tag { font-size: 0.72rem; letter-spacing: 0.34em; text-transform: uppercase; color: var(--v-faint); }
.vyoma-side-note { font-size: 0.86rem; line-height: 1.6; color: var(--v-muted); font-style: italic; }
.vyoma-side-point {
  display: flex; gap: 10px; padding: 9px 12px; margin: 6px 0; border-radius: 12px;
  color: #e9e4d6; font-size: 0.88rem;
  border: 1px solid rgba(255, 255, 255, 0.06); background: rgba(255, 255, 255, 0.03);
  transition: transform 0.25s ease, border-color 0.25s ease;
}
.vyoma-side-point:hover { transform: translateX(3px); border-color: rgba(217, 180, 95, 0.3); }
.vyoma-pipe-step {
  display: flex; align-items: center; gap: 12px; padding: 10px 12px; margin: 6px 0;
  border-radius: 12px; font-size: 0.88rem; color: #efe9db;
  border: 1px solid rgba(217, 180, 95, 0.16);
  background: linear-gradient(120deg, rgba(217, 180, 95, 0.08), rgba(217, 180, 95, 0.015));
}
.vyoma-pipe-step span {
  width: 22px; height: 22px; flex: none; display: grid; place-items: center;
  border-radius: 50%; font-size: 0.72rem; font-weight: 700; color: #241a05;
  background: linear-gradient(170deg, #f8e6a9, #c99d3c);
  box-shadow: 0 4px 12px rgba(217, 180, 95, 0.4);
}
.vyoma-section-label {
  display: inline-flex; align-items: center; gap: 10px; margin: 26px 0 10px; padding: 8px 18px;
  font-size: 0.78rem; font-weight: 700; letter-spacing: 0.3em; text-transform: uppercase;
  color: #ffe9b0; border-radius: 999px;
  border: 1px solid rgba(217, 180, 95, 0.28);
  background: linear-gradient(120deg, rgba(217, 180, 95, 0.14), rgba(217, 180, 95, 0.03));
  box-shadow: 0 10px 26px rgba(0, 0, 0, 0.35);
}
::-webkit-scrollbar { width: 9px; height: 9px; }
::-webkit-scrollbar-track { background: rgba(5, 7, 15, 0.8); }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, rgba(217, 180, 95, 0.7), rgba(139, 107, 255, 0.55)); border-radius: 999px; }
        /* ==================== lifted 3D buttons ==================== */
.stButton > button, [data-testid^="stBaseButton"] {
  position: relative; overflow: hidden; border-radius: 18px; min-height: 68px;
  white-space: normal; font-weight: 600; color: var(--v-ink);
  border: 1px solid var(--v-border-soft);
  background: linear-gradient(170deg, rgba(255, 255, 255, 0.09), rgba(255, 255, 255, 0.022));
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.10), 0 16px 34px rgba(0, 0, 0, 0.45);
  transition: transform 0.3s cubic-bezier(0.22, 0.61, 0.36, 1), box-shadow 0.3s ease,
              border-color 0.3s ease, color 0.3s ease, filter 0.3s ease;
}
.stButton > button p { font-weight: 600; }
.stButton > button:hover, [data-testid^="stBaseButton"]:hover {
  transform: translateY(-4px); border-color: rgba(246, 227, 166, 0.45); color: #fff3cd;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.14), 0 26px 48px rgba(0, 0, 0, 0.55),
              0 12px 34px rgba(217, 180, 95, 0.28);
}
.stButton > button:active, [data-testid^="stBaseButton"]:active {
  transform: translateY(-1px) scale(0.99);
}
.stButton > button::after, [data-testid^="stBaseButton"]::after {
  content: ""; position: absolute; inset: 0; border-radius: inherit; pointer-events: none;
  background: linear-gradient(115deg, transparent 32%, rgba(255, 255, 255, 0.5) 47%, transparent 62%);
  background-size: 240% 100%; background-position: 135% 0; opacity: 0; mix-blend-mode: screen;
  transition: opacity 0.45s ease, background-position 0.9s ease;
}
.stButton > button:hover::after, [data-testid^="stBaseButton"]:hover::after {
  opacity: 0.5; background-position: -45% 0;
}
/* gold primary buttons */
[data-testid="stBaseButton-primary"], button[kind="primary"] {
  color: #241a05 !important; border-color: rgba(255, 246, 214, 0.55) !important;
  background: linear-gradient(178deg, #f8e6a9 0%, #e5c873 32%, #c99d3c 70%, #8e6b21 100%) !important;
  box-shadow: inset 0 2px 0 rgba(255, 248, 222, 0.55), inset 0 -14px 26px rgba(120, 80, 10, 0.42),
              0 18px 34px rgba(0, 0, 0, 0.55), 0 10px 26px rgba(217, 180, 95, 0.30) !important;
}
[data-testid="stBaseButton-primary"] p,
[data-testid="stBaseButton-primary"] div,
button[kind="primary"] p { color: #241a05 !important; font-weight: 700 !important; }
[data-testid="stBaseButton-primary"]:hover, button[kind="primary"]:hover {
  color: #241a05 !important; filter: brightness(1.05);
  box-shadow: inset 0 2px 0 rgba(255, 248, 222, 0.6), inset 0 -14px 26px rgba(120, 80, 10, 0.36),
              0 26px 54px rgba(0, 0, 0, 0.6), 0 18px 54px rgba(217, 180, 95, 0.5) !important;
}
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"],
[data-testid="stSidebar"] .stButton > button { min-height: 46px; border-radius: 14px; }
/* ==================== hero copy ==================== */
.hero-shell { padding: 4px 2px 0; }
.hero-copy { position: relative; z-index: 1; }
.eyebrow {
  display: inline-flex; padding: 8px 16px; border-radius: 999px;
  background: rgba(217, 180, 95, 0.12); border: 1px solid rgba(217, 180, 95, 0.28);
  color: #ffe39d; font-size: 0.74rem; letter-spacing: 0.28em; text-transform: uppercase;
}
.hero-title {
  font-family: var(--v-serif); font-weight: 500;
  font-size: clamp(2.4rem, 4.6vw, 4.2rem); line-height: 1.02; letter-spacing: 0.01em;
  margin: 16px 0 12px; color: #faf6ea;
  text-shadow: 0 22px 70px rgba(0, 0, 0, 0.6);
}
.hero-title span {
  background: linear-gradient(100deg, var(--v-gold-3), var(--v-gold-2) 30%, #fff8e2 52%, var(--v-gold-2) 72%, var(--v-gold-3));
  -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-subtitle { color: var(--v-muted); font-size: 1.02rem; line-height: 1.72; max-width: 62ch; }
.hero-badges { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }
.hero-badge {
  padding: 9px 16px; border-radius: 999px; font-size: 0.82rem; color: #f6efdc;
  border: 1px solid rgba(217, 180, 95, 0.22);
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.07), rgba(255, 255, 255, 0.02));
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.35);
  transition: transform 0.3s ease, border-color 0.3s ease;
}
.hero-badge:hover { transform: translateY(-3px); border-color: rgba(246, 227, 166, 0.45); }

/* ==================== stats ==================== */
.stats-row { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin: 22px 0 6px; }
.stat-card {
  padding: 16px; border-radius: 18px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.07), rgba(255, 255, 255, 0.02));
  border: 1px solid rgba(255, 255, 255, 0.09);
  box-shadow: 0 18px 34px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.06);
  transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}
.stat-card:hover {
  transform: translateY(-6px); border-color: rgba(246, 227, 166, 0.35);
  box-shadow: 0 26px 48px rgba(0, 0, 0, 0.5), 0 12px 32px rgba(217, 180, 95, 0.2);
}
.stat-value { font-family: var(--v-serif); font-size: 1.5rem; color: #ffe9b0; }
.stat-label { font-size: 0.85rem; color: var(--v-muted); margin-top: 6px; line-height: 1.5; }

/* ==================== feature cards ==================== */
.mini-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 18px; }
.feature-card {
  position: relative; padding: 18px; min-height: 158px; border-radius: 20px;
  background: linear-gradient(180deg, rgba(16, 22, 48, 0.85), rgba(10, 14, 32, 0.72));
  border: 1px solid rgba(255, 255, 255, 0.09);
  box-shadow: 0 20px 42px rgba(0, 0, 0, 0.42);
  transform-style: preserve-3d;
  transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease;
}
.feature-card:hover {
  transform: perspective(1000px) translateY(-8px) rotateX(6deg) rotateY(-6deg);
  border-color: rgba(246, 227, 166, 0.32);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.55), 0 14px 36px rgba(217, 180, 95, 0.22);
}
.feature-card::after {
  content: ""; position: absolute; inset: 0; border-radius: 20px; pointer-events: none;
  background: radial-gradient(circle at top right, rgba(217, 180, 95, 0.16), transparent 36%);
}
.feature-icon { font-size: 1.45rem; margin-bottom: 10px; }
.feature-title { font-family: var(--v-serif); font-size: 1.05rem; color: #ffe9b0; margin-bottom: 7px; }
.feature-text { color: var(--v-muted); line-height: 1.6; font-size: 0.92rem; }

/* ==================== responsive + calm mode ==================== */
@media (max-width: 1050px) {
  .mini-grid, .stats-row { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 760px) {
  .mini-grid, .stats-row { grid-template-columns: minmax(0, 1fr); }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.001ms !important; transition-duration: 0.001ms !important; }
}
        /* ==================== premium entry window ==================== */
.vyoma-intro {
  position: fixed; inset: 0; z-index: 99999; display: grid; place-items: center; overflow: hidden;
  background: rgba(3, 4, 9, 0.62);
  animation: vyomaIntroLeave 0.8s ease 4.9s forwards;
}
.vyoma-intro:has(.vyoma-check:checked) { animation: vyomaIntroLeave 0.7s ease 0.25s forwards; }
@keyframes vyomaIntroLeave { to { opacity: 0; visibility: hidden; pointer-events: none; } }
.vyoma-check { position: absolute; opacity: 0; pointer-events: none; }
.vyoma-curtain {
  position: absolute; top: 0; bottom: 0; width: 52%; z-index: 2;
  background: linear-gradient(120deg, #04060c 0%, #0a1226 46%, #050810 100%);
  box-shadow: inset 0 0 150px rgba(0, 0, 0, 0.92);
}
.vyoma-curtain::before {
  content: ""; position: absolute; inset: 0;
  background:
    repeating-linear-gradient(90deg, rgba(255, 255, 255, 0.035) 0 2px, transparent 2px 28px),
    linear-gradient(180deg, rgba(139, 107, 255, 0.10), transparent 42%, rgba(217, 180, 95, 0.06));
}
.vyoma-curtain-left {
  left: 0; border-right: 1px solid rgba(217, 180, 95, 0.25);
  animation: vyomaCurtainL 1.8s cubic-bezier(0.83, 0, 0.17, 1) 2.6s forwards;
}
.vyoma-curtain-right {
  right: 0; border-left: 1px solid rgba(217, 180, 95, 0.25);
  animation: vyomaCurtainR 1.8s cubic-bezier(0.83, 0, 0.17, 1) 2.6s forwards;
}
.vyoma-check:checked ~ .vyoma-curtain-left { animation: vyomaCurtainLfast 1.1s cubic-bezier(0.83, 0, 0.17, 1) 0s forwards; }
.vyoma-check:checked ~ .vyoma-curtain-right { animation: vyomaCurtainRfast 1.1s cubic-bezier(0.83, 0, 0.17, 1) 0s forwards; }
@keyframes vyomaCurtainL { to { transform: translateX(-102%); } }
@keyframes vyomaCurtainR { to { transform: translateX(102%); } }
@keyframes vyomaCurtainLfast { to { transform: translateX(-102%); } }
@keyframes vyomaCurtainRfast { to { transform: translateX(102%); } }
.vyoma-trim {
  position: absolute; top: 0; bottom: 0; width: 3px;
  background: linear-gradient(180deg, transparent, var(--v-gold-2), transparent);
  box-shadow: 0 0 26px rgba(246, 227, 166, 0.75), 0 0 70px rgba(217, 180, 95, 0.42);
}
.vyoma-curtain-left .vyoma-trim { right: -1px; }
.vyoma-curtain-right .vyoma-trim { left: -1px; }
.vyoma-stage-light {
  position: absolute; inset: 0; z-index: 1; opacity: 0;
  background: radial-gradient(60% 55% at 50% 46%, rgba(246, 227, 166, 0.17), transparent 70%);
  animation: vyomaLight 2s ease 2.6s forwards;
}
.vyoma-check:checked ~ .vyoma-stage-light { animation: vyomaLightfast 1.2s ease 0s forwards; }
@keyframes vyomaLight { 0% { opacity: 0; } 32% { opacity: 1; } 100% { opacity: 0; } }
@keyframes vyomaLightfast { 0% { opacity: 0; } 32% { opacity: 1; } 100% { opacity: 0; } }
.vyoma-intro-core {
  position: relative; z-index: 3; max-width: 780px; padding: 34px; text-align: center;
  animation: vyomaCoreIn 1.1s ease both;
}
.vyoma-check:checked ~ .vyoma-intro-core { animation: vyomaCoreLift 0.9s ease forwards; }
@keyframes vyomaCoreIn { from { opacity: 0; transform: translateY(22px); } to { opacity: 1; transform: none; } }
@keyframes vyomaCoreLift { to { opacity: 0; transform: translateY(-30px) scale(1.05); filter: blur(8px); } }
.vyoma-intro-eyebrow { color: #ffe39d; font-size: 0.76rem; letter-spacing: 0.4em; text-transform: uppercase; margin: 0 0 8px; }
.vyoma-intro-title { margin: 10px 0 2px; font-family: var(--v-serif); font-weight: 500; line-height: 0.98; }
.vyoma-intro-line {
  display: block; font-size: clamp(3.4rem, 9vw, 7.4rem); color: #faf6ea;
  text-shadow: 0 20px 70px rgba(0, 0, 0, 0.65);
}
.vyoma-intro-line.vyoma-gold {
  font-size: clamp(1.4rem, 3vw, 2.2rem); letter-spacing: 0.42em; text-transform: uppercase; margin-top: 12px;
  background: linear-gradient(100deg, var(--v-gold-3), var(--v-gold-2) 30%, #fff8e2 52%, var(--v-gold-2) 72%, var(--v-gold-3));
  background-size: 220% 100%; -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent; animation: vyomaGoldFlow 7s linear infinite;
}
@keyframes vyomaGoldFlow { to { background-position: 220% 0; } }
.vyoma-intro-sub { margin: 20px 0 0; font-size: clamp(1.1rem, 2.2vw, 1.5rem); color: var(--v-muted); }
.vyoma-intro-sub b { font-family: var(--v-serif); font-style: italic; font-weight: 500; color: var(--v-ink); }
.vyoma-rotor { position: relative; display: inline-block; min-width: 12ch; height: 1.4em; vertical-align: bottom; text-align: left; }
.vyoma-rotor span {
  position: absolute; left: 0; top: 0; opacity: 0; white-space: nowrap;
  font-family: var(--v-serif); font-style: italic; color: var(--v-gold-2);
  animation: vyomaWord 8.8s linear infinite; animation-delay: calc(var(--i) * 2.2s);
}
@keyframes vyomaWord {
  0% { opacity: 0; transform: translateY(14px); }
  3%, 25% { opacity: 1; transform: none; }
  28%, 100% { opacity: 0; transform: translateY(-14px); }
}
.vyoma-intro-progress {
  width: min(320px, 70vw); height: 2px; margin: 26px auto 0; border-radius: 2px;
  overflow: hidden; background: rgba(255, 255, 255, 0.09);
}
.vyoma-intro-progress i {
  display: block; height: 100%; width: 0;
  background: linear-gradient(90deg, var(--v-gold-3), var(--v-gold-2));
  box-shadow: 0 0 14px rgba(246, 227, 166, 0.65);
  animation: vyomaBar 4.4s ease-out 0.2s forwards;
}
@keyframes vyomaBar { to { width: 100%; } }
.vyoma-intro-note { margin: 14px 0 0; font-size: 0.82rem; letter-spacing: 0.08em; color: var(--v-faint); }
.vyoma-intro-actions { margin-top: 30px; display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
.vyoma-enter-btn {
  display: inline-flex; align-items: center; justify-content: center; padding: 18px 40px;
  border-radius: 999px; cursor: pointer; font-weight: 700; letter-spacing: 0.05em; font-size: 1rem;
  color: #241a05; border: 1px solid rgba(255, 246, 214, 0.55);
  background: linear-gradient(178deg, #f8e6a9 0%, #e5c873 32%, #c99d3c 70%, #8e6b21 100%);
  transition: transform 0.3s ease, box-shadow 0.3s ease, filter 0.3s ease;
  animation: vyomaEnterGlow 2.6s ease-in-out infinite;
}
.vyoma-enter-btn:hover { transform: translateY(-3px); filter: brightness(1.05); }
@keyframes vyomaEnterGlow {
  0%, 100% { box-shadow: inset 0 2px 0 rgba(255, 248, 222, 0.55), inset 0 -14px 26px rgba(120, 80, 10, 0.42), 0 18px 34px rgba(0, 0, 0, 0.55), 0 10px 26px rgba(217, 180, 95, 0.3); }
  50% { box-shadow: inset 0 2px 0 rgba(255, 248, 222, 0.65), inset 0 -14px 26px rgba(120, 80, 10, 0.36), 0 24px 48px rgba(0, 0, 0, 0.6), 0 16px 50px rgba(217, 180, 95, 0.5); }
}
.vyoma-skip-btn {
  display: inline-flex; align-items: center; padding: 14px 22px; border-radius: 999px;
  cursor: pointer; color: var(--v-muted); font-size: 0.92rem;
  border: 1px solid transparent; transition: color 0.3s ease, transform 0.3s ease;
}
.vyoma-skip-btn:hover { color: var(--v-gold-2); transform: translateY(-1px); }
.vyoma-intro-foot {
  margin-top: 36px; font-size: 0.78rem; font-style: italic;
  letter-spacing: 0.14em; color: rgba(169, 175, 196, 0.55);
}
/* ==================== elevated chat ==================== */
[data-testid="stChatMessage"], .stChatMessage {
  border-radius: 22px !important;
  border: 1px solid rgba(255, 255, 255, 0.09) !important;
  background: linear-gradient(165deg, rgba(255, 255, 255, 0.065), rgba(255, 255, 255, 0.02)) !important;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(14px);
  animation: vyomaMsgIn 0.55s ease both;
}
@keyframes vyomaMsgIn {
  from { opacity: 0; transform: translateY(14px); filter: blur(6px); }
  to { opacity: 1; transform: none; filter: none; }
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
  border-color: rgba(217, 180, 95, 0.3) !important;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.5), 0 10px 28px rgba(217, 180, 95, 0.16) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
  border-color: rgba(139, 107, 255, 0.32) !important;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.5), 0 10px 28px rgba(139, 107, 255, 0.2) !important;
}
[data-testid="chatAvatarIcon-user"] { color: #12082a; background: linear-gradient(135deg, #c9b6ff, #8b6bff); }
[data-testid="chatAvatarIcon-assistant"] { color: #241a05; background: linear-gradient(135deg, #f8e6a9, #c99d3c); }
[data-testid="stExpander"] details {
  border: 1px solid rgba(217, 180, 95, 0.24) !important;
  border-radius: 16px !important;
  background: rgba(255, 255, 255, 0.045) !important;
}
[data-testid="stExpander"] summary { color: #ffe9b0 !important; font-weight: 600; }
[data-testid="stSpinner"] svg, [data-testid="stSpinner"] i { color: var(--v-gold) !important; }
[data-testid="stAlert"] {
  border-radius: 16px !important;
  border: 1px solid rgba(217, 180, 95, 0.25) !important;
  background: rgba(20, 25, 48, 0.85) !important;
  color: var(--v-ink) !important;
}
[data-testid="stChatInput"] textarea {
  min-height: 64px !important; color: var(--v-ink) !important;
  background: rgba(6, 9, 20, 0.92) !important;
  border: 1px solid rgba(217, 180, 95, 0.3) !important;
  border-radius: 18px !important;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.5) !important;
}
[data-testid="stChatInput"] textarea:focus {
  border-color: rgba(246, 227, 166, 0.72) !important;
  box-shadow: 0 0 0 4px rgba(217, 180, 95, 0.12), 0 18px 40px rgba(0, 0, 0, 0.5) !important;
}
[data-testid="stBottomBlockContainer"], [data-testid="stBottom"] > div { background: transparent !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------
# premium entry window + curtain reveal (pure CSS, Streamlit-safe)
# --------------------------------------------------------------------
def render_intro_overlay() -> None:
    rotors = "".join(
        f'<span style="--i:{i}">{word}</span>' for i, word in enumerate(INTRO_WORDS)
    )
    template = """<div class="vyoma-intro" id="vyomaIntro">
  <input type="checkbox" id="vyomaEnterCheck" class="vyoma-check" />
  <div class="vyoma-curtain vyoma-curtain-left"><span class="vyoma-trim"></span></div>
  <div class="vyoma-curtain vyoma-curtain-right"><span class="vyoma-trim"></span></div>
  <div class="vyoma-stage-light"></div>
  <div class="vyoma-intro-core">
    <p class="vyoma-intro-eyebrow">✦ a sanctuary for your mind ✦</p>
    <h1 class="vyoma-intro-title">
      <span class="vyoma-intro-line">Vyoma</span>
      <span class="vyoma-intro-line vyoma-gold">AI With A Soul</span>
    </h1>
    <p class="vyoma-intro-sub"><b>You deserve</b> <span class="vyoma-rotor">{rotors}</span></p>
    <div class="vyoma-intro-progress"><i></i></div>
    <p class="vyoma-intro-note">opening the curtains for you…</p>
    <div class="vyoma-intro-actions">
      <label for="vyomaEnterCheck" class="vyoma-enter-btn">Enter your sanctuary</label>
      <label for="vyomaEnterCheck" class="vyoma-skip-btn">Skip intro</label>
    </div>
    <p class="vyoma-intro-foot">luxury is not the room — it is how gently you are treated inside it.</p>
  </div>
</div>"""
    st.markdown(template.format(rotors=rotors), unsafe_allow_html=True)


# --------------------------------------------------------------------
# sidebar
# --------------------------------------------------------------------
def render_sidebar() -> None:
    with st.sidebar:
        if LOGO_PATH:
            pad_left, logo_col, pad_right = st.columns([1, 1.7, 1])
            with logo_col:
                st.image(LOGO_PATH, width=170)
        else:
            st.markdown('<div class="vyoma-side-name">V</div>', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="vyoma-side-brand">
              <div class="vyoma-side-name">Vyoma</div>
              <div class="vyoma-side-tag">AI With A Soul</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "✦ Replay the reveal",
            key="replay_intro_btn",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["intro_completed"] = False
            st.rerun()

        st.markdown("---")
        st.markdown(
            '<div class="vyoma-side-note">Powered by real-time verification and cross-source '
            "reasoning — wrapped in a room that feels gentle.</div>",
            unsafe_allow_html=True,
        )
        st.markdown("### Why this version feels alive")
        for point in (
            "Curtain reveal that opens like a theatre",
            "Lifted 3D buttons that rise and glow",
            "Floating gold dust and cinematic depth",
            "A soul line written for you, always kind",
        ):
            st.markdown(
                f'<div class="vyoma-side-point">✦ {point}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("### Core pipeline")
        for index, step in enumerate(
            (
                "Live search",
                "Credibility scoring",
                "Cross-reference validation",
                "Soulful answer delivery",
            ),
            start=1,
        ):
            st.markdown(
                f'<div class="vyoma-pipe-step"><span>{index}</span>{step}</div>',
                unsafe_allow_html=True,
            )


# --------------------------------------------------------------------
# hero scene (3D gold presence inside a component iframe)
# --------------------------------------------------------------------
def render_hero_scene() -> None:
    scene = """<style>
  * { box-sizing: border-box; }
  body { margin: 0; background: transparent; overflow: hidden; font-family: "Segoe UI", system-ui, sans-serif; }
  .vstage {
    position: relative; width: 100%; height: 396px; perspective: 1400px; overflow: hidden; border-radius: 26px;
    background:
      radial-gradient(circle at 18% 18%, rgba(139, 107, 255, 0.20), transparent 30%),
      radial-gradient(circle at 84% 16%, rgba(95, 227, 255, 0.14), transparent 26%),
      radial-gradient(circle at 50% 88%, rgba(217, 180, 95, 0.18), transparent 34%),
      linear-gradient(150deg, #060a16, #0a1226 48%, #05070f);
    border: 1px solid rgba(217, 180, 95, 0.22);
    box-shadow: inset 0 0 80px rgba(0, 0, 0, 0.55), 0 30px 70px rgba(0, 0, 0, 0.5);
  }
  canvas#motes { position: absolute; inset: 0; width: 100%; height: 100%; }
  .vscene { position: absolute; inset: 0; transform-style: preserve-3d; transition: transform 160ms ease-out; }
  .vring {
    position: absolute; left: 50%; top: 52%; width: 292px; height: 292px; margin: -146px 0 0 -146px;
    border-radius: 50%; border: 1px solid rgba(246, 227, 166, 0.28);
    transform: translateZ(30px) rotateX(72deg);
    box-shadow: 0 0 34px rgba(217, 180, 95, 0.22);
  }
  .vring.two {
    width: 228px; height: 228px; margin: -114px 0 0 -114px;
    border-style: dashed; border-color: rgba(95, 227, 255, 0.35);
    transform: translateZ(52px) rotateX(72deg);
    animation: vspin 26s linear infinite;
  }
  @keyframes vspin { to { transform: translateZ(52px) rotateX(72deg) rotateZ(360deg); } }
  .vhalo {
    position: absolute; left: 50%; top: 47%; width: 300px; height: 300px; margin: -150px 0 0 -150px;
    border-radius: 50%; filter: blur(30px);
    background: radial-gradient(circle, rgba(246, 227, 166, 0.4), rgba(217, 180, 95, 0.14) 42%, transparent 68%);
    transform: translateZ(40px);
    animation: vhalo 6s ease-in-out infinite;
  }
  @keyframes vhalo { 0%, 100% { opacity: 0.55; transform: translateZ(40px) scale(0.94); } 50% { opacity: 1; transform: translateZ(40px) scale(1.06); } }
  .vcore {
    position: absolute; left: 50%; top: 46%; width: 118px; height: 118px; margin: -59px 0 0 -59px;
    border-radius: 50%;
    background: radial-gradient(circle at 34% 28%, #fff9e6 0%, #f2d98d 24%, #c99d3c 54%, #6c4d16 80%, #241a06 100%);
    box-shadow:
      0 0 40px rgba(246, 227, 166, 0.75),
      0 0 110px rgba(217, 180, 95, 0.42),
      inset -22px -20px 34px rgba(58, 36, 4, 0.55);
    transform: translateZ(80px);
    animation: vcore 4.5s ease-in-out infinite;
  }
  @keyframes vcore { 0%, 100% { transform: translateZ(80px) scale(1); } 50% { transform: translateZ(80px) scale(1.07); } }
  .vorb { position: absolute; border-radius: 50%; }
  .vorb.one {
    width: 56px; height: 56px; left: 16%; top: 22%;
    background: radial-gradient(circle at 35% 35%, #f7feff, #8de7ff 46%, rgba(95, 227, 255, 0.2));
    box-shadow: 0 0 30px rgba(95, 227, 255, 0.55);
    animation: vfloatOne 9s ease-in-out infinite;
  }
  .vorb.two {
    width: 42px; height: 42px; right: 16%; top: 26%;
    background: radial-gradient(circle at 35% 35%, #ffffff, #b794ff 50%, rgba(139, 107, 255, 0.2));
    box-shadow: 0 0 28px rgba(139, 107, 255, 0.55);
    animation: vfloatTwo 11s ease-in-out infinite;
  }
  .vorb.three {
    width: 22px; height: 22px; right: 26%; bottom: 24%;
    background: radial-gradient(circle at 35% 35%, #fffdf2, #ffd76a 52%, rgba(217, 180, 95, 0.2));
    box-shadow: 0 0 22px rgba(246, 227, 166, 0.7);
    animation: vfloatThree 7s ease-in-out infinite;
  }
  @keyframes vfloatOne { 0%, 100% { transform: translate3d(0, 0, 80px); } 50% { transform: translate3d(18px, -20px, 130px); } }
  @keyframes vfloatTwo { 0%, 100% { transform: translate3d(0, 0, 120px); } 50% { transform: translate3d(-16px, 18px, 165px); } }
  @keyframes vfloatThree { 0%, 100% { transform: translate3d(0, 0, 140px); opacity: 0.7; } 50% { transform: translate3d(12px, -16px, 180px); opacity: 1; } }
  .vgrid {
    position: absolute; left: -12%; right: -12%; bottom: -28%; height: 56%;
    transform: rotateX(76deg);
    background-image:
      linear-gradient(rgba(217, 180, 95, 0.20) 1px, transparent 1px),
      linear-gradient(90deg, rgba(95, 227, 255, 0.14) 1px, transparent 1px);
    background-size: 40px 40px;
    -webkit-mask-image: linear-gradient(to top, rgba(0, 0, 0, 1), transparent 78%);
    mask-image: linear-gradient(to top, rgba(0, 0, 0, 1), transparent 78%);
  }
  .vhud { position: absolute; left: 34px; bottom: 54px; display: flex; gap: 10px; flex-wrap: wrap; transform: translateZ(110px); }
  .vchip {
    padding: 10px 16px; border-radius: 999px; font-size: 12px; letter-spacing: 0.05em; color: #f6efdc;
    background: rgba(255, 255, 255, 0.07); border: 1px solid rgba(217, 180, 95, 0.28);
    backdrop-filter: blur(10px);
    box-shadow: 0 12px 26px rgba(0, 0, 0, 0.4);
  }
  .vscan {
    position: absolute; inset: -12%;
    background: linear-gradient(180deg, transparent 42%, rgba(246, 227, 166, 0.05) 50%, transparent 58%);
    animation: vscan 6s linear infinite;
  }
  @keyframes vscan { from { transform: translateY(-40%); } to { transform: translateY(40%); } }
  .vcaption {
    position: absolute; left: 0; right: 0; bottom: 16px; text-align: center;
    font-size: 10.5px; letter-spacing: 0.3em; text-transform: uppercase; color: rgba(169, 175, 196, 0.65);
  }
</style>
<div class="vstage" id="vstage">
  <canvas id="motes"></canvas>
  <div class="vgrid"></div>
  <div class="vscene" id="vscene">
    <div class="vhalo"></div>
    <div class="vring"></div>
    <div class="vring two"></div>
    <div class="vcore"></div>
    <div class="vorb one"></div>
    <div class="vorb two"></div>
    <div class="vorb three"></div>
    <div class="vhud">
      <div class="vchip">✦ soul presence</div>
      <div class="vchip">verified search</div>
      <div class="vchip">modern 3D UI</div>
    </div>
  </div>
  <div class="vscan"></div>
  <div class="vcaption">vyoma presence · humming quietly</div>
</div>
<script>
  (function () {
    const stage = document.getElementById("vstage");
    const scene = document.getElementById("vscene");
    stage.addEventListener("mousemove", function (event) {
      const rect = stage.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width;
      const y = (event.clientY - rect.top) / rect.height;
      scene.style.transform =
        "rotateX(" + ((0.5 - y) * 14).toFixed(2) + "deg) rotateY(" + ((x - 0.5) * 18).toFixed(2) + "deg)";
    });
    stage.addEventListener("mouseleave", function () {
      scene.style.transform = "rotateX(0deg) rotateY(0deg)";
    });

    const canvas = document.getElementById("motes");
    const ctx = canvas.getContext("2d");
    const COLORS = ["rgba(246,227,166,", "rgba(217,180,95,", "rgba(139,107,255,", "rgba(95,227,255,", "rgba(255,255,255,"];
    let w = 0, h = 0, dpr = 1, motes = [];

    function rand(a, b) { return a + Math.random() * (b - a); }
    function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

    function size() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas.width = Math.floor(canvas.clientWidth * dpr);
      h = canvas.height = Math.floor(canvas.clientHeight * dpr);
    }

    function make(initial) {
      return {
        x: rand(0, w),
        y: initial ? rand(0, h) : h + 10,
        r: rand(0.6, 2.2) * dpr,
        vy: rand(0.15, 0.6) * dpr,
        sway: rand(0.4, 1.4),
        phase: rand(0, Math.PI * 2),
        alpha: rand(0.15, 0.6),
        color: pick(COLORS)
      };
    }

    function seed() {
      motes = Array.from({ length: 46 }, function () { return make(true); });
    }

    function step() {
      ctx.clearRect(0, 0, w, h);
      for (let i = 0; i < motes.length; i++) {
        const m = motes[i];
        m.phase += 0.008 * m.sway;
        m.y -= m.vy;
        m.x += Math.sin(m.phase) * 0.3 * dpr;
        if (m.y < -12) {
          const fresh = make(false);
          m.x = fresh.x; m.y = fresh.y; m.r = fresh.r; m.vy = fresh.vy;
          m.sway = fresh.sway; m.phase = fresh.phase; m.alpha = fresh.alpha; m.color = fresh.color;
        }
        ctx.beginPath();
        ctx.fillStyle = m.color + m.alpha + ")";
        ctx.arc(m.x, m.y, m.r, 0, Math.PI * 2);
        ctx.fill();
      }
      requestAnimationFrame(step);
    }

    size();
    seed();
    step();
    window.addEventListener("resize", function () { size(); seed(); });
  })();
</script>"""
    components.html(scene, height=412, scrolling=False)


# --------------------------------------------------------------------
# hero copy / stats / feature cards
# --------------------------------------------------------------------
def render_hero_copy() -> None:
    st.markdown(
        """
        <div class="hero-shell">
  <div class="hero-copy">
    <div class="eyebrow">✦ a sanctuary for your questions ✦</div>
    <div class="hero-title">Vyoma — an AI that <span>listens with a soul</span></div>
    <div class="hero-subtitle">
      Ask, verify, compare, explore. Vyoma searches the living web, weighs every source, and
      answers like a warm, careful friend — never a machine reading from a screen. Your
      investigation engine is untouched; only the room around it has grown gentler.
    </div>
    <div class="hero-badges">
      <div class="hero-badge">✦ real-time verification flow</div>
      <div class="hero-badge">✦ cinematic 3D presence</div>
      <div class="hero-badge">✦ warm, human tone</div>
      <div class="hero-badge">✦ soul lines between answers</div>
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
    <div class="stat-label">Cinematic depth, hover perspective and glow</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">Live</div>
    <div class="stat-label">Web-backed investigation engine, untouched</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">Soul</div>
    <div class="stat-label">Warm words, gentle pacing, human tone</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">Verified</div>
    <div class="stat-label">Sources weighed before an answer is given</div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_cards() -> None:
    st.markdown(
        """
        <div class="vyoma-section-label">✦ experience layers</div>
<div class="mini-grid">
  <div class="feature-card">
    <div class="feature-icon">🌌</div>
    <div class="feature-title">Spatial Hero</div>
    <div class="feature-text">
      A living gold-core scene with parallax depth, orbiting lights and floating dust —
      the first impression of a product, not a plain tool.
    </div>
  </div>
  <div class="feature-card">
    <div class="feature-icon">✨</div>
    <div class="feature-title">Glass Conversations</div>
    <div class="feature-text">
      Elevated chat bubbles with gold and violet glows, refined spacing and soft entrance
      motion — every answer feels set on glass.
    </div>
  </div>
  <div class="feature-card">
    <div class="feature-icon">⚡</div>
    <div class="feature-title">Quick Launch Prompts</div>
    <div class="feature-text">
      Lifted 3D tiles that rise, glow and pour a prompt straight into the conversation —
      one tap from thought to investigation.
    </div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------
# soulful praise quote card (rotating lines, gentle motion)
# --------------------------------------------------------------------
def render_soul_quotes() -> None:
    quote_html = (
        """<style>* { box-sizing: border-box; }
body { margin: 0; background: transparent; font-family: "Segoe UI", system-ui, sans-serif; }
.vyoma-quote {
  position: relative; height: 248px; overflow: hidden; border-radius: 24px;
  padding: 22px 26px; display: flex; flex-direction: column; justify-content: center; gap: 14px;
  background:
    radial-gradient(circle at 12% 20%, rgba(139, 107, 255, 0.16), transparent 34%),
    radial-gradient(circle at 88% 80%, rgba(217, 180, 95, 0.18), transparent 36%),
    linear-gradient(160deg, rgba(12, 17, 36, 0.92), rgba(7, 10, 22, 0.92));
  border: 1px solid rgba(217, 180, 95, 0.24);
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.06);
}
.vyoma-quote-eyebrow { margin: 0; font-size: 10.5px; letter-spacing: 0.4em; text-transform: uppercase; color: #ffe39d; }
.vyoma-quote-text {
  margin: 0; font-family: "Bodoni MT", Didot, Georgia, serif; font-style: italic;
  font-size: 19px; line-height: 1.6; color: #f7f2e6;
  transition: opacity 0.45s ease, transform 0.45s ease;
}
.vyoma-quote-text.swap { opacity: 0; transform: translateY(12px); }
.vyoma-quote-foot { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.vyoma-quote-index { font-size: 10.5px; letter-spacing: 0.3em; color: #6d748c; }
.vyoma-quote-btn {
  padding: 10px 18px; border-radius: 999px; cursor: pointer; font-size: 12.5px; font-weight: 600;
  color: #241a05; border: 1px solid rgba(255, 246, 214, 0.55);
  background: linear-gradient(178deg, #f8e6a9, #e5c873 32%, #c99d3c 70%, #8e6b21);
  box-shadow: inset 0 1px 0 rgba(255, 248, 222, 0.5), 0 12px 26px rgba(0, 0, 0, 0.5),
              0 8px 22px rgba(217, 180, 95, 0.3);
  transition: transform 0.3s ease, filter 0.3s ease;
}
.vyoma-quote-btn:hover { transform: translateY(-2px); filter: brightness(1.05); }
.vyoma-quote-glow {
  position: absolute; inset: auto -30% -60% -30%; height: 70%; pointer-events: none;
  background: radial-gradient(closest-side, rgba(217, 180, 95, 0.18), transparent);
  animation: vyomaQuoteGlow 7s ease-in-out infinite;
}
@keyframes vyomaQuoteGlow { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }</style>"""
        '<div class="vyoma-quote" id="vyomaQuote">'
        '<p class="vyoma-quote-eyebrow">✦ a soul line for you ✦</p>'
        '<p class="vyoma-quote-text" id="vyomaQuoteText"></p>'
        '<div class="vyoma-quote-foot">'
        '<span class="vyoma-quote-index" id="vyomaQuoteIndex"></span>'
        '<button class="vyoma-quote-btn" id="vyomaQuoteBtn" type="button">✦ another line</button>'
        "</div>"
        '<div class="vyoma-quote-glow"></div>'
        "</div>"
        "<script>const VYOMA_QUOTES = "
        + json.dumps(SOUL_QUOTES)
        + """;\n(function () {
    const quotes = VYOMA_QUOTES;
    const textEl = document.getElementById("vyomaQuoteText");
    const indexEl = document.getElementById("vyomaQuoteIndex");
    const buttonEl = document.getElementById("vyomaQuoteBtn");
    let current = Math.floor(Math.random() * quotes.length);
    let timer = null;

    function pad(n) { return n < 10 ? "0" + n : String(n); }

    function apply() {
      textEl.textContent = "\u201C" + quotes[current] + "\u201D";
      indexEl.textContent = pad(current + 1) + " / " + pad(quotes.length);
      textEl.classList.remove("swap");
    }

    function next(random) {
      textEl.classList.add("swap");
      window.setTimeout(function () {
        current = random
          ? Math.floor(Math.random() * quotes.length)
          : (current + 1) % quotes.length;
        if (random && quotes.length > 1) {
          while (quotes[current] === quotes[(current + quotes.length - 1) % quotes.length]) {
            current = Math.floor(Math.random() * quotes.length);
          }
        }
        apply();
      }, 460);
    }

    function restart() {
      if (timer) { window.clearInterval(timer); }
      timer = window.setInterval(function () { next(false); }, 8200);
    }

    buttonEl.addEventListener("click", function () {
      next(true);
      restart();
    });

    apply();
    restart();
  })();</script>"""
    )
    components.html(quote_html, height=272, scrolling=False)


# --------------------------------------------------------------------
# quick launch prompts (luxury tiles)
# --------------------------------------------------------------------
def render_quick_prompts() -> None:
    col1, col2 = st.columns(2)
    columns = [col1, col2]

    for idx, prompt in enumerate(QUICK_PROMPTS):
        icon = QUICK_PROMPT_ICONS[idx % len(QUICK_PROMPT_ICONS)]
        with columns[idx % 2]:
            if st.button(
                f"{icon}  {prompt}",
                key=f"quick_prompt_{idx}",
                use_container_width=True,
            ):
                st.session_state["queued_prompt"] = prompt


# --------------------------------------------------------------------
# response parsing (unchanged behaviour)
# --------------------------------------------------------------------
def parse_response(raw_text: str) -> tuple[str, str]:
    thinking_match = re.search(r"<thinking>(.*?)</thinking>", raw_text, re.DOTALL)
    answer_match = re.search(r"<answer>(.*?)</answer>", raw_text, re.DOTALL)

    thinking_text = thinking_match.group(1).strip() if thinking_match else ""
    answer_text = answer_match.group(1).strip() if answer_match else raw_text
    return thinking_text, answer_text


# --------------------------------------------------------------------
# conversation turn (unchanged behaviour, softer voice)
# --------------------------------------------------------------------
def handle_chat_turn(prompt: str) -> None:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Vyoma is listening, searching and weighing her sources…"):
            history = st.session_state.messages[:-1]
            try:
                raw_ai_response = run_investigation(prompt, history)
            except Exception as exc:
                raw_ai_response = (
                    "<answer>I'm having trouble reaching my investigation engine right now. "
                    "Give me a moment and try again — I'll be here.</answer>"
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


# --------------------------------------------------------------------
# main
# --------------------------------------------------------------------
def main() -> None:
    inject_global_styles()

    # the entry window with the curtain reveal plays once per session;
    # the sidebar replay button brings it back on demand
    if "intro_completed" not in st.session_state:
        st.session_state["intro_completed"] = True
        render_intro_overlay()

    render_sidebar()

    if "queued_prompt" not in st.session_state:
        st.session_state["queued_prompt"] = None

    left, right = st.columns([1.22, 1], gap="large")

    with left:
        render_hero_copy()
        render_stats()
        render_feature_cards()

    with right:
        render_hero_scene()

    render_soul_quotes()

    st.markdown(
        '<div class="vyoma-section-label">✦ Try a live prompt</div>',
        unsafe_allow_html=True,
    )
    render_quick_prompts()

    st.markdown(
        '<div class="vyoma-section-label">✦ Conversation</div>',
        unsafe_allow_html=True,
    )
    render_chat_history()

    typed_prompt = st.chat_input("Talk to Vyoma... ask, verify, compare, or explore.")
    prompt_to_process = typed_prompt or st.session_state.get("queued_prompt")

    if prompt_to_process:
        st.session_state["queued_prompt"] = None
        handle_chat_turn(prompt_to_process)


if __name__ == "__main__":
    main()

