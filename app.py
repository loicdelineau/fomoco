import streamlit as st
from calculations import risk_band, future_value_annuity
from visualizations import create_growth_chart

st.set_page_config(page_title="Fomoco", page_icon="📈", layout="wide")
st.title("📈 Fomoco – See exactly what you're missing out on")
st.caption("The tool that makes young people actually invest")

# Sidebar controls
st.sidebar.header("Your Plan")
monthly = st.sidebar.slider("Monthly investment ($)", 0, 1000, 200, step=25)
basket = st.sidebar.selectbox(
    "Investment basket",
    ["Conservative (bonds)", "Balanced (60/40)", "Aggressive (stocks)"]
)
horizon = st.sidebar.selectbox("Time horizon", [10, 20, 30])

# Basket parameters
baskets = {
    "Conservative (bonds)": {"rate": 5.0, "vol": 3.0},
    "Balanced (60/40)": {"rate": 8.0, "vol": 8.0},
    "Aggressive (stocks)": {"rate": 12.0, "vol": 15.0},
}
params = baskets[basket]

years_list = list(range(1, horizon + 1))
lower, expected, upper = risk_band(monthly, horizon, params["rate"], params["vol"])

# The chart
fig = create_growth_chart(years_list, lower, expected, upper, monthly, basket)
st.plotly_chart(fig, use_container_width=True)

# Nice summary
final_value = expected[-1]
st.success(f"🎯 In {horizon} years you could have **${final_value:,.0f}** with ${monthly}/month in a {basket.lower()} basket!")
st.info("The orange shaded area = realistic risk range. The red dashed line = what happens if you just keep the money in a bank account. See how big the gap gets?")
