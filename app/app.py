import streamlit as st
from calculations import calculate_lost_revenue

st.set_page_config(page_title="UBS • Fomoco", page_icon="📈", layout="centered")

# Session State
if "investing_mode" not in st.session_state:
    st.session_state.investing_mode = False

investing = st.toggle("🟢 Start Investing Mode", value=st.session_state.investing_mode, key="invest_toggle")
st.session_state.investing_mode = investing

accent_color = "#00A86B" if investing else "#E20613"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #FFFFFF; }}
    .main .block-container {{ padding-top: 1rem; max-width: 480px; margin: 0 auto; }}
    h1 {{ color: #E20613 !important; font-size: 2.2rem; font-weight: 700; text-align: center; }}
    p, label, .stMetricLabel {{ color: #333333 !important; }}
    
    .merged-box {{
        background: #F8F9FA;
        border-radius: 16px;
        padding: 1.5rem 1.3rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #EEEEEE;
        text-align: left;
    }}
    .account-card {{
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        padding: 1.5rem;
        margin-bottom: 1.6rem;
    }}
    .notification {{
        background: #F0FFF0 if investing else #FFF0F0;
        border-left: 5px solid {accent_color};
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        font-weight: 600;
        color: #333333;
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>UBS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#666; margin-bottom:1.8rem;'>Your Bank • Your Future</p>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Your Situation")
monthly_unused = st.sidebar.slider("Monthly unused revenue (CHF)", 500, 6000, 3000, step=100)
months_without = st.sidebar.slider("Months without investing", 0, 120, 24, step=1)
years_to_retirement = st.sidebar.slider("Years to retirement", 10, 40, 35, step=1)

from calculations import calculate_lost_revenue
total_lost, potential_upside = calculate_lost_revenue(monthly_unused, months_without, years_to_retirement)

status_text = "✅ Investing Mode Active" if investing else "❌ Not Investing"
revenue_text = "Invested Saving" if investing else "Unused revenue"

# Compact Left-Aligned Box
st.markdown(f"""
    <div class="merged-box">
        <small style="opacity:0.85;">FOMOCO — YOUR INVESTMENT ASSISTANT</small>
        <h2 style="margin: 0.5rem 0 0.1rem 0; font-size: 2.55rem; font-weight: 700; color:#E20613;">CHF {total_lost:,.0f}</h2>
        <p style="margin:0; color:#555;">Total lost revenue at retirement</p>
        <p style="margin:0.1rem 0 0.8rem 0; color:#777; font-size:0.93rem;">from the last {months_without} months</p>
        
        <p style="margin:0.8rem 0 0.2rem 0; color:#00A86B; font-weight:600;">Expected savings if you invest today</p>
        <strong style="font-size:1.95rem; color:#00A86B;">CHF {potential_upside:,.0f}</strong>
        
        <p style="margin-top:1rem; font-weight:600; color:{accent_color};">{status_text}</p>
    </div>
""", unsafe_allow_html=True)

# CTA
if st.button("📈 See My Growth Plan & Start Investing", type="primary", use_container_width=True):
    st.switch_page("pages/1_Growth_Analysis.py")

# Accounts - Using real UBS terminology
st.subheader("Your Accounts")

st.markdown(f"""
    <div class="account-card">
        <h3>💳 Personal Account</h3>
        <p style="margin:0.2rem 0 0.8rem 0;">Current Balance</p>
        <h2 style="margin:0; color:#333;">CHF 42,800</h2>
        <div class="notification">
            {revenue_text}: <strong style="color:{accent_color};">CHF {monthly_unused:,}/month</strong><br>
            <small>12-month moving average</small>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="account-card">
        <h3>🏦 Savings Account</h3>
        <p style="margin:0.2rem 0 0.8rem 0;">Current Balance</p>
        <h2 style="margin:0; color:#333;">CHF 40,000</h2>
        <div class="notification">
            {revenue_text}: <strong style="color:{accent_color};">CHF {monthly_unused:,}/month</strong><br>
            <small>12-month moving average</small>
        </div>
    </div>
""", unsafe_allow_html=True)

st.caption("Fomoco • UBS-inspired • May 2026")
