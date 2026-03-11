# dashboard/finley_chatbot.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from utils.goal_manager import get_goals
from utils.helpers import calculate_monthly_sip, format_currency, generate_insight
from src.scenario_simulator import simulate_delay
from src.monte_carlo import monte_carlo_simulation
from src.ai_advisor import generate_advice

def initialize_chat():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def finley_chat(income, savings, goals=None):
    initialize_chat()
    st.markdown("### 🤖 Chat with Finley")

    user_input = st.chat_input("Ask Finley anything about your finances")

    if user_input:
        response = generate_response(user_input, income, savings, goals)
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("assistant", response))

    # Display chat history
    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)

def generate_response(question, income, savings, goals):
    q = question.lower()
    matched_goal = None

    # Try to match a goal by name
    if goals:
        for g in goals:
            if g["name"].lower() in q:
                matched_goal = g
                break

    # Savings advice
    if "save" in q:
        rate = savings / income if income > 0 else 0
        return f"You currently save {rate*100:.1f}% of your income. Try to reach at least 20%."

    # Investment / SIP advice
    if "invest" in q or "sip" in q:
        if matched_goal:
            sip = calculate_monthly_sip(matched_goal['future_cost'], matched_goal['years'])
            return f"To achieve '{matched_goal['name']}', you should invest about {format_currency(sip)} per month."
        return "Please mention a goal to calculate SIP."

    # Delay advice
    if "delay" in q or "late" in q:
        if matched_goal:
            delay_res = simulate_delay(
                matched_goal["name"],
                matched_goal["future_cost"],
                matched_goal["years"],
                delay=1
            )
            return (
                f"If you delay '{matched_goal['name']}' by 1 year, your required SIP increases "
                f"from {format_currency(delay_res['sip_now'])} to {format_currency(delay_res['sip_delayed'])}."
            )
        return "Please mention a goal to simulate delay."

    # Probability / risk inquiry
    if "probability" in q or "chance" in q:
        if matched_goal:
            sip = calculate_monthly_sip(matched_goal['future_cost'], matched_goal['years'])
            mc = monte_carlo_simulation(sip, matched_goal['years'], simulations=500)
            success_prob = (pd.Series(mc) >= matched_goal['future_cost']).mean()
            return f"The probability of achieving '{matched_goal['name']}' is approximately {success_prob*100:.1f}%."
        return "Please mention a goal to calculate probability."

    # Advice inquiry
    if "advice" in q or "plan" in q:
        if matched_goal:
            sip = calculate_monthly_sip(matched_goal['future_cost'], matched_goal['years'])
            mc = monte_carlo_simulation(sip, matched_goal['years'], simulations=500)
            success_prob = (pd.Series(mc) >= matched_goal['future_cost']).mean()
            adv = generate_advice(matched_goal['name'], income, savings, sip, success_prob)
            return "\n".join(f"- {a}" for a in adv)
        return "Please mention a goal to get advice."

    return "That's a great question! Ask me about saving, investing, goal SIPs, probability, or planning advice."