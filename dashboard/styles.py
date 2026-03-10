import streamlit as st


def load_styles():

    st.markdown("""

<style>

.stApp{
background: linear-gradient(
135deg,
#141E30,
#243B55,
#0f2027
);
}

.finley-box{

display:flex;
align-items:center;

background:rgba(255,255,255,0.08);

padding:12px;
border-radius:14px;

margin-bottom:12px;

border:1px solid rgba(255,255,255,0.1);

}

.finley-text{
margin-left:10px;
}

div[data-testid="stMetric"]{

background:rgba(255,255,255,0.05);

padding:12px;

border-radius:12px;

}

</style>

""", unsafe_allow_html=True)