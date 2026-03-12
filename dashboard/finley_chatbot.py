
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

from src.financial_engine import future_goal_value, required_sip
from src.monte_carlo import monte_carlo_simulation


# --------------------------------------------------
# INITIALIZE CHAT
# --------------------------------------------------

def initialize_chat():

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


# --------------------------------------------------
# MAIN CHAT FUNCTION
# --------------------------------------------------

def finley_chat(income, savings, goals=None):

    initialize_chat()

    st.markdown("### 🤖 Chat with Finley")

    user_input = st.chat_input("Ask Finley about your finances")

    if user_input:

        response = generate_response(user_input, income, savings, goals)

        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("assistant", response))

        # limit history size
        if len(st.session_state.chat_history) > 20:
            st.session_state.chat_history = st.session_state.chat_history[-20:]

    # display chat
    for role, msg in st.session_state.chat_history:

        with st.chat_message(role):
            st.write(msg)


# --------------------------------------------------
# FIND GOAL BY NAME
# --------------------------------------------------

def find_goal(question, goals):

    if not goals:
        return None

    q = question.lower()

    for g in goals:
        if g.get("name","").lower() in q:
            return g

    return goals[0]  # fallback


# --------------------------------------------------
# GENERATE RESPONSE
# --------------------------------------------------

def generate_response(question, income, savings, goals):

    q = question.lower()

    # -----------------------------------------
    # SAVINGS ADVICE
    # -----------------------------------------

    if "save" in q:

        rate = savings / income if income > 0 else 0

        return f"You currently save **{rate*100:.1f}%** of your income. Aim for at least **20%**."

    # -----------------------------------------
    # GOAL COUNT
    # -----------------------------------------

    if "goal" in q:

        if not goals:
            return "You have not added any goals yet."

        return f"You currently have **{len(goals)} financial goals.**"

    # -----------------------------------------
    # SIP CALCULATION
    # -----------------------------------------

    if "sip" in q or "invest" in q:

        if not goals:
            return "Please add a goal first so I can calculate SIP."

        g = find_goal(question, goals)

        future_cost = future_goal_value(
            g.get("cost",0),
            0.06,
            g.get("years",1)
        )

        sip = required_sip(
            future_cost,
            0.10,
            g.get("years",1)
        )

        return f"For goal **'{g.get('name')}'** you should invest about **₹{sip:,.0f} per month.**"

    # -----------------------------------------
    # PROBABILITY CALCULATION
    # -----------------------------------------

    if "probability" in q or "chance" in q:

        if not goals:
            return "Please add a goal first."

        g = find_goal(question, goals)

        future_cost = future_goal_value(
            g.get("cost",0),
            0.06,
            g.get("years",1)
        )

        sip = required_sip(
            future_cost,
            0.10,
            g.get("years",1)
        )

        try:

            mc = monte_carlo_simulation(
                sip,
                g.get("years",1),
                simulations=500
            )

            mc_values = pd.to_numeric(
                pd.Series(mc),
                errors="coerce"
            ).dropna()

            prob = (mc_values >= future_cost).mean()

            return f"The probability of achieving **'{g.get('name')}'** is about **{prob*100:.1f}%**."

        except:

            return "I couldn't calculate probability due to a simulation issue."

    # -----------------------------------------
    # GENERAL ADVICE
    # -----------------------------------------

    if "advice" in q or "plan" in q:

        rate = savings / income if income > 0 else 0

        if rate < 0.1:
            return "Your savings rate is low. Try saving **at least 20% of your income.**"

        if rate < 0.2:
            return "Good start! Increasing savings slightly will help you reach goals faster."

        return "Excellent savings discipline. Consider diversifying investments."

    # -----------------------------------------
    # DEFAULT
    # -----------------------------------------

    return """
You can ask me things like:

• How much should I save?  
• What SIP do I need for my goal?  
• What is the probability of achieving my goal?  
• Give me financial advice  
"""

