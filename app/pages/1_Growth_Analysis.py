import streamlit as st
from calculations import risk_band
from visualizations import create_growth_chart

st.set_page_config(page_title="Growth Analysis • UBS", layout="centered")

st.markdown("<h1 style='text-align:center; color:#E20613;'>Growth Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>See your future if you start investing today</p>", unsafe_allow_html=True)

# Sliders on analysis page
monthly_invest = st.slider("Monthly investment (CHF)", 200, 2000, 1000, step=50)
initial_invest = st.slider("Initial investment (CHF)", 0, 100000, 7300, step=1000)
years_to_retirement = st.slider("Years to retirement", 10, 40, 35, step=1)

basket_option = st.selectbox("Investment basket", ["Balanced (60/40)", "Aggressive (stocks)", "Conservative (bonds)"])
rate = {"Conservative (bonds)": 5.0, "Balanced (60/40)": 8.0, "Aggressive (stocks)": 12.0}[basket_option]

# Chart
years_list = list(range(1, years_to_retirement + 1))
vol = 9.0 if rate == 8.0 else 18.0 if rate == 12.0 else 4.0

lower, expected, upper = risk_band(monthly_invest, years_to_retirement, rate, vol, initial_invest)

fig = create_growth_chart(years_list, lower, expected, upper, monthly_invest, basket_option, rate, initial_invest)
st.plotly_chart(fig, width="stretch")

if st.button("← Back to Overview"):
    st.switch_page("app.py")
