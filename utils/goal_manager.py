import streamlit as st

def initialize_goals():
    if "goals" not in st.session_state:
        st.session_state.goals = []


def add_goal(name,cost,years,note):

    st.session_state.goals.append({
        "name":name,
        "cost":cost,
        "years":years,
        "note":note
    })


def get_goals():
    return st.session_state.goals


def display_sticky_goals():

    for g in st.session_state.goals:

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
        ₹{g['cost']:,} | {g['years']} yrs<br><br>
        {g['note']}

        </div>
        """, unsafe_allow_html=True)