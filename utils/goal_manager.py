import streamlit as st
import json
import os

# -----------------------
# Initialize Goals
# -----------------------
def initialize_goals():
    if "goals" not in st.session_state:
        st.session_state.goals = []

# -----------------------
# Add Goal
# -----------------------
def add_goal(name, cost, years, goal_type, note):
    st.session_state.goals.append({
        "name": name,
        "cost": float(cost),
        "years": int(years),
        "goal_type": goal_type,
        "note": note
    })

# -----------------------
# Get Goals
# -----------------------
def get_goals():
    return st.session_state.get("goals", [])

# -----------------------
# Display Sticky Goals
# -----------------------
def display_sticky_goals():
    for i, g in enumerate(st.session_state.goals):
        st.markdown(f"""
        <div style="
        background:#fff59d;
        padding:12px;
        border-radius:10px;
        margin-bottom:10px;
        box-shadow:2px 2px 5px rgba(0,0,0,0.3);
        color:black;
        ">
        <b>{g['name']}</b><br>
        Goal Type: {g['goal_type']}<br>
        ₹{g['cost']:,} | {g['years']} yrs<br><br>
        {g['note']}
        </div>
        """, unsafe_allow_html=True)

# -----------------------
# Delete Goal
# -----------------------
def delete_goal(index):
    if "goals" in st.session_state and 0 <= index < len(st.session_state.goals):
        st.session_state.goals.pop(index)

# -----------------------
# Edit Goal
# -----------------------
def edit_goal(index, name, cost, years, goal_type, note):
    if 0 <= index < len(st.session_state.goals):
        st.session_state.goals[index] = {
            "name": name,
            "cost": float(cost),
            "years": int(years),
            "goal_type": goal_type,
            "note": note
        }

# -----------------------
# Save Goals
# -----------------------
def save_goals_to_file(file_path="goals.json"):
    try:
        with open(file_path, "w") as f:
            json.dump(st.session_state.get("goals", []), f, indent=4)
    except Exception as e:
        st.error(f"Error saving goals: {e}")

# -----------------------
# Load Goals
# -----------------------
def load_goals_from_file(file_path="goals.json"):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                st.session_state.goals = json.load(f)
        except Exception as e:
            st.error(f"Error loading goals: {e}")

# -----------------------
# Future Cost Calculator
# -----------------------
def calculate_future_cost(current_cost, years, inflation):
    """
    Calculate inflated future cost of a financial goal.
    """
    future_cost = current_cost * ((1 + inflation) ** years)
    return round(future_cost, 2)