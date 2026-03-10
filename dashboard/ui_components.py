import streamlit as st

def finley_intro():

    st.markdown("""
    <style>

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

    .finley-chat {
        position: fixed;
        bottom: 120px;
        right: 20px;
        width: 280px;
        background: rgba(255,255,255,0.95);
        border-radius: 12px;
        padding: 12px;
        color:black;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        z-index: 999;
    }

    </style>

    <div class="finley-walk">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" width="90">
    </div>

    """, unsafe_allow_html=True)