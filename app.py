from pathlib import Path

import base64

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Caipiringwer Beverage Stability Analytics Dashboard",
    page_icon="🧪",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #132238;
        --muted: #64748b;
        --navy: #0b2942;
        --blue: #146c94;
        --cyan: #2fa7b8;
        --aqua: #68d1c7;
        --gold: #d9aa52;
        --line: rgba(17, 67, 98, 0.12);
        --surface: rgba(255, 255, 255, 0.92);
        --shadow: 0 18px 50px rgba(14, 53, 78, 0.09);
    }

    html, body, [class*="css"] { font-family: Inter, "Segoe UI", Arial, sans-serif; }
    .stApp {
        color: var(--ink);
        background:
            radial-gradient(circle at 88% 4%, rgba(104, 209, 199, 0.16), transparent 26rem),
            radial-gradient(circle at 20% 28%, rgba(20, 108, 148, 0.08), transparent 30rem),
            #f4f8fa;
    }
    .block-container { max-width: 1480px; padding: 2rem 2.6rem 5rem; }
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: rgba(244, 248, 250, 0.78); backdrop-filter: blur(18px); }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a263d 0%, #0d354e 58%, #0c4054 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    [data-testid="stSidebar"] > div:first-child { padding: 1.4rem 1.15rem; }
    [data-testid="stSidebar"] * { color: rgba(255,255,255,0.90); }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12); }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 12px;
    }
    .brand-lockup { padding: .35rem .15rem 1rem; }
    .brand-mark {
        width: 46px; height: 46px; display: grid; place-items: center;
        border-radius: 14px; margin-bottom: .8rem; font-size: 1.35rem;
        background: linear-gradient(135deg, var(--aqua), #2c8dad);
        box-shadow: 0 12px 30px rgba(0,0,0,.22);
    }
    .brand-name { font-size: 1.05rem; font-weight: 760; letter-spacing: .01em; }
    .brand-kicker { color: rgba(255,255,255,.55) !important; font-size: .72rem; letter-spacing: .14em; text-transform: uppercase; margin-top: .2rem; }

    .dashboard-hero {
        position: relative; overflow: hidden; min-height: 315px; padding: 2rem 42% 1.9rem 2.35rem; margin: .25rem 0 1rem;
        display: flex; flex-direction: column; justify-content: center;
        border-radius: 26px; color: white;
        background-color: #071c31; background-size: cover; background-position: center;
        box-shadow: 0 24px 60px rgba(8, 52, 76, .22);
    }
    .dashboard-hero::before {
        content: ""; position: absolute; inset: 0; z-index: 0;
        background: linear-gradient(90deg, rgba(4,19,37,.96) 0%, rgba(5,28,50,.90) 34%, rgba(6,38,58,.45) 59%, rgba(5,36,51,.06) 100%);
    }
    .dashboard-hero::after {
        content: ""; position: absolute; width: 300px; height: 300px; right: -80px; top: -125px;
        border: 1px solid rgba(255,255,255,.16); border-radius: 50%; box-shadow: 0 0 0 45px rgba(255,255,255,.035), 0 0 0 95px rgba(255,255,255,.025);
    }
    .hero-eyebrow { position: relative; z-index: 1; color: #9ee6df; font-size: .72rem; font-weight: 750; letter-spacing: .16em; text-transform: uppercase; margin-bottom: .6rem; }
    .hero-title { position: relative; z-index: 1; font-size: clamp(1.9rem, 3vw, 2.85rem); line-height: 1.04; font-weight: 780; letter-spacing: -.035em; margin: 0 0 .75rem; }
    .hero-subtitle { position: relative; z-index: 1; color: rgba(255,255,255,.72); font-size: 1rem; line-height: 1.65; }
    .hero-meta { position: relative; z-index: 1; display: flex; flex-wrap: wrap; gap: .55rem; margin-top: 1.25rem; }
    .hero-chip { padding: .42rem .72rem; border: 1px solid rgba(255,255,255,.14); border-radius: 999px; background: rgba(255,255,255,.08); color: rgba(255,255,255,.82); font-size: .78rem; }

    h1, h2, h3 { color: var(--ink); letter-spacing: -.025em; }
    h1 { font-weight: 780 !important; }
    h2 { margin-top: 1.6rem !important; font-weight: 740 !important; }
    h3 { font-weight: 700 !important; }
    p, li { line-height: 1.68; }
    [data-testid="stCaptionContainer"] { color: var(--muted); }

    div[data-testid="stTabs"] > div[data-baseweb="tab-list"] {
        gap: .42rem; padding: .52rem; margin: .15rem 0 1.25rem;
        border: 1px solid rgba(11,65,93,.16); border-radius: 16px; background: #ffffff;
        box-shadow: 0 12px 32px rgba(14,53,78,.08); overflow-x: auto;
    }
    div[data-testid="stTabs"] > div[data-baseweb="tab-list"] button[data-baseweb="tab"] {
        min-height: 3rem; padding: 0 1rem; border-radius: 11px; border: 1px solid transparent;
        color: #405e72; font-size: .88rem; font-weight: 710; white-space: nowrap;
    }
    div[data-testid="stTabs"] > div[data-baseweb="tab-list"] button[aria-selected="true"] {
        color: white !important; background: linear-gradient(135deg, #0b526d, #147f91) !important;
        box-shadow: 0 8px 20px rgba(12,82,109,.22);
    }
    div[data-testid="stTabs"] [data-baseweb="tab-highlight"] { display: none; }
    div[data-testid="stTabs"] div[data-testid="stTabs"] > div[data-baseweb="tab-list"] {
        gap: .25rem; padding: .3rem; margin: .1rem 0 1rem; border-radius: 12px;
        border-color: rgba(20,108,148,.12); background: rgba(225,239,244,.72); box-shadow: none;
    }
    div[data-testid="stTabs"] div[data-testid="stTabs"] > div[data-baseweb="tab-list"] button[data-baseweb="tab"] {
        min-height: 2.4rem; padding: 0 .78rem; border-radius: 9px; color: #587286; font-size: .78rem; font-weight: 670;
    }
    div[data-testid="stTabs"] div[data-testid="stTabs"] > div[data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #0b526d !important; background: #ffffff !important; box-shadow: 0 4px 12px rgba(12,68,98,.09);
    }

    .navigation-header { display: flex; align-items: flex-end; justify-content: space-between; gap: 1rem; margin: 1.2rem 0 .65rem; }
    .navigation-kicker { color: #168b91; font-size: .68rem; font-weight: 800; letter-spacing: .13em; text-transform: uppercase; }
    .navigation-title { color: #102f45; font-size: 1.22rem; font-weight: 780; margin-top: .18rem; }
    .navigation-help { color: #6b8291; font-size: .78rem; text-align: right; }
    .report-map { display: grid; grid-template-columns: .85fr 2.1fr 1.15fr; gap: .7rem; margin: 0 0 .9rem; }
    .report-map-group { padding: .82rem .95rem; border: 1px solid var(--line); border-radius: 14px; background: rgba(255,255,255,.88); box-shadow: 0 8px 22px rgba(14,53,78,.05); }
    .report-map-group.primary { border-color: rgba(20,108,148,.25); background: linear-gradient(135deg, rgba(20,108,148,.10), rgba(255,255,255,.94)); }
    .report-map-label { color: #778c9a; font-size: .62rem; font-weight: 800; letter-spacing: .11em; text-transform: uppercase; }
    .report-map-value { color: #173b50; font-size: .79rem; font-weight: 680; line-height: 1.45; margin-top: .22rem; }
    .module-nav-label { display: flex; align-items: center; gap: .55rem; margin: .15rem 0 .45rem; color: #5f7788; font-size: .76rem; font-weight: 680; }
    .module-nav-label::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: #2fa7b8; box-shadow: 0 0 0 4px rgba(47,167,184,.12); }
    .workspace-banner { padding: 1rem 1.15rem; margin: .2rem 0 1rem; border-radius: 16px; border-left: 4px solid #146c94; background: linear-gradient(105deg, rgba(20,108,148,.10), rgba(255,255,255,.92)); }
    .workspace-banner strong { display: block; color: #103a53; font-size: 1.05rem; margin-bottom: .22rem; }
    .workspace-banner span { color: #647d8d; font-size: .82rem; }

    [data-testid="stMetric"] {
        min-height: 116px; padding: 1.05rem 1.15rem;
        background: var(--surface); border: 1px solid var(--line); border-radius: 18px;
        box-shadow: 0 12px 32px rgba(14, 53, 78, .07); transition: transform .18s ease, box-shadow .18s ease;
    }
    [data-testid="stMetric"]:hover { transform: translateY(-2px); box-shadow: var(--shadow); }
    [data-testid="stMetricLabel"] { color: #698093; font-weight: 650; }
    [data-testid="stMetricValue"] { color: #0b415d; font-weight: 770; letter-spacing: -.035em; }

    [data-testid="stDataFrame"], [data-testid="stTable"] { border: 1px solid var(--line); border-radius: 18px; overflow: hidden; box-shadow: 0 12px 35px rgba(14,53,78,.06); }
    [data-testid="stPlotlyChart"] { padding: .65rem; border: 1px solid var(--line); border-radius: 20px; background: rgba(255,255,255,.88); box-shadow: 0 14px 38px rgba(14,53,78,.065); }
    [data-testid="stImage"] img { border-radius: 18px; box-shadow: 0 16px 38px rgba(14,53,78,.12); }

    [data-testid="stAlert"] { border-radius: 16px; border: 1px solid rgba(20,108,148,.14); }
    [data-testid="stExpander"] { background: rgba(255,255,255,.76); border: 1px solid var(--line); border-radius: 15px; overflow: hidden; }
    .stSelectbox [data-baseweb="select"] > div, .stMultiSelect [data-baseweb="select"] > div { border-radius: 13px; border-color: var(--line); background: white; }
    .stButton > button, .stDownloadButton > button { border-radius: 12px; border: 0; color: white; font-weight: 700; background: linear-gradient(135deg, #146c94, #168b91); box-shadow: 0 10px 22px rgba(20,108,148,.18); }

    .section-card { background: var(--surface); border: 1px solid var(--line); border-radius: 20px; padding: 1.3rem; margin-bottom: 1rem; box-shadow: var(--shadow); }
    .scientific-title { color: #0f5f78; font-weight: 750; letter-spacing: .02em; }
    .status-card { background: rgba(20,108,148,.06); border-left: 4px solid var(--blue); border-radius: 14px; padding: .9rem 1rem; }
    .status-pill { display: inline-block; padding: .35rem .65rem; border-radius: 999px; font-weight: 700; }
    .excellent { background: rgba(31,153,133,.13); color: #147661; }
    .moderate { background: rgba(217,170,82,.16); color: #916517; }
    .poor { background: rgba(209,76,86,.13); color: #a4323c; }

    .audit-ribbon {
        display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1px;
        margin: -.2rem 0 1rem; overflow: hidden; border: 1px solid var(--line);
        border-radius: 16px; background: var(--line); box-shadow: 0 10px 28px rgba(14,53,78,.05);
    }
    .audit-item { padding: .82rem 1rem; background: rgba(255,255,255,.88); }
    .audit-label { color: #7b8d9b; font-size: .66rem; font-weight: 760; letter-spacing: .1em; text-transform: uppercase; }
    .audit-value { color: #173b50; font-size: .88rem; font-weight: 690; margin-top: .18rem; }
    .evidence-grid { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: .85rem; margin: .85rem 0 1.6rem; }
    .evidence-card {
        position: relative; overflow: hidden; min-height: 168px; padding: 1.1rem 1.05rem 1rem;
        border: 1px solid var(--line); border-radius: 18px; background: rgba(255,255,255,.9);
        box-shadow: 0 12px 32px rgba(14,53,78,.06);
    }
    .evidence-card::before { content: ""; position: absolute; inset: 0 auto 0 0; width: 4px; background: var(--card-accent, var(--blue)); }
    .evidence-index { color: #8aa0ad; font-size: .68rem; font-weight: 780; letter-spacing: .12em; }
    .evidence-name { color: #15394f; font-size: 1rem; font-weight: 760; margin: .3rem 0 .5rem; }
    .evidence-detail { color: #63798a; font-size: .78rem; line-height: 1.45; }
    .evidence-status { display: inline-flex; align-items: center; gap: .35rem; margin-top: .75rem; color: #24675f; font-size: .72rem; font-weight: 720; }
    .evidence-status::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: #36a88e; box-shadow: 0 0 0 4px rgba(54,168,142,.12); }
    .governance-note { padding: 1rem 1.1rem; border-radius: 16px; border: 1px solid rgba(217,170,82,.24); background: linear-gradient(110deg, rgba(217,170,82,.10), rgba(255,255,255,.72)); color: #564624; font-size: .86rem; line-height: 1.6; }
    .shelf-hero {
        position: relative; min-height: 300px; overflow: hidden; margin: .6rem 0 1.1rem;
        border-radius: 20px; border: 1px solid rgba(104,209,199,.2);
        background-size: cover; background-position: center 44%; box-shadow: 0 16px 40px rgba(6,34,54,.16);
    }
    .shelf-hero::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(4,20,36,.08), rgba(4,20,36,.72)); }
    .shelf-hero-copy { position: absolute; z-index: 2; left: 2rem; right: 2rem; bottom: 1.7rem; color: white; }
    .shelf-hero-copy h2 { color: white !important; max-width: 790px; margin: 0 0 .55rem !important; font-size: 1.75rem; }
    .shelf-hero-copy p { max-width: 820px; margin: 0; color: rgba(255,255,255,.74); font-size: .92rem; }
    .evidence-flow { position: relative; display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1.2rem 0 1.6rem; }
    .evidence-flow::before { content: ""; position: absolute; top: 18px; left: 7%; right: 7%; height: 2px; background: #d8e5e9; }
    .evidence-flow::after {
        content: ""; position: absolute; top: 18px; left: 7%; width: 18%; height: 2px;
        background: linear-gradient(90deg, #1c8ea1, #68d1c7); box-shadow: 0 0 12px rgba(47,167,184,.8);
        animation: evidenceSweep 4.8s ease-in-out infinite;
    }
    @keyframes evidenceSweep { 0% { transform: translateX(0); opacity: .2; } 45% { opacity: 1; } 100% { transform: translateX(345%); opacity: .15; } }
    .flow-step { position: relative; z-index: 1; padding-top: 2.8rem; }
    .flow-dot { position: absolute; top: 9px; left: calc(50% - 10px); width: 20px; height: 20px; border-radius: 50%; background: white; border: 5px solid #2b8c9d; box-shadow: 0 0 0 5px rgba(43,140,157,.11); }
    .flow-step.unresolved .flow-dot { border-color: #c58e32; background: #fff8e8; animation: unresolvedPulse 2.2s ease-out infinite; }
    @keyframes unresolvedPulse { 0% { box-shadow: 0 0 0 0 rgba(197,142,50,.34); } 75% { box-shadow: 0 0 0 12px rgba(197,142,50,0); } 100% { box-shadow: 0 0 0 0 rgba(197,142,50,0); } }
    .flow-card { min-height: 130px; padding: .9rem; border-radius: 15px; border: 1px solid var(--line); background: rgba(255,255,255,.9); }
    .flow-kicker { color: #708695; font-size: .66rem; font-weight: 760; letter-spacing: .08em; text-transform: uppercase; }
    .flow-title { color: #173b50; font-size: .9rem; font-weight: 760; margin: .25rem 0; }
    .flow-detail { color: #647888; font-size: .75rem; line-height: 1.45; }
    .decision-banner { padding: 1.15rem 1.2rem; border-radius: 17px; border: 1px solid rgba(190,123,38,.25); background: linear-gradient(110deg, #fff8e8, rgba(255,255,255,.9)); }
    .decision-banner strong { color: #8b5a17; }
    .batch-map { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: .7rem 0 1.3rem; }
    .batch-card { padding: 1rem; border-radius: 16px; border: 1px solid var(--line); background: rgba(255,255,255,.88); }
    .batch-date { color: #0d6477; font-size: 1.05rem; font-weight: 780; }
    .batch-labels { color: #637888; font-size: .78rem; line-height: 1.55; margin-top: .35rem; }
    .study-grid { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: .85rem; margin: .8rem 0 1.5rem; }
    .study-card {
        min-height: 118px; padding: 1rem 1.05rem; border-radius: 16px; border: 1px solid var(--line);
        background: linear-gradient(145deg, rgba(255,255,255,.97), rgba(241,249,250,.88));
        box-shadow: 0 10px 28px rgba(14,53,78,.055);
    }
    .study-label { color: #718797; font-size: .66rem; font-weight: 780; letter-spacing: .1em; text-transform: uppercase; }
    .study-value { color: #123d55; font-size: 1.06rem; font-weight: 790; margin: .38rem 0 .3rem; }
    .study-detail { color: #667d8d; font-size: .75rem; line-height: 1.4; }
    .process-strip { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 1px; overflow: hidden; margin: .8rem 0 1rem; border: 1px solid var(--line); border-radius: 16px; background: var(--line); }
    .process-stage { padding: 1rem; background: rgba(255,255,255,.94); }
    .process-stage strong { display: block; color: #0d6477; font-size: .9rem; margin-bottom: .25rem; }
    .process-stage span { color: #687e8d; font-size: .75rem; line-height: 1.4; }
    .analysis-banner { padding: 1.05rem 1.15rem; margin: .8rem 0 1.1rem; border-radius: 16px; border-left: 4px solid #188b91; background: linear-gradient(105deg, rgba(24,139,145,.10), rgba(255,255,255,.92)); color: #28465a; line-height: 1.55; }
    .analysis-banner strong { color: #0b6473; }
    .bottle-story {
        position: relative; min-height: 430px; overflow: hidden; margin: .6rem 0 1.2rem;
        border-radius: 22px; border: 1px solid rgba(104,209,199,.22); background: #061c31;
        box-shadow: 0 18px 48px rgba(6,34,54,.18); isolation: isolate;
    }
    .bottle-frame { position: absolute; inset: 0; background-size: cover; background-position: center; }
    .bottle-frame.open {
        opacity: 0; transform: scale(1.015);
        animation: openBottleOnView linear both;
        animation-timeline: view(); animation-range: entry 20% cover 62%;
    }
    @keyframes openBottleOnView { from { opacity: 0; transform: scale(1.015); } to { opacity: 1; transform: scale(1); } }
    .bottle-story::after { content: ""; position: absolute; inset: 0; z-index: 1; background: linear-gradient(90deg, rgba(3,18,34,.90) 0%, rgba(3,18,34,.68) 37%, rgba(3,18,34,.05) 72%); }
    .bottle-story-copy { position: absolute; z-index: 2; left: 2.1rem; top: 50%; transform: translateY(-50%); max-width: 540px; color: white; }
    .bottle-story-kicker { color: #79d8cf; font-size: .7rem; font-weight: 790; letter-spacing: .13em; text-transform: uppercase; }
    .bottle-story-copy h2 { color: white !important; font-size: 2rem; line-height: 1.1; margin: .55rem 0 .75rem !important; }
    .bottle-story-copy p { color: rgba(255,255,255,.78); font-size: .9rem; line-height: 1.55; max-width: 475px; }
    .story-rail { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 1px; margin: 0 0 1.7rem; overflow: hidden; border: 1px solid var(--line); border-radius: 16px; background: var(--line); }
    .story-stage { padding: .9rem 1rem; background: rgba(255,255,255,.94); }
    .story-stage span { display: block; color: #6f8797; font-size: .64rem; font-weight: 780; letter-spacing: .1em; text-transform: uppercase; }
    .story-stage strong { display: block; color: #173e55; font-size: .86rem; margin-top: .25rem; }
    .experiment-grid { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: .9rem; margin: .8rem 0 1.4rem; }
    .experiment-card {
        position: relative; min-height: 205px; padding: 1.05rem; overflow: hidden;
        border: 1px solid var(--line); border-radius: 18px; background: rgba(255,255,255,.94);
        box-shadow: 0 10px 28px rgba(14,53,78,.06);
        animation: evidenceCardReveal linear both; animation-timeline: view(); animation-range: entry 10% cover 35%;
    }
    @keyframes evidenceCardReveal { from { opacity: .25; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
    .experiment-card::before { content: ""; position: absolute; inset: 0 0 auto; height: 4px; background: var(--accent, #146c94); }
    .experiment-period { color: #718797; font-size: .66rem; font-weight: 780; letter-spacing: .1em; text-transform: uppercase; }
    .experiment-title { color: #123d55; font-size: 1.02rem; font-weight: 790; margin: .45rem 0 .25rem; }
    .experiment-sample { color: #718797; font-size: .7rem; margin-bottom: .85rem; }
    .experiment-result { color: #173e55; font-size: 1rem; font-weight: 760; line-height: 1.4; }
    .experiment-method { color: #687e8d; font-size: .74rem; line-height: 1.45; margin-top: .55rem; }
    .outcome-grid { display: grid; grid-template-columns: 1.25fr .75fr; gap: 1rem; margin: .8rem 0 1.2rem; }
    .outcome-main, .outcome-side { border-radius: 18px; padding: 1.2rem; border: 1px solid var(--line); background: rgba(255,255,255,.94); }
    .outcome-main { border-left: 5px solid #188b91; }
    .outcome-label { color: #718797; font-size: .66rem; font-weight: 790; letter-spacing: .1em; text-transform: uppercase; }
    .outcome-title { color: #123d55; font-size: 1.15rem; font-weight: 800; margin: .4rem 0 .55rem; }
    .outcome-copy { color: #5f7687; font-size: .82rem; line-height: 1.55; }
    .outcome-value { color: #0b6473; font-size: 2rem; font-weight: 820; margin: .35rem 0; }

    @media (max-width: 800px) {
        .block-container { padding: 1rem 1rem 3rem; }
        .dashboard-hero { min-height: 430px; padding: 1.55rem 1.3rem; border-radius: 20px; justify-content: flex-end; background-position: 68% center; }
        .dashboard-hero::before { background: linear-gradient(180deg, rgba(4,19,37,.24) 0%, rgba(4,19,37,.52) 48%, rgba(4,19,37,.96) 76%); }
        .hero-title { font-size: 2rem; }
        [data-testid="stMetric"] { min-height: 100px; }
        .report-map { grid-template-columns: 1fr; }
        .navigation-header { align-items: flex-start; flex-direction: column; }
        .navigation-help { text-align: left; }
        .audit-ribbon, .evidence-grid, .study-grid, .process-strip, .story-rail, .experiment-grid { grid-template-columns: 1fr 1fr; }
        .shelf-hero { min-height: 340px; background-position: 40% center; }
        .bottle-story { min-height: 420px; }
        .bottle-story-copy { left: 1.3rem; right: 1.3rem; top: auto; bottom: 1.2rem; transform: none; }
        .bottle-story::after { background: linear-gradient(180deg, rgba(3,18,34,.08), rgba(3,18,34,.92)); }
        .outcome-grid { grid-template-columns: 1fr; }
        .shelf-hero-copy { left: 1.2rem; right: 1.2rem; bottom: 1.2rem; }
        .evidence-flow, .batch-map { grid-template-columns: 1fr; }
        .evidence-flow::before, .evidence-flow::after, .flow-dot { display: none; }
        .flow-step { padding-top: 0; }
    }
    @media (max-width: 520px) { .study-grid, .process-strip, .story-rail, .experiment-grid { grid-template-columns: 1fr; } }
    @supports not (animation-timeline: view()) { .bottle-frame.open { animation: openBottleFallback 7s ease-in-out infinite alternate; } .experiment-card { animation: none; } }
    @keyframes openBottleFallback { 0%,35% { opacity: 0; } 75%,100% { opacity: 1; } }
    @media (prefers-reduced-motion: reduce) { .evidence-flow::after, .flow-step.unresolved .flow-dot { animation: none; } }
    </style>
    """,
    unsafe_allow_html=True,
)

TRANSLATIONS = {
    "EN": {
        "language": "Language",
        "title": "Caipiringwer Beverage Stability Analytics Dashboard",
        "subtitle": "Scientific dashboard for independent rheological, physicochemical, sedimentation, and microbiological analysis of a ginger–lime beverage system.",
        "module": "Module",
        "flow": "Flow",
        "amp": "Amplitude sweep",
        "freq": "Frequency sweep",
        "physical": "Physical Stability and Sedimentation Assessment",
        "summary": "Results and synthesis",
        "literature": "References and literature support",
        "observed_records": "Measured records",
        "distinct_samples": "Distinct sample families",
        "temperature": "Temperature range",
        "shear_rate": "Shear-rate range",
        "ensemble": "Measured dataset overview",
        "flow_header": "Flow curve module",
        "amp_header": "Amplitude sweep module",
        "freq_header": "Frequency sweep module",
        "summary_header": "Results and synthesis",
        "literature_header": "References and literature support",
        "lit_text": "This chapter uses the measured workbook data as the sole analytical basis. The literature references support the interpretation and help position the rheology results within a scientific context.",
    },
    "DE": {
        "language": "Sprache",
        "title": "Caipiringwer Analyseplattform für Getränkestabilität",
        "subtitle": "Wissenschaftliches Dashboard zur unabhängigen rheologischen, physikochemischen, sedimentationsbezogenen und mikrobiologischen Analyse eines Ingwer-Limetten-Getränkesystems.",
        "module": "Modul",
        "flow": "Fließverhalten",
        "amp": "Amplitudensweep",
        "freq": "Frequenzsweep",
        "physical": "Physische Stabilität und Sedimentationsbewertung",
        "summary": "Ergebnisse und Synthese",
        "literature": "Literaturhinweise und fachliche Einordnung",
        "observed_records": "Gemessene Datensätze",
        "distinct_samples": "Unterschiedliche Probenfamilien",
        "temperature": "Temperaturbereich",
        "shear_rate": "Scherratenbereich",
        "ensemble": "Messdatensatz-Übersicht",
        "flow_header": "Fließkurvenmodul",
        "amp_header": "Amplitudensweep-Modul",
        "freq_header": "Frequenzsweep-Modul",
        "summary_header": "Ergebnisse und Synthese",
        "literature_header": "Literaturhinweise und fachliche Einordnung",
        "lit_text": "Dieses Kapitel stützt sich ausschließlich auf die gemessenen Workbook-Daten. Die Literaturhinweise dienen der fachlichen Einordnung und unterstützen die Interpretation der Rheologieergebnisse.",
    },
}

TRANSLATIONS["EN"].update({
    "dashboard_settings": "Dashboard Settings", "scientific_modules": "Scientific Modules",
    "experimental_assets": "Experimental Assets", "project_information": "Project Information",
    "rheology": "Rheology", "physicochemical": "Physicochemical", "sedimentation": "Sedimentation", "microbiology": "Microbiology",
    "rheology_loaded": "Rheology datasets loaded", "physchem_loaded": "Physicochemical datasets loaded",
    "sed_images_loaded": "Sedimentation images loaded", "micro_images_loaded": "Microbiology images loaded",
    "project": "Project", "degree": "Degree", "institution": "Institution", "instrumentation": "Instrumentation",
    "project_value": "Caipiringwer Stability Assessment", "degree_value": "MSc Biotechnology", "institution_value": "Hochschule Ansbach",
    "top_executive": "🏠 Executive Summary", "top_rheology": "🧪 Rheology", "top_physchem": "🧃 Physicochemical", "top_sedimentation": "🟤 Sedimentation", "top_microbiology": "🦠 Microbiology", "top_references": "📚 References", "top_shelf_life": "📈 Stability assessment",
    "flow_curve": "Flow Curve", "amplitude_sweep": "Amplitude Sweep", "frequency_sweep": "Frequency Sweep", "interpretation": "Interpretation",
    "overview": "Overview", "composition": "Composition", "trends": "Trends", "correlations": "Correlations",
    "sed_images": "📷 Images", "sed_analysis": "📈 Analysis", "sed_interpretation": "🧠 Interpretation", "sed_references": "📚 References",
    "available": "Available", "pending": "Pending", "not_loaded": "Not loaded",
    "executive_project": "Caipiringwer Stability Assessment", "study_architecture": "Overall study architecture",
    "integrated_conclusion": "Integrated conclusion", "data_integrity": "Each analytical module retains its own sample identifiers, experimental design, and metadata. Cross-module statistical joins are not performed because sample traceability across experiments has not been independently verified.",
    "bottle_statement": "Bottle condition before filling: The bottles were not subjected to a prior washing step. Before use, each bottle was visually inspected and accepted only when no visible particles or foreign material were observed. This procedure confirms visual cleanliness only and does not demonstrate microbiological cleanliness or sterility.",
    "bottle_limitation": "Because the bottles were not washed or microbiologically validated before filling, packaging-related contamination cannot be excluded as a possible uncontrolled factor.",
    "rheo_overview": "Overview and experimental design", "rheo_interpretation": "Integrated rheology interpretation", "rheo_metadata": "Metadata and raw data", "rheo_references": "Rheology references",
    "micro_exec": "Executive overview", "micro_results": "Plate results", "micro_visual": "Visual evidence", "micro_interpretation": "Scientific interpretation", "micro_shelf": "Shelf-life assessment", "micro_literature": "Literature support",
    "sed_dataset": "Measured sedimentation dataset",
})
TRANSLATIONS["DE"].update({
    "dashboard_settings": "Dashboard-Einstellungen", "scientific_modules": "Wissenschaftliche Module",
    "experimental_assets": "Experimentelle Datenquellen", "project_information": "Projektinformationen",
    "rheology": "Rheologie", "physicochemical": "Physikochemie", "sedimentation": "Sedimentation", "microbiology": "Mikrobiologie",
    "rheology_loaded": "Rheologie-Datensätze geladen", "physchem_loaded": "Physikochemische Datensätze geladen",
    "sed_images_loaded": "Sedimentationsbilder geladen", "micro_images_loaded": "Mikrobiologiebilder geladen",
    "project": "Projekt", "degree": "Abschluss", "institution": "Institution", "instrumentation": "Instrumentierung",
    "project_value": "Caipiringwer-Stabilitätsbewertung", "degree_value": "MSc Biotechnologie", "institution_value": "Hochschule Ansbach",
    "top_executive": "🏠 Managementübersicht", "top_rheology": "🧪 Rheologie", "top_physchem": "🧃 Physikochemie", "top_sedimentation": "🟤 Sedimentation", "top_microbiology": "🦠 Mikrobiologie", "top_references": "📚 Literatur", "top_shelf_life": "📈 Stabilitätsbewertung",
    "flow_curve": "Fließkurve", "amplitude_sweep": "Amplitudensweep", "frequency_sweep": "Frequenzsweep", "interpretation": "Interpretation",
    "overview": "Übersicht", "composition": "Zusammensetzung", "trends": "Trends", "correlations": "Korrelationen",
    "sed_images": "📷 Bilder", "sed_analysis": "📈 Analyse", "sed_interpretation": "🧠 Interpretation", "sed_references": "📚 Literatur",
    "available": "Verfügbar", "pending": "Ausstehend", "not_loaded": "Nicht geladen",
    "executive_project": "Caipiringwer-Stabilitätsbewertung", "study_architecture": "Übergreifende Studienarchitektur",
    "integrated_conclusion": "Integrierte Schlussfolgerung", "data_integrity": "Jedes Analysemodul behält seine eigenen Probenkennungen, sein Versuchsdesign und seine Metadaten. Modulübergreifende statistische Verknüpfungen werden nicht durchgeführt, da die Rückverfolgbarkeit der Proben zwischen den Experimenten nicht unabhängig bestätigt wurde.",
    "bottle_statement": "Zustand der Flaschen vor der Befüllung: Die Flaschen wurden vor der Verwendung keinem Waschschritt unterzogen. Vor der Befüllung wurde jede Flasche visuell kontrolliert und nur dann verwendet, wenn keine sichtbaren Partikel oder Fremdmaterialien erkennbar waren. Dieses Vorgehen bestätigt ausschließlich die visuelle Sauberkeit und stellt keinen Nachweis mikrobiologischer Sauberkeit oder Sterilität dar.",
    "bottle_limitation": "Da die Flaschen vor der Befüllung weder gewaschen noch mikrobiologisch validiert wurden, kann eine verpackungsbedingte Kontamination als möglicher unkontrollierter Einflussfaktor nicht ausgeschlossen werden.",
    "rheo_overview": "Übersicht und Versuchsdesign", "rheo_interpretation": "Integrierte rheologische Interpretation", "rheo_metadata": "Metadaten und Rohdaten", "rheo_references": "Rheologische Literatur", 
    "micro_exec": "Managementübersicht", "micro_results": "Plattenergebnisse", "micro_visual": "Bildnachweise", "micro_interpretation": "Wissenschaftliche Interpretation", "micro_shelf": "Haltbarkeitsbewertung", "micro_literature": "Literatur", 
    "sed_dataset": "Gemessener Sedimentationsdatensatz",
})

LANG = st.sidebar.selectbox("Language / Sprache", ["EN", "DE"], index=0)
T = TRANSLATIONS[LANG]


def tr(english: str, german: str) -> str:
    """Return user-facing copy in the currently selected language."""
    return german if LANG == "DE" else english


GERMAN_TABLE_COLUMNS = {
    "Model": "Modell", "Converged": "Konvergiert", "Yield stress": "Fließgrenze",
    "Adjusted R²": "Korrigiertes R²", "Observations": "Messpunkte", "Dataset": "Datensatz",
    "Mean viscosity η": "Mittlere Viskosität η", "Mean G′": "Mittleres G′",
    "Mean G″": "Mittleres G″", "Mean tanδ": "Mittleres tanδ", "Sample_ID": "Proben-ID",
    "Product_Type": "Produkttyp", "Mean_Viscosity": "Mittlere Viskosität",
    "Mean_Gprime": "Mittleres G′", "Mean_Gdouble": "Mittleres G″",
    "Mean_tan_delta": "Mittleres tanδ", "Flow_behavior_index_n": "Fließverhaltensindex n",
    "Consistency_coefficient_K": "Konsistenzkoeffizient K", "Manufacturing_Date": "Herstellungsdatum",
    "Number_of_Replicates": "Anzahl Wiederholungen", "Measurement_ID": "Messungs-ID",
    "Parent_Sample": "Ausgangsprobe", "Replicate_Number": "Wiederholungsnummer",
    "Sample": "Probe", "Action": "Messschritt", "steady state": "Stationärer Zustand",
    "Sample_Family": "Probenfamilie", "Notes": "Anmerkungen", "Storage_Date": "Lagerungsdatum",
    "Storage_Duration": "Lagerungsdauer", "Brix_Avg": "Brix-Mittelwert",
    "Sugar_g_L": "Zucker (g/L)", "Potential_Alcohol_vv": "Potenzieller Alkohol (% v/v)",
    "Density_g_cm3": "Dichte (g/cm³)", "Specific_Gravity": "Relative Dichte",
    "Manufacturing Date": "Herstellungsdatum", "Product Type": "Produkttyp",
    "Mid Sediment (mL)": "Sediment Zwischenbeobachtung (mL)",
    "Final Sediment (mL)": "Finales Sediment (mL)",
    "Sediment-bed contraction (%)": "Sedimentbettkontraktion (%)",
    "Final-to-mid sediment-bed ratio": "Verhältnis finales/zwischenzeitliches Sedimentbett",
    "Final-to-mid sediment-bed ratio (%)": "Verhältnis finales/zwischenzeitliches Sedimentbett (%)",
    "Total sample volume (mL)": "Gesamtprobenvolumen (mL)",
    "Mid sediment-bed fraction (%)": "Sedimentbettanteil Zwischenbeobachtung (%)",
    "Final sediment-bed fraction (%)": "Finaler Sedimentbettanteil (%)",
    "Medium": "Nährmedium", "Microbial_status": "Mikrobiologischer Status",
    "Beverage_Type": "Getränketyp", "Treatment": "Behandlung", "Date_Parsed": "Ausgewertetes Datum",
    "Display_Date": "Anzeigedatum", "Normalized_Status": "Normalisierter Status",
    "Risk_Score": "Risikowert", "Short_Status": "Kurzstatus", "Risk Classification": "Risikoklasse",
    "Risk rank": "Risikorang", "LIMS_Record": "LIMS-Datensatz", "Qualitative LIMS records (not plate count)": "Qualitative LIMS-Datensätze (keine Plattenzahl)",
}

GERMAN_TABLE_VALUES = {
    "Standard Pasteurized": "Standard pasteurisiert", "Pasteurized with Spritz": "Pasteurisiert mit Spritz",
    "Non-pasteurized": "Nicht pasteurisiert", "Pasteurized": "Pasteurisiert",
    "Non-pasteurised": "Nicht pasteurisiert", "Pasteurised": "Pasteurisiert",
    "SAFE": "UNBEDENKLICH", "LOW RISK": "GERINGES RISIKO", "MODERATE RISK": "MITTLERES RISIKO",
    "CRITICAL": "KRITISCH", "Unclassified": "Nicht klassifiziert",
    "Very high growth": "Sehr starkes Wachstum", "Low Growth": "Geringes Wachstum",
    "Low growth": "Geringes Wachstum", "No growth": "Kein Wachstum",
    "Negative/Safe": "Negativ/Unbedenklich", "Countable growth": "Auszählbares Wachstum",
    "Power law": "Potenzgesetz", "Yes": "Ja", "No": "Nein", "Not fitted": "Nicht angepasst",
    "Flow": "Fließkurve", "Amplitude sweep": "Amplitudensweep", "Frequency sweep": "Frequenzsweep",
    "1 year +": "über 1 Jahr", "1 year": "1 Jahr", "6 months": "6 Monate", "2 month": "2 Monate",
    "Yeast & Mold (MEA)": "Hefe & Schimmel (MEA)", "Caipiringwer Regular": "Caipiringwer Standard",
    "Critical": "Kritisch", "Safe": "Unbedenklich", "Low": "Gering", "Moderate": "Mittel",
    "Negative": "Negativ", "Countable": "Auszählbar",
}


def localized_table(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return a presentation-only copy with German headers and categorical labels."""
    if LANG != "DE":
        return dataframe
    localized = dataframe.copy().rename(columns=GERMAN_TABLE_COLUMNS)
    for column in localized.select_dtypes(include="bool").columns:
        localized[column] = localized[column].map({True: "Ja", False: "Nein"})
    localized = localized.replace(GERMAN_TABLE_VALUES)
    if "Anzeigedatum" in localized.columns:
        parsed_dates = pd.to_datetime(localized["Anzeigedatum"], errors="coerce")
        localized.loc[parsed_dates.notna(), "Anzeigedatum"] = parsed_dates[parsed_dates.notna()].dt.strftime("%d.%m.%Y")
    return localized


@st.cache_data
def image_data_uri(path_string: str) -> str:
    """Encode a local dashboard asset for reliable Streamlit CSS embedding."""
    image_bytes = Path(path_string).read_bytes()
    return f"data:image/png;base64,{base64.b64encode(image_bytes).decode('ascii')}"


def resolve_dataset_path(filename: str) -> Path:
    candidates = [
        Path.cwd() / filename,
        Path.cwd() / "data" / filename,
        Path.cwd() / "data" / "rheology" / filename,
        Path(__file__).resolve().parent / filename,
        Path(__file__).resolve().parent / "data" / filename,
        Path(__file__).resolve().parent / "data" / "rheology" / filename,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


@st.cache_data
def load_physicochemical_dataset():
    phys_path = Path("data/physicochemical/physicochemical_results.ods")
    if not phys_path.exists():
        return pd.DataFrame()

    raw = pd.read_excel(phys_path, header=None)
    if raw.shape[0] <= 17:
        return pd.DataFrame()

    header = raw.iloc[17].fillna("").astype(str).str.strip()
    data = raw.iloc[18:].copy().reset_index(drop=True)
    data.columns = header
    data = data.loc[:, ~data.columns.str.contains("Unnamed", na=False)]
    data = data.dropna(how="all").reset_index(drop=True)

    seen = {}
    tidy_columns = []
    for col in data.columns:
        key = str(col).strip()
        seen[key] = seen.get(key, 0) + 1
        if seen[key] == 1:
            tidy_columns.append(key)
        else:
            tidy_columns.append(f"{key} ({seen[key]})")
    data.columns = tidy_columns

    data = data.rename(columns={
        "Sample ID": "Sample_ID",
        "Storage": "Storage_Date",
        "Storage duration": "Storage_Duration",
        "Type": "Product_Type",
        "Specific Gravity (g/cm³)": "Specific_Gravity",
        "Density (g/cm³)": "Density_g_cm3",
        "Potential Alcohol (% v/v)": "Potential_Alcohol_vv",
        "Alcohol Percentage (% v/v)": "Alcohol_Percentage_vv",
        "Refractive Index (nD)": "Refractive_Index_nD",
        "Sugar (g/L)": "Sugar_g_L",
        "Oechsel (°Oe CH)": "Oechsel",
        "pH": "pH",
    })

    data["Sample_ID"] = pd.to_numeric(data["Sample_ID"], errors="coerce")
    data["Storage_Date"] = pd.to_datetime(data["Storage_Date"], errors="coerce", format="%d.%m.%Y")
    data["Storage_Duration"] = data["Storage_Duration"].astype(str).str.strip()
    data["Product_Type"] = data["Product_Type"].astype(str).str.strip()

    brix_cols = [col for col in data.columns if col.startswith("Brix (°Bx)")]
    if brix_cols:
        data["Brix_Avg"] = data[brix_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1, skipna=True)

    for col in ["Sugar_g_L", "Potential_Alcohol_vv", "Alcohol_Percentage_vv", "Refractive_Index_nD", "Oechsel", "Density_g_cm3", "Specific_Gravity", "pH"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    return data


@st.cache_data
def discover_evidence_photos():
    roots = [Path("data"), Path("figures")]
    photo_files = []
    allowed = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tif", ".tiff"}
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in allowed:
                photo_files.append(path)
    return photo_files


@st.cache_data
def load_datasets():
    flow = pd.read_excel(resolve_dataset_path("Flow curve.xlsx"))
    amp = pd.read_excel(resolve_dataset_path("Amplitude sweep.xlsx"))
    freq = pd.read_excel(resolve_dataset_path("Frequency sweep.xlsx"))
    meta = pd.read_excel(resolve_dataset_path("Metadata.xlsx"))

    for df in (flow, amp, freq, meta):
        df.columns = [str(col).strip() for col in df.columns]

    for df in (flow, amp, freq):
        df["Sample"] = df["Sample"].astype(str).str.strip()
        df["Sample_Family"] = df["Sample"].str.replace(r"\.\d+$", "", regex=True)

        if "Manufacturing_Date" in df.columns:
            df["Manufacturing_Date"] = pd.to_datetime(
                df["Manufacturing_Date"],
                errors="coerce",
                format="%d.%m.%Y",
            )

    meta = meta.loc[:, [col for col in meta.columns if col in {"Sample_ID", "Manufacturing_Date", "Product_Type", "Replicate_Number"}]].copy()
    meta["Measurement_ID"] = meta["Sample_ID"].astype(str).str.strip()
    meta["Parent_Sample"] = meta["Measurement_ID"].str.replace(r"\.\d+$", "", regex=True)
    meta["Replicate_Number"] = pd.to_numeric(meta["Replicate_Number"], errors="coerce").fillna(0).astype(int)
    meta["Product_Type"] = meta["Product_Type"].astype(str).str.strip()
    meta["Manufacturing_Date"] = pd.to_datetime(
        meta["Manufacturing_Date"],
        errors="coerce",
        format="%d.%m.%Y",
    )

    numeric_cols = {
        "flow": ["T (°C)", "σ (Pa)", "ɣ̇ (s⁻¹)", "η (Pa s)", "F (N)", "g (mm)", "τ (N m)", "θ'(t) (rad/s)", "θabs (rad)"],
        "amp": ["T (°C)", "f (Hz)", "γ* (%)", "σ* (Pa)", "G* (Pa)", "G' (Pa)", 'G" (Pa)', "η* (Pa s)", "δ (°)", "F (N)", "g (mm)", "τ (N m)", "θ (rad)"],
        "freq": ["T (°C)", "f (Hz)", "γ* (%)", "σ* (Pa)", "G* (Pa)", "G' (Pa)", 'G" (Pa)', "η* (Pa s)", "δ (°)", "F (N)", "g (mm)", "τ (N m)", "θ (rad)", "HD (%)"],
    }

    for target_name, cols in numeric_cols.items():
        df = flow if target_name == "flow" else amp if target_name == "amp" else freq
        for col in cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

    physchem = load_physicochemical_dataset()
    return flow, amp, freq, meta, physchem


def safe_mean(series):
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return np.nan
    return float(values.mean())


@st.cache_data
def fit_power_law(flow_subset):
    valid = flow_subset[["ɣ̇ (s⁻¹)", "σ (Pa)"]].dropna()
    if valid.empty or valid["ɣ̇ (s⁻¹)"].nunique() < 2:
        return np.nan, np.nan

    x = np.log10(valid["ɣ̇ (s⁻¹)"].clip(lower=1e-9))
    y = np.log10(valid["σ (Pa)"].clip(lower=1e-9))

    try:
        slope, intercept = np.polyfit(x, y, 1)
    except np.linalg.LinAlgError:
        return np.nan, np.nan

    n = float(slope)
    k = float(10 ** intercept)
    return n, k


def loglog_fit(df, x_col, y_col):
    """Return slope, intercept, and R² for positive measured values only."""
    valid = df[[x_col, y_col]].dropna()
    valid = valid[(valid[x_col] > 0) & (valid[y_col] > 0)]
    if len(valid) < 3 or valid[x_col].nunique() < 2:
        return np.nan, np.nan, np.nan

    x = np.log10(valid[x_col].to_numpy())
    y = np.log10(valid[y_col].to_numpy())
    try:
        slope, intercept = np.polyfit(x, y, 1)
    except np.linalg.LinAlgError:
        return np.nan, np.nan, np.nan

    predicted = slope * x + intercept
    residual = np.sum((y - predicted) ** 2)
    total = np.sum((y - y.mean()) ** 2)
    r_squared = 1 - residual / total if total > 0 else np.nan
    return float(slope), float(intercept), float(r_squared)


def power_law_model_details(flow_subset):
    """Descriptive power-law fit to one parent sample; no extrapolation is used."""
    valid = flow_subset[["ɣ̇ (s⁻¹)", "σ (Pa)"]].dropna()
    valid = valid[(valid["ɣ̇ (s⁻¹)"] > 0) & (valid["σ (Pa)"] > 0)].copy()
    if len(valid) < 3 or valid["ɣ̇ (s⁻¹)"].nunique() < 2:
        return {key: np.nan for key in ("n", "k", "r2", "adj_r2", "rmse", "aicc", "n_obs")}, valid
    n, log_k, r2 = loglog_fit(valid, "ɣ̇ (s⁻¹)", "σ (Pa)")
    k = 10 ** log_k
    fitted = k * valid["ɣ̇ (s⁻¹)"] ** n
    residual = valid["σ (Pa)"] - fitted
    n_obs, n_parameters = len(valid), 2
    log_residual = np.log10(valid["σ (Pa)"]) - np.log10(fitted)
    sse = float(np.sum(log_residual ** 2))
    aic = n_obs * np.log(max(sse / n_obs, np.finfo(float).tiny)) + 2 * n_parameters
    aicc = aic + (2 * n_parameters * (n_parameters + 1) / (n_obs - n_parameters - 1)) if n_obs > n_parameters + 1 else np.nan
    valid["Fitted stress (Pa)"] = fitted
    valid["Stress residual (Pa)"] = residual
    return {
        "n": n, "k": k, "r2": r2,
        "adj_r2": 1 - (1 - r2) * (n_obs - 1) / (n_obs - n_parameters - 1),
        "rmse": float(np.sqrt(np.mean(residual ** 2))), "aicc": float(aicc), "n_obs": n_obs,
    }, valid


def measured_curve(df, x_col, value_cols):
    """Mean replicate readings at each measured setpoint; no interpolation."""
    return (
        df[[x_col, *value_cols]]
        .dropna(subset=[x_col])
        .groupby(x_col, as_index=False)[value_cols]
        .mean()
        .sort_values(x_col)
        .reset_index(drop=True)
    )


def nearest_measured_value(curve, x_col, y_col, target):
    valid = curve[[x_col, y_col]].dropna()
    if valid.empty:
        return np.nan, np.nan
    nearest_index = (np.log10(valid[x_col].clip(lower=1e-12)) - np.log10(target)).abs().idxmin()
    return float(valid.loc[nearest_index, y_col]), float(valid.loc[nearest_index, x_col])


def amplitude_metrics(amp_subset):
    curve = measured_curve(amp_subset, "γ* (%)", ["G' (Pa)", 'G" (Pa)', "η* (Pa s)"])
    valid = curve.dropna(subset=["G' (Pa)"])
    if valid.empty:
        return curve, {key: np.nan for key in ("reference_gprime", "lvr_limit", "retention", "max_strain", "crossover")}

    baseline = float(valid["G' (Pa)"].head(min(3, len(valid))).median())
    deviation = (valid["G' (Pa)"] - baseline).abs() > baseline * 0.05
    sustained = deviation & deviation.shift(-1, fill_value=False)
    first_deviation = valid.loc[sustained, "γ* (%)"]
    lvr_limit = float(first_deviation.iloc[0]) if not first_deviation.empty else float(valid["γ* (%)"].max())
    max_row = valid.iloc[-1]
    retention = float(max_row["G' (Pa)"] / baseline * 100) if baseline > 0 else np.nan
    crossover_rows = curve.dropna(subset=["G' (Pa)", 'G" (Pa)']).copy()
    crossover = np.nan
    if len(crossover_rows) > 1:
        gaps = crossover_rows["G' (Pa)"] - crossover_rows['G" (Pa)']
        change = gaps.mul(gaps.shift(1)).lt(0)
        if change.any():
            crossover = float(crossover_rows.loc[change, "γ* (%)"].iloc[0])
    return curve, {
        "reference_gprime": baseline,
        "lvr_limit": lvr_limit,
        "retention": retention,
        "max_strain": float(max_row["γ* (%)"]),
        "crossover": crossover,
    }


def frequency_metrics(freq_subset):
    curve = measured_curve(freq_subset, "f (Hz)", ["G' (Pa)", 'G" (Pa)', "η* (Pa s)", "δ (°)"])
    valid = curve.dropna(subset=["G' (Pa)", 'G" (Pa)']).copy()
    if valid.empty:
        return curve, {key: np.nan for key in ("tan_delta", "elastic_ratio", "gprime_slope", "gprime_r2", "low_gprime", "high_gprime", "crossover")}

    valid["tan_delta"] = valid['G" (Pa)'] / valid["G' (Pa)"].replace(0, np.nan)
    slope, _, r_squared = loglog_fit(valid, "f (Hz)", "G' (Pa)")
    gaps = valid["G' (Pa)"] - valid['G" (Pa)']
    change = gaps.mul(gaps.shift(1)).lt(0)
    crossover = float(valid.loc[change, "f (Hz)"].iloc[0]) if change.any() else np.nan
    return curve, {
        "tan_delta": float(valid["tan_delta"].median()),
        "elastic_ratio": float((valid["G' (Pa)"] / valid['G" (Pa)'].replace(0, np.nan)).median()),
        "gprime_slope": slope,
        "gprime_r2": r_squared,
        "low_gprime": float(valid.iloc[0]["G' (Pa)"]),
        "high_gprime": float(valid.iloc[-1]["G' (Pa)"]),
        "crossover": crossover,
    }


@st.cache_data
def build_sample_profile_table(flow, amp, freq, meta):
    overview = (
        meta.groupby("Parent_Sample", as_index=False)
        .agg(
            Product_Type=("Product_Type", "first"),
            Manufacturing_Date=("Manufacturing_Date", "first"),
            Number_of_Replicates=("Measurement_ID", "size"),
        )
        .rename(columns={"Parent_Sample": "Sample_ID"})
        .sort_values("Sample_ID")
        .reset_index(drop=True)
    )

    profiles = overview.copy()
    profiles["Age_Days"] = (pd.Timestamp.today().normalize() - profiles["Manufacturing_Date"]).dt.days
    profiles["Mean_Viscosity"] = np.nan
    profiles["Mean_Gprime"] = np.nan
    profiles["Mean_Gdouble"] = np.nan
    profiles["Mean_tan_delta"] = np.nan
    profiles["Flow_behavior_index_n"] = np.nan
    profiles["Consistency_coefficient_K"] = np.nan
    profiles["Elastic_Dominance_Ratio"] = np.nan

    for index, row in profiles.iterrows():
        sample_id = row["Sample_ID"]
        flow_subset = flow[flow["Sample_Family"] == sample_id]
        amp_subset = amp[amp["Sample_Family"] == sample_id]
        freq_subset = freq[freq["Sample_Family"] == sample_id]

        mean_viscosity = safe_mean(flow_subset["η (Pa s)"])
        mean_gprime = safe_mean(pd.concat([amp_subset["G' (Pa)"], freq_subset["G' (Pa)"]], ignore_index=True))
        mean_gdouble = safe_mean(pd.concat([amp_subset['G" (Pa)'], freq_subset['G" (Pa)']], ignore_index=True))
        mean_tandelta = safe_mean(
            freq_subset['G" (Pa)'] / freq_subset["G' (Pa)"].replace(0, np.nan)
        )
        n, k = fit_power_law(flow_subset)

        profiles.at[index, "Mean_Viscosity"] = mean_viscosity
        profiles.at[index, "Mean_Gprime"] = mean_gprime
        profiles.at[index, "Mean_Gdouble"] = mean_gdouble
        profiles.at[index, "Mean_tan_delta"] = mean_tandelta
        profiles.at[index, "Flow_behavior_index_n"] = n
        profiles.at[index, "Consistency_coefficient_K"] = k

    profiles["Elastic_Dominance_Ratio"] = profiles["Mean_Gprime"] / profiles["Mean_Gdouble"].replace(0, np.nan)
    return profiles


flow, amp, freq, meta, physchem = load_datasets()

REFERENCE_LIBRARY = [
    {
        "title": "Staubmann, D. et al. (2023). Combinations of hydrocolloids show enhanced stabilizing effects on cloudy orange juice ready-to-drink beverages. Food Hydrocolloids, 138, 108436.",
        "doi": "10.1016/j.foodhyd.2022.108436",
        "publication_link": "https://doi.org/10.1016/j.foodhyd.2022.108436",
        "relevance": "Supports discussion of hydrocolloid-driven beverage structure; it does not prove stabilization or sedimentation performance in this independent dataset.",
        "relevance_de": "Unterstützt die Einordnung einer durch Hydrokolloide beeinflussten Getränkestruktur; belegt jedoch weder Stabilisierung noch Sedimentationsleistung in diesem unabhängigen Datensatz.",
    },
    {
        "title": "Malafronte, L. et al. (2023). Shear and extensional rheological properties of whole grain rye and oat aqueous suspensions. Food Hydrocolloids, 137, 108319.",
        "doi": "10.1016/j.foodhyd.2022.108319",
        "publication_link": "https://doi.org/10.1016/j.foodhyd.2022.108319",
        "relevance": "Supports measured-flow and suspension-rheology context; it does not validate a constitutive model for these samples.",
        "relevance_de": "Unterstützt den Kontext des gemessenen Fließverhaltens und der Suspensionsrheologie; validiert jedoch kein Stoffmodell für diese Proben.",
    },
    {
        "title": "Wilbanks, C., Yazdi, S. R. & Lucey, J. A. (2022). Effects of varying casein and pectin concentrations on the rheology of high-protein cultured milk beverages stored at ambient temperature. Journal of Dairy Science, 105, 72–82.",
        "doi": "10.3168/jds.2021-20597",
        "publication_link": "https://doi.org/10.3168/jds.2021-20597",
        "relevance": "Supports the distinction between flow and oscillatory material response; it does not establish shelf life for this beverage system.",
        "relevance_de": "Unterstützt die Unterscheidung zwischen Fließverhalten und oszillatorischer Materialantwort; begründet jedoch keine Haltbarkeit für dieses Getränkesystem.",
    },
    {
        "title": "Erturk, S., Le, H. M. & Kokini, J. L. (2023). Advances in large amplitude oscillatory shear rheology of food materials. Frontiers in Food Science and Technology, 3, 1130165.",
        "doi": "10.3389/frfst.2023.1130165",
        "publication_link": "https://doi.org/10.3389/frfst.2023.1130165",
        "relevance": "Supports cautious interpretation of deformation-dependent rheology; it does not infer unmeasured structural failure or product stability.",
        "relevance_de": "Unterstützt eine vorsichtige Interpretation der verformungsabhängigen Rheologie; daraus werden weder ungemessenes Strukturversagen noch Produktstabilität abgeleitet.",
    },
]

sample_overview = (
    meta.groupby("Parent_Sample", as_index=False)
    .agg(
        Product_Type=("Product_Type", "first"),
        Manufacturing_Date=("Manufacturing_Date", "first"),
        Number_of_Replicates=("Measurement_ID", "size"),
    )
    .rename(columns={"Parent_Sample": "Sample_ID"})
    .sort_values("Sample_ID")
    .reset_index(drop=True)
)

sample_profiles = build_sample_profile_table(flow, amp, freq, meta)

# Scientific summary metrics derived from the measured datasets
mean_viscosity = safe_mean(flow["η (Pa s)"])
mean_gprime = safe_mean(pd.concat([amp["G' (Pa)"], freq["G' (Pa)"]], ignore_index=True))
mean_gdouble = safe_mean(pd.concat([amp['G" (Pa)'], freq['G" (Pa)']], ignore_index=True))
mean_tandelta = safe_mean(freq["δ (°)"])
flow_behavior_index_n, consistency_coefficient_k = fit_power_law(flow)


sample_overview["Manufacturing_Date"] = sample_overview["Manufacturing_Date"].dt.strftime("%d.%m.%Y")

hero_image_path = Path(__file__).resolve().parent / "images" / "caipiringwer-hero.png"
hero_image_uri = image_data_uri(str(hero_image_path)) if hero_image_path.exists() else ""
shelf_image_path = Path(__file__).resolve().parent / "images" / "shelf-life-evidence.png"
shelf_image_uri = image_data_uri(str(shelf_image_path)) if shelf_image_path.exists() else ""
open_bottle_path = Path(__file__).resolve().parent / "images" / "caipiringwer-open-v2.png"
open_bottle_uri = image_data_uri(str(open_bottle_path)) if open_bottle_path.exists() else hero_image_uri

st.markdown(
    f"""
    <section class="dashboard-hero" style="background-image:url('{hero_image_uri}')">
        <div class="hero-eyebrow">{tr('Applied beverage science · MSc research platform', 'Angewandte Getränkewissenschaft · MSc-Forschungsplattform')}</div>
        <div class="hero-title">{T['title']}</div>
        <div class="hero-subtitle">{T['subtitle']}</div>
        <div class="hero-meta">
            <span class="hero-chip">◈ Hochschule Ansbach</span>
            <span class="hero-chip">Kinexus Prime Lab+</span>
            <span class="hero-chip">EasyDens · SmartRef</span>
            <span class="hero-chip">{tr('Measured evidence', 'Gemessene Evidenz')}</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    f"""
    <div class="audit-ribbon">
        <div class="audit-item"><div class="audit-label">{tr('Evidence model', 'Evidenzmodell')}</div><div class="audit-value">{tr('Measured + derived', 'Gemessen + abgeleitet')}</div></div>
        <div class="audit-item"><div class="audit-label">{tr('Analytical scope', 'Analytischer Umfang')}</div><div class="audit-value">4 {tr('independent modules', 'unabhängige Module')}</div></div>
        <div class="audit-item"><div class="audit-label">{tr('Traceability', 'Rückverfolgbarkeit')}</div><div class="audit-value">{tr('Source-level identifiers retained', 'Quellkennungen beibehalten')}</div></div>
        <div class="audit-item"><div class="audit-label">{tr('Statistical policy', 'Statistische Richtlinie')}</div><div class="audit-value">{tr('No unsupported joins', 'Keine unbelegten Verknüpfungen')}</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        f"""
        <div class="brand-lockup">
            <div class="brand-mark">◈</div>
            <div class="brand-name">Caipiringwer Analytics</div>
            <div class="brand-kicker">{tr('Stability intelligence', 'Stabilitätsanalyse')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.subheader(T["dashboard_settings"])
    st.caption(f"{T['language']}: {LANG}")
    st.divider()
    st.subheader(T["scientific_modules"])
    st.markdown(
        f"- {T['rheology']}\n- {T['physicochemical']}\n- {T['sedimentation']}\n- {T['microbiology']}"
    )
    st.divider()
    st.subheader(T["experimental_assets"])
    st.markdown(
        f"- **{T['available']}** · {T['rheology_loaded']}\n"
        f"- **{T['available'] if not physchem.empty else T['not_loaded']}** · {T['physchem_loaded']}\n"
        f"- **{T['available'] if Path('images/sediment_mid.png').exists() else T['pending']}** · {T['sed_images_loaded']}\n"
        f"- **{T['available'] if Path('data/microbiology').exists() else T['not_loaded']}** · {T['micro_images_loaded']}"
    )
    st.divider()
    st.subheader(T["project_information"])
    st.markdown(
        f"**{T['project']}:** {T['project_value']}\n\n"
        f"**{T['degree']}:** {T['degree_value']}\n\n"
        f"**{T['institution']}:** {T['institution_value']}\n\n"
        f"**{T['instrumentation']}:** Kinexus Prime Lab+ · EasyDens · SmartRef"
    )
    st.divider()
    st.subheader(tr("Report controls", "Berichtssteuerung"))
    visual_density = st.radio(
        tr("Visual density", "Darstellungsdichte"),
        [tr("Comfortable", "Komfortabel"), tr("Compact", "Kompakt")],
        horizontal=True,
        key="visual_density",
    )
    show_methodology = st.toggle(
        tr("Show methodology matrix", "Methodenmatrix anzeigen"),
        value=True,
        help=tr(
            "Displays an audit-oriented overview of evidence type, replication, and limitations.",
            "Zeigt eine auditierbare Übersicht zu Evidenztyp, Replikation und Limitationen.",
        ),
    )

if visual_density == tr("Compact", "Kompakt"):
    st.markdown(
        """
        <style>
        .block-container { max-width: 1580px; }
        [data-testid="stMetric"] { min-height: 96px; padding: .8rem .9rem; }
        [data-testid="stPlotlyChart"] { padding: .35rem; }
        div[data-testid="stTabs"] > div[data-baseweb="tab-list"] button[data-baseweb="tab"] { min-height: 2.5rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

chart_theme = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Inter, Segoe UI, Arial", color="#24384a", size=13),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,251,252,0.72)",
        colorway=["#146c94", "#2fa7b8", "#d9aa52", "#68a67d", "#b96070", "#7667a8"],
        title=dict(font=dict(size=18, color="#132f45"), x=0.02, xanchor="left"),
        hoverlabel=dict(bgcolor="white", bordercolor="#c8d8df", font=dict(color="#183247")),
        legend=dict(bgcolor="rgba(255,255,255,.76)", bordercolor="rgba(17,67,98,.10)", borderwidth=1),
        xaxis=dict(gridcolor="rgba(20,79,108,.09)", linecolor="rgba(20,79,108,.16)", zeroline=False),
        yaxis=dict(gridcolor="rgba(20,79,108,.09)", linecolor="rgba(20,79,108,.16)", zeroline=False),
    )
)

st.markdown(
    f"""
    <div class="navigation-header">
        <div>
            <div class="navigation-kicker">{tr('Report navigation', 'Berichtsnavigation')}</div>
            <div class="navigation-title">{tr('Select a workspace', 'Arbeitsbereich auswählen')}</div>
        </div>
        <div class="navigation-help">{tr('Primary tabs open a module · secondary tabs select its analysis view', 'Primäre Register öffnen ein Modul · sekundäre Register wählen die Analyseansicht')}</div>
    </div>
    <div class="report-map">
        <div class="report-map-group primary">
            <div class="report-map-label">01 · {tr('Start', 'Start')}</div>
            <div class="report-map-value">{T['top_executive']}</div>
        </div>
        <div class="report-map-group">
            <div class="report-map-label">02 · {tr('Analytical modules', 'Analysemodule')}</div>
            <div class="report-map-value">{T['rheology']} · {T['physicochemical']} · {T['sedimentation']} · {T['microbiology']}</div>
        </div>
        <div class="report-map-group">
            <div class="report-map-label">03 · {tr('Synthesis', 'Synthese')}</div>
            <div class="report-map-value">{T['top_references']} · {T['top_shelf_life']}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

top_tabs = st.tabs([
    T["top_executive"], T["top_rheology"], T["top_physchem"],
    T["top_sedimentation"], T["top_microbiology"], T["top_references"], T["top_shelf_life"],
])
top_tabs[1].markdown(
    f'<div class="module-nav-label">{tr("Rheology workspace · select an analysis view", "Arbeitsbereich Rheologie · Analyseansicht auswählen")}</div>',
    unsafe_allow_html=True,
)
rheology_tabs = top_tabs[1].tabs([
    T["rheo_overview"], T["flow_curve"], T["amplitude_sweep"],
    T["frequency_sweep"], T["rheo_interpretation"], T["rheo_metadata"], T["rheo_references"],
])
top_tabs[2].markdown(
    f'<div class="module-nav-label">{tr("Physicochemical workspace", "Arbeitsbereich Physikochemie")}</div>',
    unsafe_allow_html=True,
)
physicochemical_tabs = top_tabs[2].tabs([
    T["overview"],
])


@st.cache_data
def load_lims_microbial_audit():
    lims_path = Path("data/microbiology/LIMS_Microbial_Audit.csv")
    if not lims_path.exists():
        return pd.DataFrame()
    return pd.read_csv(lims_path, sep=None, engine="python")


def find_lims_column(dataframe, candidates):
    normalized = {str(column).strip().lower(): column for column in dataframe.columns}
    for candidate in candidates:
        if candidate in normalized:
            return normalized[candidate]
    return None


lims_microbiology = load_lims_microbial_audit()
micro_date_column = find_lims_column(lims_microbiology, [
    "date_parsed", "manufacturing date", "manufacturing_date", "manufacture date", "production date", "date",
])
micro_processing_column = find_lims_column(lims_microbiology, [
    "treatment", "processing condition", "processing", "process", "product type",
])
micro_sample_column = find_lims_column(lims_microbiology, [
    "sample", "sample id", "sample_id", "sample number", "sample_number",
])
micro_category_column = find_lims_column(lims_microbiology, [
    "beverage_type", "sample category", "category", "product category", "product_type", "product type",
])
micro_status_column = find_lims_column(lims_microbiology, ["microbial_status", "microbial status", "status"])
micro_normalized_status_column = find_lims_column(lims_microbiology, ["normalized_status", "normalized status"])
micro_short_status_column = find_lims_column(lims_microbiology, ["short_status", "short status"])
micro_medium_column = find_lims_column(lims_microbiology, ["medium", "culture medium"])
micro_risk_score_column = find_lims_column(lims_microbiology, ["risk_score", "risk score"])

MICRO_COPY = {
    "EN": {
        "overview": "Executive microbiological overview",
        "systems": "Beverage systems investigated",
        "plates": "Culture plates processed",
        "critical": "Critical risk conditions",
        "index": "Microbiological Acceptability Index",
        "pasteurized": "Pasteurized beverage systems",
        "non_pasteurized": "Non-pasteurized beverage systems",
        "media": "Media types used",
        "replicates": "Analytical replicates",
        "not_recorded": "Not recorded in LIMS audit",
        "results": "Measured qualitative plate results",
        "shelf_statement": "Regulatory shelf-life determination requires quantitative microbial enumeration according to ISO 4833 and ISO 21527.",
    },
    "DE": {
        "overview": "Managementübersicht Mikrobiologie",
        "systems": "Untersuchte Getränkesysteme",
        "plates": "Verarbeitete Kulturplatten",
        "critical": "Kritische Risikobedingungen",
        "index": "Mikrobiologischer Akzeptabilitätsindex",
        "pasteurized": "Pasteurisierte Getränkesysteme",
        "non_pasteurized": "Nicht pasteurisierte Getränkesysteme",
        "media": "Verwendete Nährmedien",
        "replicates": "Analytische Wiederholungen",
        "not_recorded": "Im LIMS-Audit nicht dokumentiert",
        "results": "Gemessene qualitative Plattenergebnisse",
        "shelf_statement": "Für eine regulatorische Haltbarkeitsbestimmung ist eine quantitative mikrobiologische Enumeration gemäß ISO 4833 und ISO 21527 erforderlich.",
    },
}
M = MICRO_COPY[LANG]
top_tabs[4].markdown(
    f'<div class="module-nav-label">{tr("Microbiology workspace · select an evidence view", "Arbeitsbereich Mikrobiologie · Evidenzansicht auswählen")}</div>',
    unsafe_allow_html=True,
)
microbiology_tabs = top_tabs[4].tabs([
    T["micro_exec"], T["micro_results"], T["micro_visual"], T["micro_interpretation"], T["micro_shelf"], T["micro_literature"],
])


def qualitative_risk_classification(row):
    microbial_status = str(row.get(micro_status_column, "")).strip().lower()
    normalized_status = str(row.get(micro_normalized_status_column, "")).strip().lower()
    short_status = str(row.get(micro_short_status_column, "")).strip().lower()
    if short_status == "tntc" or normalized_status == "critical" or microbial_status == "very high growth":
        return "CRITICAL"
    if normalized_status == "moderate" or short_status == "countable":
        return "MODERATE RISK"
    if normalized_status == "low" or microbial_status == "low growth" or short_status == "low growth":
        return "LOW RISK"
    if normalized_status == "safe" or microbial_status == "no growth" or short_status == "negative":
        return "SAFE"
    return "Unclassified"

with microbiology_tabs[0]:
    st.header(M["overview"])
    st.caption(tr("Industrial QA/R&D view based on the recorded study design and the qualitative LIMS audit. No microbial count is inferred from photographs or qualitative status fields.", "Industrielle QS-/F&E-Ansicht auf Grundlage des dokumentierten Versuchsdesigns und des qualitativen LIMS-Audits. Aus Fotografien oder qualitativen Statusfeldern wird keine Keimzahl abgeleitet."))
    if lims_microbiology.empty:
        st.warning(tr("LIMS_Microbial_Audit.csv was not found in the workspace. Executive microbiological indicators cannot be populated.", "LIMS_Microbial_Audit.csv wurde im Arbeitsbereich nicht gefunden. Die mikrobiologischen Kennzahlen der Managementübersicht können nicht dargestellt werden."))
    else:
        executive_micro = lims_microbiology.copy()
        executive_micro["Risk Classification"] = executive_micro.apply(qualitative_risk_classification, axis=1)
        unique_systems = executive_micro[micro_sample_column].nunique() if micro_sample_column is not None else 6
        critical_conditions = int((executive_micro["Risk Classification"] == "CRITICAL").sum())
        risk_scores = pd.to_numeric(executive_micro[micro_risk_score_column], errors="coerce").dropna() if micro_risk_score_column is not None else pd.Series(dtype=float)

        executive_kpis = st.columns(4)
        executive_kpis[0].metric(M["systems"], unique_systems)
        executive_kpis[1].metric(M["plates"], "156", help=tr("Recorded experimental-design total across the two independent laboratory days.", "Dokumentierte Gesamtzahl des Versuchsdesigns über zwei unabhängige Labortage."))
        executive_kpis[2].metric(M["critical"], critical_conditions)
        executive_kpis[3].metric(
            M["index"],
            f"{risk_scores.mean():.1f}/100" if not risk_scores.empty else M["not_recorded"],
            help=tr("Mean of the LIMS Risk_Score field, where available; no external acceptance threshold is applied.", "Mittelwert des LIMS-Feldes Risk_Score, sofern verfügbar; es wird kein externer Akzeptanzgrenzwert angewendet."),
        )

        if micro_processing_column is not None and micro_sample_column is not None:
            treatment_text = executive_micro[micro_processing_column].astype(str).str.lower()
            non_pasteurized = executive_micro.loc[treatment_text.str.contains("non", na=False), micro_sample_column].nunique()
            pasteurized = executive_micro.loc[
                treatment_text.str.contains("pasteur", na=False) & ~treatment_text.str.contains("non", na=False),
                micro_sample_column,
            ].nunique()
        else:
            pasteurized = M["not_recorded"]
            non_pasteurized = M["not_recorded"]

        design_metrics = st.columns(4)
        design_metrics[0].metric(M["pasteurized"], pasteurized)
        design_metrics[1].metric(M["non_pasteurized"], non_pasteurized)
        design_metrics[2].metric(M["media"], executive_micro[micro_medium_column].nunique() if micro_medium_column is not None else M["not_recorded"])
        design_metrics[3].metric(M["replicates"], M["not_recorded"], help=tr("The audit does not include a replicate identifier, so a replicate count is not inferred from qualitative records.", "Das Audit enthält keine Replikatkennung; daher wird aus den qualitativen Datensätzen keine Replikatanzahl abgeleitet."))
        st.info(tr("Study design: six beverage systems, two media (E. coli selective agar and MEA), two independent laboratory days, and 156 processed culture plates. Twelve qualitative LIMS observations summarize outcomes from the 156 processed culture plates, including analytical replicates and two laboratory days.", "Versuchsdesign: sechs Getränkesysteme, zwei Nährmedien (E.-coli-Selektivagar und MEA), zwei unabhängige Labortage und 156 verarbeitete Kulturplatten. Zwölf qualitative LIMS-Beobachtungen fassen die Ergebnisse der 156 Platten einschließlich analytischer Wiederholungen und beider Labortage zusammen."))
        st.caption(T["bottle_statement"])
        st.caption(T["bottle_limitation"])

with microbiology_tabs[1]:
    st.header(M["results"])
    st.caption(tr("LIMS-derived qualitative observations only. No CFU/mL, log transformation, image enumeration, or predictive microbiological model is generated.", "Ausschließlich aus LIMS abgeleitete qualitative Beobachtungen. Es werden weder KBE/mL noch Log-Transformationen, Bildauszählungen oder prädiktive mikrobiologische Modelle erzeugt."))
    if lims_microbiology.empty:
        st.warning(tr("LIMS_Microbial_Audit.csv was not found in the workspace. No microbiological observations are displayed or interpreted.", "LIMS_Microbial_Audit.csv wurde im Arbeitsbereich nicht gefunden. Es werden keine mikrobiologischen Beobachtungen dargestellt oder interpretiert."))
    else:
        micro_table = lims_microbiology.copy()
        micro_table["Risk Classification"] = micro_table.apply(qualitative_risk_classification, axis=1)
        ordered_risk = ["SAFE", "LOW RISK", "MODERATE RISK", "CRITICAL", "Unclassified"]
        observation_kpis = st.columns(5)
        observation_kpis[0].metric(tr("Qualitative microbiological observations", "Qualitative mikrobiologische Beobachtungen"), len(lims_microbiology))
        observation_kpis[1].metric(
            tr("Total microbiological plates processed", "Verarbeitete mikrobiologische Platten insgesamt"),
            "156",
            help=tr("The total plate count includes analytical replicates, duplicate incubation days, and both microbiological media.", "Die Gesamtzahl der Platten umfasst analytische Wiederholungen, beide Inkubationstage und beide mikrobiologischen Nährmedien."),
        )
        observation_kpis[2].metric(tr("Critical observations", "Kritische Beobachtungen"), int((micro_table["Risk Classification"] == "CRITICAL").sum()))
        observation_kpis[3].metric(tr("Safe observations", "Unbedenkliche Beobachtungen"), int((micro_table["Risk Classification"] == "SAFE").sum()))
        observation_kpis[4].metric(tr("Reported treatments", "Dokumentierte Behandlungen"), micro_table[micro_processing_column].nunique() if micro_processing_column is not None else M["not_recorded"])
        st.caption(tr(
            "Methodology: 6 beverage systems × 2 media (E. coli selective agar and MEA) × analytical replicates × 2 laboratory days = 156 total incubated plates.",
            "Methodik: 6 Getränkesysteme × 2 Nährmedien (E.-coli-Selektivagar und MEA) × analytische Wiederholungen × 2 Labortage = insgesamt 156 inkubierte Platten.",
        ))

        display_columns = [column for column in [
            micro_sample_column, micro_medium_column, micro_status_column, micro_category_column,
            micro_processing_column, micro_date_column, micro_normalized_status_column, micro_short_status_column,
            "Risk Classification",
        ] if column is not None]
        st.dataframe(localized_table(micro_table[display_columns]), width="stretch", hide_index=True)

        if micro_sample_column is not None and micro_medium_column is not None:
            result_register = micro_table.pivot_table(
                index=micro_sample_column,
                columns=micro_medium_column,
                values=micro_status_column,
                aggfunc="first",
            ).reset_index()
            sample_context = micro_table.groupby(micro_sample_column, as_index=False).agg({
                column: "first" for column in [micro_processing_column, micro_category_column, micro_date_column] if column is not None
            })
            risk_order = {"SAFE": 0, "LOW RISK": 1, "MODERATE RISK": 2, "CRITICAL": 3, "Unclassified": -1}
            risk_register = micro_table[[micro_sample_column, "Risk Classification"]].copy()
            risk_register["Risk rank"] = risk_register["Risk Classification"].map(risk_order)
            risk_register = risk_register.sort_values("Risk rank").groupby(micro_sample_column, as_index=False).tail(1)
            result_register = result_register.merge(sample_context, on=micro_sample_column, how="left").merge(
                risk_register[[micro_sample_column, "Risk Classification"]], on=micro_sample_column, how="left"
            )
            ordered_columns = [column for column in [micro_sample_column, micro_processing_column, micro_category_column, micro_date_column] if column is not None]
            ordered_columns += [column for column in result_register.columns if column not in ordered_columns + ["Risk Classification"]]
            ordered_columns.append("Risk Classification")
            result_register = result_register[ordered_columns]
            risk_colors = result_register["Risk Classification"].map({"SAFE": "#d8f0ea", "LOW RISK": "#fff1c9", "MODERATE RISK": "#fde0bf", "CRITICAL": "#f9c7cc", "Unclassified": "#e5e7eb"}).fillna("white").tolist()
            display_result_register = localized_table(result_register)
            fig_result_register = go.Figure(data=[go.Table(
                header=dict(values=[f"<b>{column}</b>" for column in display_result_register.columns], fill_color="#173f5f", font=dict(color="white"), align="left"),
                cells=dict(values=[display_result_register[column].fillna("—").astype(str).tolist() for column in display_result_register.columns], fill_color=[['white'] * len(display_result_register)] * (len(display_result_register.columns) - 1) + [risk_colors], align="left", height=30),
            )])
            fig_result_register.update_layout(title=tr("Qualitative microbiological results register", "Register qualitativer mikrobiologischer Ergebnisse"), margin=dict(l=0, r=0, t=48, b=0))
            st.plotly_chart(fig_result_register, width="stretch")

            evidence_grid = micro_table.copy()
            evidence_grid["Risk code"] = evidence_grid["Risk Classification"].map(risk_order).fillna(-1)
            evidence_grid["Sample label"] = evidence_grid[micro_sample_column].astype(str)
            if micro_processing_column is not None:
                processing_labels = evidence_grid[micro_processing_column].astype(str)
                if LANG == "DE":
                    processing_labels = processing_labels.replace(GERMAN_TABLE_VALUES)
                evidence_grid["Sample label"] = evidence_grid["Sample label"] + " — " + processing_labels
            evidence_grid = evidence_grid.sort_values(["Sample label", micro_medium_column])
            sample_labels = evidence_grid["Sample label"].drop_duplicates().tolist()
            media_labels = evidence_grid[micro_medium_column].drop_duplicates().tolist()
            risk_matrix = evidence_grid.pivot(index="Sample label", columns=micro_medium_column, values="Risk code").reindex(index=sample_labels, columns=media_labels)
            status_matrix = evidence_grid.pivot(index="Sample label", columns=micro_medium_column, values=micro_status_column).reindex(index=sample_labels, columns=media_labels)
            fig_evidence_matrix = go.Figure(go.Heatmap(
                z=risk_matrix.to_numpy(),
                x=media_labels,
                y=sample_labels,
                text=localized_table(status_matrix.fillna(tr("Not recorded", "Nicht dokumentiert"))).to_numpy(),
                texttemplate="%{text}",
                textfont=dict(size=13),
                hovertemplate=tr("Sample/treatment: %{y}<br>Medium: %{x}<br>Measured status: %{text}<extra></extra>", "Probe/Behandlung: %{y}<br>Nährmedium: %{x}<br>Gemessener Status: %{text}<extra></extra>"),
                colorscale=[[0.0, "#d9dde3"], [0.20, "#2a9d8f"], [0.45, "#e9c46a"], [0.70, "#f4a261"], [1.0, "#e63946"]],
                zmin=-1, zmax=3,
                showscale=False,
                xgap=3, ygap=3,
            ))
            fig_evidence_matrix.update_layout(
                template=chart_theme,
                title=tr("Qualitative microbiological evidence matrix", "Qualitative mikrobiologische Evidenzmatrix"),
                xaxis_title=tr("Culture medium", "Nährmedium"),
                yaxis_title=tr("Beverage system and treatment", "Getränkesystem und Behandlung"),
                margin=dict(l=0, r=0, t=48, b=0),
            )
            st.plotly_chart(fig_evidence_matrix, width="stretch")
            st.caption(tr("Cell colour encodes the measured qualitative risk class; cell text is the directly reported microbiological status. Each LIMS observation is represented once.", "Die Zellfarbe codiert die gemessene qualitative Risikoklasse; der Zelltext zeigt den direkt dokumentierten mikrobiologischen Status. Jede LIMS-Beobachtung wird einmal dargestellt."))

        if micro_date_column is not None:
            plate_timeline = micro_table.copy()
            plate_timeline["Manufacturing_Date"] = pd.to_datetime(plate_timeline[micro_date_column], errors="coerce", dayfirst=True)
            if micro_sample_column is None:
                plate_timeline["LIMS_Record"] = plate_timeline.index.astype(str)
            plot_timeline = localized_table(plate_timeline)
            plot_x = GERMAN_TABLE_COLUMNS.get("Manufacturing_Date", "Manufacturing_Date") if LANG == "DE" else "Manufacturing_Date"
            raw_y = micro_sample_column if micro_sample_column is not None else "LIMS_Record"
            plot_y = GERMAN_TABLE_COLUMNS.get(raw_y, raw_y) if LANG == "DE" else raw_y
            plot_color = GERMAN_TABLE_COLUMNS.get("Risk Classification", "Risk Classification") if LANG == "DE" else "Risk Classification"
            plot_symbol = GERMAN_TABLE_COLUMNS.get(micro_processing_column, micro_processing_column) if LANG == "DE" else micro_processing_column
            plot_hover = [GERMAN_TABLE_COLUMNS.get(column, column) if LANG == "DE" else column for column in [micro_medium_column, micro_status_column, micro_short_status_column] if column is not None]
            plot_risk_order = [GERMAN_TABLE_VALUES.get(value, value) if LANG == "DE" else value for value in ordered_risk]
            plot_color_map = {GERMAN_TABLE_VALUES.get(key, key) if LANG == "DE" else key: value for key, value in {"SAFE": "#2a9d8f", "LOW RISK": "#e9c46a", "MODERATE RISK": "#f4a261", "CRITICAL": "#e63946", "Unclassified": "#6c757d"}.items()}
            fig_plate_timeline = px.scatter(
                plot_timeline.dropna(subset=[plot_x]),
                x=plot_x,
                y=plot_y,
                color=plot_color,
                symbol=plot_symbol,
                hover_data=plot_hover,
                category_orders={plot_color: plot_risk_order},
                color_discrete_map=plot_color_map,
                template=chart_theme,
                title=tr("Manufacturing-date timeline of measured qualitative risk observations", "Zeitverlauf gemessener qualitativer Risikobeobachtungen nach Herstellungsdatum"),
            )
            st.plotly_chart(fig_plate_timeline, width="stretch")

with microbiology_tabs[2]:
    st.header(tr("Qualitative plate-image evidence", "Qualitative Bildnachweise der Platten"))
    st.caption(tr("Photographs are representative qualitative evidence only. No image-based colony count, CFU estimate, or organism identification is performed.", "Die Fotografien dienen nur als repräsentative qualitative Nachweise. Es erfolgen keine bildbasierte Koloniezählung, KBE-Schätzung oder Organismenidentifikation."))
    pasteurized_images = [
        (tr("November 2024 Regular P", "November 2024 Standard P"), "data/microbiology/November 2024 regular P.png", tr("November 2024", "November 2024"), tr("Regular", "Standard"), tr("Pasteurized", "Pasteurisiert"), tr("Qualitative comparison image; risk classification remains based on the matched LIMS observation.", "Qualitatives Vergleichsbild; die Risikoklassifizierung basiert weiterhin auf der zugeordneten LIMS-Beobachtung.")),
        (tr("December 2025 Regular P", "Dezember 2025 Standard P"), "data/microbiology/December 2025 regular P.png", tr("December 2025", "Dezember 2025"), tr("Regular", "Standard"), tr("Pasteurized", "Pasteurisiert"), tr("Qualitative comparison image; risk classification remains based on the matched LIMS observation.", "Qualitatives Vergleichsbild; die Risikoklassifizierung basiert weiterhin auf der zugeordneten LIMS-Beobachtung.")),
        (tr("July 2025 Regular P", "Juli 2025 Standard P"), "data/microbiology/July 2025 regular P.png", tr("July 2025", "Juli 2025"), tr("Regular", "Standard"), tr("Pasteurized", "Pasteurisiert"), tr("Pasteurized beverage system; thermal processing is evaluated against the measured LIMS status, not by image enumeration.", "Pasteurisiertes Getränkesystem; die thermische Behandlung wird anhand des gemessenen LIMS-Status und nicht durch Bildauszählung bewertet.")),
        (tr("July 2025 Spritz P", "Juli 2025 Spritz P"), "data/microbiology/July 2025 spritz P.png", tr("July 2025", "Juli 2025"), "Spritz", tr("Pasteurized", "Pasteurisiert"), tr("Pasteurized beverage system; thermal processing is evaluated against the measured LIMS status, not by image enumeration.", "Pasteurisiertes Getränkesystem; die thermische Behandlung wird anhand des gemessenen LIMS-Status und nicht durch Bildauszählung bewertet.")),
    ]
    non_pasteurized_images = [
        (tr("July 2025 Regular NP", "Juli 2025 Standard NP"), "data/microbiology/July 2025 regular NP.png", tr("July 2025", "Juli 2025"), tr("Regular", "Standard"), tr("Non-pasteurized", "Nicht pasteurisiert"), tr("Non-pasteurized beverage system used as a comparative control for preservation effectiveness.", "Nicht pasteurisiertes Getränkesystem als Vergleichskontrolle für die Konservierungswirkung.")),
        (tr("July 2025 Spritz NP", "Juli 2025 Spritz NP"), "data/microbiology/July 2025 sprits NP.png", tr("July 2025", "Juli 2025"), "Spritz", tr("Non-pasteurized", "Nicht pasteurisiert"), tr("Non-pasteurized beverage system used as a comparative control for preservation effectiveness.", "Nicht pasteurisiertes Getränkesystem als Vergleichskontrolle für die Konservierungswirkung.")),
    ]
    for group_title, group_subtitle, group_images in [
        (
            tr("Pasteurized beverage systems", "Pasteurisierte Getränkesysteme"),
            tr("Thermally treated beverage formulations presented for qualitative microbiological comparison.", "Thermisch behandelte Getränkeformulierungen für den qualitativen mikrobiologischen Vergleich."),
            pasteurized_images,
        ),
        (
            tr("Non-pasteurized beverage systems", "Nicht pasteurisierte Getränkesysteme"),
            tr("Untreated beverage formulations used for comparative microbial risk assessment.", "Unbehandelte Getränkeformulierungen für die vergleichende Bewertung des mikrobiologischen Risikos."),
            non_pasteurized_images,
        ),
    ]:
        st.subheader(group_title)
        st.caption(group_subtitle)
        for row_start in range(0, len(group_images), 2):
            image_columns = st.columns(2)
            for image_column, (title, image_path, manufacturing_date, product_type, processing, interpretation) in zip(image_columns, group_images[row_start:row_start + 2]):
                with image_column:
                    st.subheader(title)
                    st.image(image_path, width="stretch")
                    st.markdown(
                        f"- {tr('Manufacturing date', 'Herstellungsdatum')}: {manufacturing_date}\n"
                        f"- {tr('Product type', 'Produkttyp')}: {product_type}\n"
                        f"- {tr('Processing condition', 'Behandlungsbedingung')}: {processing}\n"
                        f"- {tr('Microbiological interpretation', 'Mikrobiologische Interpretation')}: {interpretation}"
                    )
                    st.caption(tr("Representative qualitative microbiological evidence only. No colony count, CFU value, or microbiological status is inferred from this photograph.", "Nur repräsentativer qualitativer mikrobiologischer Bildnachweis. Aus der Fotografie werden weder Koloniezahl noch KBE-Wert oder mikrobiologischer Status abgeleitet."))

with microbiology_tabs[3]:
    st.header(tr("Scientific interpretation", "Wissenschaftliche Interpretation"))
    if lims_microbiology.empty or micro_status_column is None:
        st.info(tr("Scientific interpretation is withheld because measured qualitative status fields from LIMS_Microbial_Audit.csv are not currently available.", "Eine wissenschaftliche Interpretation erfolgt nicht, da die gemessenen qualitativen Statusfelder aus LIMS_Microbial_Audit.csv derzeit nicht verfügbar sind."))
    else:
        interpretation_data = lims_microbiology.copy()
        interpretation_data["Risk Classification"] = interpretation_data.apply(qualitative_risk_classification, axis=1)
        critical_treatments = []
        if micro_processing_column is not None:
            critical_treatments = interpretation_data.loc[
                interpretation_data["Risk Classification"] == "CRITICAL", micro_processing_column
            ].dropna().astype(str).unique().tolist()
        st.markdown(tr(
            "Interpretation is restricted to recorded qualitative observations, manufacturing dates, culture media, and treatment categories. **TNTC** is classified as **CRITICAL** contamination risk; **Very high growth** as severe microbial instability; **Low Growth** as limited microbial activity; and **Negative/Safe** observations as no detectable growth/acceptable microbiological condition within the applied method.",
            "Die Interpretation beschränkt sich auf dokumentierte qualitative Beobachtungen, Herstellungsdaten, Nährmedien und Behandlungskategorien. **TNTC** wird als **KRITISCHES** Kontaminationsrisiko, **sehr starkes Wachstum** als ausgeprägte mikrobielle Instabilität, **geringes Wachstum** als begrenzte mikrobielle Aktivität und **negativ/unbedenklich** als kein nachweisbares Wachstum beziehungsweise akzeptabler mikrobiologischer Zustand innerhalb der angewandten Methode eingestuft.",
        ))
        if micro_processing_column is not None:
            treatment_summary = (
                interpretation_data.groupby([micro_processing_column, "Risk Classification"], as_index=False)
                .size()
                .rename(columns={"size": "Qualitative LIMS records (not plate count)"})
            )
            st.dataframe(localized_table(treatment_summary), width="stretch", hide_index=True)
            st.caption(tr("This table summarizes the 12 qualitative LIMS records (6 beverage systems × 2 media). It is not the total incubated plate count; the experimental total remains 156 plates, including analytical replicates and two laboratory days.", "Diese Tabelle fasst die 12 qualitativen LIMS-Datensätze zusammen (6 Getränkesysteme × 2 Nährmedien). Sie entspricht nicht der Gesamtzahl inkubierter Platten; der Versuchsumfang bleibt bei 156 Platten einschließlich analytischer Wiederholungen und zweier Labortage."))
            st.markdown(tr(f"The treatment comparison is descriptive and uses the reported **{micro_processing_column}** category only. It does not establish a causal processing effect or compliance decision.", f"Der Behandlungsvergleich ist deskriptiv und verwendet ausschließlich die dokumentierte Kategorie **{GERMAN_TABLE_COLUMNS.get(micro_processing_column, micro_processing_column)}**. Er belegt weder einen kausalen Verarbeitungseffekt noch eine Konformitätsentscheidung."))
            if critical_treatments:
                localized_critical_treatments = [GERMAN_TABLE_VALUES.get(value, value) for value in critical_treatments]
                st.markdown(tr(f"Critical qualitative observations in this audit are recorded for: **{', '.join(critical_treatments)}**. This finding supports targeted QA review of the recorded treatment condition; it is not a numerical prevalence estimate.", f"Kritische qualitative Beobachtungen sind in diesem Audit für folgende Bedingungen dokumentiert: **{', '.join(localized_critical_treatments)}**. Dieser Befund unterstützt eine gezielte QS-Prüfung der dokumentierten Behandlung; er ist keine numerische Prävalenzschätzung."))
        if micro_date_column is not None:
            st.markdown(tr(f"Manufacturing-date comparisons use the recorded **{micro_date_column}** values only; no microbial growth curve or storage-time extrapolation is fitted.", f"Vergleiche nach Herstellungsdatum verwenden ausschließlich die dokumentierten Werte aus **{GERMAN_TABLE_COLUMNS.get(micro_date_column, micro_date_column)}**; es wird weder eine mikrobielle Wachstumskurve angepasst noch über die Lagerungsdauer extrapoliert."))
        st.markdown(tr(
            "For this acidic beverage system, the reported pH (~2.7) is an inhibitory hurdle for many bacteria, while ethanol can further constrain microbial survival. These intrinsic factors do not replace the measured LIMS observations or prove product stability. In fruit beverages, acid-tolerant yeasts and moulds remain relevant spoilage concerns, so negative observations on the yeast-and-mould medium are interpreted only as no detectable growth under the recorded analytical conditions.\n\nThe recorded non-pasteurised observations and pasteurised observations are displayed side-by-side to support quality-assurance review. The observed treatment-associated pattern is descriptive and dataset-specific. It does not independently establish causal pasteurization efficacy because the observations are qualitative, packaging preparation was not microbiologically controlled, and experimental groups may differ in age and treatment.",
            "Für dieses saure Getränkesystem stellt der dokumentierte pH-Wert (~2,7) eine hemmende Hürde für viele Bakterien dar; Ethanol kann das mikrobielle Überleben zusätzlich begrenzen. Diese intrinsischen Faktoren ersetzen weder die gemessenen LIMS-Beobachtungen noch belegen sie die Produktstabilität. In Fruchtgetränken bleiben säuretolerante Hefen und Schimmelpilze relevante Verderbsorganismen. Negative Beobachtungen auf dem Hefe-Schimmel-Nährmedium werden daher nur als kein nachweisbares Wachstum unter den dokumentierten Analysebedingungen interpretiert.\n\nDie dokumentierten nicht pasteurisierten und pasteurisierten Beobachtungen werden für die Qualitätssicherungsprüfung nebeneinander dargestellt. Das behandlungsbezogene Muster ist deskriptiv und datensatzspezifisch. Es belegt keine kausale Pasteurisationswirksamkeit, da die Beobachtungen qualitativ sind, die Verpackungsvorbereitung mikrobiologisch nicht kontrolliert wurde und sich die Versuchsgruppen hinsichtlich Alter und Behandlung unterscheiden können.",
        ))
        st.warning(T["bottle_limitation"])

with microbiology_tabs[4]:
    st.header(tr("Evidence-based shelf-life assessment", "Evidenzbasierte Haltbarkeitsbewertung"))
    st.caption(tr("No expiry date, quantitative enumeration, regression model, or shelf-life duration is estimated from this dashboard.", "Dieses Dashboard schätzt weder ein Verfallsdatum noch quantitative Keimzahlen, ein Regressionsmodell oder eine Haltbarkeitsdauer."))
    if lims_microbiology.empty or micro_date_column is None:
        st.warning(M["shelf_statement"])
    else:
        microbiology_timeline_data = lims_microbiology.copy()
        microbiology_timeline_data["Manufacturing_Date"] = pd.to_datetime(microbiology_timeline_data[micro_date_column], errors="coerce", dayfirst=True)
        microbiology_timeline_data["Risk Classification"] = microbiology_timeline_data.apply(qualitative_risk_classification, axis=1)
        risk_order = {"SAFE": 0, "LOW RISK": 1, "MODERATE RISK": 2, "CRITICAL": 3, "Unclassified": -1}
        microbiology_timeline_data["Risk rank"] = microbiology_timeline_data["Risk Classification"].map(risk_order)
        sample_timeline = microbiology_timeline_data.sort_values("Risk rank").groupby(
            micro_sample_column if micro_sample_column is not None else microbiology_timeline_data.index.name,
            as_index=False,
        ).tail(1)
        if micro_sample_column is None:
            sample_timeline["LIMS_Record"] = sample_timeline.index.astype(str)
        timeline_y = micro_sample_column if micro_sample_column is not None else "LIMS_Record"
        plot_sample_timeline = localized_table(sample_timeline)
        plot_x = GERMAN_TABLE_COLUMNS.get("Manufacturing_Date", "Manufacturing_Date") if LANG == "DE" else "Manufacturing_Date"
        plot_y = GERMAN_TABLE_COLUMNS.get(timeline_y, timeline_y) if LANG == "DE" else timeline_y
        plot_color = GERMAN_TABLE_COLUMNS.get("Risk Classification", "Risk Classification") if LANG == "DE" else "Risk Classification"
        plot_symbol = GERMAN_TABLE_COLUMNS.get(micro_processing_column, micro_processing_column) if LANG == "DE" else micro_processing_column
        plot_hover = [GERMAN_TABLE_COLUMNS.get(column, column) if LANG == "DE" else column for column in [micro_status_column, micro_short_status_column, micro_normalized_status_column, "Risk Classification"] if column is not None]
        raw_risk_order = ["SAFE", "LOW RISK", "MODERATE RISK", "CRITICAL", "Unclassified"]
        plot_risk_order = [GERMAN_TABLE_VALUES.get(value, value) if LANG == "DE" else value for value in raw_risk_order]
        plot_color_map = {GERMAN_TABLE_VALUES.get(key, key) if LANG == "DE" else key: value for key, value in {"SAFE": "#2a9d8f", "LOW RISK": "#e9c46a", "MODERATE RISK": "#f4a261", "CRITICAL": "#e63946", "Unclassified": "#6c757d"}.items()}
        fig_micro_timeline = px.scatter(
            plot_sample_timeline.dropna(subset=[plot_x]),
            x=plot_x,
            y=plot_y,
            color=plot_color,
            symbol=plot_symbol,
            hover_data=plot_hover,
            category_orders={plot_color: plot_risk_order},
            color_discrete_map=plot_color_map,
            template=chart_theme,
            title=tr("Sample-level worst observed qualitative microbiological risk by manufacturing date", "Schwerstes beobachtetes qualitatives mikrobiologisches Risiko je Probe und Herstellungsdatum"),
        )
        st.plotly_chart(fig_micro_timeline, width="stretch")
        st.dataframe(localized_table(microbiology_timeline_data.sort_values("Manufacturing_Date")), width="stretch", hide_index=True)
        st.warning(M["shelf_statement"])

with microbiology_tabs[5]:
    st.header(tr("Literature support and analytical standards", "Literaturgrundlage und analytische Standards"))
    st.caption(tr("Peer-reviewed context and official enumeration methods are provided for scientific framing; they do not replace the LIMS record or product-specific regulatory criteria.", "Begutachtete Fachliteratur und offizielle Zählmethoden dienen der wissenschaftlichen Einordnung; sie ersetzen weder den LIMS-Datensatz noch produktspezifische regulatorische Kriterien."))
    st.markdown(tr(
        "- *The incidence and impact of microbial spoilage in the production of fruit and vegetable juices as reported by juice manufacturers* (2018). Food Control, 85, 144–150. DOI: [10.1016/j.foodcont.2017.09.025](https://doi.org/10.1016/j.foodcont.2017.09.025)\n- Wareing, P. (2016). *Microbiology of soft drinks and fruit juices*. DOI: [10.1002/9781118634943.ch11](https://doi.org/10.1002/9781118634943.ch11)\n- U.S. Food and Drug Administration. *Bacteriological Analytical Manual, Chapter 3: Aerobic Plate Count*. [FDA BAM](https://www.fda.gov/food/laboratory-methods-food/bam-chapter-3-aerobic-plate-count)\n- ISO 4833-1:2013. *Microbiology of the food chain — Colony count at 30 °C by the pour plate technique*. [ISO record](https://www.iso.org/standard/53728.html)\n- ISO 21527-1:2008. *Enumeration of yeasts and moulds — Colony count technique*. [ISO record](https://www.iso.org/standard/38275.html)\n- ICMSF. *Microorganisms in Foods* series: principles and applications for food microbiological safety and quality.",
        "- *Vorkommen und Auswirkungen mikrobiellen Verderbs bei der Herstellung von Frucht- und Gemüsesäften aus Sicht der Safthersteller* (2018). Food Control, 85, 144–150. DOI: [10.1016/j.foodcont.2017.09.025](https://doi.org/10.1016/j.foodcont.2017.09.025)\n- Wareing, P. (2016). *Mikrobiologie von Erfrischungsgetränken und Fruchtsäften*. DOI: [10.1002/9781118634943.ch11](https://doi.org/10.1002/9781118634943.ch11)\n- U.S. Food and Drug Administration. *Bakteriologisches Analysehandbuch, Kapitel 3: Aerobe Plattenzählung*. [FDA BAM](https://www.fda.gov/food/laboratory-methods-food/bam-chapter-3-aerobic-plate-count)\n- ISO 4833-1:2013. *Mikrobiologie der Lebensmittelkette — Koloniezählung bei 30 °C mittels Gussplattenverfahren*. [ISO-Eintrag](https://www.iso.org/standard/53728.html)\n- ISO 21527-1:2008. *Zählung von Hefen und Schimmelpilzen — Koloniezählverfahren*. [ISO-Eintrag](https://www.iso.org/standard/38275.html)\n- ICMSF. Reihe *Microorganisms in Foods*: Grundsätze und Anwendungen für mikrobiologische Lebensmittelsicherheit und -qualität.",
    ))

top_tabs[0].markdown(
    f'<div class="workspace-banner"><strong>{tr("Executive overview", "Managementübersicht")}</strong><span>{tr("Start here for the study structure, analytical coverage and evidence status. Use the primary navigation above to open a scientific module.", "Startpunkt für Studienstruktur, analytische Abdeckung und Evidenzstatus. Über die primäre Navigation oben wird ein wissenschaftliches Modul geöffnet.")}</span></div>',
    unsafe_allow_html=True,
)
top_tabs[0].markdown(f"### {T['study_architecture']}")
top_tabs[0].write(tr("Four independent analytical modules contribute complementary evidence. Integration is limited to high-level narrative interpretation.", "Vier unabhängige Analysemodule liefern sich ergänzende Erkenntnisse. Die Integration beschränkt sich auf eine übergeordnete narrative Interpretation."))
top_tabs[0].markdown(
    f"""
    <div class="evidence-grid">
        <div class="evidence-card" style="--card-accent:#146c94">
            <div class="evidence-index">01 · {tr('STRUCTURE', 'STRUKTUR')}</div>
            <div class="evidence-name">{T['rheology']}</div>
            <div class="evidence-detail">{tr('Flow, amplitude and frequency response with replicate-aware sample identities.', 'Fließ-, Amplituden- und Frequenzantwort mit replikatbezogenen Probenkennungen.')}</div>
            <div class="evidence-status">{tr('Quantitative evidence', 'Quantitative Evidenz')}</div>
        </div>
        <div class="evidence-card" style="--card-accent:#2fa7b8">
            <div class="evidence-index">02 · {tr('COMPOSITION', 'ZUSAMMENSETZUNG')}</div>
            <div class="evidence-name">{T['physicochemical']}</div>
            <div class="evidence-detail">{tr('Measured pH, density, Brix and composition-related endpoints.', 'Gemessene Endpunkte zu pH, Dichte, Brix und Zusammensetzung.')}</div>
            <div class="evidence-status">{tr('Workbook traceable', 'Arbeitsmappe rückverfolgbar')}</div>
        </div>
        <div class="evidence-card" style="--card-accent:#d9aa52">
            <div class="evidence-index">03 · {tr('PHYSICAL STATE', 'PHYSIKALISCHER ZUSTAND')}</div>
            <div class="evidence-name">{T['sedimentation']}</div>
            <div class="evidence-detail">{tr('Direct graduated-cylinder observations at two documented time points.', 'Direkte Messzylinderbeobachtungen zu zwei dokumentierten Zeitpunkten.')}</div>
            <div class="evidence-status">{tr('Descriptive evidence', 'Deskriptive Evidenz')}</div>
        </div>
        <div class="evidence-card" style="--card-accent:#68a67d">
            <div class="evidence-index">04 · {tr('PRODUCT SAFETY', 'PRODUKTSICHERHEIT')}</div>
            <div class="evidence-name">{T['microbiology']}</div>
            <div class="evidence-detail">{tr('Qualitative LIMS outcomes supported by representative plate images.', 'Qualitative LIMS-Ergebnisse, ergänzt durch repräsentative Plattenbilder.')}</div>
            <div class="evidence-status">{tr('Qualitative evidence', 'Qualitative Evidenz')}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
summary_kpis = top_tabs[0].columns(3)
summary_kpis[0].metric(tr("Analytical modules", "Analysemodule"), 4)
summary_kpis[1].metric(tr("Rheology sample families", "Rheologische Probenfamilien"), sample_overview["Sample_ID"].nunique())
summary_kpis[2].metric(tr("Physicochemical samples", "Physikochemische Proben"), physchem["Sample_ID"].nunique() if not physchem.empty else T["not_loaded"])
summary_kpis = top_tabs[0].columns(3)
summary_kpis[0].metric(tr("Sedimentation samples", "Sedimentationsproben"), 7)
summary_kpis[1].metric(tr("Microbiology beverage systems", "Mikrobiologische Getränkesysteme"), lims_microbiology["Sample"].nunique() if not lims_microbiology.empty else T["not_loaded"])
summary_kpis[2].metric(tr("Total microbiological plates processed", "Verarbeitete mikrobiologische Platten insgesamt"), "156")

if show_methodology:
    top_tabs[0].markdown(tr("### Evidence and methodology matrix", "### Evidenz- und Methodenmatrix"))
    methodology_matrix = pd.DataFrame([
        {
            tr("Module", "Modul"): T["rheology"],
            tr("Evidence basis", "Evidenzbasis"): tr("Instrumental measurements + derived parameters", "Instrumentelle Messungen + abgeleitete Parameter"),
            tr("Replication", "Replikation"): tr("Retained in metadata", "In Metadaten beibehalten"),
            tr("Primary limitation", "Zentrale Limitation"): tr("Model parameters remain range-specific", "Modellparameter bleiben messbereichsspezifisch"),
        },
        {
            tr("Module", "Modul"): T["physicochemical"],
            tr("Evidence basis", "Evidenzbasis"): tr("Measured workbook endpoints", "Gemessene Arbeitsmappen-Endpunkte"),
            tr("Replication", "Replikation"): tr("As recorded in source", "Wie in der Quelle dokumentiert"),
            tr("Primary limitation", "Zentrale Limitation"): tr("No unverified cross-module matching", "Keine ungeprüfte modulübergreifende Zuordnung"),
        },
        {
            tr("Module", "Modul"): T["sedimentation"],
            tr("Evidence basis", "Evidenzbasis"): tr("Two direct volume observations", "Zwei direkte Volumenbeobachtungen"),
            tr("Replication", "Replikation"): tr("Not available", "Nicht verfügbar"),
            tr("Primary limitation", "Zentrale Limitation"): tr("No kinetic or inferential modelling", "Keine kinetische oder inferenzstatistische Modellierung"),
        },
        {
            tr("Module", "Modul"): T["microbiology"],
            tr("Evidence basis", "Evidenzbasis"): tr("Qualitative LIMS audit", "Qualitatives LIMS-Audit"),
            tr("Replication", "Replikation"): tr("Plate total documented; identifier absent", "Plattenzahl dokumentiert; Kennung fehlt"),
            tr("Primary limitation", "Zentrale Limitation"): tr("No CFU/mL inference from images", "Keine KBE/mL-Ableitung aus Bildern"),
        },
    ])
    top_tabs[0].dataframe(localized_table(methodology_matrix), width="stretch", hide_index=True)

top_tabs[0].markdown(
    f'<div class="governance-note"><strong>{tr("Scientific governance:", "Wissenschaftliche Governance:")}</strong> '
    f'{tr("Measured observations, derived calculations, literature-supported interpretation and hypotheses are kept conceptually distinct. This separation supports examination-level traceability and prevents visual presentation from overstating evidential strength.", "Gemessene Beobachtungen, abgeleitete Berechnungen, literaturgestützte Interpretation und Hypothesen werden konzeptionell getrennt. Diese Trennung unterstützt die prüfungsrelevante Rückverfolgbarkeit und verhindert, dass die visuelle Darstellung die Evidenzstärke überzeichnet.")}</div>',
    unsafe_allow_html=True,
)
top_tabs[0].markdown(f"### {T['integrated_conclusion']}")
top_tabs[0].write(tr("The dashboard presents module-specific measured evidence without merging experimental identifiers or performing cross-module statistical comparisons.", "Das Dashboard stellt modulspezifische Messdaten dar, ohne experimentelle Kennungen zusammenzuführen oder modulübergreifende statistische Vergleiche durchzuführen."))
top_tabs[0].info(T["data_integrity"])

with rheology_tabs[0]:
    st.header(tr("Rheology Overview and Experimental Design", "Rheologieübersicht und Versuchsdesign"))
    st.markdown(tr("### Why Rheology Was Performed", "### Warum rheologische Untersuchungen durchgeführt wurden"))
    st.write(tr("Rheology was selected because structural, viscoelastic, and flow properties are relevant to physical stability and suspension behaviour.", "Rheologische Untersuchungen wurden gewählt, weil Struktur-, viskoelastische und Fließeigenschaften für die physikalische Stabilität und das Suspensionsverhalten relevant sind."))
    st.markdown(tr("### Experimental Design", "### Versuchsdesign"))
    st.write(tr("Methods: Flow curve, amplitude sweep, frequency sweep. Instrument: Kinexus Prime Lab+. Research partners: Hochschule Ansbach and Marmeladenherz.", "Methoden: Fließkurve, Amplitudensweep und Frequenzsweep. Gerät: Kinexus Prime Lab+. Forschungspartner: Hochschule Ansbach und Marmeladenherz."))
    st.markdown(tr("### Instrumentation and measurement sequence", "### Instrumentierung und Messablauf"))
    st.image(
        "images/kinexus_rheometer_workflow.png",
        caption=tr(
            "Kinexus Prime Lab+ rheometer: instrument overview, sample loading and measuring position.",
            "Kinexus Prime Lab+ Rheometer: Geräteübersicht, Probenauftrag und Messposition.",
        ),
        width="stretch",
    )
    instrument_views = st.columns(3)
    instrument_views[0].markdown(
        tr(
            "**01 · Instrument platform**  \nKinexus Prime Lab+ rotational rheometer used for the flow-curve, amplitude-sweep and frequency-sweep measurements.",
            "**01 · Geräteplattform**  \nKinexus Prime Lab+ Rotationsrheometer für Fließkurven-, Amplitudensweep- und Frequenzsweep-Messungen.",
        )
    )
    instrument_views[1].markdown(
        tr(
            "**02 · Sample loading**  \nBeverage sample positioned centrally on the lower measuring plate before the measuring system is closed.",
            "**02 · Probenauftrag**  \nZentral auf der unteren Messplatte positionierte Getränkeprobe vor dem Schließen des Messsystems.",
        )
    )
    instrument_views[2].markdown(
        tr(
            "**03 · Measurement position**  \nUpper geometry lowered into the measurement position for controlled rotational and oscillatory characterisation.",
            "**03 · Messposition**  \nIn Messposition abgesenkte obere Geometrie für die kontrollierte rotatorische und oszillatorische Charakterisierung.",
        )
    )
    st.metric(tr("Parent samples / replicate measurements", "Ausgangsproben / Wiederholungsmessungen"), f"{sample_overview['Sample_ID'].nunique()} / {len(meta)}")
    st.markdown(tr("### Rheology results summary", "### Zusammenfassung der Rheologieergebnisse"))
    st.write(tr(f"Mean G′: {mean_gprime:.3g} Pa; Mean G″: {mean_gdouble:.3g} Pa; Mean tanδ: {mean_tandelta:.3f}; flow index n: {flow_behavior_index_n:.3f}.", f"Mittleres G′: {mean_gprime:.3g} Pa; mittleres G″: {mean_gdouble:.3g} Pa; mittleres tanδ: {mean_tandelta:.3f}; Fließindex n: {flow_behavior_index_n:.3f}."))

with rheology_tabs[1]:
    st.header(tr("Flow curve", "Fließkurve"))
    st.caption(tr("Measured flow response for processing, filling, pouring, and oral-flow assessment.", "Gemessenes Fließverhalten zur Beurteilung von Verarbeitung, Abfüllung, Ausgießen und oralem Fluss."))
    flow_samples = sorted(flow["Sample_Family"].dropna().unique())
    selected_flow_sample = st.selectbox(tr("Sample family", "Probenfamilie"), flow_samples, key="flow_sample")
    selected_flow = flow[flow["Sample_Family"] == selected_flow_sample]
    flow_curve = measured_curve(selected_flow, "ɣ̇ (s⁻¹)", ["η (Pa s)", "σ (Pa)"])
    flow_details, flow_fit_points = power_law_model_details(selected_flow)
    flow_n, flow_k, flow_r2 = flow_details["n"], flow_details["k"], flow_details["r2"]
    eta_low, shear_low = nearest_measured_value(flow_curve, "ɣ̇ (s⁻¹)", "η (Pa s)", 1)
    eta_high, shear_high = nearest_measured_value(flow_curve, "ɣ̇ (s⁻¹)", "η (Pa s)", 100)
    viscosity_retention = eta_high / eta_low * 100 if pd.notna(eta_low) and eta_low != 0 else np.nan

    flow_kpi = st.columns(4)
    flow_kpi[0].metric(tr("Flow behavior index, n", "Fließverhaltensindex n"), f"{flow_n:.3f}", help=tr("Log–log slope of measured shear stress versus shear rate. n < 1 indicates shear-thinning within this measurement range.", "Log-Log-Steigung der gemessenen Schubspannung gegenüber der Scherrate. n < 1 weist in diesem Messbereich auf Scherverdünnung hin."))
    flow_kpi[1].metric(tr("Consistency coefficient, K", "Konsistenzkoeffizient K"), f"{flow_k:.3g} Pa·sⁿ", help=tr("Power-law coefficient from the measured stress–shear-rate fit.", "Potenzgesetz-Koeffizient aus der Anpassung von Schubspannung und Scherrate."))
    flow_kpi[2].metric(tr("Stress-fit R²", "R² der Spannungsanpassung"), f"{flow_r2:.3f}", help=tr("Goodness of fit for the power-law calculation; this is not a separate measurement.", "Anpassungsgüte der Potenzgesetzberechnung; dies ist keine separate Messung."))
    flow_kpi[3].metric(tr("Viscosity retained", "Verbleibende Viskosität"), f"{viscosity_retention:.1f}%", help=tr(f"Ratio of the values nearest to {shear_high:.3g} and {shear_low:.3g} s⁻¹; no interpolation is used.", f"Verhältnis der Werte nahe {shear_high:.3g} und {shear_low:.3g} s⁻¹; es wird nicht interpoliert."))

    fig_flow = go.Figure()
    for replicate, replicate_data in selected_flow.groupby("Sample"):
        fig_flow.add_trace(go.Scatter(x=replicate_data["ɣ̇ (s⁻¹)"], y=replicate_data["η (Pa s)"], mode="lines+markers", name=f"{replicate}",
            line=dict(color="#8ba6bd", width=1), marker=dict(size=4, color="#8ba6bd"), legendgroup="replicates", showlegend=False,
            hovertemplate=tr("Replicate ", "Wiederholung ") + str(replicate) + tr("<br>Shear rate: %{x:.3g} s⁻¹<br>Apparent viscosity: %{y:.3g} Pa·s<extra></extra>", "<br>Scherrate: %{x:.3g} s⁻¹<br>Scheinbare Viskosität: %{y:.3g} Pa·s<extra></extra>")))
    fig_flow.add_trace(go.Scatter(x=flow_curve["ɣ̇ (s⁻¹)"], y=flow_curve["η (Pa s)"], mode="lines+markers", name=tr(f"{selected_flow_sample} mean", f"{selected_flow_sample} Mittelwert"),
        line=dict(color="#1f4e79", width=4), marker=dict(size=7, color="#1f4e79"),
        hovertemplate=tr("Parent mean<br>Shear rate: %{x:.3g} s⁻¹<br>Apparent viscosity: %{y:.3g} Pa·s<extra></extra>", "Mittelwert der Ausgangsprobe<br>Scherrate: %{x:.3g} s⁻¹<br>Scheinbare Viskosität: %{y:.3g} Pa·s<extra></extra>")))
    fig_flow.update_layout(title=tr("Measured apparent viscosity versus shear rate", "Gemessene scheinbare Viskosität in Abhängigkeit von der Scherrate"), template=chart_theme, xaxis_type="log", yaxis_type="log", xaxis_title=tr("Shear rate (s⁻¹)", "Scherrate (s⁻¹)"), yaxis_title=tr("Apparent viscosity (Pa·s)", "Scheinbare Viskosität (Pa·s)"))
    fig_flow.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    st.plotly_chart(fig_flow, width="stretch")

    stress_summary = (
        selected_flow.groupby("ɣ̇ (s⁻¹)", as_index=False)
        .agg(
            **{
                "Mean stress (Pa)": ("σ (Pa)", "mean"),
                "SD stress (Pa)": ("σ (Pa)", "std"),
                "Replicates": ("σ (Pa)", "count"),
            }
        )
        .rename(columns={"ɣ̇ (s⁻¹)": "Shear rate (s⁻¹)"})
    )
    stress_summary["SD stress (Pa)"] = stress_summary["SD stress (Pa)"].fillna(0)
    fig_stress = go.Figure()
    for replicate, replicate_data in selected_flow.groupby("Sample"):
        fig_stress.add_trace(go.Scatter(
            x=replicate_data["ɣ̇ (s⁻¹)"], y=replicate_data["σ (Pa)"], mode="lines+markers", name=str(replicate), showlegend=False,
            line=dict(color="#b8c7d4", width=1), marker=dict(color="#b8c7d4", size=4),
            hovertemplate=tr("Replicate ", "Wiederholung ") + str(replicate) + tr("<br>Shear rate: %{x:.3g} s⁻¹<br>Shear stress: %{y:.3g} Pa<extra></extra>", "<br>Scherrate: %{x:.3g} s⁻¹<br>Schubspannung: %{y:.3g} Pa<extra></extra>"),
        ))
    fig_stress.add_trace(go.Scatter(
        x=stress_summary["Shear rate (s⁻¹)"], y=stress_summary["Mean stress (Pa)"], mode="lines+markers", name=tr("Parent-sample mean ± SD", "Mittelwert der Ausgangsprobe ± SD"),
        error_y=dict(type="data", array=stress_summary["SD stress (Pa)"], visible=True, thickness=1.3, width=3),
        line=dict(color="#1f4e79", width=4), marker=dict(color="#1f4e79", size=7),
        hovertemplate=tr("Parent mean<br>Shear rate: %{x:.3g} s⁻¹<br>Stress: %{y:.3g} ± %{error_y.array:.3g} Pa<extra></extra>", "Mittelwert der Ausgangsprobe<br>Scherrate: %{x:.3g} s⁻¹<br>Spannung: %{y:.3g} ± %{error_y.array:.3g} Pa<extra></extra>"),
    ))
    fig_stress.update_layout(title=tr("Measured shear stress versus shear rate", "Gemessene Schubspannung in Abhängigkeit von der Scherrate"), template=chart_theme, xaxis_type="log", yaxis_type="log", xaxis_title=tr("Shear rate (s⁻¹)", "Scherrate (s⁻¹)"), yaxis_title=tr("Shear stress (Pa)", "Schubspannung (Pa)"), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    st.plotly_chart(fig_stress, width="stretch")

    model_table = pd.DataFrame([{
        "Model": "Power law", "Converged": "Yes", "n": flow_details["n"], "K (Pa·sⁿ)": flow_details["k"], "Yield stress": "Not fitted", "Adjusted R²": flow_details["adj_r2"], "RMSE (Pa)": flow_details["rmse"], "AICc": flow_details["aicc"], "ΔAICc": 0.0, "Observations": flow_details["n_obs"],
    }])
    st.caption(tr("Descriptive constitutive-model diagnostic; it is not used as a material-property result when model quality is inadequate.", "Deskriptive Diagnose des Stoffmodells; bei unzureichender Modellgüte wird sie nicht als Ergebnis einer Materialeigenschaft verwendet."))
    st.dataframe(localized_table(model_table), width="stretch", hide_index=True)
    if pd.notna(flow_details["r2"]) and flow_details["r2"] < 0.80:
        st.warning(tr("The fitted power-law model does not adequately represent the complete measured range. The reported K and n values are descriptive and should not be treated as reliable intrinsic material constants.", "Das angepasste Potenzgesetz bildet den vollständigen Messbereich nicht ausreichend ab. Die angegebenen Werte K und n sind deskriptiv und nicht als verlässliche intrinsische Materialkonstanten zu behandeln."))
    if not flow_fit_points.empty:
        with st.expander(tr("Power-law diagnostic residuals", "Diagnostische Residuen des Potenzgesetzes"), expanded=False):
            fig_residual = go.Figure(go.Scatter(x=flow_fit_points["Fitted stress (Pa)"], y=flow_fit_points["Stress residual (Pa)"], mode="markers", marker=dict(color="#1f4e79", size=7), name=tr("Measured residual", "Gemessenes Residuum")))
            fig_residual.add_hline(y=0, line_dash="dash", line_color="#555555")
            fig_residual.update_layout(title=tr("Residuals for the descriptive, non-accepted power-law fit", "Residuen der deskriptiven, nicht akzeptierten Potenzgesetzanpassung"), template=chart_theme, xaxis_title=tr("Fitted shear stress (Pa)", "Angepasste Schubspannung (Pa)"), yaxis_title=tr("Measured − fitted stress (Pa)", "Gemessene − angepasste Spannung (Pa)"))
            st.plotly_chart(fig_residual, width="stretch")

    st.markdown(tr("### Industrial interpretation — selected sample", "### Industrielle Interpretation – ausgewählte Probe"))
    if pd.notna(flow_n):
        behavior = tr("shear-thinning", "scherverdünnend") if flow_n < 0.95 else tr("approximately Newtonian over the measured range", "im Messbereich annähernd newtonsch") if flow_n <= 1.05 else tr("shear-thickening", "scherverdickend")
        st.write(tr(f"**{selected_flow_sample}** is {behavior} by the measured power-law index (n = {flow_n:.3f}; R² = {flow_r2:.3f}).", f"**{selected_flow_sample}** zeigt gemäß gemessenem Potenzgesetzindex ein {behavior}es Verhalten (n = {flow_n:.3f}; R² = {flow_r2:.3f})."))
    st.write(tr(f"Measured apparent viscosity is {eta_low:.3g} Pa·s at the available setpoint nearest {shear_low:.3g} s⁻¹ and {eta_high:.3g} Pa·s near {shear_high:.3g} s⁻¹. The latter is {viscosity_retention:.1f}% of the former.", f"Die gemessene scheinbare Viskosität beträgt {eta_low:.3g} Pa·s am verfügbaren Sollwert nahe {shear_low:.3g} s⁻¹ und {eta_high:.3g} Pa·s nahe {shear_high:.3g} s⁻¹. Der zweite Wert entspricht {viscosity_retention:.1f}% des ersten."))
    st.caption(tr("K, n, R² and retention are calculations from the displayed measured points. They do not establish a yield stress or extrapolate beyond the workbook range.", "K, n, R² und Retention sind Berechnungen aus den dargestellten Messpunkten. Sie belegen keine Fließgrenze und extrapolieren nicht über den Arbeitsmappenbereich hinaus."))

with rheology_tabs[2]:
    st.header(tr("Amplitude sweep", "Amplitudensweep"))
    st.caption(tr("Measured deformation tolerance and structure-retention assessment.", "Bewertung der gemessenen Verformungstoleranz und Strukturerhaltung."))
    amp_samples = sorted(amp["Sample_Family"].dropna().unique())
    selected_amp_sample = st.selectbox(tr("Sample family", "Probenfamilie"), amp_samples, key="amp_sample")
    amp_curve, amp_metrics = amplitude_metrics(amp[amp["Sample_Family"] == selected_amp_sample])
    amp_curve["tan_delta"] = amp_curve['G" (Pa)'] / amp_curve["G' (Pa)"].replace(0, np.nan)

    amp_kpi = st.columns(4)
    amp_kpi[0].metric(tr("Initial G′ reference", "Initialer G′-Referenzwert"), f"{amp_metrics['reference_gprime']:.3g} Pa", help=tr("Median G′ of the first up to three measured strain points.", "Medianes G′ der ersten bis zu drei gemessenen Dehnungspunkte."))
    amp_kpi[1].metric(tr("LVR limit (±5% G′)", "LVR-Grenze (±5% G′)"), f"{amp_metrics['lvr_limit']:.3g}%", help=tr("Highest measured strain whose G′ remains within ±5% of the initial reference.", "Höchste gemessene Dehnung, bei der G′ innerhalb von ±5% des initialen Referenzwertes bleibt."))
    amp_kpi[2].metric(tr("G′ retention at max strain", "G′-Retention bei maximaler Dehnung"), f"{amp_metrics['retention']:.1f}%", help=tr("G′ at the highest measured strain divided by the initial G′ reference.", "G′ bei der höchsten gemessenen Dehnung dividiert durch den initialen G′-Referenzwert."))
    amp_kpi[3].metric(tr("Median tanδ (G″/G′)", "Medianes tanδ (G″/G′)"), f"{amp_curve['tan_delta'].median():.3f}", help=tr("Calculated directly from measured G″ and G′ values.", "Direkt aus den gemessenen G″- und G′-Werten berechnet."))

    modulus_label = tr("Modulus", "Modul")
    amp_plot = amp_curve.melt(id_vars="γ* (%)", value_vars=["G' (Pa)", 'G" (Pa)'], var_name=modulus_label, value_name="Pa")
    fig_amp = px.line(
        amp_plot,
        x="γ* (%)",
        y="Pa",
        color=modulus_label,
        title=tr(f"Measured viscoelastic moduli vs. strain — {selected_amp_sample}", f"Gemessene viskoelastische Moduli in Abhängigkeit von der Dehnung – {selected_amp_sample}"),
        template=chart_theme,
        log_x=True,
        log_y=True,
    )
    fig_amp.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    st.plotly_chart(fig_amp, width="stretch")

    st.markdown(tr("### Industrial interpretation — selected sample", "### Industrielle Interpretation – ausgewählte Probe"))
    if pd.notna(amp_metrics["lvr_limit"]):
        st.write(tr(f"The measured linear-viscoelastic region extends to {amp_metrics['lvr_limit']:.3g}% strain using a ±5% G′ criterion. At the highest measured strain ({amp_metrics['max_strain']:.3g}%), G′ retains {amp_metrics['retention']:.1f}% of its initial reference.", f"Der gemessene linear-viskoelastische Bereich reicht bei Anwendung eines ±5%-G′-Kriteriums bis {amp_metrics['lvr_limit']:.3g}% Dehnung. Bei der höchsten gemessenen Dehnung ({amp_metrics['max_strain']:.3g}%) behält G′ {amp_metrics['retention']:.1f}% seines initialen Referenzwertes."))
    if amp_curve["tan_delta"].median() < 1:
        st.write(tr("Across the measured amplitude points, the median G″/G′ ratio is below 1, so the response is elastically dominated within this test range.", "Über die gemessenen Amplitudenpunkte liegt das mediane G″/G′-Verhältnis unter 1; die Antwort ist in diesem Prüfbereich daher elastisch dominiert."))
    else:
        st.write(tr("Across the measured amplitude points, the median G″/G′ ratio is at or above 1, so viscous dissipation is not secondary within this test range.", "Über die gemessenen Amplitudenpunkte liegt das mediane G″/G′-Verhältnis bei oder über 1; die viskose Dissipation ist in diesem Prüfbereich daher nicht nachrangig."))
    st.caption(tr("The LVR limit is a stated data-reduction criterion, not an unmeasured failure point. No amplitude values are interpolated.", "Die LVR-Grenze ist ein festgelegtes Auswertungskriterium und kein ungemessener Versagenspunkt. Amplitudenwerte werden nicht interpoliert."))

with rheology_tabs[3]:
    st.header(tr("Frequency sweep", "Frequenzsweep"))
    st.caption(tr("Measured time-scale dependence and elastic-versus-viscous balance.", "Gemessene Zeitskalenabhängigkeit und Verhältnis von elastischem zu viskosem Verhalten."))
    freq_samples = sorted(freq["Sample_Family"].dropna().unique())
    selected_freq_sample = st.selectbox(tr("Sample family", "Probenfamilie"), freq_samples, key="freq_sample")
    freq_curve, freq_metrics = frequency_metrics(freq[freq["Sample_Family"] == selected_freq_sample])

    freq_kpi = st.columns(4)
    freq_kpi[0].metric(tr("Median tanδ (G″/G′)", "Medianes tanδ (G″/G′)"), f"{freq_metrics['tan_delta']:.3f}", help=tr("Calculated from measured G″ and G′; it is distinct from the measured phase angle in degrees.", "Aus gemessenem G″ und G′ berechnet; dieser Wert ist vom gemessenen Phasenwinkel in Grad zu unterscheiden."))
    freq_kpi[1].metric(tr("Median G′/G″", "Medianes G′/G″"), f"{freq_metrics['elastic_ratio']:.2f}")
    freq_kpi[2].metric(tr("G′ frequency slope", "G′-Frequenzsteigung"), f"{freq_metrics['gprime_slope']:.3f}", help=tr("Log–log slope of measured G′ versus frequency.", "Log-Log-Steigung des gemessenen G′ gegenüber der Frequenz."))
    freq_kpi[3].metric(tr("G′ fit R²", "R² der G′-Anpassung"), f"{freq_metrics['gprime_r2']:.3f}")

    modulus_label = tr("Modulus", "Modul")
    freq_plot = freq_curve.melt(id_vars="f (Hz)", value_vars=["G' (Pa)", 'G" (Pa)'], var_name=modulus_label, value_name="Pa")
    fig_freq = px.line(
        freq_plot,
        x="f (Hz)",
        y="Pa",
        color=modulus_label,
        title=tr(f"Measured viscoelastic moduli across frequency — {selected_freq_sample}", f"Gemessene viskoelastische Moduli über die Frequenz – {selected_freq_sample}"),
        template=chart_theme,
        log_x=True,
        log_y=True,
    )
    fig_freq.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    st.plotly_chart(fig_freq, width="stretch")

    st.markdown(tr("### Industrial interpretation — selected sample", "### Industrielle Interpretation – ausgewählte Probe"))
    elastic_dominance = tr("elastic-dominant", "elastisch dominiert") if freq_metrics["tan_delta"] < 1 else tr("viscous-dominant", "viskos dominiert")
    st.write(tr(f"The median measured G″/G′ ratio is {freq_metrics['tan_delta']:.3f}; the response is therefore {elastic_dominance} over the measured frequency range.", f"Das gemessene mediane G″/G′-Verhältnis beträgt {freq_metrics['tan_delta']:.3f}; die Antwort ist über den gemessenen Frequenzbereich daher {elastic_dominance}."))
    st.write(tr(f"G′ changes from {freq_metrics['low_gprime']:.3g} Pa at the lowest measured frequency to {freq_metrics['high_gprime']:.3g} Pa at the highest. Its log–log frequency slope is {freq_metrics['gprime_slope']:.3f} (R² = {freq_metrics['gprime_r2']:.3f}).", f"G′ ändert sich von {freq_metrics['low_gprime']:.3g} Pa bei der niedrigsten gemessenen Frequenz auf {freq_metrics['high_gprime']:.3g} Pa bei der höchsten. Die Log-Log-Frequenzsteigung beträgt {freq_metrics['gprime_slope']:.3f} (R² = {freq_metrics['gprime_r2']:.3f})."))
    st.caption(tr("This describes the observed oscillatory response only; it does not assign a gel class or infer behavior outside the measured frequency range.", "Dies beschreibt ausschließlich die beobachtete oszillatorische Antwort; es wird weder eine Gelklasse zugeordnet noch Verhalten außerhalb des Messbereichs abgeleitet."))

with physicochemical_tabs[0]:
    st.header(T["physical"])
    st.caption(tr("Measured-data chapter on physical stability, sedimentation evidence, clarification, and re-dispersibility.", "Messdatenkapitel zu physikalischer Stabilität, Sedimentationsnachweisen, Klärung und Redispergierbarkeit."))

    st.markdown(tr("### 1. Introduction", "### 1. Einleitung"))
    st.markdown(
        tr("This module is limited to measured physicochemical observations and any sedimentation photographs that are actually present in the workspace. It does not infer sedimentation severity from an invented score or unsupported model output.", "Dieses Modul beschränkt sich auf gemessene physikochemische Beobachtungen und tatsächlich im Arbeitsbereich vorhandene Sedimentationsfotografien. Der Schweregrad der Sedimentation wird weder aus einem erfundenen Score noch aus nicht gestützten Modellergebnissen abgeleitet.")
    )

    st.markdown(tr("### 2. Experimental Design", "### 2. Versuchsdesign"))
    st.markdown(tr("#### Sample preparation and analytical instruments", "#### Probenvorbereitung und Analysegeräte"))
    st.image(
        "images/physicochemical_workflow.png",
        caption=tr(
            "Physicochemical workflow: filtration before analysis, followed by EasyDens and SmartRef measurement.",
            "Physikochemischer Ablauf: Filtration vor der Analyse, anschließend Messung mit EasyDens und SmartRef.",
        ),
        width="stretch",
    )
    physchem_workflow = st.columns(2)
    physchem_workflow[0].markdown(
        tr(
            "**01 · Filtration before analysis**  \nThe beverage samples were filtered individually before instrumental measurement to obtain the prepared analytical fractions shown. Samples remain identified separately throughout preparation.",
            "**01 · Filtration vor der Analyse**  \nDie Getränkeproben wurden vor der instrumentellen Messung einzeln filtriert, um die dargestellten vorbereiteten Analysefraktionen zu erhalten. Die Probenkennzeichnung bleibt während der Vorbereitung getrennt erhalten.",
        )
    )
    physchem_workflow[1].markdown(
        tr(
            "**02 · EasyDens and SmartRef**  \nThe Anton Paar EasyDens density meter and SmartRef refractometer form the documented instrument set for density-related measurements and soluble-solids determination in °Bx.",
            "**02 · EasyDens und SmartRef**  \nDas Anton Paar EasyDens Dichtemessgerät und das SmartRef Refraktometer bilden den dokumentierten Gerätesatz für dichtebezogene Messungen und die Bestimmung der löslichen Feststoffe in °Bx.",
        )
    )
    if physchem.empty:
        st.warning(tr("The measured physicochemical workbook was not found at data/physicochemical/physicochemical_results.ods.", "Die gemessene physikochemische Arbeitsmappe wurde unter data/physicochemical/physicochemical_results.ods nicht gefunden."))
    else:
        measured_columns = ["Sample_ID", "Storage_Date", "Storage_Duration", "Product_Type", "Brix_Avg", "Sugar_g_L", "Potential_Alcohol_vv", "Density_g_cm3", "Specific_Gravity", "pH"]
        display_df = physchem[measured_columns].copy()
        display_df = display_df.sort_values(["Storage_Date", "Sample_ID"]).reset_index(drop=True)
        st.dataframe(localized_table(display_df), width="stretch", hide_index=True)

        experimental_summary = st.columns(4)
        with experimental_summary[0]:
            st.metric(tr("Measured samples", "Gemessene Proben"), int(display_df["Sample_ID"].nunique()))
        with experimental_summary[1]:
            st.metric(tr("Storage ages represented", "Erfasste Lagerungsdauern"), display_df["Storage_Duration"].nunique())
        with experimental_summary[2]:
            st.metric(tr("Mean Brix", "Mittlerer Brix-Wert"), f"{safe_mean(display_df['Brix_Avg']):.2f} °Bx")
        with experimental_summary[3]:
            st.metric(tr("Mean pH", "Mittlerer pH-Wert"), f"{safe_mean(display_df['pH']):.2f}")

    # ==========================================================
# REAL SEDIMENTATION ANALYSIS
# ==========================================================

top_tabs[3].markdown(
    f'<div class="module-nav-label">{tr("Sedimentation workspace · select an evidence view", "Arbeitsbereich Sedimentation · Evidenzansicht auswählen")}</div>',
    unsafe_allow_html=True,
)
sed_tabs = top_tabs[3].tabs([
    "📊 " + T["overview"],
    T["sed_images"],
    T["sed_analysis"],
    T["sed_interpretation"],
    T["sed_references"],
])

sed_df = pd.DataFrame({
    "Sample": ["A","B","C","D","E","F","G"],
    "Manufacturing Date": [
        "04.12.2025",
        "04.12.2025",
        "04.12.2025",
        "04.12.2025",
        "24.07.2025",
        "14.03.2025",
        "01.11.2024"
    ],
    "Product Type": [
        "Standard Pasteurized",
        "Standard Pasteurized",
        "Standard Pasteurized",
        "Pasteurized with Spritz",
        "Standard Pasteurized",
        "Standard Pasteurized",
        "Standard Pasteurized"
    ],
    "Mid Sediment (mL)": [8,7,7.5,6,8,5,3.8],
    "Final Sediment (mL)": [5,5,4,5,8,5,3.5]
})
sed_df["Sediment-bed contraction (%)"] = (
    (sed_df["Mid Sediment (mL)"] -
     sed_df["Final Sediment (mL)"])
    / sed_df["Mid Sediment (mL)"] * 100
).round(1)

sed_df["Final-to-mid sediment-bed ratio"] = (
    sed_df["Final Sediment (mL)"]
    / sed_df["Mid Sediment (mL)"]
).round(2)

sed_df["Final-to-mid sediment-bed ratio (%)"] = (
    sed_df["Final-to-mid sediment-bed ratio"] * 100
).round(1)
sed_df["Total sample volume (mL)"] = np.where(sed_df["Sample"] == "G", 10.0, 50.0)
sed_df["Mid sediment-bed fraction (%)"] = (
    100 * sed_df["Mid Sediment (mL)"] / sed_df["Total sample volume (mL)"]
).round(1)
sed_df["Final sediment-bed fraction (%)"] = (
    100 * sed_df["Final Sediment (mL)"] / sed_df["Total sample volume (mL)"]
).round(1)

with sed_tabs[0]:
    st.header(T["sed_dataset"])
    st.dataframe(localized_table(sed_df), width="stretch", hide_index=True)

    col1,col2,col3,col4 = st.columns(4)
    col1.metric(tr("Samples evaluated", "Bewertete Proben"), len(sed_df))
    col2.metric(tr("Observation points", "Beobachtungszeitpunkte"), 2)
    col3.metric(tr("Largest measured sediment-bed contraction", "Größte gemessene Sedimentbettkontraktion"), f"{sed_df['Sediment-bed contraction (%)'].max():.1f}%")
    col4.metric(tr("Highest final sediment volume", "Höchstes finales Sedimentvolumen"), f"{sed_df['Final Sediment (mL)'].max():.1f} mL")
    st.caption(tr("Sediment-bed fractions are calculated using the recorded total sample volumes: 50 mL for Samples A–F and 10 mL for Sample G.", "Die Sedimentbettanteile werden anhand der dokumentierten Gesamtprobenvolumina berechnet: 50 mL für die Proben A–F und 10 mL für Probe G."))

sed_tabs[2].markdown(tr("### Sedimentation results plate", "### Übersicht der Sedimentationsergebnisse"))
sed_plot = sed_df.sort_values("Final sediment-bed fraction (%)").reset_index(drop=True)
sample_order = sed_plot["Sample"].tolist()
sample_y = {sample: index for index, sample in enumerate(sample_order)}
neutral, accent, pale = "#667785", "#173f5f", "#d8e1e8"

# Figure 1 — direct trajectory result.  The common neutral treatment avoids a categorical colour legend.
fig_trajectory = go.Figure()
for _, row in sed_plot.iterrows():
    y = sample_y[row["Sample"]]
    fig_trajectory.add_trace(go.Scatter(
        x=[0, 1], y=[row["Mid sediment-bed fraction (%)"], row["Final sediment-bed fraction (%)"]],
        mode="lines+markers", showlegend=False,
        line=dict(color=neutral, width=1.6), marker=dict(size=8, color=["white", accent], line=dict(color=neutral, width=1.5)),
        customdata=[[row["Sample"], tr("Intermediate", "Zwischenbeobachtung")], [row["Sample"], tr("Final", "Endbeobachtung")]],
        hovertemplate=tr("Sample %{customdata[0]}<br>%{customdata[1]} sediment-bed fraction: %{y:.1f}%<extra></extra>", "Probe %{customdata[0]}<br>%{customdata[1]} – Sedimentbettanteil: %{y:.1f}%<extra></extra>"),
    ))
    fig_trajectory.add_annotation(x=1.03, y=row["Final sediment-bed fraction (%)"], text=f"{row['Sample']}  {row['Final sediment-bed fraction (%)']:.1f}%", showarrow=False, xanchor="left", font=dict(size=11, color="#243447"))
fig_trajectory.update_layout(
    title=tr("A. Sedimentation trajectory map", "A. Verlaufskarte der Sedimentation"), template=chart_theme, height=360, showlegend=False,
    margin=dict(l=55, r=85, t=50, b=45), font=dict(family="Arial, sans-serif", size=13, color="#243447"),
    xaxis=dict(tickmode="array", tickvals=[0, 1], ticktext=[tr("Mid observation", "Zwischenbeobachtung"), tr("Final observation", "Endbeobachtung")], showgrid=False, zeroline=False),
    yaxis=dict(title=tr("Sediment-bed fraction (% of total sample volume)", "Sedimentbettanteil (% des Gesamtprobenvolumens)"), gridcolor="#edf0f2", zeroline=False),
)
fig_trajectory.add_annotation(x=0, y=1.08, xref="x", yref="paper", text=tr("○ Intermediate", "○ Zwischenbeobachtung"), showarrow=False, font=dict(color=neutral, size=11))
fig_trajectory.add_annotation(x=1, y=1.08, xref="x", yref="paper", text=tr("● Final", "● Endbeobachtung"), showarrow=False, font=dict(color=accent, size=11))
sed_tabs[2].plotly_chart(fig_trajectory, width="stretch", config={"displayModeBar": False})

# Figure 2 — numerical fingerprint uses direct values only and makes the result hierarchy immediately visible.
fingerprint_columns = ["Mid sediment-bed fraction (%)", "Final sediment-bed fraction (%)", "Sediment-bed contraction (%)", "Final-to-mid sediment-bed ratio (%)"]
fingerprint_labels = [tr("Mid fraction", "Zwischenanteil"), tr("Final fraction", "Finaler Anteil"), tr("Contraction", "Kontraktion"), tr("Final / mid ratio", "Final-/Zwischenverhältnis")]
fingerprint_values = sed_plot[fingerprint_columns].to_numpy()
fig_fingerprint = go.Figure(go.Heatmap(
    z=fingerprint_values, x=fingerprint_labels, y=[tr(f"Sample {sample}", f"Probe {sample}") for sample in sample_order],
    text=np.array([[f"{value:.1f}%" for value in row] for row in fingerprint_values]), texttemplate="%{text}", textfont=dict(size=12),
    colorscale=[[0, "#f3f6f8"], [0.5, "#aebfcd"], [1, accent]], showscale=False, xgap=2, ygap=2,
    hovertemplate="%{y}<br>%{x}: %{z:.1f}%<extra></extra>",
))
fig_fingerprint.update_layout(title=tr("B. Sedimentation fingerprint heatmap", "B. Heatmap des Sedimentationsprofils"), template=chart_theme, height=330, margin=dict(l=55, r=25, t=50, b=35), xaxis=dict(side="top", showgrid=False), yaxis=dict(showgrid=False, autorange="reversed"))
sed_tabs[2].plotly_chart(fig_fingerprint, width="stretch", config={"displayModeBar": False})

# Figure 3 — observation-state diagram, with the identity line as a physical reference rather than a stability class.
axis_limit = float(max(sed_plot["Mid sediment-bed fraction (%)"].max(), sed_plot["Final sediment-bed fraction (%)"].max()) * 1.12)
fig_state = go.Figure()
fig_state.add_trace(go.Scatter(x=[0, axis_limit], y=[0, axis_limit], mode="lines", line=dict(color="#9ba8b3", width=1, dash="dash"), hoverinfo="skip", showlegend=False))
fig_state.add_trace(go.Scatter(
    x=sed_plot["Mid sediment-bed fraction (%)"], y=sed_plot["Final sediment-bed fraction (%)"], mode="markers+text",
    marker=dict(size=11, color=accent, line=dict(color="white", width=1)), text=[f"{sample}" for sample in sample_order], textposition="top center", showlegend=False,
    hovertemplate=tr("Sample %{text}<br>Intermediate: %{x:.1f}%<br>Final: %{y:.1f}%<extra></extra>", "Probe %{text}<br>Zwischenbeobachtung: %{x:.1f}%<br>Endbeobachtung: %{y:.1f}%<extra></extra>"),
))
fig_state.add_annotation(x=axis_limit * 0.72, y=axis_limit * 0.84, text=tr("Identity line: no measured bed-volume change", "Identitätslinie: keine gemessene Änderung des Bettvolumens"), showarrow=False, font=dict(size=11, color="#52616d"))
fig_state.add_annotation(x=axis_limit * 0.70, y=axis_limit * 0.34, text=tr("Below line: reduced sediment-bed fraction", "Unterhalb der Linie: verringerter Sedimentbettanteil"), showarrow=False, font=dict(size=11, color="#52616d"))
fig_state.update_layout(title=tr("C. Sedimentation state diagram", "C. Zustandsdiagramm der Sedimentation"), template=chart_theme, height=360, margin=dict(l=60, r=25, t=50, b=50), xaxis=dict(title=tr("Mid sediment-bed fraction (%)", "Sedimentbettanteil Zwischenbeobachtung (%)"), range=[0, axis_limit], zeroline=False), yaxis=dict(title=tr("Final sediment-bed fraction (%)", "Finaler Sedimentbettanteil (%)"), range=[0, axis_limit], zeroline=False, scaleanchor="x", scaleratio=1))
sed_tabs[2].plotly_chart(fig_state, width="stretch", config={"displayModeBar": False})

sed_tabs[2].caption(tr("Samples A–F were evaluated at 50 mL total volume, whereas Sample G was evaluated at 10 mL. All marks are direct graduated-cylinder measurements; no interpolation, kinetic model, stability class, or cross-module comparison is applied.", "Die Proben A–F wurden bei einem Gesamtvolumen von 50 mL bewertet, Probe G bei 10 mL. Alle Markierungen beruhen auf direkten Messzylinderablesungen; es werden weder Interpolation noch kinetisches Modell, Stabilitätsklasse oder modulübergreifender Vergleich angewandt."))
sed_tabs[2].info(tr(
    "**Measured observation.** The trajectory map and state diagram show the direct change between the intermediate and final observations. Sample C has the largest measured sediment-bed contraction (46.7%), while Samples E and F show no measurable change.\n\n**Derived parameter.** The heatmap reports normalized sediment-bed fractions, contraction, and final-to-intermediate ratio for the independently evaluated A–G dataset.\n\n**Literature-supported interpretation.** A decrease in sediment-bed volume is consistent with bed consolidation or particle rearrangement; it does not independently establish redispersibility or suspension stability.\n\n**Limitation.** Only two observation times and no sedimentation replicates were available. Settling velocity, kinetic modelling, statistical significance, and long-term stability ranking are not supported.",
    "**Gemessene Beobachtung.** Verlaufskarte und Zustandsdiagramm zeigen die direkte Änderung zwischen Zwischen- und Endbeobachtung. Probe C weist die größte gemessene Sedimentbettkontraktion auf (46,7%), während bei den Proben E und F keine messbare Änderung vorliegt.\n\n**Abgeleiteter Parameter.** Die Heatmap zeigt normalisierte Sedimentbettanteile, Kontraktion und das Verhältnis von finalem zu zwischenzeitlichem Wert für den unabhängig bewerteten Datensatz A–G.\n\n**Literaturgestützte Interpretation.** Eine Abnahme des Sedimentbettvolumens ist mit Bettkonsolidierung oder Partikelumlagerung vereinbar; sie belegt für sich allein weder Redispergierbarkeit noch Suspensionsstabilität.\n\n**Limitation.** Es lagen nur zwei Beobachtungszeitpunkte und keine Sedimentationswiederholungen vor. Aussagen zu Sinkgeschwindigkeit, kinetischer Modellierung, statistischer Signifikanz und langfristiger Stabilitätsrangfolge sind nicht gestützt.",
))

sed_tabs[3].markdown(tr("### 6. Scientific interpretation", "### 6. Wissenschaftliche Interpretation"))

sed_tabs[3].markdown(tr(
    "**Measured observation.** Final sediment-layer heights range from 3.5 to 8.0 mL in the recorded dataset. The paired trajectories show the within-sample change between the two storage observations.\n\n**Derived calculation.** Sediment-bed contraction and final-to-intermediate sediment-bed ratio express the recorded geometric change between the two observations. They do not independently measure redispersibility.\n\n**Literature-supported interpretation.** Changes in sediment-bed geometry can be consistent with particle-network restructuring during storage; physical stability should also be evaluated with direct redispersion testing, particle-size data, density contrast, and continuous-phase rheology.\n\n**Hypothesis requiring validation.** Differences among formulations may reflect variation in aggregation or network structure, but the present sedimentation dataset alone does not identify the mechanism.",
    "**Gemessene Beobachtung.** Die finalen Sedimentschichthöhen liegen im dokumentierten Datensatz zwischen 3,5 und 8,0 mL. Die gepaarten Verläufe zeigen die Änderung innerhalb jeder Probe zwischen den beiden Lagerungsbeobachtungen.\n\n**Abgeleitete Berechnung.** Sedimentbettkontraktion und das Verhältnis von finalem zu zwischenzeitlichem Sedimentbett beschreiben die dokumentierte geometrische Änderung zwischen beiden Beobachtungen. Sie messen die Redispergierbarkeit nicht eigenständig.\n\n**Literaturgestützte Interpretation.** Änderungen der Sedimentbettgeometrie können mit einer Umstrukturierung des Partikelnetzwerks während der Lagerung vereinbar sein. Die physikalische Stabilität sollte zusätzlich durch direkte Redispergiertests, Partikelgrößendaten, Dichtekontrast und Rheologie der kontinuierlichen Phase bewertet werden.\n\n**Zu validierende Hypothese.** Unterschiede zwischen Formulierungen können Schwankungen der Aggregation oder Netzwerkstruktur widerspiegeln; der vorliegende Sedimentationsdatensatz allein identifiziert den Mechanismus nicht.",
))
sed_tabs[3].warning(tr("Only two observation times were available and sedimentation measurements were not replicated. Therefore, statistical hypothesis testing, settling-rate estimation, and kinetic modelling are not justified.", "Es lagen nur zwei Beobachtungszeitpunkte vor, und die Sedimentationsmessungen wurden nicht wiederholt. Daher sind statistische Hypothesentests, die Schätzung der Sinkgeschwindigkeit und eine kinetische Modellierung nicht gerechtfertigt."))

sed_tabs[1].markdown(tr("### 8. Visual evidence", "### 8. Visuelle Evidenz"))

with sed_tabs[1]:
  st.subheader(tr("Visual sedimentation evolution", "Visuelle Sedimentationsentwicklung"))

col1, col2, col3 = sed_tabs[1].columns(3)

with col1:
    st.image(
        "images/sediment_initial_labeled.png",
        caption=tr("Initial phase · Samples A–G", "Ausgangsphase · Proben A–G"),
        width="stretch"
    )

with col2:
    st.image(
        "images/sediment_mid_labeled.png",
        caption=tr("Intermediate observation (11 February) · Samples A–G", "Zwischenbeobachtung (11. Februar) · Proben A–G"),
        width="stretch"
    )

with col3:
    st.image(
        "images/sediment_final_labeled.png",
        caption=tr("Final sedimentation observation (11 March) · Samples A–G", "Finale Sedimentationsbeobachtung (11. März) · Proben A–G"),
        width="stretch"
    )

sed_tabs[4].markdown(tr("### 9. References", "### 9. Literatur"))
sed_tabs[4].markdown(tr(
        "- Stokes, G. G. (1851). On the effect of internal friction of fluids on the motion of pendulums.\n- Mewis, J. and Wagner, N. J. (2012). Colloidal Suspension Rheology.\n- Food Hydrocolloids — network formation, viscoelastic response, and suspension structure.\n- Steffe, J. F. (1996). Rheological Methods in Food Process Engineering.",
        "- Stokes, G. G. (1851). Über den Einfluss der inneren Reibung von Flüssigkeiten auf die Bewegung von Pendeln.\n- Mewis, J. und Wagner, N. J. (2012). Rheologie kolloidaler Suspensionen.\n- Food Hydrocolloids — Netzwerkbildung, viskoelastische Antwort und Suspensionsstruktur.\n- Steffe, J. F. (1996). Rheologische Methoden in der Lebensmittelverfahrenstechnik.",
    ))

with rheology_tabs[4]:
    st.header(T["summary_header"])
    st.info(
        tr("This section reports only measured observables from the three rheology workbooks and converts them into a research-style stability interpretation.", "Dieser Abschnitt berichtet ausschließlich gemessene Größen aus den drei Rheologie-Arbeitsmappen und überführt sie in eine wissenschaftliche Stabilitätsinterpretation.")
    )

    summary_metrics = pd.DataFrame(
        {
            "Dataset": ["Flow", "Amplitude sweep", "Frequency sweep"],
            "Mean viscosity η": [safe_mean(flow["η (Pa s)"]), np.nan, np.nan],
            "Mean G′": [np.nan, safe_mean(amp["G' (Pa)"]), safe_mean(freq["G' (Pa)"])],
            "Mean G″": [np.nan, safe_mean(amp['G" (Pa)']), safe_mean(freq['G" (Pa)'])],
            "Mean tanδ": [np.nan, np.nan, safe_mean(freq['δ (°)'])],
        }
    )
    st.dataframe(localized_table(summary_metrics), width="stretch", hide_index=True)

    sample_compare = st.multiselect(
        tr("Sample comparison mode", "Probenvergleich"),
        options=sample_profiles["Sample_ID"].tolist(),
        default=sample_profiles["Sample_ID"].tolist()[:3],
    )

    parameter_features = [
        "Mean_Viscosity",
        "Mean_Gprime",
        "Mean_Gdouble",
        "Mean_tan_delta",
        "Flow_behavior_index_n",
        "Consistency_coefficient_K",
    ]

    if sample_compare:
        parameter_df = sample_profiles[sample_profiles["Sample_ID"].isin(sample_compare)].copy()
        st.markdown(tr("### Sample-level derived rheology parameters", "### Abgeleitete rheologische Parameter auf Probenebene"))
        radar_features = [
            ("Mean_Viscosity", tr("Low-shear viscosity", "Viskosität bei niedriger Scherrate")),
            ("Flow_behavior_index_n", tr("Shear-thinning strength", "Stärke der Scherverdünnung")),
            ("Mean_Gprime", tr("Elastic modulus G′", "Elastischer Modul G′")),
            ("Mean_tan_delta", tr("Elastic dominance", "Elastische Dominanz")),
            ("Consistency_coefficient_K", tr("Frequency independence", "Frequenzunabhängigkeit")),
        ]
        radar_source = parameter_df[["Sample_ID", *[feature for feature, _ in radar_features]]].copy()
        usable_features = [feature for feature, _ in radar_features if radar_source[feature].notna().any()]
        radar_labels = [label for feature, label in radar_features if feature in usable_features]
        radar_normalized = radar_source[usable_features].copy()
        for feature in usable_features:
            values = radar_normalized[feature]
            span = values.max() - values.min()
            radar_normalized[feature] = (values - values.min()) / span if pd.notna(span) and span > 0 else np.nan
        if "Flow_behavior_index_n" in usable_features:
            radar_normalized["Flow_behavior_index_n"] = 1 - radar_normalized["Flow_behavior_index_n"]
        radar_fig = go.Figure()
        palette = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00"]
        for index, (_, row) in enumerate(radar_normalized.iterrows()):
            if row.notna().all():
                radar_fig.add_trace(go.Scatterpolar(
                    r=row.tolist() + [row.iloc[0]], theta=radar_labels + [radar_labels[0]],
                    fill="toself", opacity=0.18, line=dict(color=palette[index % len(palette)], width=2),
                    name=radar_source.iloc[index]["Sample_ID"],
                ))
        radar_fig.update_layout(template=chart_theme, title=tr("Relative rheological fingerprint", "Relatives rheologisches Profil"), height=600,
                                polar=dict(radialaxis=dict(visible=True, range=[0, 1], tickvals=[0, 0.5, 1])),
                                legend=dict(orientation="h", yanchor="bottom", y=1.08))
        st.plotly_chart(radar_fig, width="stretch")
        st.caption(tr("Radar dimensions are min–max normalized across the selected parent samples and therefore represent relative rheological fingerprints rather than values in physical units.", "Die Radardimensionen sind über die ausgewählten Ausgangsproben Min-Max-normalisiert und stellen daher relative rheologische Profile statt Werte in physikalischen Einheiten dar."))
        st.info(tr("The radar area is not a validated stability score. Each rheological dimension must be interpreted separately and together with replicate variability and model quality.", "Die Radarfläche ist kein validierter Stabilitätsscore. Jede rheologische Dimension muss einzeln sowie zusammen mit Replikatvariabilität und Modellqualität interpretiert werden."))
        st.dataframe(
            localized_table(parameter_df[["Sample_ID", "Product_Type", *parameter_features]]),
            width="stretch",
            hide_index=True,
        )
        st.caption(tr("Values are sample-level derived summaries. A parameter forest plot is not shown because replicate-level parameter confidence intervals have not yet been calculated independently.", "Die Werte sind abgeleitete Zusammenfassungen auf Probenebene. Ein Forest-Plot wird nicht gezeigt, da Konfidenzintervalle der Parameter auf Replikatebene noch nicht unabhängig berechnet wurden."))
    else:
        st.warning(tr("Select at least one sample to display the sample-level derived parameter table.", "Wählen Sie mindestens eine Probe aus, um die Tabelle der abgeleiteten Parameter anzuzeigen."))

    st.markdown(tr("### Thesis conclusion", "### Schlussfolgerung der Masterarbeit"))
    st.markdown(
        tr("The synthesis section summarizes the measured rheological evidence in a thesis-style context. The resulting interpretation is based on elastic dominance, structural retention, and suspension behaviour rather than on raw spreadsheet presentation alone.", "Der Syntheseabschnitt fasst die gemessenen rheologischen Erkenntnisse im Kontext der Masterarbeit zusammen. Die Interpretation basiert auf elastischer Dominanz, Strukturerhaltung und Suspensionsverhalten und nicht allein auf der Darstellung von Rohdaten.")
    )

with rheology_tabs[5]:
    st.header(tr("Rheology Metadata and Raw Data", "Rheologie-Metadaten und Rohdaten"))
    sample_overview_table = sample_overview[["Sample_ID", "Product_Type", "Manufacturing_Date", "Number_of_Replicates"]].copy()
    st.dataframe(localized_table(sample_overview_table), width="stretch", hide_index=True)
    st.subheader(tr("Replicate Details", "Details der Wiederholungen"))
    replicate_details = (
        meta[["Measurement_ID", "Parent_Sample", "Replicate_Number"]]
        .sort_values(["Parent_Sample", "Replicate_Number"])
        .reset_index(drop=True)
    )
    st.dataframe(localized_table(replicate_details), width="stretch", hide_index=True)
    st.subheader(tr("Raw Rheology Data", "Rheologische Rohdaten"))
    with st.expander(tr("Flow curve workbook data", "Arbeitsmappendaten der Fließkurve")):
        st.dataframe(localized_table(flow), width="stretch", hide_index=True)
    with st.expander(tr("Amplitude sweep workbook data", "Arbeitsmappendaten des Amplitudensweeps")):
        st.dataframe(localized_table(amp), width="stretch", hide_index=True)
    with st.expander(tr("Frequency sweep workbook data", "Arbeitsmappendaten des Frequenzsweeps")):
        st.dataframe(localized_table(freq), width="stretch", hide_index=True)

with rheology_tabs[6]:
    st.header(tr("Rheology References", "Rheologische Literatur"))
    st.caption(tr("Rheology-specific scientific sources supporting interpretation of the measured response.", "Rheologiespezifische wissenschaftliche Quellen zur Unterstützung der Interpretation der gemessenen Antwort."))
    for ref in REFERENCE_LIBRARY:
        with st.expander(ref["title"]):
            st.write(tr("Link to publication:", "Link zur Publikation:"), ref["publication_link"])
            st.write(tr("DOI / journal reference:", "DOI / Zeitschriftenreferenz:"), ref["doi"])
            st.write(tr("Relevance:", "Relevanz:"), ref["relevance_de"] if LANG == "DE" else ref["relevance"])

with top_tabs[6]:
    st.header(tr("From formulation to stability decision", "Von der Rezeptur zur Stabilitätsentscheidung"))
    st.caption(tr(
        "A structured evidence story connecting product composition, manufacturing conditions, confirmed batches, experiments and the resulting stability assessment.",
        "Eine strukturierte Evidenzgeschichte, die Produktzusammensetzung, Herstellungsbedingungen, bestätigte Lose, Experimente und die daraus resultierende Stabilitätsbewertung verbindet.",
    ))
    st.markdown(
        f"""
        <section class="bottle-story">
            <div class="bottle-frame closed" style="background-image:url('{hero_image_uri}')"></div>
            <div class="bottle-frame open" style="background-image:url('{open_bottle_uri}')"></div>
            <div class="bottle-story-copy">
                <div class="bottle-story-kicker">{tr('Integrated product assessment', 'Integrierte Produktbewertung')}</div>
                <h2>{tr('Evidence across manufacturing, composition, structure and microbiological quality.', 'Evidenz zu Herstellung, Zusammensetzung, Struktur und mikrobiologischer Qualität.')}</h2>
                <p>{tr('Follow the evidence chain from formulation and processing to the documented analytical outcome.', 'Folgen Sie der Evidenzkette von Rezeptur und Verarbeitung bis zum dokumentierten analytischen Ergebnis.')}</p>
            </div>
        </section>
        <div class="story-rail">
            <div class="story-stage"><span>01</span><strong>{tr('Product & process', 'Produkt & Prozess')}</strong></div>
            <div class="story-stage"><span>02</span><strong>{tr('Confirmed batches', 'Bestätigte Lose')}</strong></div>
            <div class="story-stage"><span>03</span><strong>{tr('Experimental evidence', 'Experimentelle Evidenz')}</strong></div>
            <div class="story-stage"><span>04</span><strong>{tr('Integrated outcome', 'Integriertes Ergebnis')}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(tr("### 01 · Product composition and process conditions", "### 01 · Produktzusammensetzung und Prozessbedingungen"))
    st.markdown(
        f"""
        <div class="study-grid">
            <div class="study-card"><div class="study-label">{tr('Composition', 'Zusammensetzung')}</div><div class="study-value">{tr('Ginger · lime · Cachaça', 'Ingwer · Limette · Cachaça')}</div><div class="study-detail">{tr('Water and sugar form the beverage base; ginger and lime define the dispersed acidic system.', 'Wasser und Zucker bilden die Getränkebasis; Ingwer und Limette definieren das disperse saure System.')}</div></div>
            <div class="study-card"><div class="study-label">{tr('Primary heating', 'Primärerhitzung')}</div><div class="study-value">90–100 °C · 4 min</div><div class="study-detail">{tr('Controlled heating of the lime-containing mixture before Cachaça addition.', 'Kontrollierte Erhitzung der limettenhaltigen Mischung vor der Cachaça-Zugabe.')}</div></div>
            <div class="study-card"><div class="study-label">{tr('Final treatment', 'Abschließende Behandlung')}</div><div class="study-value">85 °C × 15 min</div><div class="study-detail">{tr('Treatment in the RATIONAL ClimaPlus Combi® CPC after filling.', 'Behandlung im RATIONAL ClimaPlus Combi® CPC nach der Abfüllung.')}</div></div>
            <div class="study-card"><div class="study-label">{tr('Study conditions', 'Untersuchungsbedingungen')}</div><div class="study-value">{tr('Ambient · Feb–Mar 2026', 'Raumtemperatur · Feb–Mär 2026')}</div><div class="study-detail">{tr('Homogenised filling and repeated mixing applied to both confirmed batches.', 'Homogenisierte Abfüllung und wiederholtes Durchmischen bei beiden bestätigten Losen.')}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="process-strip">
            <div class="process-stage"><strong>01 · {tr('Thermal extraction', 'Thermische Extraktion')}</strong><span>{tr('Lime-containing mixture at 90–100 °C for four minutes.', 'Limettenhaltige Mischung vier Minuten bei 90–100 °C.')}</span></div>
            <div class="process-stage"><strong>02 · {tr('Homogenisation', 'Homogenisierung')}</strong><span>{tr('Stick-blender treatment after ginger addition.', 'Stabmixerbehandlung nach der Ingwerzugabe.')}</span></div>
            <div class="process-stage"><strong>03 · {tr('Controlled filling', 'Kontrollierte Abfüllung')}</strong><span>{tr('Cachaça addition followed by repeated mixing during 200 mL filling.', 'Cachaça-Zugabe mit wiederholtem Durchmischen bei der 200-ml-Abfüllung.')}</span></div>
            <div class="process-stage"><strong>04 · {tr('Final treatment', 'Abschließende Behandlung')}</strong><span>85 °C × 15 min · RATIONAL ClimaPlus Combi® CPC</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(tr(
        "Bennani (2025) reported uniform visual appearance in the 200 mL bottles after two weeks. The optimized process was confirmed for both manufacturing batches displayed below.",
        "Bennani (2025) dokumentierte nach zwei Wochen ein einheitliches visuelles Erscheinungsbild der 200-ml-Flaschen. Der optimierte Prozess wurde für beide unten dargestellten Herstellungslose bestätigt.",
    ))

    st.markdown(tr("### 02 · Confirmed batch traceability", "### 02 · Bestätigte Los-Rückverfolgbarkeit"))
    st.markdown(
        f"""
        <div class="batch-map">
            <div class="batch-card">
                <div class="batch-date">01.11.2024 · {tr('Standard pasteurized', 'Standard pasteurisiert')}</div>
                <div class="batch-labels"><strong>{T['rheology']}:</strong> S1 / {tr('Sample 4', 'Probe 4')}<br><strong>{T['physicochemical']}:</strong> {tr('Sample 7', 'Probe 7')}<br><strong>{T['sedimentation']}:</strong> {tr('Sample G', 'Probe G')}<br><strong>{T['microbiology']}:</strong> S6</div>
            </div>
            <div class="batch-card">
                <div class="batch-date">04.12.2025 · {tr('Standard pasteurized', 'Standard pasteurisiert')}</div>
                <div class="batch-labels"><strong>{T['rheology']}:</strong> S4 / {tr('Sample 16', 'Probe 16')}<br><strong>{T['physicochemical']}:</strong> {tr('Samples 1–3', 'Proben 1–3')}<br><strong>{T['sedimentation']}:</strong> {tr('Samples A–C', 'Proben A–C')}<br><strong>{T['microbiology']}:</strong> S5</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_common_batch = st.selectbox(
        tr("Inspect confirmed manufacturing batch", "Bestätigtes Herstellungslos untersuchen"),
        ["01.11.2024 · Standard Pasteurized", "04.12.2025 · Standard Pasteurized"],
        format_func=lambda value, language=LANG: value if language == "EN" else value.replace("Standard Pasteurized", "Standard pasteurisiert"),
        key=f"confirmed_batch_shelf_life_{LANG}",
    )
    batch_date_text = selected_common_batch.split(" · ")[0]
    batch_date = pd.to_datetime(batch_date_text, dayfirst=True)
    batch_iso_date = batch_date.strftime("%Y-%m-%d")
    batch_rheo_sample = "S1" if batch_date_text == "01.11.2024" else "S4"
    batch_physchem = physchem[
        (physchem["Storage_Date"] == batch_date)
        & physchem["Product_Type"].astype(str).str.contains("Standard", case=False, na=False)
    ].copy()
    batch_sedimentation = sed_df[
        (sed_df["Manufacturing Date"] == batch_date_text)
        & sed_df["Product Type"].astype(str).str.contains("Standard", case=False, na=False)
    ].copy()
    batch_microbiology = lims_microbiology[
        lims_microbiology["Date_Parsed"].astype(str).eq(batch_iso_date)
    ].copy()
    batch_flow = flow[flow["Sample_Family"] == batch_rheo_sample]
    flow_details, _ = power_law_model_details(batch_flow)
    physicochemical_test_date = pd.Timestamp("2026-02-11")
    documented_checkpoint_days = int((physicochemical_test_date - batch_date).days)
    ph_min = pd.to_numeric(batch_physchem["pH"], errors="coerce").min()
    ph_max = pd.to_numeric(batch_physchem["pH"], errors="coerce").max()
    brix_mean = pd.to_numeric(batch_physchem["Brix_Avg"], errors="coerce").mean()
    final_sed_min = pd.to_numeric(batch_sedimentation["Final sediment-bed fraction (%)"], errors="coerce").min()
    final_sed_max = pd.to_numeric(batch_sedimentation["Final sediment-bed fraction (%)"], errors="coerce").max()
    microbial_status = "; ".join(
        f"{row['Medium']}: {GERMAN_TABLE_VALUES.get(row['Microbial_status'], row['Microbial_status']) if LANG == 'DE' else row['Microbial_status']}"
        for _, row in batch_microbiology.iterrows()
    ) or tr("Not recorded", "Nicht dokumentiert")
    approximate_age_months = max(1, int(round(documented_checkpoint_days / 30.4375)))
    approximate_age = tr(f"~{approximate_age_months} months", f"ca. {approximate_age_months} Monate")
    sediment_result = f"{final_sed_min:.1f}%" if final_sed_min == final_sed_max else f"{final_sed_min:.1f}–{final_sed_max:.1f}%"

    rheology_sample = tr("S1 / Sample 4", "S1 / Probe 4") if batch_date_text == "01.11.2024" else tr("S4 / Sample 16", "S4 / Probe 16")
    physicochemical_sample = tr("Sample 7", "Probe 7") if batch_date_text == "01.11.2024" else tr("Samples 1–3", "Proben 1–3")
    sedimentation_sample = tr("Sample G", "Probe G") if batch_date_text == "01.11.2024" else tr("Samples A–C", "Proben A–C")
    microbiology_sample = "S6" if batch_date_text == "01.11.2024" else "S5"

    st.markdown(tr("### 03 · Experimental evidence", "### 03 · Experimentelle Evidenz"))
    st.caption(tr(
        "All analytical periods are presented at the same study-level precision for a coherent comparison.",
        "Alle Analysezeiträume werden für einen konsistenten Vergleich mit derselben studienbezogenen Genauigkeit dargestellt.",
    ))
    st.markdown(
        f"""
        <div class="experiment-grid">
            <div class="experiment-card" style="--accent:#146c94"><div class="experiment-period">{tr('February 2026', 'Februar 2026')}</div><div class="experiment-title">{T['rheology']}</div><div class="experiment-sample">{rheology_sample}</div><div class="experiment-result">n = {flow_details['n']:.3f}<br>R² = {flow_details['r2']:.3f}</div><div class="experiment-method">{tr('Descriptive power-law flow profile.', 'Deskriptives Potenzgesetz-Fließprofil.')}</div></div>
            <div class="experiment-card" style="--accent:#1c8ea1"><div class="experiment-period">{tr('February 2026', 'Februar 2026')}</div><div class="experiment-title">{T['physicochemical']}</div><div class="experiment-sample">{physicochemical_sample}</div><div class="experiment-result">pH {ph_min:.2f}{'' if ph_min == ph_max else f'–{ph_max:.2f}'}<br>{brix_mean:.2f} °Bx</div><div class="experiment-method">{tr('Acidity and soluble-solids profile.', 'Säure- und lösliches-Feststoff-Profil.')}</div></div>
            <div class="experiment-card" style="--accent:#68b7a7"><div class="experiment-period">{tr('February–March 2026', 'Februar–März 2026')}</div><div class="experiment-title">{T['sedimentation']}</div><div class="experiment-sample">{sedimentation_sample}</div><div class="experiment-result">{sediment_result}</div><div class="experiment-method">{tr('Final measured sediment fraction.', 'Final gemessener Sedimentanteil.')}</div></div>
            <div class="experiment-card" style="--accent:#d0a34a"><div class="experiment-period">{tr('Early March 2026', 'Anfang März 2026')}</div><div class="experiment-title">{T['microbiology']}</div><div class="experiment-sample">{microbiology_sample}</div><div class="experiment-result">{microbial_status}</div><div class="experiment-method">{tr('Qualitative plate assessment.', 'Qualitative Plattenbewertung.')}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(tr("### 04 · Integrated outcome", "### 04 · Integriertes Ergebnis"))
    shelf_kpis = st.columns(4)
    shelf_kpis[0].metric(tr("Approx. assessment age", "Ungefähres Bewertungsalter"), approximate_age)
    shelf_kpis[1].metric("pH", f"{ph_min:.2f}" if ph_min == ph_max else f"{ph_min:.2f}–{ph_max:.2f}")
    shelf_kpis[2].metric(tr("Soluble solids", "Lösliche Feststoffe"), f"{brix_mean:.2f} °Bx")
    shelf_kpis[3].metric(tr("Final sediment fraction", "Finaler Sedimentanteil"), sediment_result)
    st.markdown(
        f"""
        <div class="outcome-grid">
            <div class="outcome-main"><div class="outcome-label">{tr('Evidence-supported result', 'Evidenzgestütztes Ergebnis')}</div><div class="outcome-title">{tr('Batch characterisation consolidated across four analytical domains', 'Loscharakterisierung über vier analytische Bereiche konsolidiert')}</div><div class="outcome-copy">{tr('The selected manufacturing batch is traceably connected to rheological, physicochemical, sedimentation and qualitative microbiological observations from the February–March 2026 study. The result is a consolidated stability profile, not an inferred expiry date.', 'Das ausgewählte Herstellungslose ist rückverfolgbar mit rheologischen, physikochemischen, sedimentationsbezogenen und qualitativen mikrobiologischen Beobachtungen der Studie Februar–März 2026 verknüpft. Das Ergebnis ist ein konsolidiertes Stabilitätsprofil, kein abgeleitetes Verfallsdatum.')}</div></div>
            <div class="outcome-side"><div class="outcome-label">{tr('Current evidence output', 'Aktuelles Evidenzergebnis')}</div><div class="outcome-value">{tr('Stability profile', 'Stabilitätsprofil')}</div><div class="outcome-copy">{tr('A numerical market shelf life is the next validation phase and requires repeated quantitative microbial and sensory measurements.', 'Eine numerische Markt-Haltbarkeit ist die nächste Validierungsphase und erfordert wiederholte quantitative mikrobiologische und sensorische Messungen.')}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander(tr("Recommended shelf-life validation plan", "Empfohlener Validierungsplan zur Haltbarkeit")):
        validation_requirements = pd.DataFrame([
            [tr("Measurement schedule", "Messplan"), tr("Use standardised storage intervals from production through the intended market-life endpoint.", "Standardisierte Lagerintervalle von der Produktion bis zum vorgesehenen Marktlebensdauer-Endpunkt verwenden.")],
            [tr("Quantitative microbiology", "Quantitative Mikrobiologie"), tr("Track total viable count and yeast/mould populations using validated enumeration methods.", "Gesamtkeimzahl sowie Hefe-/Schimmelpopulationen mit validierten Zählmethoden verfolgen.")],
            [tr("Thermal validation", "Thermische Validierung"), tr("Confirm the product core temperature–time profile for the 85 °C/15 min treatment.", "Kerntemperatur-Zeit-Profil des Produkts für die Behandlung bei 85 °C/15 min bestätigen.")],
            [tr("Storage profile", "Lagerungsprofil"), tr("Log ambient temperature, light exposure and package orientation throughout the study.", "Raumtemperatur, Lichtexposition und Verpackungsorientierung während der Studie protokollieren.")],
            [tr("Quality endpoint", "Qualitätsendpunkt"), tr("Apply predefined sensory, colour, carbonation and physical-stability specifications.", "Vordefinierte Spezifikationen für Sensorik, Farbe, Karbonisierung und physikalische Stabilität anwenden.")],
            [tr("Statistical design", "Statistisches Design"), tr("Assess unopened replicate packages from independent production batches at each interval.", "Ungeöffnete Replikatverpackungen unabhängiger Produktionslose bei jedem Intervall untersuchen.")],
        ], columns=[tr("Work package", "Arbeitspaket"), tr("Proposed design", "Vorgeschlagenes Design")])
        st.dataframe(localized_table(validation_requirements), width="stretch", hide_index=True)

    with st.expander(tr("Scientific basis and source traceability", "Wissenschaftliche Grundlage und Quellenrückverfolgung")):
        st.markdown(tr(
            "**Internal process source:** Bennani, I. (2025). _Herstellung eines alkoholischen Mischgetränks_. FH JOANNEUM project report, prepared at Mandi-o Qualität Lebensmittel GbR. Methods pp. 7–13; results pp. 14–17; Appendix A pp. 25–28.",
            "**Interne Prozessquelle:** Bennani, I. (2025). _Herstellung eines alkoholischen Mischgetränks_. Projektarbeit, FH JOANNEUM, bearbeitet bei Mandi-o Qualität Lebensmittel GbR. Methodik S. 7–13; Ergebnisse S. 14–17; Anhang A S. 25–28.",
        ))
        st.markdown(tr(
            "- **EFSA BIOHAZ Panel (2021).** Risk-based shelf-life decisions must consider intrinsic factors, processing, packaging and storage within the food-safety management system. [EFSA Journal 19(4):6510](https://doi.org/10.2903/j.efsa.2021.6510)\n"
            "- **Tiencheu et al. (2021).** Lemon–ginger beverage work combined physicochemical, microbiological and sensory measurements; its formulation-specific results cannot be transferred as a Caipiringwer expiry date. [Heliyon 7:e07177](https://doi.org/10.1016/j.heliyon.2021.e07177)\n"
            "- **Szczepańska et al. (2021).** A controlled apple-juice storage study measured microbial, rheological and physicochemical change repeatedly for up to 12 weeks, illustrating the longitudinal design needed for a shelf-life claim. [LWT 150:112038](https://doi.org/10.1016/j.lwt.2021.112038)\n"
            "- **Li et al. (2021).** Cloudy mixed-juice quality research evaluated sedimentation and other quality changes during refrigerated storage, supporting physical stability as one endpoint rather than a proxy for microbial shelf life. [Current Research in Food Science](https://doi.org/10.1016/j.crfs.2021.09.002)\n"
            "- **Prisacaru et al. (2023).** Ginger-containing juice research monitored physicochemical and microbiological characteristics during storage; differences in recipe, processing and storage prevent direct duration transfer. [Foods 12:1311](https://doi.org/10.3390/foods12061311)\n"
            "- **Shiekh et al. (2024).** Pasteurized passion-fruit juice shelf life was determined from repeated yeast/mould measurements under defined refrigeration, not pH alone. [Foods 13:719](https://doi.org/10.3390/foods13050719)\n"
            "- **ISO 4833-1:2013/Amd 1:2022.** Current amendment for aerobic colony enumeration at 30 °C. [ISO record](https://www.iso.org/standard/73329.html)",
            "- **EFSA-BIOHAZ-Gremium (2021).** Risikobasierte Haltbarkeitsentscheidungen müssen intrinsische Faktoren, Verarbeitung, Verpackung und Lagerung im Lebensmittelsicherheitsmanagement berücksichtigen. [EFSA Journal 19(4):6510](https://doi.org/10.2903/j.efsa.2021.6510)\n"
            "- **Tiencheu et al. (2021).** Die Arbeit zu einem Zitronen-Ingwer-Getränk kombinierte physikochemische, mikrobiologische und sensorische Messungen; die rezepturspezifischen Ergebnisse sind nicht als Caipiringwer-Verfallsdatum übertragbar. [Heliyon 7:e07177](https://doi.org/10.1016/j.heliyon.2021.e07177)\n"
            "- **Szczepańska et al. (2021).** Eine kontrollierte Apfelsaftstudie erfasste mikrobiologische, rheologische und physikochemische Veränderungen wiederholt über bis zu zwölf Wochen und zeigt das für eine Haltbarkeitsaussage erforderliche Längsschnittdesign. [LWT 150:112038](https://doi.org/10.1016/j.lwt.2021.112038)\n"
            "- **Li et al. (2021).** Die Qualitätsstudie zu trüben Mischsäften untersuchte Sedimentation und weitere Qualitätsänderungen während Kühllagerung und stützt physikalische Stabilität als einzelnen Endpunkt, nicht als Ersatz für mikrobiologische Haltbarkeit. [Current Research in Food Science](https://doi.org/10.1016/j.crfs.2021.09.002)\n"
            "- **Prisacaru et al. (2023).** Forschung zu ingwerhaltigen Säften überwachte physikochemische und mikrobiologische Merkmale während der Lagerung; Unterschiede in Rezeptur, Verarbeitung und Lagerung verhindern eine direkte Übertragung der Dauer. [Foods 12:1311](https://doi.org/10.3390/foods12061311)\n"
            "- **Shiekh et al. (2024).** Die Haltbarkeit pasteurisierten Passionsfruchtsafts wurde anhand wiederholter Hefe-/Schimmelmessungen unter definierter Kühllagerung bestimmt, nicht allein anhand des pH-Werts. [Foods 13:719](https://doi.org/10.3390/foods13050719)\n"
            "- **ISO 4833-1:2013/Amd 1:2022.** Aktuelle Änderung zur aeroben Koloniezählung bei 30 °C. [ISO-Eintrag](https://www.iso.org/standard/73329.html)",
        ))

with top_tabs[5]:
    st.header(T["literature_header"])
    st.markdown(T["lit_text"])
    st.markdown(tr("### Internal project source", "### Interne Projektquelle"))
    st.markdown(tr(
        "**Bennani, I. (2025). _Herstellung eines alkoholischen Mischgetränks_.** Project report in Product Development, Food: Product and Process Development, FH JOANNEUM, prepared at Mandi-o Qualität Lebensmittel GbR, submitted 30 June 2025.",
        "**Bennani, I. (2025). _Herstellung eines alkoholischen Mischgetränks_.** Projektarbeit im Themenschwerpunkt Produktentwicklung, Studiengang Lebensmittel: Produkt- und Prozessentwicklung, FH JOANNEUM, bearbeitet bei Mandi-o Qualität Lebensmittel GbR, eingereicht am 30. Juni 2025.",
    ))
    st.caption(tr(
        "Evidence used in this dashboard: manufacturing method (pp. 7–13), visual process-comparison results (pp. 14–17), and experimental protocols (Appendix A, pp. 25–28). The researcher confirmed that the optimized procedure was applied to both displayed manufacturing batches. Source type: internal project report supplied by the research collaborator; no DOI or public URL was provided.",
        "Im Dashboard verwendete Evidenz: Herstellungsmethode (S. 7–13), visuelle Ergebnisse des Prozessvergleichs (S. 14–17) und Versuchsprotokolle (Anhang A, S. 25–28). Die Forscherin bestätigte die Anwendung des optimierten Verfahrens auf beide dargestellten Herstellungslose. Quellentyp: vom Forschungspartner bereitgestellter interner Projektbericht; DOI oder öffentliche URL wurden nicht angegeben.",
    ))
    st.markdown(tr(
        "- Food Hydrocolloids — network formation, viscoelastic response, and suspension structure.\n- Journal of Food Engineering — flow behaviour, rheological characterization, and industrial process interpretation.\n- Journal of Rheology — oscillatory and linear viscoelastic methodology constraints.\n- Journal of Texture Studies — particulate stability and textural implications.",
        "- Food Hydrocolloids — Netzwerkbildung, viskoelastische Antwort und Suspensionsstruktur.\n- Journal of Food Engineering — Fließverhalten, rheologische Charakterisierung und industrielle Prozessinterpretation.\n- Journal of Rheology — methodische Grenzen oszillatorischer und linear-viskoelastischer Messungen.\n- Journal of Texture Studies — Partikelstabilität und texturelle Auswirkungen.",
    ))
    st.markdown(tr("### Scientific support principle", "### Prinzip der wissenschaftlichen Einordnung"))
    st.markdown(tr(
        "The measured values from the workbooks remain the analytical foundation of the chapter. The literature is used to support interpretation, strengthen scientific context, and help place the observed response within established rheological theory.",
        "Die Messwerte aus den Arbeitsmappen bleiben die analytische Grundlage des Kapitels. Die Literatur unterstützt die Interpretation, stärkt den wissenschaftlichen Kontext und ordnet die beobachtete Antwort in die etablierte rheologische Theorie ein.",
    ))
