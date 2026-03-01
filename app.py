"""
Equilytics — Quantum Race Prediction Engine
Streamlit Cloud App for quantumraceprediction/quantum_racing_predictor
Password: EQUI2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Equilytics — Quantum Race Predictor",
    page_icon="🏇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif !important;
}

.main-title {
    font-size: 2.4rem;
    font-weight: 900;
    background: linear-gradient(135deg, #FF6B9D, #C44569);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}
.tagline {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 1.5rem;
}
.race-banner {
    background: linear-gradient(135deg, #1e293b, #7f1d1d);
    border-radius: 12px;
    padding: 16px 20px;
    color: white;
    margin-bottom: 1.5rem;
}
.winner-card {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    border-radius: 12px;
    padding: 20px;
    color: white;
    text-align: center;
}
.metric-card {
    background: white;
    border-radius: 10px;
    padding: 16px;
    border: 1px solid #e2e8f0;
    text-align: center;
}
.section-title {
    font-size: 1rem;
    font-weight: 700;
    background: linear-gradient(135deg, #FF6B9D, #C44569);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.kelly-box {
    background: linear-gradient(135deg, #064e3b, #065f46);
    border-radius: 12px;
    padding: 16px 20px;
    color: white;
    margin-bottom: 1rem;
}
.benter-box {
    background: linear-gradient(135deg, #0f172a, #1e1b4b);
    border-radius: 12px;
    padding: 16px 20px;
    color: white;
    margin-bottom: 1rem;
}
.sci-box {
    background: linear-gradient(135deg, #1e3a8a, #1e40af);
    border-radius: 12px;
    padding: 16px 20px;
    color: white;
    margin-bottom: 1rem;
}
stButton > button {
    background: linear-gradient(135deg, #FF6B9D, #C44569) !important;
    color: white !important;
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'race_df' not in st.session_state:
    st.session_state.race_df = None
if 'results' not in st.session_state:
    st.session_state.results = None

# ─────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────
CORRECT_PASSWORD = "EQUI2024"

# Regression coefficients from READINESS_GENERATOR_V2
REG = {
    'intercept':      -0.9675,
    'qRatingLS':      -0.1584,
    'l800':            0.5336,
    'l200':           -0.4530,
    'marginLS':       -0.2181,
    'speedRatingLS':   0.0575,
    'placeSR':        -1.9478,
    'runInPrep':      -0.0949
}

ZONE_COLORS = {
    'Z0': '#78350f', 'Z1': '#14532d', 'Z2': '#166534',
    'Z3': '#0c4a6e', 'Z4': '#1e3a8a', 'Z5': '#7f1d1d',
    'Z6': '#831843', 'Z7': '#4c1d95'
}

# ─────────────────────────────────────────
#  LOGIN SCREEN
# ─────────────────────────────────────────
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div class="main-title">🏇 Equilytics</div>', unsafe_allow_html=True)
        st.markdown('<div class="tagline">Art & Science of Training</div>', unsafe_allow_html=True)
        st.markdown("### Quantum Race Prediction Engine")
        st.markdown("*Benter Model · Sport Science · Kelly Criterion*")
        st.markdown("---")
        pwd = st.text_input("Access Code", type="password", placeholder="Enter access code")
        if st.button("🔐 Enter Prediction Lab", use_container_width=True):
            if pwd == CORRECT_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Invalid access code. Please try again.")
        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3)
        col_a.markdown("🤖 **ML Prediction**")
        col_b.markdown("📐 **Benter Model**")
        col_c.markdown("💰 **Kelly Criterion**")
    st.stop()

# ─────────────────────────────────────────
#  AUTHENTICATED — MAIN APP
# ─────────────────────────────────────────

# ── SIDEBAR ──
with st.sidebar:
    st.markdown('<div class="main-title">Equilytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Quantum Race Prediction</div>', unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio("Navigation", [
        "📤 Upload & Predict",
        "🎯 Full Predictions",
        "📐 Benter Model",
        "🧬 Sport Science",
        "💰 Kelly Betting",
        "📖 Methodology"
    ])

    st.markdown("---")

    # Bankroll settings
    st.markdown("### 💼 Bankroll Settings")
    bankroll = st.number_input("Bankroll ($)", min_value=100, value=1000, step=100)
    kelly_fraction = st.slider("Kelly Fraction", 0.1, 1.0, 0.5, 0.1,
                                help="0.5 = Half-Kelly (recommended). Full Kelly is aggressive.")

    st.markdown("---")
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.race_df = None
        st.session_state.results = None
        st.rerun()

    st.markdown("---")
    st.markdown("**v1.0** · Password: EQUI2024")
    st.markdown("*Not financial advice*")


# ─────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────
COL_MAP = {
    'horseName':     ['Horse Name', 'horse_name', 'Horse', 'HORSE', 'name'],
    'speedRatingLS': ['Speed Rating LS', 'SR LS', 'Speed Rating', 'SR'],
    'qRatingLS':     ['Q Rating LS', 'Q-Rating LS', 'Q_Rating LS', 'QRating', 'Q Rating'],
    'l800':          ['Last 800 RAT LS', 'L800', 'Last 800', 'L 800 LS'],
    'l200':          ['Last 200 RAT LS', 'L200', 'Last 200', 'L 200 LS'],
    'marginLS':      ['Margin LS', 'Margin', 'MARGIN LS'],
    'placeSR':       ['Place SR', 'place_sr', 'PlaceSR'],
    'winSR':         ['Wins SR', 'Win SR', 'win_sr'],
    'runInPrep':     ['Run In Prep', 'RunInPrep', 'Run-In Prep'],
    'barrier':       ['Barrier', 'barrier', 'BARRIER', 'Gate'],
    'weight':        ['Weight Carried', 'Weight', 'weight', 'WGT'],
    'track':         ['Track', 'track', 'Course', 'Racecourse'],
    'distance':      ['Distance', 'distance', 'Dist'],
    'date':          ['Date', 'date', 'Race Date'],
    'classCode':     ['Class Code', 'Class', 'class'],
    'going':         ['Going', 'going', 'Track Condition'],
    'raceNo':        ['Race Number', 'Race No', 'RaceNo'],
    'bestL800':      ['Best L800 RAT L3', 'Best L800'],
    't600':          ['To 600 RAT LS', 'T600'],
}

def map_columns(df):
    """Map raw CSV columns to standard names."""
    result = {}
    for std_name, candidates in COL_MAP.items():
        for c in candidates:
            if c in df.columns:
                result[std_name] = df[c]
                break
        if std_name not in result:
            result[std_name] = pd.Series([None] * len(df))
    mapped = pd.DataFrame(result)
    # Numeric conversion
    num_cols = ['speedRatingLS','qRatingLS','l800','l200','marginLS','placeSR',
                'winSR','runInPrep','barrier','weight','bestL800','t600']
    for c in num_cols:
        mapped[c] = pd.to_numeric(mapped[c], errors='coerce')
    return mapped


def softmax(scores):
    """Convert scores to probabilities (lower score = better, so negate)."""
    neg = -np.array(scores, dtype=float)
    neg = np.where(np.isnan(neg), neg.min(), neg)
    e = np.exp(neg - neg.max())
    return e / e.sum()


def compute_fundamental_score(row):
    """Regression model from READINESS_GENERATOR_V2."""
    def v(col, scale=1.0):
        val = row.get(col)
        if val is None or (isinstance(val, float) and np.isnan(val)):
            return 0.0
        return float(val) * scale
    return (REG['intercept']
            + REG['qRatingLS']     * v('qRatingLS')
            + REG['l800']          * v('l800', 1/100)
            + REG['l200']          * v('l200', 1/100)
            + REG['marginLS']      * v('marginLS', 1/10)
            + REG['speedRatingLS'] * v('speedRatingLS', 1/100)
            + REG['placeSR']       * v('placeSR')
            + REG['runInPrep']     * v('runInPrep'))


def compute_composite(row):
    """Weighted composite speed rating."""
    total, weight = 0.0, 0.0
    pairs = [('speedRatingLS', 0.35), ('qRatingLS', 0.25),
             ('l800', 0.20), ('bestL800', 0.10), ('l200', 0.10)]
    for col, w in pairs:
        val = row.get(col)
        if val is not None and not (isinstance(val, float) and np.isnan(val)):
            total += float(val) * w
            weight += w
    return total / weight if weight > 0 else 0.0


def compute_science_profile(row):
    sr  = float(row.get('speedRatingLS') or 90)
    l8  = float(row.get('l800') or 90)
    l2  = float(row.get('l200') or 90)
    t6  = float(row.get('t600') or sr)
    bl8 = float(row.get('bestL800') or l8)

    vo2proxy = min(100, max(0, ((sr - 80) / 30) * 100))
    lf = l8 / max(sr, 1)
    if lf >= 0.99:      lac_zone, lac_name = 'Z4', 'VO₂Max'
    elif lf >= 0.96:    lac_zone, lac_name = 'Z3', 'Threshold'
    elif lf >= 0.92:    lac_zone, lac_name = 'Z2', 'Aerobic'
    else:               lac_zone, lac_name = 'Z1', 'Recovery'

    sprint_reserve = round(l2 - l8, 1)
    aerobic_window = round(t6 - l8, 1)
    readiness = min(100, max(0, round(
        (sr/110*0.3 + l8/110*0.3 + l2/110*0.2 + float(row.get('qRatingLS') or 90)/110*0.2) * 100
    )))
    return {
        'vo2proxy': round(vo2proxy),
        'lac_zone': lac_zone, 'lac_name': lac_name,
        'sprint_reserve': sprint_reserve,
        'aerobic_window': aerobic_window,
        'peak_l8': round(bl8, 1),
        'readiness': readiness
    }


def benter_combine(fund_probs, pub_probs, alpha=1.0, beta=0.85):
    """Benter's log-odds blending of fundamental + public probabilities."""
    lf = np.log(np.maximum(fund_probs, 0.001))
    lp = np.log(np.maximum(pub_probs,  0.001))
    logit = alpha * lf + beta * lp
    e = np.exp(logit - logit.max())
    return e / e.sum()


def kelly_bet(model_prob, decimal_odds, fraction=0.5):
    """Kelly Criterion with fractional staking."""
    b = decimal_odds - 1
    q = 1 - model_prob
    full = (model_prob * b - q) / b
    return max(0.0, full * fraction)


def run_models(df):
    """Run all prediction models and return sorted results DataFrame."""
    rows = df.to_dict('records')
    n = len(rows)

    fund_scores = np.array([compute_fundamental_score(r) for r in rows])
    comp_scores = np.array([compute_composite(r)          for r in rows])

    # Barrier & weight adjustments
    def barrier_adj(b, n):
        if pd.isna(b): return 1.0
        b = int(b)
        if b <= 4: return 1.02
        if b <= 8: return 1.00
        return 0.97

    def weight_adj(w):
        if pd.isna(w): return 1.0
        return 0.997 ** max(0, float(w) - 55)

    adj = np.array([barrier_adj(rows[i].get('barrier'), n) *
                    weight_adj(rows[i].get('weight')) for i in range(n)])

    fund_probs = softmax(fund_scores)
    comp_probs = softmax(-comp_scores)   # higher composite = better

    # Blend fundamental + composite
    blended = fund_probs * 0.6 + comp_probs * 0.4
    blended = blended * adj
    blended /= blended.sum()

    sci = [compute_science_profile(r) for r in rows]

    results = pd.DataFrame({
        'Horse':         [r['horseName'] for r in rows],
        'Barrier':       [r.get('barrier') for r in rows],
        'Weight':        [r.get('weight') for r in rows],
        'SR_LS':         [r.get('speedRatingLS') for r in rows],
        'Q_Rating':      [r.get('qRatingLS') for r in rows],
        'L800':          [r.get('l800') for r in rows],
        'L200':          [r.get('l200') for r in rows],
        'Margin_LS':     [r.get('marginLS') for r in rows],
        'Place_SR':      [r.get('placeSR') for r in rows],
        'Fund_Score':    fund_scores,
        'Fund_Prob':     blended,
        'Benter_Prob':   blended.copy(),   # updated when odds entered
        'Decimal_Odds':  [None] * n,
        'VO2_Proxy':     [s['vo2proxy']      for s in sci],
        'Lac_Zone':      [s['lac_zone']      for s in sci],
        'Lac_Name':      [s['lac_name']      for s in sci],
        'Sprint_Reserve':[s['sprint_reserve'] for s in sci],
        'Readiness':     [s['readiness']     for s in sci],
    })

    results = results.sort_values('Fund_Prob', ascending=False).reset_index(drop=True)
    results.insert(0, 'Rank', range(1, len(results) + 1))
    return results


def extract_race_info(df):
    """Pull race metadata from first row."""
    def g(cols):
        for c in cols:
            if c in df.columns and not df[c].isna().all():
                return str(df[c].iloc[0])
        return '—'
    return {
        'track':    g(['Track','track','Course','Racecourse']),
        'date':     g(['Date','date','Race Date']),
        'distance': g(['Distance','distance','Dist']),
        'class':    g(['Class Code','Class','class']),
        'going':    g(['Going','going','Track Condition']),
        'race_no':  g(['Race Number','Race No','RaceNo']),
    }


# ─────────────────────────────────────────
#  PAGE: UPLOAD & PREDICT
# ─────────────────────────────────────────
if page == "📤 Upload & Predict":
    st.markdown('<div class="main-title">📤 Upload Race Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Upload your CSV to generate instant predictions</div>', unsafe_allow_html=True)

    st.info("💡 Accepts Equilytics CSV format — columns: Speed Rating LS, Q-Rating LS, Last 800 RAT LS, Last 200 RAT LS, Margin LS, Place SR, Run In Prep, Barrier, Weight Carried.")

    uploaded = st.file_uploader("Choose your race CSV", type=['csv'])

    if uploaded:
        try:
            df_raw = pd.read_csv(uploaded)
            df = map_columns(df_raw)
            df = df[df['horseName'].notna() & (df['horseName'] != '')].reset_index(drop=True)
            race_info = extract_race_info(df_raw)

            with st.spinner("Running prediction models..."):
                results = run_models(df)

            st.session_state.race_df   = df
            st.session_state.results   = results
            st.session_state.race_info = race_info

            st.success(f"✅ Race data loaded! {len(results)} runners analysed.")

            # Race banner
            c1,c2,c3,c4,c5,c6 = st.columns(6)
            c1.metric("🏁 Track",    race_info['track'])
            c2.metric("📅 Date",     race_info['date'])
            c3.metric("📏 Distance", race_info['distance']+'m' if race_info['distance']!='—' else '—')
            c4.metric("🏷️ Class",   race_info['class'])
            c5.metric("🌱 Going",    race_info['going'])
            c6.metric("🐎 Runners",  len(results))

            st.markdown("---")
            st.markdown("### 🏆 Quick Results")
            winner = results.iloc[0]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="winner-card">
                    <div style="font-size:1.8rem;font-weight:900;">🥇 {winner['Horse']}</div>
                    <div style="font-size:1.1rem;margin-top:8px;">Win Probability: {winner['Fund_Prob']*100:.1f}%</div>
                    <div style="font-size:0.9rem;margin-top:4px;">SR: {winner['SR_LS']} | L800: {winner['L800']} | {winner['Lac_Zone']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"**🥈 2nd Choice:** {results.iloc[1]['Horse']} ({results.iloc[1]['Fund_Prob']*100:.1f}%)")
                st.markdown(f"**🥉 3rd Choice:** {results.iloc[2]['Horse']} ({results.iloc[2]['Fund_Prob']*100:.1f}%)" if len(results) > 2 else "")
                st.markdown(f"**Trifecta Box:** {' / '.join(results.head(3)['Horse'].tolist())}")
            with col3:
                st.markdown(f"**Winner Readiness:** {winner['Readiness']}%")
                st.markdown(f"**VO₂max Proxy:** {winner['VO2_Proxy']}%")
                st.markdown(f"**Physio Zone:** {winner['Lac_Zone']} — {winner['Lac_Name']}")

            st.markdown("---")
            st.markdown("➡️ **Navigate to '🎯 Full Predictions' in the sidebar for complete analysis**")

        except Exception as e:
            st.error(f"Error loading CSV: {e}")

    else:
        st.markdown("### Awaiting CSV Upload...")
        st.markdown("""
        **Required columns (at minimum):**
        - `Horse Name` — horse identifier
        - `Speed Rating LS` — last start speed rating
        - `Last 800 RAT LS` — last 800m rating
        - `Q Rating LS` — quality rating

        **Optional but recommended:**
        - `Last 200 RAT LS`, `Margin LS`, `Place SR`, `Barrier`, `Weight Carried`
        """)


# ─────────────────────────────────────────
#  PAGE: FULL PREDICTIONS
# ─────────────────────────────────────────
elif page == "🎯 Full Predictions":
    st.markdown('<div class="main-title">🎯 Full Predictions</div>', unsafe_allow_html=True)

    if st.session_state.results is None:
        st.warning("📤 Please upload a race CSV on the Upload page first.")
        st.stop()

    results = st.session_state.results
    ri = st.session_state.race_info

    st.markdown(f"**{ri['track']} · {ri['date']} · {ri['distance']}m · {ri['going']} · {ri['class']} · {len(results)} runners**")
    st.markdown("---")

    # Display table
    display_cols = ['Rank','Horse','Barrier','Weight','SR_LS','Q_Rating','L800','L200',
                    'Fund_Prob','Lac_Zone','Readiness']
    display_df = results[display_cols].copy()
    display_df['Fund_Prob'] = display_df['Fund_Prob'].apply(lambda x: f"{x*100:.1f}%")
    display_df['Readiness'] = display_df['Readiness'].apply(lambda x: f"{x}%")
    display_df.columns = ['#','Horse','Barrier','Weight (kg)','SR LS','Q-Rating','L800','L200',
                           'Win Prob','Physio Zone','Readiness']

    # Colour top 3
    def highlight_top3(row):
        if row['#'] == 1: return ['background-color: #fef3c7']*len(row)
        if row['#'] == 2: return ['background-color: #f1f5f9']*len(row)
        if row['#'] == 3: return ['background-color: #fdf4ff']*len(row)
        return ['']*len(row)

    st.dataframe(display_df.style.apply(highlight_top3, axis=1), use_container_width=True)

    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📊 Win Probability")
        fig = px.bar(
            results, x='Horse', y=results['Fund_Prob']*100,
            labels={'y':'Win Probability (%)', 'x':'Horse'},
            color=results['Fund_Prob']*100,
            color_continuous_scale=['#94a3b8','#3b82f6','#f59e0b'],
            text=results['Fund_Prob'].apply(lambda x: f"{x*100:.1f}%")
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, coloraxis_showscale=False,
                          plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          height=350, margin=dict(t=20,b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📈 Speed Ratings Comparison")
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name='Speed Rating LS', x=results['Horse'],
                              y=results['SR_LS'], marker_color='rgba(255,107,157,0.8)'))
        fig2.add_trace(go.Bar(name='L800 Rating', x=results['Horse'],
                              y=results['L800'], marker_color='rgba(59,130,246,0.8)'))
        fig2.update_layout(barmode='group', height=350,
                           plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                           margin=dict(t=20,b=20), legend=dict(orientation='h', yanchor='bottom', y=1))
        st.plotly_chart(fig2, use_container_width=True)

    # Feature importance
    st.markdown("#### 🎯 Model Feature Importance")
    fi_data = pd.DataFrame({
        'Feature': ['Place SR','L200','L800','Q-Rating LS','Margin LS','Speed Rating LS','Run-In Prep'],
        'Importance': [42, 28, 23, 19, 15, 13, 9]
    })
    fig3 = px.bar(fi_data, x='Importance', y='Feature', orientation='h',
                  color='Importance', color_continuous_scale=['#e2e8f0','#FF6B9D','#C44569'])
    fig3.update_layout(coloraxis_showscale=False, height=280,
                       plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                       margin=dict(t=10, b=10))
    st.plotly_chart(fig3, use_container_width=True)

    # Print button
    if st.button("🖨️ Prepare Print Report"):
        report = results[['Rank','Horse','SR_LS','L800','L200','Fund_Prob','Lac_Zone','Readiness']].copy()
        report['Fund_Prob'] = report['Fund_Prob'].apply(lambda x: f"{x*100:.1f}%")
        report['Readiness'] = report['Readiness'].apply(lambda x: f"{x}%")
        st.markdown("### 🖨️ Print Report")
        st.dataframe(report, use_container_width=True)
        st.markdown(f"*Generated by Equilytics Quantum Race Predictor · {ri['track']} · {ri['date']} · Not financial advice*")


# ─────────────────────────────────────────
#  PAGE: BENTER MODEL
# ─────────────────────────────────────────
elif page == "📐 Benter Model":
    st.markdown('<div class="main-title">📐 Benter Combined Model</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Multinomial Logit: Fundamental × Public Odds Blending</div>', unsafe_allow_html=True)

    if st.session_state.results is None:
        st.warning("📤 Upload a CSV first.")
        st.stop()

    results = st.session_state.results.copy()

    st.markdown("""
    <div class="benter-box">
        <strong style="color:#FF6B9D;font-size:1.1rem;">📐 Bill Benter's $1 Billion Algorithm</strong><br>
        <span style="color:rgba(255,255,255,0.8);font-size:0.85rem;">
        Combined Score = α × log(P_fundamental) + β × log(P_public)<br>
        Where α = 1.0 (model weight), β = 0.85 (market weight)<br>
        Key finding: 20–25% model probability at 8–20x odds = documented market inefficiency (~114% OOS ROI)
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Enter odds
    st.markdown("#### 🎰 Enter Current Market Odds (decimal)")
    st.caption("Leave blank to use fundamental model only. Enter tote or SP odds (e.g. 4.50)")

    odds_cols = st.columns(min(len(results), 4))
    odds_values = {}
    for i, (_, row) in enumerate(results.iterrows()):
        col_idx = i % 4
        with odds_cols[col_idx]:
            odds_values[row['Horse']] = st.number_input(
                row['Horse'][:20], min_value=1.01, value=None,
                step=0.5, key=f"odds_benter_{i}", format="%.2f"
            )

    if st.button("🔄 Run Benter Combined Model"):
        valid_odds = {h: o for h, o in odds_values.items() if o is not None}
        if valid_odds:
            all_odds = [valid_odds.get(h, 99) for h in results['Horse']]
            raw_pub = np.array([1/o for o in all_odds])
            pub_probs = raw_pub / raw_pub.sum()
            combined = benter_combine(results['Fund_Prob'].values, pub_probs)
            results['Benter_Prob'] = combined
            results['Pub_Prob']    = pub_probs
            results['Edge']        = results.apply(
                lambda r: r['Benter_Prob'] - (1/valid_odds[r['Horse']]) if r['Horse'] in valid_odds else np.nan,
                axis=1
            )
            results = results.sort_values('Benter_Prob', ascending=False).reset_index(drop=True)
            results['Rank'] = range(1, len(results)+1)
            st.session_state.results = results
            st.success("✅ Benter combined model applied!")
        else:
            st.info("No odds entered — showing fundamental model probabilities.")

    # Display Benter table
    display = results[['Rank','Horse','Fund_Prob','Benter_Prob']].copy()
    if 'Pub_Prob' in results.columns:
        display['Pub_Prob'] = results['Pub_Prob']
        display['Edge']     = results['Edge']
    display['Fund_Prob']   = display['Fund_Prob'].apply(lambda x: f"{x*100:.1f}%")
    display['Benter_Prob'] = display['Benter_Prob'].apply(lambda x: f"{x*100:.1f}%")
    if 'Pub_Prob' in display.columns:
        display['Pub_Prob'] = display['Pub_Prob'].apply(lambda x: f"{x*100:.1f}%")
        display['Edge']     = display['Edge'].apply(
            lambda x: f"+{x*100:.1f}%" if (isinstance(x, float) and not np.isnan(x) and x > 0)
            else (f"{x*100:.1f}%" if isinstance(x, float) and not np.isnan(x) else "—"))

    st.dataframe(display, use_container_width=True)

    # Market inefficiency alert
    st.markdown("#### 🔍 Market Inefficiency Alert")
    midband = results[(results['Fund_Prob'] >= 0.18) & (results['Fund_Prob'] <= 0.28)]
    if len(midband) > 0:
        st.success(f"⭐ Horses in the 18–28% model probability band (optimal betting zone per MartianOak HK research):")
        for _, r in midband.iterrows():
            st.markdown(f"**{r['Horse']}** — {r['Fund_Prob']*100:.1f}% model probability → watch for tote odds ≥ 8.0")
    else:
        st.info("No horses in the optimal 18–28% probability band for this race.")

    # Doughnut chart
    fig = px.pie(results, values='Fund_Prob', names='Horse',
                 title="Win Probability Distribution",
                 color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(height=350, margin=dict(t=40,b=10))
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────
#  PAGE: SPORT SCIENCE
# ─────────────────────────────────────────
elif page == "🧬 Sport Science":
    st.markdown('<div class="main-title">🧬 Equine Sport Science</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">VO₂max Proxy · Lactate Zones · Sprint Reserve · Aerobic Window</div>', unsafe_allow_html=True)

    if st.session_state.results is None:
        st.warning("📤 Upload a CSV first.")
        st.stop()

    results = st.session_state.results

    st.markdown("""
    <div class="sci-box">
        <strong style="color:#93c5fd;font-size:1.1rem;">🧬 Physiological Performance Framework</strong><br>
        <span style="color:rgba(255,255,255,0.8);font-size:0.85rem;">
        VO₂max proxy derived from Speed Rating LS · Lactate zone from L800/SR ratio ·
        Sprint reserve = L200 − L800 · Aerobic window = T600 − L800 · 
        Training zones Z0–Z7 mapped to physiological performance
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Science metrics display
    sci_display = results[['Rank','Horse','VO2_Proxy','Lac_Zone','Lac_Name',
                            'Sprint_Reserve','Readiness','SR_LS','L800','L200']].copy()
    sci_display['VO2_Proxy']  = sci_display['VO2_Proxy'].apply(lambda x: f"{x}%")
    sci_display['Readiness']  = sci_display['Readiness'].apply(lambda x: f"{x}%")
    sci_display.columns = ['#','Horse','VO₂max Proxy','Zone','Zone Name','Sprint Reserve',
                            'Readiness','SR LS','L800','L200']
    st.dataframe(sci_display, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📊 VO₂max Proxy by Horse")
        fig = px.bar(results, x='Horse', y='VO2_Proxy',
                     color='VO2_Proxy', color_continuous_scale=['#bfdbfe','#1d4ed8'],
                     labels={'VO2_Proxy':'VO₂max Proxy (%)', 'Horse':''},
                     text=results['VO2_Proxy'].apply(lambda x: f"{x}%"))
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, coloraxis_showscale=False,
                          height=320, plot_bgcolor='rgba(0,0,0,0)',
                          paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=20,b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 🎯 Readiness Index by Horse")
        fig2 = px.bar(results, x='Horse', y='Readiness',
                      color='Readiness', color_continuous_scale=['#d1fae5','#059669'],
                      labels={'Readiness':'Readiness Index (%)', 'Horse':''},
                      text=results['Readiness'].apply(lambda x: f"{x}%"))
        fig2.update_traces(textposition='outside')
        fig2.update_layout(showlegend=False, coloraxis_showscale=False,
                           height=320, plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=20,b=20))
        st.plotly_chart(fig2, use_container_width=True)

    # Zone reference
    st.markdown("---")
    st.markdown("#### 📚 Training Zone Reference (Z0–Z7)")
    zone_data = [
        ("Z0", "Rest Day",          "Paddock rest & recovery",             "#78350f"),
        ("Z1", "Recovery",          "Easy walking & light movement",        "#14532d"),
        ("Z2", "Aerobic Base",      "Foundational aerobic fitness",         "#166534"),
        ("Z3", "Threshold",         "Lactate threshold training intensity",  "#0c4a6e"),
        ("Z4", "VO₂ Max",           "Hard interval training",               "#1e3a8a"),
        ("Z5", "Lactate Prod.",     "High lactate building",                "#7f1d1d"),
        ("Z6", "Lactate Tol.",      "Lactate clearance training",           "#831843"),
        ("Z7", "Maximum",           "Competition intensity",                 "#4c1d95"),
    ]
    cols = st.columns(4)
    for i, (z, name, desc, color) in enumerate(zone_data):
        with cols[i % 4]:
            count = len(results[results['Lac_Zone'] == z])
            st.markdown(f"""
            <div style="background:{color}20;border:1px solid {color}60;border-radius:10px;padding:12px;margin-bottom:8px;">
                <div style="color:{color};font-weight:800;font-size:0.9rem;">{z} — {name}</div>
                <div style="font-size:1.4rem;font-weight:900;color:{color};">{count}</div>
                <div style="font-size:0.7rem;color:#64748b;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────
#  PAGE: KELLY BETTING
# ─────────────────────────────────────────
elif page == "💰 Kelly Betting":
    st.markdown('<div class="main-title">💰 Kelly Criterion Betting</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Optimal Bet Sizing · Edge Calculation · Bankroll Management</div>', unsafe_allow_html=True)

    if st.session_state.results is None:
        st.warning("📤 Upload a CSV first.")
        st.stop()

    results = st.session_state.results.copy()

    st.markdown("""
    <div class="kelly-box">
        <strong style="color:#6ee7b7;font-size:1.1rem;">💰 Kelly Criterion Formula</strong><br>
        <span style="color:rgba(255,255,255,0.8);font-size:0.85rem;">
        Kelly % = (p × b − q) / b × Fraction<br>
        Where: p = model win probability, q = 1−p, b = decimal odds − 1<br>
        Half-Kelly (0.5) recommended to reduce variance. Only bet when Kelly% > 0.
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"**Bankroll: ${bankroll:,.0f} | Kelly Fraction: {kelly_fraction}**")
    st.caption("Enter tote or SP odds below, then click Calculate.")

    # Odds input
    odds_cols = st.columns(min(len(results), 4))
    odds_values = {}
    for i, (_, row) in enumerate(results.iterrows()):
        with odds_cols[i % 4]:
            odds_values[row['Horse']] = st.number_input(
                row['Horse'][:18], min_value=1.01, value=None,
                step=0.5, key=f"odds_kelly_{i}", format="%.2f"
            )

    if st.button("💰 Calculate Kelly Stakes", use_container_width=True):
        valid = {h: o for h, o in odds_values.items() if o is not None}

        if valid:
            # Benter update with odds
            all_odds_arr = [valid.get(h, 99) for h in results['Horse']]
            raw_pub = np.array([1/o for o in all_odds_arr])
            pub_probs = raw_pub / raw_pub.sum()
            combined = benter_combine(results['Fund_Prob'].values, pub_probs)
            results['Model_Prob'] = combined
        else:
            results['Model_Prob'] = results['Fund_Prob']

        kelly_rows = []
        for _, row in results.iterrows():
            horse = row['Horse']
            model_p = row['Model_Prob']
            odds = valid.get(horse)
            if odds:
                k = kelly_bet(model_p, odds, kelly_fraction)
                stake = bankroll * k
                edge  = model_p - (1/odds)
                fair  = 1 / model_p
            else:
                k, stake, edge, odds, fair = 0, 0, None, None, 1/model_p
            kelly_rows.append({
                'Horse': horse,
                'Model Prob': f"{model_p*100:.1f}%",
                'Market Odds': f"${odds:.2f}" if odds else "—",
                'Fair Odds':   f"${fair:.2f}",
                'Edge':        f"+{edge*100:.1f}%" if edge and edge>0 else (f"{edge*100:.1f}%" if edge else "—"),
                'Kelly %':     f"{k*100:.1f}%",
                'Stake ($)':   f"${stake:.0f}" if k>0 else "—",
                'Action':      "✅ BET" if k>0 else "❌ Skip"
            })

        kelly_df = pd.DataFrame(kelly_rows)
        st.markdown("---")
        st.markdown("### 📋 Kelly Stakes Table")

        def highlight_kelly(row):
            if row['Action'] == '✅ BET': return ['background-color:#d1fae5']*len(row)
            return ['']*len(row)

        st.dataframe(kelly_df.style.apply(highlight_kelly, axis=1), use_container_width=True)

        # Totals
        bets_n    = sum(1 for r in kelly_rows if r['Action'] == '✅ BET')
        total_stk = sum(float(r['Stake ($)'].replace('$','').replace(',',''))
                        for r in kelly_rows if r['Stake ($)'] != '—')
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Bets Recommended", bets_n)
        c2.metric("Total Stake",      f"${total_stk:,.0f}")
        c3.metric("% of Bankroll",    f"{total_stk/bankroll*100:.1f}%")
        c4.metric("Bankroll Remaining", f"${bankroll-total_stk:,.0f}")

    else:
        # Show fair odds from model
        st.markdown("### 📊 Model-Derived Fair Odds")
        fair_df = pd.DataFrame({
            'Horse':     results['Horse'],
            'Model Prob': results['Fund_Prob'].apply(lambda x: f"{x*100:.1f}%"),
            'Fair Price': results['Fund_Prob'].apply(lambda x: f"${1/x:.2f}"),
            'Signal':     results['Rank'].apply(
                lambda r: "⭐ Back if odds > fair" if r==1 else "👁️ Watch" if r<=3 else "Skip")
        })
        st.dataframe(fair_df, use_container_width=True)


# ─────────────────────────────────────────
#  PAGE: METHODOLOGY
# ─────────────────────────────────────────
elif page == "📖 Methodology":
    st.markdown('<div class="main-title">📖 Methodology</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">How the Quantum Race Prediction Engine Works</div>', unsafe_allow_html=True)

    st.markdown("""
    ---
    ### 🏆 1. Fundamental Speed Model

    Based on the Equilytics READINESS_GENERATOR_V2 regression coefficients, calibrated to position prediction:

    ```
    Predicted Position = −0.9675
        − 0.1584 × Q-Rating LS
        + 0.5336 × L800
        − 0.4530 × L200
        − 0.2181 × Margin LS
        + 0.0575 × Speed Rating LS
        − 1.9478 × Place SR
        − 0.0949 × Run-In Prep
    ```

    **Validation:** Random Forest (100 trees) — 60.4% variance explained, RMSE 2.05 positions.
    Lower predicted position = better. Scores converted to win probabilities via softmax.

    ---
    ### 📐 2. Benter Combined Model

    Bill Benter's key breakthrough: a fundamental model alone is **systematically biased**.
    The fix is to blend fundamental probabilities with public market odds:

    ```
    Combined Score = α × log(P_fundamental) + β × log(P_public)
    Final Win Probability = softmax(Combined Score)
    α = 1.0 (model weight), β = 0.85 (market weight)
    ```

    **Key research findings:**
    - MartianOak HK engine: 1,050 features, CatBoost ranker → Hit@1 **78%**, OOS ROI **~114%**
    - Market inefficiency band: **0.20–0.25 model probability at 8–20x tote odds**
    - Top SHAP features: Win Odds (42.3 gain), Rating Progression (3.1–3.5), Recent Form (2.0–2.4)

    ---
    ### 🧬 3. Equine Sport Science Integration

    | Metric | Derivation | Racing Significance |
    |--------|-----------|-------------------|
    | **VO₂max Proxy** | (SR − 80) / 30 × 100 | Aerobic capacity ceiling |
    | **Lactate Zone** | L800/SR ratio | Metabolic efficiency |
    | **Sprint Reserve** | L200 − L800 | Neuromuscular finish |
    | **Aerobic Window** | T600 − L800 | Sustained pace capacity |
    | **Readiness Index** | Weighted composite | Overall race preparation |

    ---
    ### 💰 4. Kelly Criterion Bet Sizing

    ```
    Kelly % = (p × b − q) / b × Fraction
    p = model win probability
    q = 1 − p
    b = decimal odds − 1
    Fraction = 0.5 (Half-Kelly recommended)
    ```

    **Rules:**
    - Only bet when Kelly% > 0 (positive edge)
    - Max single bet: 5% of bankroll
    - Track ≥ 100 bets before assessing system profitability
    - Use Half-Kelly (0.5) to reduce variance significantly

    ---
    ### 🌏 Hong Kong → Australian Racing

    | Factor | Hong Kong (HKJC) | Australia (TAB/Betfair) |
    |--------|-----------------|------------------------|
    | Population | Closed (~1,400 horses) | Open, multi-state |
    | Races/year | ~700 | ~20,000+ |
    | Data quality | Excellent (Edina schema) | Good (Racing Australia) |
    | Market efficiency | High (Benter era) | Moderate |
    | Edge opportunity | Moderate but measurable | Higher variance, more edge |

    ---
    *Equilytics Quantum Race Prediction Engine v1.0 · Not financial advice · For research purposes only*
    """)
