"""
╔══════════════════════════════════════════════════════════════════╗
║   EQUILYTICS — QUANTUM RACE PREDICTION ENGINE v4.0              ║
║   Streamlit Cloud | quantumraceprediction/quantum_racing_predictor║
║   Password: EQUI2024                                             ║
║   Two Modes: MY STABLE (CSV) + PUBLIC RACES (No Training Data)   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import json
from datetime import datetime, date
import requests
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Equilytics — Quantum Race Predictor",
    page_icon="🏇",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
.stApp { background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2e 50%, #0a1a2e 100%); }
.eq-header { background: linear-gradient(90deg, #6B21A8, #9333EA, #EC4899); padding: 20px 30px; border-radius: 12px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; }
.eq-logo { font-size: 2.2em; font-weight: 900; color: white; letter-spacing: 3px; }
.eq-tagline { font-size: 0.75em; color: rgba(255,255,255,0.8); letter-spacing: 4px; margin-top: 2px; }
.eq-badges span { background: rgba(255,255,255,0.2); color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.7em; margin-left: 6px; font-weight: 600; }
.metric-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(147,51,234,0.3); border-radius: 10px; padding: 16px; text-align: center; margin: 5px 0; }
.metric-card .val { font-size: 1.8em; font-weight: 700; color: #A78BFA; }
.metric-card .lab { font-size: 0.7em; color: rgba(255,255,255,0.6); letter-spacing: 2px; margin-top: 4px; }
.winner-card { background: linear-gradient(135deg, rgba(107,33,168,0.4), rgba(236,72,153,0.3)); border: 2px solid #9333EA; border-radius: 14px; padding: 20px; margin: 10px 0; }
.winner-card .wname { font-size: 1.6em; font-weight: 900; color: #F0ABFC; }
.winner-card .wprob { font-size: 1.1em; color: #A78BFA; }
.pred-table { width: 100%; border-collapse: collapse; margin: 10px 0; }
.pred-table th { background: rgba(147,51,234,0.4); color: white; padding: 10px 14px; text-align: left; font-size: 0.75em; letter-spacing: 1px; font-weight: 700; }
.pred-table td { padding: 9px 14px; font-size: 0.82em; color: rgba(255,255,255,0.88); border-bottom: 1px solid rgba(255,255,255,0.07); }
.pred-table tr:hover td { background: rgba(147,51,234,0.15); }
.rank1 { color: #F0ABFC; font-weight: 700; }
.rank2 { color: #93C5FD; }
.rank3 { color: #86EFAC; }
.bet-yes { color: #4ADE80; font-weight: 700; }
.bet-no { color: rgba(255,255,255,0.4); }
.value-bet { background: rgba(74,222,128,0.15); border-left: 3px solid #4ADE80; }
.info-box { background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.4); border-radius: 8px; padding: 12px 16px; margin: 8px 0; font-size: 0.82em; color: #93C5FD; }
.warn-box { background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.4); border-radius: 8px; padding: 12px 16px; margin: 8px 0; font-size: 0.82em; color: #FCD34D; }
.success-box { background: rgba(74,222,128,0.15); border: 1px solid rgba(74,222,128,0.4); border-radius: 8px; padding: 12px 16px; margin: 8px 0; font-size: 0.82em; color: #4ADE80; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #1a0a2e 0%, #0a0a1a 100%); border-right: 1px solid rgba(147,51,234,0.3); }
</style>
""", unsafe_allow_html=True)

CORRECT_PASSWORD = "EQUI2024"

def show_login():
    st.markdown("""
    <div style='display:flex;justify-content:center;align-items:center;min-height:60vh;'>
    <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(147,51,234,0.4);border-radius:20px;padding:48px 40px;max-width:400px;width:100%;text-align:center;'>
        <div style='font-size:3em;margin-bottom:12px;'>🏇</div>
        <div style='font-size:1.8em;font-weight:900;color:white;letter-spacing:4px;margin-bottom:6px;'>EQUILYTICS</div>
        <div style='font-size:0.7em;color:rgba(255,255,255,0.5);letter-spacing:5px;margin-bottom:32px;'>ART & SCIENCE OF TRAINING</div>
        <div style='display:flex;justify-content:center;gap:8px;margin-bottom:32px;flex-wrap:wrap;'>
            <span style='background:rgba(147,51,234,0.3);color:#C4B5FD;padding:4px 10px;border-radius:20px;font-size:0.65em;font-weight:700;'>ML PREDICTION</span>
            <span style='background:rgba(236,72,153,0.3);color:#F9A8D4;padding:4px 10px;border-radius:20px;font-size:0.65em;font-weight:700;'>BENTER MODEL</span>
            <span style='background:rgba(59,130,246,0.3);color:#93C5FD;padding:4px 10px;border-radius:20px;font-size:0.65em;font-weight:700;'>KELLY CRITERION</span>
        </div>
    </div></div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd = st.text_input("Access Code", type="password", placeholder="Enter access code", label_visibility="collapsed")
        if st.button("🔓 ENTER", use_container_width=True, type="primary"):
            if pwd == CORRECT_PASSWORD or pwd == CORRECT_PASSWORD.lower():
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect access code. Try EQUI2024")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if not st.session_state["authenticated"]:
    show_login()
    st.stop()

st.markdown("""
<div class='eq-header'>
  <div>
    <div class='eq-logo'>🏇 EQUILYTICS</div>
    <div class='eq-tagline'>ART & SCIENCE OF TRAINING</div>
  </div>
  <div class='eq-badges'>
    <span>ML PREDICTION</span><span>BENTER MODEL</span>
    <span>KELLY CRITERION</span><span>PUBLIC RACES</span>
  </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div style='color:#A78BFA;font-weight:700;font-size:0.8em;letter-spacing:2px;margin-bottom:10px;'>NAVIGATION</div>", unsafe_allow_html=True)
    page = st.radio("", ["🏠 Home","📁 My Stable Races","🌏 Public Races (No CSV)","💰 Betting Template","📊 Analytics","🔬 Methodology"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='color:#A78BFA;font-weight:700;font-size:0.8em;letter-spacing:2px;margin-bottom:10px;'>BANKROLL</div>", unsafe_allow_html=True)
    bankroll = st.number_input("Bankroll ($)", value=1000, min_value=50, step=50)
    kelly_fraction = st.slider("Kelly Fraction", 0.1, 1.0, 0.5, 0.05)
    st.markdown(f"<div class='metric-card'><div class='val'>${bankroll:,.0f}</div><div class='lab'>BANKROLL</div></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div style='color:rgba(255,255,255,0.4);font-size:0.65em;text-align:center;'>v4.0 · EQUI2024 · Benter Method</div>", unsafe_allow_html=True)

def fundamental_score_from_csv(row):
    try:
        q  = float(row.get("qRatingLS", row.get("QRating", 50)))
        l8 = float(row.get("l800", row.get("L800", 50)))
        l2 = float(row.get("l200", row.get("L200", 50)))
        mg = float(row.get("marginLS", row.get("Margin", 2)))
        sr = float(row.get("speedRatingLS", row.get("SpeedRating", 80)))
        ps = float(row.get("placeSR", row.get("PlaceSR", 0.3)))
        rp = float(row.get("runInPrep", row.get("RunInPrep", 3)))
        return (-0.9675 - 0.1584*q + 0.5336*l8 - 0.4530*l2 - 0.2181*mg + 0.0575*sr - 1.9478*ps - 0.0949*rp)
    except:
        return 0.0

def public_race_fundamental_score(barrier, weight, days_since_run, jockey_sr, trainer_sr, dist_suitability, recent_form, class_advantage):
    score = 0.0
    score -= max(0, (barrier - 8) * 0.04)
    score += (58.0 - weight) * 0.04
    if days_since_run <= 7: score -= 0.3
    elif days_since_run <= 28: score += 0.3
    elif days_since_run <= 60: score += 0.1
    else: score -= 0.5
    score += jockey_sr * 1.2
    score += trainer_sr * 0.8
    score += dist_suitability * 0.6
    score += recent_form * 0.5
    score += class_advantage * 0.4
    return score

def softmax_probs(scores):
    s = np.array(scores, dtype=float)
    s -= s.max()
    e = np.exp(s)
    return e / e.sum()

def odds_to_prob(odds):
    return 1.0 / odds if odds > 1.0 else 0.0

def benter_combined(p_fundamental, p_public, alpha=1.0, beta=0.85):
    eps = 1e-9
    raw = alpha * np.log(np.array(p_fundamental) + eps) + beta * np.log(np.array(p_public) + eps)
    raw -= raw.max()
    e = np.exp(raw)
    return e / e.sum()

def kelly_stake(prob, odds, bankroll, fraction=0.5):
    if odds <= 1.0 or prob <= 0: return 0.0
    b = odds - 1.0
    k = max(0.0, (prob * b - (1 - prob)) / b) * fraction
    return round(k * bankroll, 2)

def value_edge(prob, odds):
    return prob - (1.0 / odds) if odds > 1.0 else 0.0

def implied_overround(odds_list):
    return round(sum(1.0 / o for o in odds_list if o > 1.0) * 100, 1)

def form_string_to_score(form_str):
    try:
        positions = [int(x.strip()) for x in str(form_str).replace(",", "-").split("-") if x.strip().isdigit()]
        if not positions: return 0.5
        return max(0, min(1, (10 - np.mean(positions[:5])) / 9))
    except:
        return 0.5

def attempt_tab_odds_fetch(meeting, race_number):
    try:
        url = f"https://api.tab.com.au/v1/tab-info-service/racing/dates/today/meetings/{meeting}/races/{race_number}?jurisdiction=NSW"
        r = requests.get(url, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"}, timeout=8)
        if r.status_code == 200:
            odds_dict = {}
            for runner in r.json().get("runners", []):
                name = runner.get("runnerName", "")
                win_odd = runner.get("fixedOdds", {}).get("returnWin", None)
                if name and win_odd:
                    odds_dict[name.upper()] = float(win_odd)
            return odds_dict if odds_dict else None
    except:
        return None

for k, v in [("race_df", None), ("predictions", None), ("public_runners", []), ("public_predictions", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

if page == "🏠 Home":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='metric-card'><div class='val'>TWO MODES</div><div class='lab'>MY STABLE + PUBLIC RACES</div></div>", unsafe_allow_html=True)
        st.markdown("<div style='background:rgba(255,255,255,0.04);border:1px solid rgba(147,51,234,0.25);border-radius:10px;padding:18px;margin-top:10px;'><div style='color:#A78BFA;font-weight:700;font-size:0.85em;letter-spacing:2px;margin-bottom:12px;'>📁 MY STABLE RACES</div><div style='color:rgba(255,255,255,0.75);font-size:0.82em;line-height:1.7;'>✅ Upload race CSV with training data<br>✅ Full 7-feature regression model<br>✅ Speed ratings, L800, L200, form<br>✅ Best for horses you train & know<br>✅ 60.4% variance explained</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'><div class='val'>BENTER METHOD</div><div class='lab'>FUNDAMENTAL + MARKET ODDS</div></div>", unsafe_allow_html=True)
        st.markdown("<div style='background:rgba(255,255,255,0.04);border:1px solid rgba(236,72,153,0.25);border-radius:10px;padding:18px;margin-top:10px;'><div style='color:#F9A8D4;font-weight:700;font-size:0.85em;letter-spacing:2px;margin-bottom:12px;'>🌏 PUBLIC RACES (NO CSV)</div><div style='color:rgba(255,255,255,0.75);font-size:0.82em;line-height:1.7;'>✅ No training data needed<br>✅ Enter horse names + public stats<br>✅ Jockey/trainer strike rates<br>✅ TAB live odds auto-fetch (AU)<br>✅ Benter crowd-power model<br>✅ Races Australia, HK, anywhere</div></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div style='background:rgba(255,255,255,0.04);border:1px solid rgba(147,51,234,0.25);border-radius:12px;padding:20px;'><div style='color:#A78BFA;font-weight:700;font-size:0.9em;letter-spacing:2px;margin-bottom:14px;'>🧠 BILL BENTER'S KEY INSIGHT</div><div style='color:rgba(255,255,255,0.8);font-size:0.83em;line-height:1.8;'>Benter discovered that combining a fundamental model with public odds consistently outperforms either alone. The formula: <strong style='color:#4ADE80;'>log(P_combined) = 1.0 × log(P_fundamental) + 0.85 × log(P_market)</strong><br><br>When you have NO training data, market odds become your most powerful predictor — the crowd has already priced jockey form, trainer form, track bias, recent work, and insider knowledge.</div></div>", unsafe_allow_html=True)
    col3, col4, col5, col6 = st.columns(4)
    for col, val, lab, clr in zip([col3,col4,col5,col6],["78%","0.85","½ Kelly","114%"],["HIT@1 (with odds)","BENTER BETA","RECOMMENDED","OOS ROI"],["#F0ABFC","#93C5FD","#4ADE80","#FCD34D"]):
        with col:
            st.markdown(f"<div class='metric-card'><div class='val' style='color:{clr};'>{val}</div><div class='lab'>{lab}</div></div>", unsafe_allow_html=True)

elif page == "📁 My Stable Races":
    st.markdown("## 📁 My Stable Races — CSV Upload")
    st.markdown("<div class='info-box'>Upload your race CSV. The model uses 7 features: QRating, L800, L200, Margin, SpeedRating, PlaceSR, RunInPrep.</div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload Race CSV", type=["csv"])
    if uploaded:
        try:
            df = pd.read_csv(uploaded, encoding="utf-8-sig")
            df.columns = df.columns.str.strip()
            st.session_state["race_df"] = df
            st.success(f"✅ Loaded {len(df)} runners from {uploaded.name}")
            st.dataframe(df.head(5), use_container_width=True)
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    if st.session_state["race_df"] is not None:
        df = st.session_state["race_df"]
        name_cols = [c for c in df.columns if any(k in c.lower() for k in ["horse","name","runner"])]
        name_col = name_cols[0] if name_cols else df.columns[0]
        if st.button("🚀 RUN PREDICTION", type="primary", use_container_width=True):
            results = []
            for _, row in df.iterrows():
                results.append({"Horse": str(row.get(name_col, f"Horse {_}")), "raw_score": fundamental_score_from_csv(row)})
            probs = softmax_probs([r["raw_score"] for r in results])
            for i, r in enumerate(results):
                r["Win Prob %"] = round(probs[i] * 100, 1)
            results.sort(key=lambda x: x["Win Prob %"], reverse=True)
            for rank, r in enumerate(results, 1):
                r["Model Rank"] = rank
            st.session_state["predictions"] = results
        if st.session_state["predictions"]:
            preds = st.session_state["predictions"]
            winner = preds[0]
            st.markdown(f"<div class='winner-card'><div style='font-size:0.7em;color:#F9A8D4;letter-spacing:3px;margin-bottom:6px;'>🏆 PREDICTED WINNER</div><div class='wname'>{winner['Horse']}</div><div class='wprob'>{winner['Win Prob %']}% Win Probability</div></div>", unsafe_allow_html=True)
            rows_html = ""
            for r in preds:
                medal = "🥇" if r["Model Rank"]==1 else ("🥈" if r["Model Rank"]==2 else ("🥉" if r["Model Rank"]==3 else f"#{r['Model Rank']}"))
                rc = "rank1" if r["Model Rank"]==1 else ("rank2" if r["Model Rank"]==2 else ("rank3" if r["Model Rank"]==3 else ""))
                rows_html += f"<tr class='{'value-bet' if r['Model Rank']<=3 else ''}'><td class='{rc}'>{medal}</td><td class='{rc}'>{r['Horse']}</td><td>{r['Win Prob %']}%</td><td>{'⭐ Back' if r['Model Rank']<=3 else '—'}</td></tr>"
            st.markdown(f"<table class='pred-table'><thead><tr><th>#</th><th>HORSE</th><th>WIN PROB</th><th>SIGNAL</th></tr></thead><tbody>{rows_html}</tbody></table>", unsafe_allow_html=True)
            fig = go.Figure(go.Bar(x=[p["Horse"] for p in preds], y=[p["Win Prob %"] for p in preds], marker_color=[f"rgba(147,51,234,{0.3+p['Win Prob %']/100*0.7})" for p in preds], text=[f"{p['Win Prob %']}%" for p in preds], textposition="auto"))
            fig.update_layout(template="plotly_dark", title="Win Probability", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", xaxis_tickangle=-30, font=dict(family="Montserrat"))
            st.plotly_chart(fig, use_container_width=True)
            top3 = [p["Horse"] for p in preds[:3]]
            st.markdown(f"<div class='success-box'>🎯 <strong>TRIFECTA BOX:</strong> {top3[0]} / {top3[1]} / {top3[2] if len(top3)>2 else '—'}<br>💡 Go to 💰 Betting Template to calculate Kelly stakes.</div>", unsafe_allow_html=True)

elif page == "🌏 Public Races (No CSV)":
    st.markdown("## 🌏 Public Races — No Training Data Needed")
    st.markdown("<div class='info-box'>Use this for ANY race — Australia, Hong Kong, anywhere. Enter publicly available info: barrier, weight, jockey/trainer strike rates, days since run, distance suitability, recent form. Odds are the most powerful input.</div>", unsafe_allow_html=True)
    st.markdown("### 🏟️ Race Details")
    col1, col2, col3, col4 = st.columns(4)
    with col1: race_name_pub = st.text_input("Race / Meeting", "e.g. Eagle Farm R5")
    with col2: race_dist_pub = st.number_input("Distance (m)", 1000, 3200, 1200, 100)
    with col3: race_class_pub = st.selectbox("Class", ["BM50","BM56","BM64","BM72","BM78","BM88","G3","G2","G1","Open","Maiden","CL1","CL2","CL3","CL4","CL5","CL6"])
    with col4: going_pub = st.selectbox("Going", ["Firm","Good","Soft","Heavy","Synthetic"])
    st.markdown("---")
    num_runners = st.number_input("Number of runners", 2, 24, 8, 1)
    with st.expander("🔴 LIVE ODDS — TAB Auto-Fetch (Optional)"):
        st.markdown("<div class='warn-box'>TAB live odds require the exact meeting code and race number. If auto-fetch fails, enter odds manually below.</div>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3)
        with col_a: tab_meeting = st.text_input("TAB Meeting Code", "EF")
        with col_b: tab_race_no = st.number_input("Race Number", 1, 12, 1)
        with col_c: jurisdiction = st.selectbox("Jurisdiction", ["NSW","VIC","QLD","SA","WA","TAS"])
        if st.button("🔴 ATTEMPT AUTO-FETCH ODDS"):
            with st.spinner("Attempting TAB API..."):
                fetched = attempt_tab_odds_fetch(tab_meeting, tab_race_no)
                if fetched:
                    st.session_state["fetched_odds"] = fetched
                    st.success(f"✅ Fetched {len(fetched)} runners!")
                    for h, o in fetched.items(): st.write(f"  {h}: ${o:.2f}")
                else:
                    st.session_state["fetched_odds"] = {}
                    st.warning("Could not auto-fetch. Enter odds manually.")
    if "fetched_odds" not in st.session_state: st.session_state["fetched_odds"] = {}
    st.markdown("---")
    st.markdown("### 📝 Runner Entry Form")
    st.markdown("<div class='info-box'>HORSE NAME | BARRIER | WEIGHT | ODDS $ | JOCKEY SR% | TRAINER SR% | DIST SUITABILITY (0-10) | FORM (e.g. 1-2-3) | DAYS SINCE RUN</div>", unsafe_allow_html=True)
    header_cols = st.columns([2,1,1,1.5,1.5,1.5,1.5,1.5,1.5])
    for hc, hd in zip(header_cols, ["HORSE NAME","BARR","WT(kg)","ODDS $","JOC SR%","TRN SR%","DIST SUIT","FORM","DAYS OFF"]):
        hc.markdown(f"<div style='color:#A78BFA;font-size:0.65em;font-weight:700;'>{hd}</div>", unsafe_allow_html=True)
    runners_input = []
    for i in range(int(num_runners)):
        cols = st.columns([2,1,1,1.5,1.5,1.5,1.5,1.5,1.5])
        with cols[0]: name = st.text_input(f"N{i}", f"Horse {i+1}", key=f"name_{i}", label_visibility="collapsed")
        with cols[1]: barrier = st.number_input(f"B{i}", 1, 24, i+1, key=f"bar_{i}", label_visibility="collapsed")
        with cols[2]: weight = st.number_input(f"W{i}", 50.0, 65.0, 57.5, 0.5, key=f"wt_{i}", label_visibility="collapsed")
        with cols[3]:
            pf = st.session_state["fetched_odds"].get(name.upper() if name else "", 0.0)
            odds = st.number_input(f"O{i}", 1.0, 999.0, max(1.5, pf) if pf > 0 else 10.0, 0.5, key=f"odds_{i}", label_visibility="collapsed")
        with cols[4]: jsr = st.number_input(f"J{i}", 0, 50, 12, key=f"jsr_{i}", label_visibility="collapsed") / 100
        with cols[5]: tsr = st.number_input(f"T{i}", 0, 50, 14, key=f"tsr_{i}", label_visibility="collapsed") / 100
        with cols[6]: dst = st.slider(f"DS{i}", 0, 10, 5, key=f"dst_{i}", label_visibility="collapsed") / 10
        with cols[7]:
            form_raw = st.text_input(f"F{i}", "1-2-3", key=f"frm_{i}", label_visibility="collapsed")
        with cols[8]: days_off = st.number_input(f"DO{i}", 0, 365, 21, key=f"doff_{i}", label_visibility="collapsed")
        runners_input.append({"name": name, "barrier":<span class="cursor">█</span>
