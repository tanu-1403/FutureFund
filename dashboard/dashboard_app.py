
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("LifePath Financial Simulator")

income = st.slider("Current Income", 10000, 200000, 50000)
growth = st.slider("Income Growth Rate", 1, 15, 5)

years = list(range(2025, 2045))
values = [income*(1+growth/100)**i for i in range(len(years))]

df = pd.DataFrame({
    "Year": years,
    "Income": values
})

fig = px.line(df, x="Year", y="Income", title="Income Projection")

st.plotly_chart(fig)