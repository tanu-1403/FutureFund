import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px

from styles import load_styles
from ui_components import finley_intro
from finley_chatbot import finley_chat

from src.financial_engine import future_goal_value, required_sip
from src.projections import investment_projection
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

load_styles()
initialize_goals()

finley_intro()

st.title("🚀 FutureFund")
st.markdown("### Design Your Future. One Goal at a Time.")

# --------------------------------------------------
# CREATE 3 COLUMN LAYOUT (2 SIDEBARS SIMULATION)
# --------------------------------------------------

left, center, right = st.columns([1.1,2.5,1.1])


# --------------------------------------------------
# LEFT PANEL → GOAL NOTEBOOK
# --------------------------------------------------

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

    if st.button("Save Goal"):

        add_goal(goal_name,goal_cost,goal_years,note)

        st.success("Goal Saved")

    st.divider()

    st.subheader("📌 Saved Goals")

    display_sticky_goals()


# --------------------------------------------------
# RIGHT PANEL → PROFILE
# --------------------------------------------------

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


# --------------------------------------------------
# CENTER DASHBOARD
# --------------------------------------------------

with center:

    goals = get_goals()

    sip = 0   # 🔥 FINAL FIX FOR ERROR

    if len(goals) == 0:

        st.info("Add your first goal to start planning.")

    else:

        goal = goals[-1]

        future_value = future_goal_value(
            goal["cost"],
            inflation,
            goal["years"]
        )

        sip = required_sip(
            future_value,
            return_rate,
            goal["years"]
        )


        # -----------------------------
        # METRICS
        # -----------------------------

        c1,c2,c3 = st.columns(3)

        c1.metric(
            "Future Goal Cost",
            format_currency(future_value)
        )

        c2.metric(
            "Required SIP",
            format_currency(sip)
        )

        c3.metric(
            "Current Savings",
            format_currency(savings)
        )


        # -----------------------------
        # INVESTMENT GROWTH
        # -----------------------------

        portfolio = investment_projection(
            sip,
            return_rate,
            goal["years"]
        )

        df = pd.DataFrame({
            "Month":range(len(portfolio)),
            "Portfolio":portfolio
        })

        fig = px.line(
            df,
            x="Month",
            y="Portfolio",
            template="plotly_dark",
            title="Investment Growth"
        )

        st.plotly_chart(fig,use_container_width=True)


        # -----------------------------
        # MONTE CARLO
        # -----------------------------

        st.subheader("📊 Investment Simulation")

        mc = monte_carlo_simulation(
            sip,
            goal["years"]
        )

        mc_df = pd.DataFrame(mc,columns=["Final Value"])

        fig_mc = px.histogram(
            mc_df,
            x="Final Value",
            nbins=40,
            template="plotly_dark"
        )

        st.plotly_chart(fig_mc,use_container_width=True)

        probability = (mc_df["Final Value"]>=future_value).mean()

        st.metric(
            "Goal Success Probability",
            f"{probability*100:.1f}%"
        )


        # -----------------------------
        # LIFETIME WEALTH
        # -----------------------------

        st.subheader("📈 Lifetime Wealth Projection")

        life = simulate_life(income,savings)

        life_df = pd.DataFrame({
            "Year":range(len(life)),
            "Wealth":life
        })

        fig_life = px.line(
            life_df,
            x="Year",
            y="Wealth",
            template="plotly_dark"
        )

        st.plotly_chart(fig_life,use_container_width=True)


# --------------------------------------------------
# FINLEY CHATBOT
# --------------------------------------------------

st.divider()

finley_chat(income,savings,sip)