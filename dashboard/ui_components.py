import streamlit as st

def finley_intro():
    """
    Displays the Finley assistant on the dashboard with a walking animation
    and a floating chat window ready for messages.
    """
    st.markdown("""
    <style>
    /* Walking animation for Finley */
    @keyframes walk {
        0% {left:-120px;}
        100% {left:100%;}
    }
    .finley-walk {
        position: fixed;
        bottom: 30px;
        animation: walk 20s linear infinite;
        z-index: 999;
    }

    /* Chat bubble container */
    .finley-chat {
        position: fixed;
        bottom: 120px;
        right: 20px;
        width: 320px;
        max-height: 400px;
        background: rgba(255,255,255,0.95);
        border-radius: 12px;
        padding: 12px;
        color: black;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        overflow-y: auto;
        z-index: 999;
    }

    /* User message style */
    .finley-message-user {
        background: #d1e7ff;
        padding: 6px 10px;
        border-radius: 10px;
        margin: 4px 0;
        text-align: right;
    }

    /* Assistant message style */
    .finley-message-assistant {
        background: #fff59d;
        padding: 6px 10px;
        border-radius: 10px;
        margin: 4px 0;
        text-align: left;
    }
    </style>

    <!-- Finley character -->
    <div class="finley-walk">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" width="90">
    </div>

    <!-- Chat window -->
    <div class="finley-chat" id="chat-box">
        <div class="finley-message-assistant">
            Hi! I'm Finley, your financial assistant. Ask me about your goals, SIPs, or simulations!
        </div>
    </div>
    """, unsafe_allow_html=True)