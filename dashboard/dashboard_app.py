
import sys
import os

# --------------------------------------------------
# ADD PROJECT ROOT TO PYTHON PATH
# --------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px

# ---- UI / Styles ----
from styles import load_styles
from ui_components import finley_intro
from finley_chatbot import finley_chat

# ---- Financial Modules ----
from src.financial_engine import future_goal_value, required_sip
from src.monte_carlo import monte_carlo_simulation
from src.life_simulator import simulate_life

from utils.goal_manager import (
    initialize_goals,
    add_goal,
    get_goals
)

from utils.helpers import format_currency

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="FutureFund",
    page_icon="💰",
    layout="wide"
)

load_styles()
initialize_goals()

# --------------------------------------------------
# FINLEY INTRO
# --------------------------------------------------

finley_intro()

st.title("🚀 FutureFund")
st.markdown("### Design Your Future. One Goal at a Time.")

# --------------------------------------------------
# CREATE 3 COLUMN LAYOUT
# --------------------------------------------------

left, center, right = st.columns([1.2, 2.8, 1.2])

# ==================================================
# LEFT PANEL → GOALS
# ==================================================

with left:

    st.header("🎯 Goal Notebook")

    goal_name = st.text_input("Goal Name")

    goal_cost = st.number_input(
        "Goal Cost",
        min_value=1000,
        max_value=100000000,
        value=100000
    )

    goal_years = st.slider(
        "Years",
        min_value=1,
        max_value=30,
        value=5
    )

    note = st.text_area("Notes")

    if st.button("Save Goal"):

        if goal_name.strip() == "":
            st.warning("Please enter a goal name")

        else:
            try:
                add_goal(goal_name, goal_cost, goal_years, note)
                st.success("Goal Saved!")
                st.rerun()
            except Exception as e:
                st.error(f"Could not save goal: {e}")

    st.divider()

    st.subheader("📌 Saved Goals")

    goals_list = get_goals()

    if not goals_list:
        st.info("No goals added yet")

    for g in goals_list:

        st.markdown(f"**{g.get('name','Unknown Goal')}**")
        st.write(f"Cost: ₹{g.get('cost',0):,}")
        st.write(f"Years: {g.get('years',0)}")
        st.write(g.get("note",""))
        st.divider()

# ==================================================
# RIGHT PANEL → USER PROFILE
# ==================================================

with right:

    st.header("👤 Profile")

    income = st.number_input(
        "Monthly Income",
        min_value=1000,
        max_value=500000,
        value=20000
    )

    savings = st.number_input(
        "Monthly Savings",
        min_value=500,
        max_value=200000,
        value=5000
    )

    inflation = st.slider(
        "Inflation Rate",
        0.02,
        0.10,
        0.06
    )

    return_rate = st.slider(
        "Expected Return",
        0.05,
        0.15,
        0.10
    )

    st.divider()

    # --------------------------------------------------
    # FINANCIAL HEALTH SCORE
    # --------------------------------------------------

    st.subheader("💡 Financial Health Score")

    savings_rate = savings / income if income > 0 else 0

    score = 0

    if savings_rate >= 0.20:
        score += 40
    elif savings_rate >= 0.10:
        score += 20

    if len(goals_list) > 0:
        score += 30

    if savings >= 0.2 * income:
        score += 30

    st.metric("Health Score", f"{score}/100")

    if score > 70:
        st.success("Excellent financial discipline")
    elif score > 40:
        st.info("Good start. Try increasing savings")
    else:
        st.warning("Consider improving your savings rate")

# ==================================================
# CENTER PANEL → DASHBOARD
# ==================================================

with center:

    goals = goals_list

    if not goals:

        st.info("Add a goal to start planning.")

    else:

        dashboard_data = []

        for g in goals:

            try:

                future_value = future_goal_value(
                    g.get("cost",0),
                    inflation,
                    g.get("years",1)
                )

                sip = required_sip(
                    future_value,
                    return_rate,
                    g.get("years",1)
                )

                mc = monte_carlo_simulation(
                    sip,
                    g.get("years",1),
                    simulations=500
                )

                mc_values = pd.to_numeric(pd.Series(mc), errors="coerce").dropna()

                probability = (
                    (mc_values >= future_value).mean()
                    if not mc_values.empty else 0
                )

                dashboard_data.append({

                    "Goal": g.get("name","Unknown"),
                    "Future Cost": future_value,
                    "Required SIP": sip,
                    "Probability": probability

                })

            except Exception as e:

                st.warning(f"Simulation failed for goal {g.get('name')}")

        df_goals = pd.DataFrame(dashboard_data)

        # --------------------------------------------------
        # GOALS TABLE
        # --------------------------------------------------

        st.subheader("📊 Goals Overview")

        st.dataframe(
            df_goals.style.format({
                "Future Cost": "₹{:,.0f}",
                "Required SIP": "₹{:,.0f}",
                "Probability": "{:.1%}"
            }),
            use_container_width=True
        )

        # --------------------------------------------------
        # TOTAL SIP METRIC
        # --------------------------------------------------

        total_sip = df_goals["Required SIP"].sum()

        st.metric(
            "Total Monthly SIP Needed",
            format_currency(total_sip)
        )

        # --------------------------------------------------
        # SIP BAR CHART
        # --------------------------------------------------

        fig = px.bar(
            df_goals,
            x="Goal",
            y="Required SIP",
            color="Required SIP",
            template="plotly_dark",
            title="Monthly SIP Needed per Goal"
        )

        st.plotly_chart(fig, use_container_width=True)

        # --------------------------------------------------
        # SUCCESS PROBABILITY
        # --------------------------------------------------

        fig_prob = px.bar(
            df_goals,
            x="Goal",
            y="Probability",
            color="Probability",
            template="plotly_dark",
            title="Goal Success Probability"
        )

        st.plotly_chart(fig_prob, use_container_width=True)

        # --------------------------------------------------
        # LIFETIME WEALTH PROJECTION
        # --------------------------------------------------

        st.subheader("📈 Lifetime Wealth Projection")

        try:

            life = simulate_life(income, savings)

            life_df = pd.DataFrame({
                "Year": range(len(life)),
                "Wealth": life
            })

            fig_life = px.line(
                life_df,
                x="Year",
                y="Wealth",
                template="plotly_dark",
                title="Future Wealth Growth"
            )

            st.plotly_chart(fig_life, use_container_width=True)

        except Exception as e:

            st.warning("Could not generate life projection")

# ==================================================
# FINLEY CHATBOT
# ==================================================

st.divider()

finley_chat(
    income,
    savings,
    goals=goals_list
)

