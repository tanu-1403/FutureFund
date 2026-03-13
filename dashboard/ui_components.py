"""
FutureFund – UI Components
Reusable HTML/Streamlit component builders.
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from utils.helpers import fmt_inr, fmt_pct, probability_label
from utils.goal_manager import PRIORITY_COLORS


# ── Metric card ────────────────────────────────────────────────────────────

def metric_card(label: str, value: str, sub: str = "", color_class: str = "") -> str:
    return f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value {color_class}">{value}</div>
      {'<div class="metric-sub">' + sub + '</div>' if sub else ''}
    </div>
    """


def render_metric_card(label, value, sub="", color_class=""):
    st.markdown(metric_card(label, value, sub, color_class), unsafe_allow_html=True)


# ── KPI Row ────────────────────────────────────────────────────────────────

def render_kpi_row(items: list[dict]):
    """items: list of {label, value, color}"""
    html = '<div class="kpi-row">'
    for item in items:
        color = item.get("color", "#e6edf3")
        html += f"""
        <div class="kpi-item">
          <div class="kpi-num" style="color:{color}">{item['value']}</div>
          <div class="kpi-lbl">{item['label']}</div>
        </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ── Section header ─────────────────────────────────────────────────────────

def section_header(icon: str, title: str):
    st.markdown(
        f'<div class="section-header">{icon} {title}</div>',
        unsafe_allow_html=True,
    )


# ── Goal sticky note ───────────────────────────────────────────────────────

def goal_sticky_note(goal: dict, fv: float, sip: float) -> str:
    pri_color = PRIORITY_COLORS.get(goal.get("priority", "Medium"), "#ffa502")
    notes_html = (
        f'<div class="goal-note-notes">💬 {goal["notes"]}</div>'
        if goal.get("notes") else ""
    )
    return f"""
    <div class="goal-note">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;">
        <div>
          <div class="goal-note-title">{goal['icon']} {goal['name']}</div>
          <div class="goal-note-meta">🗓️ {goal['years']} yrs away · Added {goal['created_at']}</div>
        </div>
        <span class="priority-badge" style="background:{pri_color}22;color:{pri_color};border:1px solid {pri_color}44;">
          {goal['priority']}
        </span>
      </div>
      <div class="ff-divider" style="background:#d9770640;"></div>
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <div>
          <div style="font-size:0.65rem;color:#6b6b6b;font-weight:600;">TODAY'S COST</div>
          <div class="goal-note-cost">{fmt_inr(goal['cost'])}</div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:0.65rem;color:#6b6b6b;font-weight:600;">FUTURE COST</div>
          <div style="font-weight:700;font-size:0.95rem;color:#92400e;">{fmt_inr(fv)}</div>
        </div>
      </div>
      <div style="background:#d9770620;border-radius:6px;padding:0.4rem 0.6rem;margin-top:0.5rem;">
        <span style="font-size:0.7rem;font-weight:700;color:#92400e;">SIP Required: {fmt_inr(sip)}/mo</span>
      </div>
      {notes_html}
    </div>
    """


# ── Probability badge ─────────────────────────────────────────────────────

def probability_badge(prob: float) -> str:
    label, color = probability_label(prob)
    return f"""
    <div style="display:inline-flex;align-items:center;gap:0.5rem;
                background:{color}18;border:1px solid {color}44;
                border-radius:8px;padding:0.5rem 1rem;">
      <div style="font-size:1.6rem;font-weight:800;color:{color}">{prob:.0f}%</div>
      <div>
        <div style="font-size:0.65rem;color:#8b949e;font-weight:600;text-transform:uppercase;">Probability</div>
        <div style="font-size:0.75rem;font-weight:700;color:{color}">{label}</div>
      </div>
    </div>
    """


# ── Gauge bar ──────────────────────────────────────────────────────────────

def gauge_bar(label: str, value: float, max_val: float, color: str = "#58a6ff"):
    pct = min(100, (value / max_val * 100)) if max_val > 0 else 0
    st.markdown(f"""
    <div style="margin-bottom:0.6rem;">
      <div style="display:flex;justify-content:space-between;font-size:0.72rem;margin-bottom:0.2rem;">
        <span style="color:#8b949e;">{label}</span>
        <span style="color:#e6edf3;font-weight:600;">{fmt_inr(value)}</span>
      </div>
      <div class="gauge-bar">
        <div class="gauge-fill" style="width:{pct:.1f}%;background:{color};"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Hero bar ───────────────────────────────────────────────────────────────

def render_hero_bar(total_goals: int, total_sip: float, savings: float):
    can_cover = savings >= total_sip
    status_color = "#3fb950" if can_cover else "#f85149"
    status_text  = "On Track" if can_cover else "Needs Attention"
    st.markdown(f"""
    <div class="hero-bar">
      <div>
        <div class="hero-title">FutureFund</div>
        <div class="hero-sub">Your life-path financial simulator</div>
      </div>
      <div style="display:flex;gap:2rem;align-items:center;">
        <div style="text-align:center;">
          <div style="font-size:1.4rem;font-weight:800;color:#58a6ff;">{total_goals}</div>
          <div style="font-size:0.65rem;color:#8b949e;text-transform:uppercase;letter-spacing:.05em;">Goals</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:1.4rem;font-weight:800;color:#d29922;">{fmt_inr(total_sip, short=True)}</div>
          <div style="font-size:0.65rem;color:#8b949e;text-transform:uppercase;letter-spacing:.05em;">Total SIP/mo</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:1.1rem;font-weight:700;color:{status_color};">● {status_text}</div>
          <div style="font-size:0.65rem;color:#8b949e;">Budget Health</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Empty state ───────────────────────────────────────────────────────────

def empty_state(icon: str, message: str, sub: str = ""):
    st.markdown(f"""
    <div style="text-align:center;padding:2rem 1rem;color:#8b949e;">
      <div style="font-size:2.5rem;margin-bottom:0.5rem;">{icon}</div>
      <div style="font-size:0.9rem;font-weight:600;color:#c9d1d9;">{message}</div>
      {'<div style="font-size:0.75rem;margin-top:0.25rem;">' + sub + '</div>' if sub else ''}
    </div>
    """, unsafe_allow_html=True)
