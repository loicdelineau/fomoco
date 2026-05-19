import streamlit as st
from calculations import risk_band, future_value_annuity, format_chf
from visualizations import create_growth_chart

st.set_page_config(page_title="Growth Analysis • Fomoco", page_icon="📈", layout="centered")

# Load styles
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Fixed parameters
monthly = 3000
years = 35
annual_rate = 5.0
volatility = 4.0

years_list = list(range(1, years + 1))
lower, expected, upper = risk_band(monthly, years, annual_rate, volatility)

fig = create_growth_chart(years_list, lower, expected, upper, monthly, annual_rate)
st.plotly_chart(fig, use_container_width=True)

# Summary box
final_value = expected[-1]
bank_final = future_value_annuity(monthly, years, 0.25)[-1]

st.markdown(f"""
<div class="merged-box" style="background:#EAF6EE; border:2px solid #008A3D;">
    <p style="color:#008A3D; font-weight:600; margin:0 0 0.5rem 0;">
        If you invest CHF 3’000 monthly in the Conservative profile
    </p>
    <h2 style="color:#008A3D; margin:0; font-size:2.1rem;">
        {format_chf(final_value)}
    </h2>
    <p style="color:#666666; margin:0.8rem 0 0 0;">
        vs <span style="text-decoration: line-through; color:#E60000;">{format_chf(bank_final)}</span> in a savings account at 0.25%
    </p>
</div>
""", unsafe_allow_html=True)

st.info("""
**Green curve**: Expected growth at 5% (conservative bonds)  
**Red dashed curve**: Same money left in bank account  
**Shaded area**: Realistic risk range for this profile
""")

# ==================== BUTTONS SECTION ====================
# Red primary button
if st.button("🚀 Start investing with Fomoco", 
             type="primary", 
             use_container_width=True,
             key="start_investing_growth"):
    st.success("Excellent choice! Let's get you started.")
    st.switch_page("app.py")

# Grey back button using custom CSS class
st.markdown("""
    <style>
    .grey-back-btn button {
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

if st.button("← Back to Home", 
             key="back_to_home",
             use_container_width=True):
    st.switch_page("app.py")

