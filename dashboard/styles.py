"""
FutureFund – Styles
All CSS injected into Streamlit via st.markdown.
"""

MAIN_CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sora:wght@600;700;800&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary:     #0d1117;
    --bg-secondary:   #161b22;
    --bg-card:        #1c2333;
    --bg-elevated:    #21262d;
    --accent-blue:    #58a6ff;
    --accent-green:   #3fb950;
    --accent-gold:    #d29922;
    --accent-red:     #f85149;
    --accent-purple:  #bc8cff;
    --text-primary:   #e6edf3;
    --text-secondary: #8b949e;
    --text-muted:     #484f58;
    --border:         rgba(255,255,255,0.08);
    --radius-sm:      8px;
    --radius-md:      12px;
    --radius-lg:      16px;
    --shadow:         0 4px 24px rgba(0,0,0,0.4);
}

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: var(--bg-primary) !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
    color: var(--text-primary) !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 4px; }

/* ── Metric Cards ── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: var(--accent-blue); }
.metric-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-bottom: 0.35rem;
}
.metric-value {
    font-family: 'Sora', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.1;
}
.metric-sub {
    font-size: 0.72rem;
    color: var(--text-secondary);
    margin-top: 0.25rem;
}
.metric-value.green  { color: var(--accent-green); }
.metric-value.blue   { color: var(--accent-blue);  }
.metric-value.gold   { color: var(--accent-gold);  }
.metric-value.red    { color: var(--accent-red);   }
.metric-value.purple { color: var(--accent-purple);}

/* ── Goal Sticky Note Cards ── */
.goal-note {
    background: linear-gradient(135deg, #fef9c3 0%, #fde68a 100%);
    border-radius: var(--radius-md);
    padding: 1rem 1.1rem;
    margin-bottom: 0.75rem;
    border-left: 4px solid #d97706;
    box-shadow: 3px 3px 10px rgba(0,0,0,0.3), 0 1px 3px rgba(0,0,0,0.2);
    color: #1a1a1a;
    position: relative;
    transform: rotate(-0.3deg);
    transition: transform 0.2s, box-shadow 0.2s;
}
.goal-note:nth-child(even) { transform: rotate(0.3deg); }
.goal-note:hover {
    transform: rotate(0deg) scale(1.01);
    box-shadow: 4px 4px 16px rgba(0,0,0,0.4);
}
.goal-note::before {
    content: '';
    position: absolute;
    top: -6px;
    left: 50%;
    transform: translateX(-50%);
    width: 20px;
    height: 12px;
    background: rgba(0,0,0,0.15);
    border-radius: 2px;
}
.goal-note-title {
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 0.25rem;
    color: #1a1a1a;
}
.goal-note-meta {
    font-size: 0.72rem;
    color: #4a4a4a;
    margin-bottom: 0.3rem;
}
.goal-note-cost {
    font-weight: 700;
    font-size: 1.05rem;
    color: #92400e;
}
.goal-note-notes {
    font-size: 0.68rem;
    color: #6b6b6b;
    font-style: italic;
    margin-top: 0.4rem;
    line-height: 1.4;
}
.priority-badge {
    display: inline-block;
    padding: 0.1rem 0.5rem;
    border-radius: 99px;
    font-size: 0.62rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Section Headers ── */
.section-header {
    font-family: 'Sora', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Panel containers ── */
.panel {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.1rem;
    height: 100%;
}

/* ── Top hero bar ── */
.hero-bar {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.1rem 1.6rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #58a6ff, #bc8cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-top: 0.15rem;
}

/* ── Finley Mascot ── */
@keyframes finley-walk {
    0%   { left: -120px; }
    100% { left: calc(100% + 20px); }
}
@keyframes finley-bob {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-6px); }
}
.finley-wrapper {
    position: fixed;
    bottom: 16px;
    left: -120px;
    width: 90px;
    z-index: 999;
    animation:
        finley-walk 18s linear infinite,
        finley-bob  0.9s ease-in-out infinite;
    pointer-events: none;
    user-select: none;
}
.finley-speech {
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: white;
    color: #1a1a1a;
    border-radius: 10px;
    padding: 0.4rem 0.7rem;
    font-size: 0.65rem;
    font-weight: 600;
    white-space: nowrap;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    margin-bottom: 4px;
}
.finley-speech::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 5px solid transparent;
    border-top-color: white;
}

/* ── Chatbot ── */
.chat-container {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    overflow: hidden;
}
.chat-header {
    background: linear-gradient(90deg, #1c2333, #21262d);
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    font-weight: 600;
}
.chat-bubble-user {
    background: #1d4ed8;
    color: white;
    border-radius: 12px 12px 2px 12px;
    padding: 0.55rem 0.9rem;
    font-size: 0.82rem;
    max-width: 85%;
    margin-left: auto;
    margin-bottom: 0.5rem;
    line-height: 1.5;
}
.chat-bubble-finley {
    background: var(--bg-elevated);
    color: var(--text-primary);
    border-radius: 12px 12px 12px 2px;
    padding: 0.55rem 0.9rem;
    font-size: 0.82rem;
    max-width: 92%;
    margin-bottom: 0.5rem;
    line-height: 1.6;
    border-left: 3px solid var(--accent-blue);
}
.chat-messages {
    padding: 0.75rem 1rem;
    max-height: 260px;
    overflow-y: auto;
}

/* ── Progress / Gauge ── */
.gauge-bar {
    height: 8px;
    border-radius: 99px;
    background: #30363d;
    overflow: hidden;
    margin-top: 0.4rem;
}
.gauge-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.6s ease;
}

/* ── Badges ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.2rem 0.6rem;
    border-radius: 99px;
    font-size: 0.68rem;
    font-weight: 600;
}

/* ── Stacked metric row ── */
.kpi-row {
    display: flex;
    gap: 0.6rem;
    margin-bottom: 0.75rem;
    flex-wrap: wrap;
}
.kpi-item {
    flex: 1;
    min-width: 90px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0.6rem 0.75rem;
    text-align: center;
}
.kpi-num {
    font-family: 'Sora', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
}
.kpi-lbl {
    font-size: 0.62rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.15rem;
}

/* ── Dividers ── */
.ff-divider {
    height: 1px;
    background: var(--border);
    margin: 0.8rem 0;
}

/* ── Streamlit overrides ── */
.stSlider > div > div > div { background: var(--accent-blue) !important; }
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea textarea {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: var(--radius-sm) !important;
}
.stSelectbox > div > div {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
}
div[data-testid="stButton"] > button {
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(88,166,255,0.3) !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary) !important;
    border-bottom: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent-blue) !important;
}
</style>
"""

FINLEY_MASCOT_HTML = """
<div class="finley-wrapper" aria-hidden="true">
  <div class="finley-speech">💰 Plan smart!</div>
  <svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg" width="90">
    <!-- Body -->
    <ellipse cx="50" cy="75" rx="28" ry="32" fill="#58a6ff"/>
    <!-- Head -->
    <circle cx="50" cy="38" r="24" fill="#ffd97d"/>
    <!-- Eyes -->
    <circle cx="42" cy="34" r="4" fill="#1a1a1a"/>
    <circle cx="58" cy="34" r="4" fill="#1a1a1a"/>
    <!-- Eye shine -->
    <circle cx="44" cy="32" r="1.5" fill="white"/>
    <circle cx="60" cy="32" r="1.5" fill="white"/>
    <!-- Smile -->
    <path d="M 40 44 Q 50 52 60 44" stroke="#1a1a1a" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <!-- Blush -->
    <circle cx="36" cy="42" r="5" fill="#ffb3ba" opacity="0.6"/>
    <circle cx="64" cy="42" r="5" fill="#ffb3ba" opacity="0.6"/>
    <!-- Hair -->
    <ellipse cx="50" cy="16" rx="20" ry="10" fill="#1a6fb5"/>
    <!-- Tie -->
    <polygon points="50,63 44,70 50,80 56,70" fill="#3fb950"/>
    <!-- Coin bag right hand -->
    <ellipse cx="82" cy="80" rx="12" ry="11" fill="#d29922"/>
    <text x="82" y="84" text-anchor="middle" font-size="12" fill="white" font-weight="bold">₹</text>
    <!-- Arm right -->
    <line x1="78" y1="72" x2="82" y2="80" stroke="#ffd97d" stroke-width="6" stroke-linecap="round"/>
    <!-- Arm left -->
    <line x1="22" y1="72" x2="18" y2="80" stroke="#ffd97d" stroke-width="6" stroke-linecap="round"/>
    <!-- Legs -->
    <rect x="38" y="104" width="10" height="14" rx="5" fill="#1a6fb5"/>
    <rect x="52" y="104" width="10" height="14" rx="5" fill="#1a6fb5"/>
    <!-- Shoes -->
    <ellipse cx="43" cy="117" rx="8" ry="4" fill="#1a1a1a"/>
    <ellipse cx="57" cy="117" rx="8" ry="4" fill="#1a1a1a"/>
  </svg>
</div>
"""


def get_chart_layout() -> dict:
    """Base Plotly layout for all charts – dark fintech theme."""
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(28,35,51,0.6)",
        font=dict(family="Inter, sans-serif", color="#8b949e", size=11),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            linecolor="rgba(255,255,255,0.08)",
            tickfont=dict(size=10),
            showgrid=True,
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            linecolor="rgba(255,255,255,0.08)",
            tickfont=dict(size=10),
            showgrid=True,
        ),
        legend=dict(
            bgcolor="rgba(22,27,34,0.9)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            font=dict(size=10),
        ),
        margin=dict(l=10, r=10, t=30, b=10),
        hovermode="x unified",
    )
