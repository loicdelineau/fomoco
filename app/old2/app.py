import streamlit as st
from calculations import calculate_lost_revenue

st.set_page_config(page_title="UBS • Fomoco", page_icon="📈", layout="centered")

# Load external CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session State - Toggle button default
if "investing_mode" not in st.session_state:
    st.session_state.investing_mode = False


# Header
st.markdown("<h1>Home</h1>", unsafe_allow_html=True)
# FOMOCO
st.subheader("FOMOCO - Investment Advisor")

# Sidebar
st.sidebar.header("Your Situation")
monthly_unused = st.sidebar.slider("Monthly unused revenue (CHF)", 500, 6000, 3000, step=100)
months_without = st.sidebar.slider("Months without investing", 0, 120, 24, step=1)
years_to_retirement = st.sidebar.slider("Years to retirement", 10, 40, 35, step=1)

from calculations import calculate_lost_revenue
total_lost, potential_upside = calculate_lost_revenue(monthly_unused, months_without, years_to_retirement)



# Lost Revenue Box
st.markdown(f"""
    <div class="merged-box" style="margin: 0rem 0rem -2rem 0rem;">
        <h2 style="margin: -1rem 0 -1rem 0; font-size: 2.55rem; font-weight: 700; color:#E20613;">
            CHF {total_lost:,.0f}
        </h2>
        <p>Retirement savings already lost</p>
        <p class="small-text" style="margin: -1rem 0 -1rem 0;">from the past {months_without} months of passively saving</p>
    </div>
""", unsafe_allow_html=True)

# ====================== TOGGLE + CTA SIDE BY SIDE ======================
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div style="text-align: center; padding: 20px 0;">', unsafe_allow_html=True)
    if st.button("📈 View Investment Plan", 
                 type="primary", 
                 use_container_width=True):
        st.switch_page("pages/1_Growth_Analysis.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div style="text-align: right; padding: 28px 0px">', unsafe_allow_html=True)
    investing = st.toggle("🟢 Start Investing", 
                         value=st.session_state.investing_mode, 
                         key="invest_toggle")
    st.markdown('</div>', unsafe_allow_html=True)


if "investing_mode" not in st.session_state:
    st.session_state.investing_mode = investing
else:
    st.session_state.investing_mode = investing

accent_color = "#00A86B" if investing else "#E20613"
status_text = "✅ Investing Mode Active" if investing else "❌ Not Investing"
revenue_text = "Invested Saving" if investing else "Unused revenue"

# ====================== POTENTIAL REVENUE BOX ======================
if investing:
    box_style = 'background: #E6F4EA; border: 2px solid #00A86B;'
    text_color = '#00A86B'
    label = '✅ Retirement savings if you continue investing'
else:
    box_style = 'background: #F8F9FA; border: 1px solid #DDDDDD; opacity: 0.75;'
    text_color = '#888888'
    label = 'Expected savings if you start investing today'

st.markdown(f"""
    <div class="merged-box" style="{box_style}; margin: -1.5rem 0rem 2rem 0rem;">
        <p style="margin:-0.6rem 0 0.2rem 0; color:{text_color}; font-weight:600;">
            {label}
        </p>
        <strong style="font-size:1.95rem; color:{text_color};">CHF {potential_upside:,.0f}</strong>
        <p style="margin:0rem 0 -1.2rem 0; color:{text_color}; font-weight:600;">
        </p>
    </div>
""", unsafe_allow_html=True)







# Accounts
st.subheader("Your Accounts")

st.markdown(f"""
    <div class="account-card">
        <h3>💳 Private Account</h3>
        <p>Current Balance</p>
        <h2 style="margin:0; color:#333; margin:-1.5rem 0rem -1.5rem 0rem">CHF 32,800</h2>
        <div class="notification" style="{box_style}">
            {revenue_text}: <strong style="color:{accent_color};">CHF {monthly_unused:,}/month</strong><br>
            <small>12-month moving average</small>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="account-card">
        <h3>🏦 Savings Account</h3>
        <p>Current Balance</p>
        <h2 style="margin:0; color:#333; margin:-1.5rem 0rem -1.5rem 0rem">CHF 90,800</h2>
        <div class="notification" style="{box_style}">
            {revenue_text}: <strong style="color:{accent_color};">CHF {monthly_unused:,}/month</strong><br>
            <small>12-month moving average</small>
        </div>
    </div>
""", unsafe_allow_html=True)

st.caption("Fomoco • UBS-inspired • May 2026")
