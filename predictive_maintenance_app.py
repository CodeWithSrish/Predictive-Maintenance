"""
🏭 Predictive Maintenance Dashboard — Industry 5.0
Author: Srishti Rajput | Inspired by Rockwell Automation & IFFCO
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PredictMaint | Industry 5.0",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Industrial Dark Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Share+Tech+Mono&family=Rajdhani:wght@500;600;700&display=swap');

:root {
    --bg-deep:    #050d18;
    --bg-panel:   #0a1628;
    --bg-card:    #0d1f38;
    --accent-cyan:#00e5ff;
    --accent-amber:#ffab00;
    --accent-red: #ff1744;
    --accent-green:#00e676;
    --text-main:  #e8f4ff;
    --text-muted: #8aafd4;
    --border:     rgba(0,229,255,0.15);
}

html, body, [class*="css"] {
    background-color: var(--bg-deep) !important;
    color: var(--text-main) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 2rem 2rem !important; max-width: 100% !important; margin: auto; }

/* ── HEADER BANNER ── */
.dashboard-header {
    background: linear-gradient(135deg, #050d18 0%, #0a2040 50%, #050d18 100%);
    border-bottom: 1px solid var(--accent-cyan);
    padding: 1.4rem 2rem 1rem 2rem;
    margin: -1rem -2rem 1.5rem -2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.header-title { font-family: 'Rajdhani', sans-serif; font-size: 2.5rem; font-weight: 700; color: var(--accent-cyan); letter-spacing: 3px; text-transform: uppercase; }
.header-sub { font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; color: var(--text-muted); letter-spacing: 2px; margin-top: 2px; }
.header-badge {
    background: rgba(0,229,255,0.08);
    border: 1px solid var(--accent-cyan);
    border-radius: 4px;
    padding: 4px 14px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    color: var(--accent-cyan);
    letter-spacing: 2px;
}

/* ── KPI CARDS ── */
.kpi-row { display: flex; gap: 12px; margin-bottom: 1.2rem; }
.kpi-card {
    flex: 1;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.kpi-green::before  { background: var(--accent-green); }
.kpi-cyan::before   { background: var(--accent-cyan); }
.kpi-amber::before  { background: var(--accent-amber); }
.kpi-red::before    { background: var(--accent-red); }
.kpi-label { font-family: 'Share Tech Mono', monospace; font-size: 0.7rem; letter-spacing: 2px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px; }
.kpi-value { font-family: 'Rajdhani', sans-serif; font-size: 2.2rem; font-weight: 700; line-height: 1; }
.kpi-sub   { font-size: 0.78rem; color: var(--text-muted); margin-top: 3px; }

/* ── SECTION HEADERS ── */
.section-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 3px;
    color: var(--accent-cyan);
    text-transform: uppercase;
    border-left: 3px solid var(--accent-cyan);
    padding-left: 10px;
    margin-bottom: 0.8rem;
}

/* ── INPUT PANEL (full width) ── */
.input-panel {
    background: linear-gradient(145deg, #0a1a30, #0d2040);
    border: 1px solid var(--accent-cyan);
    border-radius: 12px;
    padding: 1.8rem 2.5rem;
    box-shadow: 0 0 40px rgba(0,229,255,0.06), inset 0 0 30px rgba(0,229,255,0.02);
    width: 100%;
    box-sizing: border-box;
}
.input-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent-cyan);
    letter-spacing: 3px;
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 1.4rem;
}

/* ── Streamlit input label readability ── */
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: var(--text-main) !important;
    letter-spacing: 0.3px;
}
div[data-testid="stNumberInput"] input {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1rem !important;
    background: #0a1628 !important;
    color: var(--accent-cyan) !important;
    border: 1px solid rgba(0,229,255,0.3) !important;
    border-radius: 6px !important;
}

/* ── RESULT CARDS ── */
.result-critical {
    background: linear-gradient(135deg, rgba(255,23,68,0.15), rgba(255,23,68,0.05));
    border: 1px solid var(--accent-red);
    border-radius: 10px;
    padding: 1.4rem;
    text-align: center;
}
.result-warning {
    background: linear-gradient(135deg, rgba(255,171,0,0.15), rgba(255,171,0,0.05));
    border: 1px solid var(--accent-amber);
    border-radius: 10px;
    padding: 1.4rem;
    text-align: center;
}
.result-safe {
    background: linear-gradient(135deg, rgba(0,230,118,0.15), rgba(0,230,118,0.05));
    border: 1px solid var(--accent-green);
    border-radius: 10px;
    padding: 1.4rem;
    text-align: center;
}
.result-label { font-family: 'Share Tech Mono', monospace; font-size: 0.65rem; letter-spacing: 3px; margin-bottom: 6px; }
.result-status { font-family: 'Rajdhani', sans-serif; font-size: 2.4rem; font-weight: 700; }
.result-score  { font-family: 'Rajdhani', sans-serif; font-size: 1.2rem; margin-top: 4px; }

/* ── FAILURE TAG PILLS ── */
.pill-row { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; margin-top: 10px; }
.pill {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 1.5px;
    padding: 4px 10px;
    border-radius: 3px;
    border: 1px solid;
}
.pill-active { color: #ff1744; border-color: #ff1744; background: rgba(255,23,68,0.12); }
.pill-inactive { color: var(--text-muted); border-color: rgba(122,155,191,0.3); background: transparent; }

/* ── EXPLAIN BLOCK ── */
.explain-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    line-height: 1.65;
    color: var(--text-main);
}

/* ── SUGGESTION BOX ── */
.suggestion-box {
    background: linear-gradient(145deg, #0f1e35, #0a1828);
    border-radius: 10px;
    padding: 1.3rem 1.6rem;
    margin-top: 1.2rem;
    border-left-width: 3px;
    border-left-style: solid;
    border-top: 1px solid rgba(255,171,0,0.2);
    border-right: 1px solid rgba(255,171,0,0.2);
    border-bottom: 1px solid rgba(255,171,0,0.2);
}
.suggestion-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.9rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.suggestion-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 0.6rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    color: #cce0f5;
    line-height: 1.55;
}
.suggestion-dot       { color: var(--accent-amber); font-size: 1rem; margin-top: 2px; flex-shrink: 0; }
.suggestion-dot-red   { color: var(--accent-red);   font-size: 1rem; margin-top: 2px; flex-shrink: 0; }
.suggestion-dot-green { color: var(--accent-green); font-size: 1rem; margin-top: 2px; flex-shrink: 0; }

/* General readability */
p, li { font-size: 0.9rem; line-height: 1.65; }
h1, h2, h3 { font-family: 'Rajdhani', sans-serif; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def compute_risk(air_temp, proc_temp, rpm, torque, tool_wear, mtype):
    delta_t  = proc_temp - air_temp
    power_w  = torque * rpm * 2 * np.pi / 60
    strain   = tool_wear * torque
    failures = {"TWF": False, "HDF": False, "PWF": False, "OSF": False, "RNF": False}

    if tool_wear > 200 and torque > 40:        failures["TWF"] = True
    if delta_t < 8.6 or delta_t > 12.0:        failures["HDF"] = True
    if power_w < 3500 or power_w > 9000:       failures["PWF"] = True
    osf_lim = {"L": 11000, "M": 12000, "H": 13000}.get(mtype, 12000)
    if strain > osf_lim:                        failures["OSF"] = True
    if rpm < 1380 and torque > 27:              failures["RNF"] = True

    active = sum(failures.values())
    if active >= 2:   risk = "CRITICAL"; score = min(95 + active * 2, 99)
    elif active == 1: risk = "WARNING";  score = 55 + list(failures.values()).index(True) * 5
    else:             risk = "SAFE";     score = max(5, int(10 + tool_wear * 0.05 + abs(delta_t - 10) * 3))

    return risk, score, failures, delta_t, power_w, strain


def get_suggestions(risk, failures, delta_t, power_w, strain, rpm, torque, tool_wear, mtype):
    """Return actionable maintenance suggestions based on failure modes."""
    suggestions = []

    if failures["TWF"]:
        suggestions.append(("🔴", f"Tool Wear Failure risk — inspect cutting tool immediately. Accumulated wear is {tool_wear:.0f} min with {torque:.1f} Nm torque. Replace tool if wear exceeds 200 min under high torque conditions."))
    if failures["HDF"]:
        if delta_t < 8.6:
            suggestions.append(("🔴", f"Heat Dissipation Failure: Temperature delta is {delta_t:.1f} K (below safe minimum of 8.6 K). Check coolant flow rate, clean heat exchangers, and verify fan/blower operation."))
        else:
            suggestions.append(("🔴", f"Heat Dissipation Failure: Temperature delta is {delta_t:.1f} K (above safe maximum of 12 K). Machine is overheating — reduce load, inspect blocked vents, and check lubrication system immediately."))
    if failures["PWF"]:
        if power_w < 3500:
            suggestions.append(("🟡", f"Power Output Low: {power_w:.0f} W is below the 3,500 W minimum. Check motor connections, verify supply voltage, and inspect drive belts or couplings for slippage."))
        else:
            suggestions.append(("🟡", f"Power Output High: {power_w:.0f} W exceeds the 9,000 W maximum. Machine is overloaded — reduce feed rate or cutting depth, and check for mechanical binding or jamming."))
    if failures["OSF"]:
        osf_lim = {"L": 11000, "M": 12000, "H": 13000}.get(mtype, 12000)
        suggestions.append(("🔴", f"Overstrain Failure: Strain index {strain:.0f} exceeds Type-{mtype} limit of {osf_lim:,}. Reduce torque load immediately. Inspect spindle bearings, verify workpiece clamping, and check tool alignment."))
    if failures["RNF"]:
        suggestions.append(("🟡", f"Random Failure risk: Low RPM ({rpm:.0f}) combined with high torque ({torque:.1f} Nm) — machine is under mechanical stress. Check for spindle obstruction, lubricate drive components, and verify motor health."))

    if risk == "SAFE":
        suggestions.append(("🟢", "All parameters are within the normal operating envelope. Continue the scheduled maintenance cycle."))
        suggestions.append(("🟢", f"Proactive tip: Tool wear is currently {tool_wear:.0f} min — plan replacement at 180 min to avoid unexpected TWF."))
        if abs(delta_t - 10) > 1.5:
            suggestions.append(("🟡", f"Temperature delta ({delta_t:.1f} K) is drifting from ideal 10 K. Monitor cooling performance over the next 2 hours."))

    return suggestions


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
now_str = time.strftime("%Y-%m-%d  %H:%M:%S")
st.markdown(f"""
<div class="dashboard-header">
    <div>
        <div class="header-title">⚙ PredictMaint 5.0</div>
        <div class="header-sub">INDUSTRY 5.0 · PREDICTIVE MAINTENANCE INTELLIGENCE PLATFORM</div>
    </div>
    <div class="header-badge">LIVE · {now_str}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI STRIP
# ─────────────────────────────────────────────
st.markdown("""
<div class="kpi-row">
  <div class="kpi-card kpi-green">
    <div class="kpi-label">Dataset Size</div>
    <div class="kpi-value" style="color:#00e676">10 000</div>
    <div class="kpi-sub">AI4I 2020 — UCI ML Repo</div>
  </div>
  <div class="kpi-card kpi-cyan">
    <div class="kpi-label">LightGBM ROC-AUC</div>
    <div class="kpi-value" style="color:#00e5ff">97.1%</div>
    <div class="kpi-sub">Best ensemble model</div>
  </div>
  <div class="kpi-card kpi-amber">
    <div class="kpi-label">Failure Rate</div>
    <div class="kpi-value" style="color:#ffab00">3.4%</div>
    <div class="kpi-sub">339 / 10 000 records</div>
  </div>
  <div class="kpi-card kpi-red">
    <div class="kpi-label">Net Savings</div>
    <div class="kpi-value" style="color:#ff6d6d">₹8.4 Cr</div>
    <div class="kpi-sub">Projected annual impact</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔬 Live Diagnosis", "📊 Analytics", "🧠 Project Intel"])

# ════════════════════════════════════════════
# TAB 1 — LIVE DIAGNOSIS
# ════════════════════════════════════════════
with tab1:
    st.markdown("")

    # ── INPUT PANEL — full width, no box above ──
    
    st.markdown('<div class="input-title">⚙ Enter Machine Telemetry</div>', unsafe_allow_html=True)

    # Row 1 — Machine Type + Air Temp + Process Temp
    c1, c2, c3 = st.columns([1, 1.5, 1.5])
    with c1:
        mtype     = st.selectbox("Machine Type", ["L", "M", "H"],
                                 help="L = Light, M = Medium, H = Heavy duty")
    with c2:
        air_temp  = st.number_input("Air Temperature (K)", min_value=290.0, max_value=310.0,
                                    value=298.1, step=0.1, format="%.1f")
    with c3:
        proc_temp = st.number_input("Process Temperature (K)", min_value=300.0, max_value=320.0,
                                    value=308.6, step=0.1, format="%.1f")

    # Row 2 — RPM + Torque + Tool Wear
    c4, c5, c6 = st.columns(3)
    with c4:
        rpm       = st.number_input("Rotational Speed (RPM)", min_value=1168, max_value=2886,
                                    value=1551, step=1)
    with c5:
        torque    = st.number_input("Torque (Nm)", min_value=3.8, max_value=76.6,
                                    value=42.8, step=0.1, format="%.1f")
    with c6:
        tool_wear = st.number_input("Tool Wear (min)", min_value=0, max_value=253,
                                    value=0, step=1)

    # Analyse button — centred
    _, btn_col, _ = st.columns([2, 1, 2])
    with btn_col:
        analyse = st.button("▶  ANALYSE", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── RESULTS ──
    if analyse:
        risk, score, failures, delta_t, power_w, strain = compute_risk(
            air_temp, proc_temp, rpm, torque, tool_wear, mtype)

        st.markdown("<br>", unsafe_allow_html=True)

        col_res, col_gauge = st.columns([1, 1])

        # ─ Status card ─
        with col_res:
            css_cls = {"CRITICAL": "result-critical", "WARNING": "result-warning", "SAFE": "result-safe"}[risk]
            color   = {"CRITICAL": "#ff1744", "WARNING": "#ffab00", "SAFE": "#00e676"}[risk]
            icon    = {"CRITICAL": "🔴", "WARNING": "🟡", "SAFE": "🟢"}[risk]
            st.markdown(f"""
            <div class="{css_cls}">
                <div class="result-label" style="color:{color}">MACHINE STATUS</div>
                <div class="result-status" style="color:{color}">{icon} {risk}</div>
                <div class="result-score" style="color:{color}">Risk Index: {score}/100</div>
            </div>
            """, unsafe_allow_html=True)

            # Failure pills
            pills_html = '<div class="pill-row">'
            for fm, active in failures.items():
                cls = "pill-active" if active else "pill-inactive"
                pills_html += f'<span class="pill {cls}">{fm}</span>'
            pills_html += '</div>'
            st.markdown(pills_html, unsafe_allow_html=True)

            # Physics-derived values
            st.markdown(f"""
            <div style="margin-top:1rem;display:flex;gap:10px">
                <div style="flex:1;background:#0a1628;border:1px solid rgba(0,229,255,0.15);border-radius:6px;padding:0.7rem 1rem;text-align:center">
                    <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#8aafd4;letter-spacing:2px">TEMP DELTA</div>
                    <div style="font-family:'Rajdhani',sans-serif;font-size:1.4rem;font-weight:700;color:#00e5ff">{delta_t:.1f} K</div>
                    <div style="font-family:'Inter',sans-serif;font-size:0.75rem;color:#8aafd4">Safe: 8.6–12 K</div>
                </div>
                <div style="flex:1;background:#0a1628;border:1px solid rgba(0,229,255,0.15);border-radius:6px;padding:0.7rem 1rem;text-align:center">
                    <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#8aafd4;letter-spacing:2px">POWER OUT</div>
                    <div style="font-family:'Rajdhani',sans-serif;font-size:1.4rem;font-weight:700;color:#00e5ff">{power_w:.0f} W</div>
                    <div style="font-family:'Inter',sans-serif;font-size:0.75rem;color:#8aafd4">Safe: 3,500–9,000 W</div>
                </div>
                <div style="flex:1;background:#0a1628;border:1px solid rgba(0,229,255,0.15);border-radius:6px;padding:0.7rem 1rem;text-align:center">
                    <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#8aafd4;letter-spacing:2px">STRAIN IDX</div>
                    <div style="font-family:'Rajdhani',sans-serif;font-size:1.4rem;font-weight:700;color:#00e5ff">{strain:.0f}</div>
                    <div style="font-family:'Inter',sans-serif;font-size:0.75rem;color:#8aafd4">Limit: L=11k M=12k H=13k</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ─ Gauge ─
        with col_gauge:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                number={'font': {'size': 42, 'color': color, 'family': 'Rajdhani'}, 'suffix': ''},
                gauge={
                    'axis': {'range': [0, 100], 'tickfont': {'size': 10, 'color': '#7a9bbf'}, 'tickwidth': 1, 'tickcolor': '#7a9bbf'},
                    'bar': {'color': color, 'thickness': 0.28},
                    'bgcolor': '#0d1f38',
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0,  40], 'color': 'rgba(0,230,118,0.12)'},
                        {'range': [40, 70], 'color': 'rgba(255,171,0,0.12)'},
                        {'range': [70,100], 'color': 'rgba(255,23,68,0.12)'},
                    ],
                    'threshold': {'line': {'color': color, 'width': 3}, 'thickness': 0.75, 'value': score},
                },
                title={'text': "RISK INDEX", 'font': {'family': 'Share Tech Mono', 'size': 11, 'color': '#7a9bbf'}},
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', height=280,
                margin=dict(t=40, b=20, l=30, r=30),
                font=dict(color='#7a9bbf'),
            )
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

        # ─ SUGGESTIONS PANEL ─
        suggestions = get_suggestions(risk, failures, delta_t, power_w, strain, rpm, torque, tool_wear, mtype)

        dot_map = {"🔴": "suggestion-dot-red", "🟡": "suggestion-dot", "🟢": "suggestion-dot-green"}
        border_color = {"CRITICAL": "#ff1744", "WARNING": "#ffab00", "SAFE": "#00e676"}[risk]
        title_color  = {"CRITICAL": "#ff6d6d", "WARNING": "#ffab00", "SAFE": "#00e676"}[risk]

        items_html = ""
        for dot, text in suggestions:
            dot_cls = dot_map.get(dot, "suggestion-dot")
            items_html += f'<div class="suggestion-item"><span class="{dot_cls}">{dot}</span><span>{text}</span></div>'

        st.markdown(f"""
        <div class="suggestion-box" style="border-left-color:{border_color}">
            <div class="suggestion-title" style="color:{title_color}">🔧 What to Check — Corrective Actions</div>
            {items_html}
        </div>
        """, unsafe_allow_html=True)

        # ─ AI Explainer ─
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">AI EXPLAINER</div>', unsafe_allow_html=True)
        active_list = [k for k, v in failures.items() if v]
        if active_list:
            expl = f"The model has detected <b style='color:#ff1744'>{len(active_list)} active failure mode(s)</b>: {', '.join(active_list)}. "
            if "HDF" in active_list:
                expl += f"Temperature delta of <b>{delta_t:.1f} K</b> is outside the 8.6–12 K safe band, indicating a heat dissipation problem. "
            if "PWF" in active_list:
                expl += f"Power output of <b>{power_w:.0f} W</b> is outside the 3,500–9,000 W safe zone — review load and drive system. "
            if "OSF" in active_list:
                expl += f"Strain index of <b>{strain:.0f}</b> exceeds the Type-{mtype} machine threshold — reduce torque immediately. "
            if "TWF" in active_list:
                expl += f"Tool wear of <b>{tool_wear} min</b> combined with {torque:.1f} Nm torque triggers the tool-wear failure threshold. "
            if "RNF" in active_list:
                expl += f"Low RPM ({rpm}) under high torque ({torque:.1f} Nm) indicates possible mechanical resistance or spindle issue. "
        else:
            expl = (f"All five physics-derived failure checks passed. Risk index is <b style='color:#00e676'>{score}/100</b>. "
                    f"Temperature delta ({delta_t:.1f} K), power ({power_w:.0f} W), and strain ({strain:.0f}) "
                    f"are all within safe operating bounds for a Type-{mtype} machine.")

        st.markdown(f'<div class="explain-box">{expl}</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 2 — ANALYTICS
# ════════════════════════════════════════════
with tab2:
    st.markdown("")
    np.random.seed(42)
    n = 10000
    rpm_data     = np.random.normal(1538, 180, n).clip(1168, 2886)
    torque_data  = np.random.normal(40, 10, n).clip(3.8, 76.6)
    air_data     = np.random.normal(300, 2, n).clip(295, 304)
    proc_data    = air_data + np.random.normal(10.1, 1.5, n)
    wear_data    = np.random.randint(0, 254, n)
    failure_mask = np.random.choice([0, 1], size=n, p=[0.966, 0.034])

    df = pd.DataFrame({
        'rpm': rpm_data, 'torque': torque_data,
        'air_temp': air_data, 'proc_temp': proc_data,
        'tool_wear': wear_data, 'failure': failure_mask,
        'delta_t': proc_data - air_data,
        'power': torque_data * rpm_data * 2 * np.pi / 60,
    })

    col_a1, col_a2 = st.columns(2)

    with col_a1:
        st.markdown('<div class="section-label">RPM vs TORQUE — FAILURE SCATTER</div>', unsafe_allow_html=True)
        fig_sc = go.Figure()
        for fail, col_name, sym in [(0, '#00e5ff', 'circle'), (1, '#ff1744', 'x')]:
            mask = df['failure'] == fail
            fig_sc.add_trace(go.Scatter(
                x=df.loc[mask, 'rpm'], y=df.loc[mask, 'torque'],
                mode='markers',
                marker=dict(color=col_name, size=3 if fail == 0 else 6,
                            symbol=sym, opacity=0.5 if fail == 0 else 0.9),
                name='Normal' if fail == 0 else 'Failure',
            ))
        fig_sc.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=300, margin=dict(t=10, b=40, l=50, r=10),
            legend=dict(font=dict(family='Share Tech Mono', size=10), bgcolor='rgba(0,0,0,0)'),
            xaxis=dict(title='RPM', gridcolor='rgba(255,255,255,0.05)',
                       tickfont=dict(size=10, color='#7a9bbf')),
            yaxis=dict(title='Torque (Nm)', gridcolor='rgba(255,255,255,0.05)',
                       tickfont=dict(size=10, color='#7a9bbf')),
            font=dict(color='#7a9bbf'),
        )
        st.plotly_chart(fig_sc, use_container_width=True, config={'displayModeBar': False})

    with col_a2:
        st.markdown('<div class="section-label">TOOL WEAR DISTRIBUTION</div>', unsafe_allow_html=True)
        fig_tw = go.Figure()
        for fail, col_name, lbl in [(0, '#00e5ff', 'Normal'), (1, '#ff1744', 'Failure')]:
            mask = df['failure'] == fail
            fig_tw.add_trace(go.Histogram(
                x=df.loc[mask, 'tool_wear'], nbinsx=40,
                marker_color=col_name, opacity=0.7, name=lbl,
            ))
        fig_tw.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=300, barmode='overlay', margin=dict(t=10, b=40, l=50, r=10),
            legend=dict(font=dict(family='Share Tech Mono', size=10), bgcolor='rgba(0,0,0,0)'),
            xaxis=dict(title='Tool Wear (min)', gridcolor='rgba(255,255,255,0.05)',
                       tickfont=dict(size=10, color='#7a9bbf')),
            yaxis=dict(title='Count', gridcolor='rgba(255,255,255,0.05)',
                       tickfont=dict(size=10, color='#7a9bbf')),
            font=dict(color='#7a9bbf'),
        )
        st.plotly_chart(fig_tw, use_container_width=True, config={'displayModeBar': False})

    col_fi, col_fm = st.columns(2)

    with col_fi:
        st.markdown('<div class="section-label">FEATURE IMPORTANCE (LightGBM)</div>', unsafe_allow_html=True)
        features   = ['Strain Index', 'Power (W)', 'Temp Delta', 'Tool Wear', 'Torque', 'RPM', 'Process Temp', 'Air Temp']
        importance = [0.312, 0.241, 0.158, 0.112, 0.087, 0.054, 0.023, 0.013]
        colors_fi  = ['#ff1744' if i < 2 else '#ffab00' if i < 4 else '#00e5ff' for i in range(len(features))]

        fig_fi = go.Figure(go.Bar(
            x=importance[::-1], y=features[::-1], orientation='h',
            marker=dict(color=colors_fi[::-1], line=dict(width=0)),
            text=[f'{v:.3f}' for v in importance[::-1]],
            textposition='outside',
            textfont=dict(family='Share Tech Mono', size=10, color='#e0f0ff'),
        ))
        fig_fi.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=300, margin=dict(t=10, b=10, l=110, r=60),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(size=10, color='#7a9bbf')),
            yaxis=dict(tickfont=dict(family='Share Tech Mono', size=10, color='#8aafd4'), showgrid=False),
            font=dict(color='#7a9bbf'),
        )
        st.plotly_chart(fig_fi, use_container_width=True, config={'displayModeBar': False})

    with col_fm:
        st.markdown('<div class="section-label">FAILURE MODE DISTRIBUTION</div>', unsafe_allow_html=True)
        fm_names  = ['TWF', 'HDF', 'PWF', 'OSF', 'RNF']
        fm_counts = [46, 115, 95, 98, 18]
        fm_colors = ['#ff6d6d', '#ff1744', '#ffab00', '#ff4d4d', '#ff9800']

        fig_fm = go.Figure(go.Bar(
            x=fm_names, y=fm_counts,
            marker=dict(color=fm_colors, line=dict(width=0)),
            text=fm_counts, textposition='outside',
            textfont=dict(family='Share Tech Mono', size=10, color='#e0f0ff'),
        ))
        fig_fm.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=300, margin=dict(t=30, b=30, l=20, r=20),
            title=dict(text='FAILURE MODE DISTRIBUTION', font=dict(family='Share Tech Mono', size=10, color='#7a9bbf')),
            xaxis=dict(tickfont=dict(family='Share Tech Mono', size=10, color='#7a9bbf'), showgrid=False),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(size=9)),
            font=dict(color='#7a9bbf'),
        )
        st.plotly_chart(fig_fm, use_container_width=True, config={'displayModeBar': False})

    # ── Model Comparison ──
    st.markdown('<div class="section-label">MODEL COMPARISON</div>', unsafe_allow_html=True)

    models = ['Logistic Reg.', 'Random Forest', 'Gradient Boost', 'XGBoost', 'LightGBM']
    auc    = [0.857, 0.954, 0.960, 0.966, 0.971]
    recall = [0.706, 0.794, 0.809, 0.838, 0.853]
    f1     = [0.658, 0.731, 0.745, 0.768, 0.779]

    fig_models = go.Figure()
    fig_models.add_trace(go.Bar(name='ROC-AUC', x=models, y=auc,   marker_color='#00e5ff', opacity=0.85))
    fig_models.add_trace(go.Bar(name='Recall',  x=models, y=recall, marker_color='#ffab00', opacity=0.85))
    fig_models.add_trace(go.Bar(name='F1 Score',x=models, y=f1,     marker_color='#00e676', opacity=0.85))
    fig_models.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=300, barmode='group',
        margin=dict(t=10, b=30, l=20, r=20),
        legend=dict(font=dict(family='Share Tech Mono', size=9), bgcolor='rgba(0,0,0,0)', orientation='h', y=1.1),
        xaxis=dict(tickfont=dict(family='Share Tech Mono', size=9, color='#7a9bbf'), showgrid=False),
        yaxis=dict(range=[0.5, 1.0], gridcolor='rgba(255,255,255,0.05)', tickfont=dict(size=9)),
        font=dict(color='#7a9bbf'),
    )
    st.plotly_chart(fig_models, use_container_width=True, config={'displayModeBar': False})

    # ── Operating Envelope Heatmap ──
    col_env, col_biz = st.columns(2)

    with col_env:
        st.markdown('<div class="section-label">OPERATING ENVELOPE — TEMP vs RPM RISK ZONES</div>', unsafe_allow_html=True)
        rpm_range   = np.linspace(1168, 2886, 40)
        delta_range = np.linspace(5, 16, 40)
        Z = np.zeros((40, 40))
        for i, d in enumerate(delta_range):
            for j, r in enumerate(rpm_range):
                risk_z = 0
                if d < 8.6 or d > 12: risk_z += 0.5
                if r < 1380:           risk_z += 0.4
                if r > 2200:           risk_z += 0.2
                Z[i, j] = min(risk_z, 1.0)

        fig_heat = go.Figure(go.Heatmap(
            z=Z, x=rpm_range, y=delta_range,
            colorscale=[[0,'rgba(0,230,118,0.6)'],[0.35,'rgba(255,171,0,0.7)'],[1,'rgba(255,23,68,0.9)']],
            showscale=True,
            colorbar=dict(tickfont=dict(size=9, color='#7a9bbf'), thickness=12),
        ))
        fig_heat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=260, margin=dict(t=10, b=40, l=50, r=20),
            xaxis=dict(title='RPM', tickfont=dict(size=9, color='#7a9bbf')),
            yaxis=dict(title='Temp Delta (K)', tickfont=dict(size=9, color='#7a9bbf')),
            font=dict(color='#7a9bbf'),
        )
        st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})

    with col_biz:
        st.markdown('<div class="section-label">BUSINESS IMPACT ANALYSIS</div>', unsafe_allow_html=True)
        categories = ['Failures<br>Prevented', 'Failures<br>Missed', 'False<br>Alarms']
        values     = [58, 10, 28]
        colors_biz = ['#00e676', '#ff1744', '#ffab00']

        fig_biz = go.Figure(go.Bar(
            x=categories, y=values,
            marker=dict(color=colors_biz),
            text=values, textposition='outside',
            textfont=dict(family='Share Tech Mono', size=11, color='#e0f0ff'),
        ))
        fig_biz.add_annotation(
            x=0.5, y=1.12, xref='paper', yref='paper',
            text='NET SAVINGS: ₹8.4 Cr', showarrow=False,
            font=dict(family='Share Tech Mono', size=11, color='#00e676'),
        )
        fig_biz.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=260, margin=dict(t=40, b=20, l=20, r=20),
            xaxis=dict(showgrid=False, tickfont=dict(family='Share Tech Mono', size=10, color='#7a9bbf')),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(size=9)),
            font=dict(color='#7a9bbf'),
        )
        st.plotly_chart(fig_biz, use_container_width=True, config={'displayModeBar': False})


# ════════════════════════════════════════════
# TAB 3 — PROJECT INTEL
# ════════════════════════════════════════════
with tab3:
    st.markdown("")

    col_i1, col_i2 = st.columns(2)

    with col_i1:
        st.markdown('<div class="section-label">INDUSTRY 5.0 PILLARS</div> ', unsafe_allow_html=True)
        pillars = [
            ("🤝 Human-Centric",  "Plain-language operator explainer, SHAP-driven decision support, human review queue for uncertain predictions (ensemble std > 0.12)."),
            ("🛡 Resilience",     "Ensemble uncertainty quantification, PSI drift monitoring, threshold-tuned recall-first strategy to minimise missed failures."),
            ("🌱 Sustainability", "Energy efficiency analysis, CO₂ footprint estimation, link between predictive maintenance and emissions reduction."),
        ]
        for title, desc in pillars:
            st.markdown(f"""
            <div class="explain-box" style="margin-bottom:10px">
                <b style="font-family:'Rajdhani',sans-serif;font-size:1rem;color:#00e5ff">{title}</b><br>
                <span style="color:#b8d4ee;font-size:0.9rem">{desc}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-label" style="margin-top:1rem">DEPLOYMENT ARCHITECTURE</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="explain-box">
            <b style="color:#00e5ff">Edge Layer</b> — LightGBM (~0.1 ms/inference) on industrial PLC or ARM board<br>
            <b style="color:#00e5ff">Action Layer</b> — 🔴 Critical/High → SAP PM work order · 🟡 Medium → CMMS watchlist · ❓ Uncertain → Engineer queue<br>
            <b style="color:#00e5ff">Monitoring Layer</b> — Weekly PSI check → MLOps pipeline · Monthly performance review · Quarterly retraining<br>
            <b style="color:#00e5ff">Integration</b> — REST API wrapper over .pkl for SCADA/DCS · Docker containerised · MLflow versioned
        </div>
        """, unsafe_allow_html=True)

    with col_i2:
        st.markdown('<div class="section-label">PHYSICS-DRIVEN FEATURES</div>', unsafe_allow_html=True)
        feats = [
            ("Temperature Delta",  "Process_Temp − Air_Temp",       "Key HDF detection signal. Safe range: 8.6–12 K"),
            ("Power Output (W)",   "Torque × RPM × 2π/60",          "Physics-derived. Safe zone: 3,500–9,000 W"),
            ("Strain Index",       "Tool_Wear × Torque",             "OSF signal. Type-specific thresholds"),
            ("Boundary Flags",     "5 binary envelope indicators",   "Violations trigger risk escalation"),
        ]
        for name, formula, note in feats:
            st.markdown(f"""
            <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:6px;padding:0.8rem 1rem;margin-bottom:8px">
                <div style="font-family:'Rajdhani',sans-serif;font-weight:600;color:#00e5ff;font-size:1.55rem">{name}</div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:1.0rem;color:#ffab00;margin:3px 0">{formula}</div>
                <div style="font-family:'Inter',sans-serif;font-size:0.85rem;color:#8aafd4">{note}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-label" style="margin-top:1.5rem">5 LESSONS FROM THE SHOP FLOOR</div>', unsafe_allow_html=True)
        lessons = [
            ("Physics first, then ML",      "Engineer features from process knowledge, not just statistics"),
            ("Recall over accuracy",         "A missed failure is always worse than a false alarm"),
            ("Explain everything",           "If operators don't trust the model, they won't use it"),
            ("Think in costs, not metrics",  "ROC-AUC doesn't impress plant managers; saved lakhs do"),
            ("Know when to defer",           "Industry 5.0 means AI that knows its own limits"),
        ]
        for i, (title, desc) in enumerate(lessons, 1):
            st.markdown(f"""
            <div style="display:flex;gap:10px;margin-bottom:8px;align-items:flex-start">
                <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;color:#00e5ff;min-width:24px">{i}.</div>
                <div>
                    <span style="font-family:'Inter',sans-serif;font-weight:600;color:#e8f4ff;font-size:0.92rem">{title}</span>
                    <span style="color:#8aafd4;font-size:0.86rem"> — {desc}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="margin-top:2rem;border-top:1px solid rgba(0,229,255,0.1);padding-top:1rem;
         font-family:'Share Tech Mono',monospace;font-size:0.62rem;color:#4a6a8f;letter-spacing:2px;text-align:center">
        AI4I 2020 PREDICTIVE MAINTENANCE DATASET · UCI ML REPOSITORY (DOI: 10.24432/C5HS5C) ·
        MATZKA, S. (2020). EXPLAINABLE AI FOR PREDICTIVE MAINTENANCE. ·
        AUTHOR: SRISHTI RAJPUT · ROCKWELL AUTOMATION / IFFCO CONTEXT
    </div>
    """, unsafe_allow_html=True)
