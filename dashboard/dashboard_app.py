"""
FutureFund – Main Dashboard
Life-path financial simulator | Streamlit app entry point

Run with:
    streamlit run dashboard/dashboard_app.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from dashboard.styles        import MAIN_CSS, FINLEY_MASCOT_HTML, get_chart_layout
from dashboard.ui_components import (
    render_metric_card, render_kpi_row, section_header,
    goal_sticky_note, probability_badge, gauge_bar,
    render_hero_bar, empty_state,
)
from dashboard.finley_chatbot import FinleyBot
from src.financial_engine    import future_value, required_sip, sip_future_value, affordability_score
from src.projections         import build_growth_projection
from src.monte_carlo         import run_monte_carlo, monte_carlo_distribution_data
from src.life_simulator      import simulate_lifetime_wealth
from utils.goal_manager      import (
    make_goal, add_goal, remove_goal, total_sip_required,
    sort_goals, GOAL_ICONS, PRIORITY_COLORS,
)
from utils.helpers import fmt_inr, fmt_pct, probability_label

# ─────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FutureFund – Life-Path Financial Simulator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject CSS
st.markdown(MAIN_CSS, unsafe_allow_html=True)
st.markdown(FINLEY_MASCOT_HTML, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Session State init
# ─────────────────────────────────────────────────────────────
if "goals"        not in st.session_state: st.session_state.goals        = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "finley_bot"   not in st.session_state: st.session_state.finley_bot   = FinleyBot()
if "active_goal"  not in st.session_state: st.session_state.active_goal  = None
if "profile"      not in st.session_state:
    st.session_state.profile = {
        "monthly_income":  80000,
        "monthly_savings": 20000,
        "current_savings": 200000,
        "current_age":     28,
        "inflation_rate":  6.0,
        "annual_return":   12.0,
        "risk_profile":    "Moderate",
    }

# ─────────────────────────────────────────────────────────────
# Derived values
# ─────────────────────────────────────────────────────────────
profile   = st.session_state.profile
goals     = st.session_state.goals
inf_rate  = profile["inflation_rate"]
ret_rate  = profile["annual_return"]

total_sip = total_sip_required(goals, ret_rate, inf_rate)
selected  = st.session_state.active_goal or (goals[0] if goals else None)

# Active goal derived values
if selected:
    fv_selected  = future_value(selected["cost"], inf_rate, selected["years"])
    sip_selected = required_sip(fv_selected, ret_rate, selected["years"])
    afford       = affordability_score(sip_selected, profile["monthly_savings"], profile["monthly_income"])
else:
    fv_selected  = 0.0
    sip_selected = 0.0
    afford       = {"score": 0, "label": "No Goal", "color": "#888"}

# ─────────────────────────────────────────────────────────────
# Hero bar
# ─────────────────────────────────────────────────────────────
render_hero_bar(len(goals), total_sip, profile["monthly_savings"])

# ─────────────────────────────────────────────────────────────
# Three-column layout
# ─────────────────────────────────────────────────────────────
left_col, center_col, right_col = st.columns([1.1, 2.5, 1.1], gap="small")


# ═══════════════════════════════════════════════════════════════
# LEFT PANEL — Goal Notebook
# ═══════════════════════════════════════════════════════════════
with left_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    section_header("📒", "Goal Notebook")

    # ── Add Goal Form ──
    with st.expander("➕ Add New Goal", expanded=not bool(goals)):
        with st.form("goal_form", clear_on_submit=True):
            g_name     = st.text_input("Goal Name", placeholder="e.g. Dream Car")
            g_category = st.selectbox("Category", list(GOAL_ICONS.keys()), format_func=lambda x: f"{GOAL_ICONS[x]} {x.title()}")
            g_cost     = st.number_input("Current Cost (₹)", min_value=1000, value=500000, step=10000)
            g_years    = st.slider("Years to Goal", 1, 40, 5)
            g_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            g_notes    = st.text_area("Personal Notes", placeholder="Why this goal matters...", height=60)
            submitted  = st.form_submit_button("💾 Save Goal", use_container_width=True)

            if submitted and g_name.strip():
                new_goal = make_goal(g_name, g_cost, g_years, g_category, g_notes, g_priority)
                st.session_state.goals = add_goal(st.session_state.goals, new_goal)
                st.session_state.active_goal = new_goal
                st.success(f"Goal '{g_name}' added!")
                st.rerun()

    st.markdown('<div class="ff-divider"></div>', unsafe_allow_html=True)

    # ── Goal Cards ──
    if not goals:
        empty_state("🎯", "No goals yet", "Add your first financial goal above!")
    else:
        sorted_goals = sort_goals(goals, by="years")
        for g in sorted_goals:
            fv  = future_value(g["cost"], inf_rate, g["years"])
            sip = required_sip(fv, ret_rate, g["years"])
            st.markdown(goal_sticky_note(g, fv, sip), unsafe_allow_html=True)

            col_sel, col_del = st.columns([3, 1])
            with col_sel:
                if st.button(f"📊 Analyze", key=f"sel_{g['id']}", use_container_width=True):
                    st.session_state.active_goal = g
                    st.rerun()
            with col_del:
                if st.button("🗑️", key=f"del_{g['id']}", use_container_width=True, help="Delete goal"):
                    st.session_state.goals = remove_goal(st.session_state.goals, g["id"])
                    if st.session_state.active_goal and st.session_state.active_goal.get("id") == g["id"]:
                        st.session_state.active_goal = None
                    st.rerun()

    # ── Total SIP Summary ──
    if goals:
        st.markdown('<div class="ff-divider"></div>', unsafe_allow_html=True)
        remaining = profile["monthly_savings"] - total_sip
        color = "#3fb950" if remaining >= 0 else "#f85149"
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Total Monthly SIP Needed</div>
          <div class="metric-value gold">{fmt_inr(total_sip)}</div>
          <div class="metric-sub" style="color:{color};">
            {'✅' if remaining >= 0 else '⚠️'} {fmt_inr(abs(remaining))} {'surplus' if remaining >= 0 else 'shortfall'} vs savings
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close panel


# ═══════════════════════════════════════════════════════════════
# CENTER PANEL — Dashboard Visualizations
# ═══════════════════════════════════════════════════════════════
with center_col:
    if not selected:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        empty_state("💰", "Welcome to FutureFund!", "Add a goal on the left to see your financial projections.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # ── Goal selector tabs ──
        goal_names = [f"{g['icon']} {g['name']}" for g in goals]
        sel_idx = goals.index(selected) if selected in goals else 0
        goal_tab = st.radio("Active Goal", goal_names, index=sel_idx, horizontal=True, label_visibility="collapsed")
        selected = goals[goal_names.index(goal_tab)] if goal_tab in goal_names else selected
        st.session_state.active_goal = selected

        fv_selected  = future_value(selected["cost"], inf_rate, selected["years"])
        sip_selected = required_sip(fv_selected, ret_rate, selected["years"])
        afford       = affordability_score(sip_selected, profile["monthly_savings"], profile["monthly_income"])

        # ── KPI Row ──
        render_kpi_row([
            {"label": "Today's Cost",    "value": fmt_inr(selected["cost"], short=True), "color": "#8b949e"},
            {"label": "Future Cost",     "value": fmt_inr(fv_selected, short=True),      "color": "#d29922"},
            {"label": "Monthly SIP",     "value": fmt_inr(sip_selected, short=True),     "color": "#58a6ff"},
            {"label": "Time Horizon",    "value": f"{selected['years']} yrs",            "color": "#bc8cff"},
            {"label": "Affordability",   "value": afford["label"],                       "color": afford["color"]},
        ])

        # ── Tabs ──
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Growth Chart", "🎲 Monte Carlo", "🌍 Lifetime Wealth", "📋 Goal Summary"])

        # ════════════════════════
        # TAB 1 – Investment Growth
        # ════════════════════════
        with tab1:
            df = build_growth_projection(sip_selected, ret_rate, selected["years"], fv_selected)

            fig = go.Figure()
            # Area fill: gains
            fig.add_trace(go.Scatter(
                x=df["year"], y=df["portfolio_value"],
                name="Portfolio Value",
                fill="tonexty",
                line=dict(color="#58a6ff", width=2.5),
                fillcolor="rgba(88,166,255,0.15)",
                hovertemplate="Year %{x:.1f}<br>Portfolio: ₹%{y:,.0f}<extra></extra>",
            ))
            fig.add_trace(go.Scatter(
                x=df["year"], y=df["invested"],
                name="Amount Invested",
                line=dict(color="#3fb950", width=2, dash="dot"),
                fillcolor="rgba(63,185,80,0.08)",
                fill="tozeroy",
                hovertemplate="Year %{x:.1f}<br>Invested: ₹%{y:,.0f}<extra></extra>",
            ))
            fig.add_trace(go.Scatter(
                x=df["year"], y=df["goal_line"],
                name="Goal Target",
                line=dict(color="#f85149", width=1.5, dash="dash"),
                hovertemplate="Goal: ₹%{y:,.0f}<extra></extra>",
            ))
            layout = get_chart_layout()
            layout.update(
                title=dict(text=f"Investment Growth – {selected['name']}", font=dict(size=13, color="#c9d1d9")),
                xaxis_title="Years",
                yaxis_title="Value (₹)",
                height=320,
            )
            fig.update_layout(**layout)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            # Gains breakdown
            final = df.iloc[-1]
            total_inv = final["invested"]
            total_val = final["portfolio_value"]
            gains     = final["gains"]
            st.markdown(f"""
            <div style="display:flex;gap:0.75rem;margin-top:0.25rem;">
              <div class="kpi-item" style="flex:1;">
                <div class="kpi-num" style="color:#3fb950;">{fmt_inr(total_inv, short=True)}</div>
                <div class="kpi-lbl">Total Invested</div>
              </div>
              <div class="kpi-item" style="flex:1;">
                <div class="kpi-num" style="color:#58a6ff;">{fmt_inr(gains, short=True)}</div>
                <div class="kpi-lbl">Gains from Returns</div>
              </div>
              <div class="kpi-item" style="flex:1;">
                <div class="kpi-num" style="color:#d29922;">{fmt_inr(total_val, short=True)}</div>
                <div class="kpi-lbl">Final Value</div>
              </div>
              <div class="kpi-item" style="flex:1;">
                <div class="kpi-num" style="color:#bc8cff;">{(gains/total_inv*100):.0f}%</div>
                <div class="kpi-lbl">Return on Investment</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # ════════════════════════
        # TAB 2 – Monte Carlo
        # ════════════════════════
        with tab2:
            mc_col1, mc_col2 = st.columns([2, 1])
            with mc_col2:
                n_sims    = st.select_slider("Simulations", [500, 1000, 2000, 5000], value=1000)
                volatility = st.slider("Market Volatility (%)", 4.0, 20.0, 8.0, 0.5,
                                       help="Annual std dev of returns")

            mc = run_monte_carlo(
                monthly_sip=sip_selected,
                mean_return=ret_rate,
                years=selected["years"],
                goal_target=fv_selected,
                n_simulations=n_sims,
                volatility=volatility,
            )

            with mc_col1:
                # Distribution histogram
                dist_df = monte_carlo_distribution_data(mc)
                fig2 = go.Figure()
                fig2.add_trace(go.Histogram(
                    x=dist_df[dist_df["meets_goal"]]["final_value"],
                    name="Meets Goal ✅",
                    nbinsx=50,
                    marker_color="rgba(63,185,80,0.7)",
                    hovertemplate="Value: ₹%{x:,.0f}<br>Count: %{y}<extra></extra>",
                ))
                fig2.add_trace(go.Histogram(
                    x=dist_df[~dist_df["meets_goal"]]["final_value"],
                    name="Below Goal ❌",
                    nbinsx=50,
                    marker_color="rgba(248,81,73,0.6)",
                    hovertemplate="Value: ₹%{x:,.0f}<br>Count: %{y}<extra></extra>",
                ))
                fig2.add_vline(x=fv_selected, line_color="#f85149", line_dash="dash",
                               annotation_text="Goal", annotation_font_color="#f85149")
                fig2.add_vline(x=mc["percentiles"]["p50"], line_color="#d29922", line_dash="dot",
                               annotation_text="Median", annotation_font_color="#d29922")
                layout2 = get_chart_layout()
                layout2.update(
                    title=dict(text=f"Monte Carlo – {n_sims} Simulations", font=dict(size=13, color="#c9d1d9")),
                    xaxis_title="Final Portfolio Value (₹)",
                    yaxis_title="Frequency",
                    barmode="overlay",
                    height=290,
                )
                fig2.update_layout(**layout2)
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

            # Probability + percentiles
            st.markdown(probability_badge(mc["probability"]), unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            p = mc["percentiles"]
            st.markdown(f"""
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-top:0.4rem;">
              {"".join(f'''
              <div class="kpi-item" style="flex:1;min-width:80px;">
                <div class="kpi-num" style="font-size:0.9rem;color:#8b949e;">{fmt_inr(p[k], short=True)}</div>
                <div class="kpi-lbl">{k.upper()}</div>
              </div>''' for k in ["p10","p25","p50","p75","p90"])}
            </div>
            """, unsafe_allow_html=True)
            st.caption("⚠️ Monte Carlo results are illustrative. Not investment advice.")

        # ════════════════════════
        # TAB 3 – Lifetime Wealth
        # ════════════════════════
        with tab3:
            goal_withdrawals = [
                {"year_from_now": g["years"], "amount": future_value(g["cost"], inf_rate, g["years"])}
                for g in goals
            ]
            life_df = simulate_lifetime_wealth(
                current_age    = profile["current_age"],
                current_savings= profile["current_savings"],
                monthly_income = profile["monthly_income"],
                annual_return  = ret_rate,
                inflation_rate = inf_rate,
                goal_withdrawals=goal_withdrawals,
            )

            fig3 = go.Figure()

            # Shade by phase
            phase_colors = {
                "Early Career":   "rgba(88,166,255,0.07)",
                "Growth Phase":   "rgba(63,185,80,0.07)",
                "Peak Earnings":  "rgba(188,140,255,0.07)",
                "Pre-Retirement": "rgba(210,153,34,0.07)",
                "Retirement":     "rgba(248,81,73,0.07)",
            }
            for phase, color in phase_colors.items():
                phase_data = life_df[life_df["phase"] == phase]
                if not phase_data.empty:
                    fig3.add_vrect(
                        x0=phase_data["age"].min(),
                        x1=phase_data["age"].max(),
                        fillcolor=color, layer="below", line_width=0,
                        annotation_text=phase.split()[0],
                        annotation_font=dict(size=9, color="#8b949e"),
                        annotation_position="top left",
                    )

            fig3.add_trace(go.Scatter(
                x=life_df["age"], y=life_df["net_worth"],
                name="Net Worth",
                fill="tozeroy",
                line=dict(color="#bc8cff", width=2.5),
                fillcolor="rgba(188,140,255,0.12)",
                hovertemplate="Age %{x}<br>Net Worth: ₹%{y:,.0f}<extra></extra>",
            ))

            # Mark goal years
            for g in goals:
                target_age = profile["current_age"] + g["years"]
                if target_age <= 85:
                    fig3.add_vline(
                        x=target_age,
                        line_color="#d29922", line_dash="dot", line_width=1,
                        annotation_text=g["icon"],
                        annotation_font=dict(size=12),
                        annotation_position="top",
                    )

            layout3 = get_chart_layout()
            layout3.update(
                title=dict(text="Lifetime Wealth Journey", font=dict(size=13, color="#c9d1d9")),
                xaxis_title="Age",
                yaxis_title="Net Worth (₹)",
                height=330,
            )
            fig3.update_layout(**layout3)
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

            # Peak wealth stat
            peak = life_df["net_worth"].max()
            peak_age = life_df.loc[life_df["net_worth"].idxmax(), "age"]
            retirement_wealth = life_df[life_df["age"] == 65]["net_worth"].values
            ret_wealth_val = retirement_wealth[0] if len(retirement_wealth) > 0 else 0

            st.markdown(f"""
            <div style="display:flex;gap:0.75rem;margin-top:0.25rem;">
              <div class="kpi-item" style="flex:1;">
                <div class="kpi-num" style="color:#bc8cff;">{fmt_inr(peak, short=True)}</div>
                <div class="kpi-lbl">Peak Net Worth</div>
              </div>
              <div class="kpi-item" style="flex:1;">
                <div class="kpi-num" style="color:#58a6ff;">{peak_age}</div>
                <div class="kpi-lbl">Peak Age</div>
              </div>
              <div class="kpi-item" style="flex:1;">
                <div class="kpi-num" style="color:#d29922;">{fmt_inr(ret_wealth_val, short=True)}</div>
                <div class="kpi-lbl">At Retirement (65)</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # ════════════════════════
        # TAB 4 – Goal Summary
        # ════════════════════════
        with tab4:
            if goals:
                rows = []
                for g in goals:
                    fv  = future_value(g["cost"], inf_rate, g["years"])
                    sip = required_sip(fv, ret_rate, g["years"])
                    aff = affordability_score(sip, profile["monthly_savings"], profile["monthly_income"])
                    rows.append({
                        "Goal": f"{g['icon']} {g['name']}",
                        "Current Cost": fmt_inr(g["cost"]),
                        "Years Away": g["years"],
                        "Inflation-Adj Cost": fmt_inr(fv),
                        "Monthly SIP": fmt_inr(sip),
                        "Priority": g["priority"],
                        "Affordability": aff["label"],
                    })
                df_goals = pd.DataFrame(rows)
                st.dataframe(
                    df_goals,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Goal":              st.column_config.TextColumn(width="medium"),
                        "Monthly SIP":       st.column_config.TextColumn("Monthly SIP 💰"),
                        "Affordability":     st.column_config.TextColumn("Status"),
                        "Years Away":        st.column_config.NumberColumn(format="%d yrs"),
                    },
                )

                # SIP pie chart
                sip_values = []
                sip_names  = []
                for g in goals:
                    fv_  = future_value(g["cost"], inf_rate, g["years"])
                    sip_ = required_sip(fv_, ret_rate, g["years"])
                    if sip_ > 0:
                        sip_values.append(sip_)
                        sip_names.append(f"{g['icon']} {g['name']}")

                if sip_values:
                    fig_pie = go.Figure(go.Pie(
                        values=sip_values,
                        labels=sip_names,
                        hole=0.55,
                        marker=dict(colors=["#58a6ff","#3fb950","#d29922","#bc8cff","#f85149","#79c0ff"]),
                        textinfo="label+percent",
                        textfont=dict(size=10),
                    ))
                    layout_pie = get_chart_layout()
                    layout_pie.update(
                        title=dict(text="SIP Allocation by Goal", font=dict(size=12, color="#c9d1d9")),
                        showlegend=False,
                        height=260,
                        margin=dict(l=10,r=10,t=40,b=10),
                    )
                    fig_pie.update_layout(**layout_pie)
                    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
            else:
                empty_state("📋", "No goals to summarise", "Add goals in the Goal Notebook!")

    # ── Finley Chatbot ──────────────────────────────────────────────────────
    st.markdown('<div class="ff-divider"></div>', unsafe_allow_html=True)
    section_header("🤖", "Ask Finley")

    # Update Finley's context
    bot = st.session_state.finley_bot
    bot.update_context(profile, goals)

    # Display chat history
    if not st.session_state.chat_history:
        st.session_state.chat_history.append({
            "role": "finley",
            "msg": "Hey! 👋 I'm **Finley**, your AI finance buddy! Ask me anything about saving, goals, SIPs, or investing. What's on your mind?",
        })

    chat_html = '<div class="chat-messages">'
    for entry in st.session_state.chat_history[-8:]:
        if entry["role"] == "user":
            chat_html += f'<div class="chat-bubble-user">{entry["msg"]}</div>'
        else:
            chat_html += f'<div class="chat-bubble-finley">{entry["msg"]}</div>'
    chat_html += "</div>"
    st.markdown(f'<div class="chat-container"><div class="chat-header">🤖 Finley AI Assistant · <span style="color:#3fb950;font-size:0.7rem;">● Online</span></div>{chat_html}</div>', unsafe_allow_html=True)

    # Input
    chat_col1, chat_col2 = st.columns([4, 1])
    with chat_col1:
        user_input = st.text_input(
            "Ask Finley",
            placeholder="e.g. How much should I save? Can I afford a house?",
            label_visibility="collapsed",
            key="chat_input",
        )
    with chat_col2:
        send = st.button("Send 🚀", use_container_width=True)

    if send and user_input.strip():
        response = bot.respond(user_input)
        st.session_state.chat_history.append({"role": "user",   "msg": user_input})
        st.session_state.chat_history.append({"role": "finley", "msg": response})
        st.rerun()

    # Quick prompts
    st.markdown('<div style="display:flex;gap:0.4rem;flex-wrap:wrap;margin-top:0.4rem;">', unsafe_allow_html=True)
    quick_prompts = ["How much should I save?", "Can I afford a car?", "What is SIP?", "Tell me about inflation", "When can I retire?"]
    qp_cols = st.columns(len(quick_prompts))
    for i, (col, prompt) in enumerate(zip(qp_cols, quick_prompts)):
        with col:
            if st.button(prompt, key=f"qp_{i}", use_container_width=True):
                response = bot.respond(prompt)
                st.session_state.chat_history.append({"role": "user",   "msg": prompt})
                st.session_state.chat_history.append({"role": "finley", "msg": response})
                st.rerun()


# ═══════════════════════════════════════════════════════════════
# RIGHT PANEL — User Profile
# ═══════════════════════════════════════════════════════════════
with right_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    section_header("👤", "Your Profile")

    with st.form("profile_form"):
        st.markdown("**💼 Income & Savings**")
        monthly_income  = st.number_input("Monthly Income (₹)",  min_value=0, value=profile["monthly_income"],  step=5000, help="Take-home income per month")
        monthly_savings = st.number_input("Monthly Savings (₹)", min_value=0, value=profile["monthly_savings"], step=1000, help="Amount you can invest monthly")
        current_savings = st.number_input("Existing Savings (₹)", min_value=0, value=profile["current_savings"], step=10000, help="Total current investments/savings")

        st.markdown('<div class="ff-divider"></div>', unsafe_allow_html=True)
        st.markdown("**🎂 Personal**")
        current_age = st.slider("Current Age", 18, 65, profile["current_age"])
        risk_profile = st.selectbox("Risk Profile", ["Conservative", "Moderate", "Aggressive"],
                                    index=["Conservative", "Moderate", "Aggressive"].index(profile["risk_profile"]))

        st.markdown('<div class="ff-divider"></div>', unsafe_allow_html=True)
        st.markdown("**📊 Assumptions**")
        inflation_rate = st.slider("Inflation Rate (%)", 3.0, 12.0, profile["inflation_rate"], 0.5,
                                   help="Average annual price rise")

        # Auto-suggest return based on risk
        return_defaults = {"Conservative": 8.0, "Moderate": 12.0, "Aggressive": 15.0}
        default_return  = return_defaults.get(risk_profile, 12.0)
        annual_return   = st.slider("Expected Return (%)", 5.0, 20.0, default_return, 0.5,
                                    help="Annual investment return assumption")

        save_btn = st.form_submit_button("💾 Update Profile", use_container_width=True)
        if save_btn:
            st.session_state.profile = {
                "monthly_income":  monthly_income,
                "monthly_savings": monthly_savings,
                "current_savings": current_savings,
                "current_age":     current_age,
                "inflation_rate":  inflation_rate,
                "annual_return":   annual_return,
                "risk_profile":    risk_profile,
            }
            st.success("Profile updated!")
            st.rerun()

    st.markdown('<div class="ff-divider"></div>', unsafe_allow_html=True)

    # ── Financial Health Card ──
    section_header("❤️", "Financial Health")

    savings_rate_val = (profile["monthly_savings"] / profile["monthly_income"] * 100) if profile["monthly_income"] > 0 else 0
    sip_coverage     = (profile["monthly_savings"] / total_sip * 100) if total_sip > 0 else 100

    gauge_bar("Savings Rate", profile["monthly_savings"], profile["monthly_income"], "#3fb950")
    st.caption(f"Savings rate: {savings_rate_val:.1f}% (target: ≥20%)")

    if total_sip > 0:
        gauge_bar("SIP Coverage", min(profile["monthly_savings"], total_sip), total_sip, "#58a6ff")
        st.caption(f"Goal SIP coverage: {min(sip_coverage, 100):.0f}%")

    # Health scores
    scores = []
    if savings_rate_val >= 20:
        scores.append(("✅ Savings Rate", "#3fb950", "Great discipline"))
    elif savings_rate_val >= 10:
        scores.append(("⚠️ Savings Rate", "#d29922", "Could be higher"))
    else:
        scores.append(("🔴 Savings Rate", "#f85149", "Below 10% — critical"))

    real_return = profile["annual_return"] - profile["inflation_rate"]
    if real_return >= 5:
        scores.append(("✅ Real Return",   "#3fb950", f"+{real_return:.1f}% real p.a."))
    elif real_return >= 2:
        scores.append(("⚠️ Real Return",   "#d29922", f"+{real_return:.1f}% real p.a."))
    else:
        scores.append(("🔴 Real Return",   "#f85149", "Return barely beats inflation"))

    for icon_label, color, desc in scores:
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
                    padding:0.35rem 0.6rem;background:{color}12;
                    border-left:3px solid {color};border-radius:0 6px 6px 0;
                    margin-bottom:0.35rem;">
          <span style="font-size:0.75rem;font-weight:600;">{icon_label}</span>
          <span style="font-size:0.65rem;color:#8b949e;">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Rule of 72 ──
    st.markdown('<div class="ff-divider"></div>', unsafe_allow_html=True)
    double_years = round(72 / profile["annual_return"], 1) if profile["annual_return"] > 0 else "∞"
    half_years   = round(70 / profile["inflation_rate"], 1) if profile["inflation_rate"] > 0 else "∞"

    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">Rule of 72 — Money Doubles In</div>
      <div class="metric-value blue">{double_years} years</div>
      <div class="metric-sub">At {profile['annual_return']}% return</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Rule of 70 — Purchasing Power Halves In</div>
      <div class="metric-value gold">{half_years} years</div>
      <div class="metric-sub">At {profile['inflation_rate']}% inflation</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Disclaimer ──
    st.markdown('<div class="ff-divider"></div>', unsafe_allow_html=True)
    st.caption("⚠️ FutureFund is for educational purposes only. Not financial advice. Consult a SEBI-registered advisor before investing.")

    st.markdown('</div>', unsafe_allow_html=True)  # close panel
