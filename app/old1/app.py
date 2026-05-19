import streamlit as st
from calculations import risk_band, future_value_annuity
from visualizations import create_growth_chart

st.set_page_config(page_title="Fomoco", page_icon="📈", layout="wide")
st.title("📈 Fomoco – See exactly what you're missing out on")
st.caption("The tool that makes young people actually invest")

# Sidebar controls
st.sidebar.header("Your Plan")
monthly = st.sidebar.slider("Monthly investment ($)", 0, 1000, 200, step=25)

# Investment basket with realistic volatility
basket_option = st.sidebar.selectbox(
    "Investment basket",
    [
        "Conservative (bonds)",
        "Balanced (60/40)",
        "Aggressive (stocks)"
    ]
)

horizon = st.sidebar.slider("Time horizon (years)", 10, 30, 20, step=10)

# Better volatility numbers (as you wanted)
baskets = {
    "Conservative (bonds)": {"rate": 5.0,  "vol": 4.0},
    "Balanced (60/40)":     {"rate": 8.0,  "vol": 9.0},
    "Aggressive (stocks)":  {"rate": 12.0, "vol": 18.0},
}

params = baskets[basket_option]
basket_name = basket_option
annual_rate = params["rate"]

# Calculations
years_list = list(range(1, horizon + 1))
lower, expected, upper = risk_band(monthly, horizon, params["rate"], params["vol"])

# Create chart
fig = create_growth_chart(
    years_list,
    lower,
    expected,
    upper,
    monthly,
    basket_name,
    annual_rate
)

st.plotly_chart(fig, use_container_width=True)

# === Powerful "Instead Of" Message - Strong Green Box ===
final_value = expected[-1]
bank_rate = 0.25
bank_values = future_value_annuity(monthly, horizon, bank_rate)
bank_final = bank_values[-1]

st.markdown(f"""
<div style="background-color: #a8e6b0; padding: 22px; border-radius: 12px; 
            border-left: 8px solid #28a745; margin: 15px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    <strong style="font-size: 1.45em; color: #1e4d2b;">
        🎯 In {horizon} years you could have
    </strong><br>
    <span style="font-size: 2.55em; font-weight: 900; color: #0f3d1f;">
        ${final_value:,.0f}
    </span>
    <br>
    <strong style="color: #1e4d2b;">instead of</strong><br>
    <span style="font-size: 1.7em; font-weight: 700; color: #c9302c; text-decoration: line-through;">
        ${bank_final:,.0f}
    </span>
    <br>
    <small style="color: #1e4d2b; font-size: 1.05em;">
        investing ${monthly}/month in a <strong>{basket_name}</strong> basket
    </small>
</div>
""", unsafe_allow_html=True)


# Blue info box
st.info("""
**Green curve**: Standard investment Returns

**Red curve**: Same money left in bank at 0.25%

**Orange shaded area**: realistic risk range for this basket

""")
