
import streamlit as st


def finley_intro():
    """
    Displays the Finley AI assistant intro banner.
    """

    st.markdown(
        """
        <div style="
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.12);
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 12px;
        ">

        <div style="font-size:28px">
        🤖
        </div>

        <div>

        <div style="
            font-size:18px;
            font-weight:600;
            margin-bottom:4px;
        ">
        Finley — Your AI Financial Assistant
        </div>

        <div style="
            font-size:14px;
            opacity:0.85;
        ">
        Ask about <b>goals</b>, <b>SIP planning</b>, or 
        <b>investment probability</b>.
        </div>

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

