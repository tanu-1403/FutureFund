# dashboard_app.py

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
    get_goals,
    display_sticky_goals
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

# --------------------------------------------------
# LOAD STYLES
# --------------------------------------------------

load_styles()

# --------------------------------------------------
# INITIALIZE GOALS
# --------------------------------------------------

initialize_goals()

# --------------------------------------------------
# FINLEY INTRO
# --------------------------------------------------

finley_intro()

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("🚀 FutureFund")
st.markdown("### Design Your Future. One Goal at a Time.")

st.markdown(
"""
---
### 📊 Your Personal Financial Planning Dashboard
Track goals, simulate investments, and design your future wealth.
---
"""
)

# --------------------------------------------------
# CREATE 3 COLUMN LAYOUT
# --------------------------------------------------

left, center, right = st.columns([1.1, 2.5, 1.1])

# ==================================================
# LEFT PANEL → GOAL NOTEBOOK
# ==================================================

with left:

    st.header("🎯 Goal Notebook")

    goal_name = st.text_input("Goal Name")

    goal_cost = st.number_input(
        "Goal Cost",
        1000,
        100000000,
        100000
    )

    goal_years = st.slider(
        "Years",
        1,
        25,
        5
    )

    note = st.text_area("Notes")

    col1, col2 = st.columns(2)

    # ---- Save Goal ----
    if col1.button("Save Goal"):

        if goal_name.strip() == "":
            st.warning("Please enter a goal name.")

        else:
            add_goal(goal_name, goal_cost, goal_years, note)
            st.success("Goal Saved!")

    # ---- Save All Goals ----
    if col2.button("Save All Goals"):

        from utils.goal_manager import save_goals_to_file
        save_goals_to_file()

        st.success("Goals saved to goals.json")

    st.divider()

    st.subheader("📌 Saved Goals")

    goals_list = get_goals()

    if len(goals_list) == 0:
        st.info("No goals yet")

    for i, g in enumerate(goals_list):

        st.markdown(f"**{g['name']}**")
        st.write(f"Cost: ₹{g['cost']:,}")
        st.write(f"Years: {g['years']}")
        st.write(g["note"])

        edit_col, delete_col = st.columns(2)

        if edit_col.button("Edit", key=f"edit{i}"):

            st.session_state.edit_index = i
            st.session_state.edit_name = g["name"]
            st.session_state.edit_cost = g["cost"]
            st.session_state.edit_years = g["years"]
            st.session_state.edit_note = g["note"]

        if delete_col.button("Delete", key=f"del{i}"):

            from utils.goal_manager import delete_goal
            delete_goal(i)

            st.experimental_rerun()

        st.divider()

    # ---- Editing Section ----

    if "edit_index" in st.session_state:

        st.subheader("✏️ Edit Goal")

        idx = st.session_state.edit_index

        new_name = st.text_input(
            "Edit Name",
            value=st.session_state.edit_name
        )

        new_cost = st.number_input(
            "Edit Cost",
            1000,
            100000000,
            value=st.session_state.edit_cost
        )

        new_years = st.slider(
            "Edit Years",
            1,
            25,
            value=st.session_state.edit_years
        )

        new_note = st.text_area(
            "Edit Notes",
            value=st.session_state.edit_note
        )

        if st.button("Update Goal"):

            from utils.goal_manager import edit_goal

            edit_goal(
                idx,
                new_name,
                new_cost,
                new_years,
                new_note
            )

            for key in [
                "edit_index",
                "edit_name",
                "edit_cost",
                "edit_years",
                "edit_note"
            ]:
                st.session_state.pop(key)

            st.success("Goal Updated!")
            st.experimental_rerun()

# ==================================================
# RIGHT PANEL → USER PROFILE
# ==================================================

with right:

    st.header("👤 Profile")

    income = st.number_input(
        "Monthly Income",
        1000,
        500000,
        20000
    )

    savings = st.number_input(
        "Monthly Savings",
        500,
        200000,
        5000
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

    if len(get_goals()) > 0:
        score += 30

    if savings >= 0.2 * income:
        score += 30

    st.metric("Health Score", f"{score}/100")

    if score > 70:
        st.success("Excellent financial discipline!")
    elif score > 40:
        st.info("Good start. Improve savings rate.")
    else:
        st.warning("Consider increasing savings.")

# ==================================================
# CENTER PANEL → DASHBOARD
# ==================================================

with center:

    goals = get_goals()

    if len(goals) == 0:

        st.info("Add your first goal to start planning.")

    else:

        dashboard_data = []

        for g in goals:

            future_value = future_goal_value(
                g["cost"],
                inflation,
                g["years"]
            )

            sip = required_sip(
                future_value,
                return_rate,
                g["years"]
            )

            # ---- Monte Carlo Safety ----

            if sip > 0 and g["years"] > 0:

                mc = monte_carlo_simulation(
                    sip,
                    g["years"],
                    simulations=500
                )

                probability = (
                    pd.Series(mc) >= future_value
                ).mean()

            else:

                probability = 0

            g["future_cost"] = future_value
            g["required_sip"] = sip
            g["success_prob"] = probability

            dashboard_data.append({

                "Goal": g["name"],
                "Future Cost": future_value,
                "Required SIP": sip,
                "Probability": probability

            })

        df_goals = pd.DataFrame(dashboard_data)

        # --------------------------------------------------
        # GOALS TABLE
        # --------------------------------------------------

        st.subheader("📊 All Goals Overview")

        st.dataframe(

            df_goals.assign(

                **{

                    "Future Cost": lambda x:
                    x["Future Cost"].apply(format_currency),

                    "Required SIP": lambda x:
                    x["Required SIP"].apply(format_currency),

                    "Probability": lambda x:
                    (x["Probability"]*100).map("{:.1f}%".format)

                }

            ),

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

        fig_sip = px.bar(
            df_goals,
            x="Goal",
            y="Required SIP",
            template="plotly_dark",
            color="Required SIP",
            title="Monthly SIP Required per Goal"
        )

        st.plotly_chart(
            fig_sip,
            use_container_width=True
        )

        # --------------------------------------------------
        # SUCCESS PROBABILITY
        # --------------------------------------------------

        fig_prob = px.bar(
            df_goals,
            x="Goal",
            y="Probability",
            template="plotly_dark",
            color="Probability",
            title="Goal Success Probability"
        )

        st.plotly_chart(
            fig_prob,
            use_container_width=True
        )

        # --------------------------------------------------
        # LIFETIME WEALTH PROJECTION
        # --------------------------------------------------

        st.subheader("📈 Lifetime Wealth Projection")

        life = simulate_life(income, savings)

        life_df = pd.DataFrame({

            "Year": range(len(life)),
            "Wealth": life

        })

        fig_life = px.line(
            life_df,
            x="Year",
            y="Wealth",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_life,
            use_container_width=True
        )

# ==================================================
# FINLEY CHATBOT
# ==================================================

st.divider()

finley_chat(
    income,
    savings,
    goals=get_goals()
)