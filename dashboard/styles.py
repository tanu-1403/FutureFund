import streamlit as st

def load_styles():
    """
    Applies custom CSS styles for the FutureFund dashboard and Finley chatbot.
    """
    st.markdown("""
    <style>
    /* Main app background gradient */
    .stApp {
        background: linear-gradient(
            135deg,
            #141E30,
            #243B55,
            #0f2027
        );
        color: #ffffff;
    }

    /* Finley chat bubble / UI container */
    .finley-box {
        display: flex;
        align-items: center;
        background: rgba(255,255,255,0.08);
        padding: 12px;
        border-radius: 14px;
        margin-bottom: 12px;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .finley-text {
        margin-left: 10px;
    }

    /* Streamlit metrics */
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.05);
        padding: 12px;
        border-radius: 12px;
        color: #ffffff;
    }

    /* Finley chat messages */
    .finley-chat {
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
    }

    .finley-message-user {
        background: #d1e7ff;
        color: #000;
    }

    .finley-message-assistant {
        background: #fff59d;
        color: #000;
    }

    /* Scrollbar for chat window */
    .finley-chat::-webkit-scrollbar {
        width: 6px;
    }

    .finley-chat::-webkit-scrollbar-thumb {
        background-color: rgba(255,255,255,0.3);
        border-radius: 3px;
    }

    </style>
    """, unsafe_allow_html=True)