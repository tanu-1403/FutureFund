
import streamlit as st


def load_styles():
    """
    Apply custom CSS styling to the Streamlit app.
    Improves UI appearance and consistency.
    """

    st.markdown(
        """
        <style>

        /* -------------------------
        MAIN APP BACKGROUND
        ------------------------- */
        .stApp {
            background: linear-gradient(
                135deg,
                #141E30,
                #243B55
            );
            color: white;
        }

        /* -------------------------
        HEADINGS
        ------------------------- */
        h1, h2, h3, h4 {
            color: #f1f1f1;
            font-weight: 600;
        }

        /* -------------------------
        METRIC CARDS
        ------------------------- */
        div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.06);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
        }

        /* -------------------------
        SIDEBAR
        ------------------------- */
        section[data-testid="stSidebar"] {
            background-color: #0f172a;
        }

        /* -------------------------
        BUTTONS
        ------------------------- */
        button[kind="primary"] {
            background-color: #4CAF50;
            border-radius: 10px;
            border: none;
        }

        button[kind="primary"]:hover {
            background-color: #43a047;
        }

        /* -------------------------
        INPUT FIELDS
        ------------------------- */
        input, textarea {
            border-radius: 8px !important;
        }

        /* -------------------------
        CHAT BUBBLES
        ------------------------- */
        div[data-testid="stChatMessage"] {
            background: rgba(255,255,255,0.04);
            border-radius: 10px;
            padding: 10px;
        }

        /* -------------------------
        DATAFRAME
        ------------------------- */
        .stDataFrame {
            border-radius: 12px;
        }

        /* -------------------------
        DIVIDER
        ------------------------- */
        hr {
            border-color: rgba(255,255,255,0.1);
        }

        </style>
        """,
        unsafe_allow_html=True
    )

