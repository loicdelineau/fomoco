import streamlit as st
from calculations import calculate_lost_revenue, format_chf

st.set_page_config(page_title="UBS • Fomoco", page_icon="📈", layout="centered")

# Load UBS styling
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "investing_mode" not in st.session_state:
    st.session_state.investing_mode = False

st.markdown("<h1>Home</h1>", unsafe_allow_html=True)
st.subheader("FOMOCO – Investment Advisor")

# Sidebar
st.sidebar.header("Your Situation")
monthly_unused = st.sidebar.slider("Monthly unused revenue (CHF)", 500, 6000, 3000, step=100)
months_without = st.sidebar.slider("Months without investing", 0, 120, 16, step=1)
years_to_retirement = st.sidebar.slider("Years to retirement", 10, 40, 35, step=1)

total_lost, potential_upside = calculate_lost_revenue(monthly_unused, months_without, years_to_retirement)

# ====================== RED LOST BOX (only when toggle OFF) ======================
if not st.session_state.investing_mode:
    st.markdown(f"""
        <div class="merged-box" style="margin: 0rem 0rem 1rem 0rem;">
            <h2 style="margin: -1rem 0 -1rem 0; font-size: 2.55rem; font-weight: 700; color:#E60000;">
                {format_chf(total_lost)}
                <span style="cursor:help; font-size:1.1rem; margin-left:8px;" title="Future value of each missed monthly contribution compounded at conservative 4.8% until retirement.">ℹ️</span>
            </h2>
            <p>Retirement savings already lost</p>
            <p class="small-text" style="margin: -1rem 0 0.8rem 0;">from the past {months_without} months of passively saving at 0.25%</p>
        </div>
    """, unsafe_allow_html=True)

# ====================== GREEN POTENTIAL BOX (ALWAYS VISIBLE) ======================
box_style = 'background: #EAF6EE; border: 2px solid #008A3D;' if st.session_state.investing_mode else 'background: #F8F9FA; border: 1px solid #DDDDDD;'
text_color = '#008A3D' if st.session_state.investing_mode else '#1A1A1A'

st.markdown(f"""
    <div class="merged-box" style="{box_style}; margin: 0rem 0rem 1.5rem 0rem;">
        <p style="margin:-0.6rem 0 0.2rem 0; color:{text_color}; font-weight:600;">
            Retirement savings if you {'continue' if st.session_state.investing_mode else 'start'} investing CHF {monthly_unused}/month
        </p>
        <strong style="font-size:2.55rem; font-weight:700; color:{text_color};">
            {format_chf(potential_upside)}
        </strong>
    </div>
""", unsafe_allow_html=True)

# ====================== CTA + TOGGLE ======================
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown('<div style="margin-top: -10px;"> <br><br>', unsafe_allow_html=True)
    if st.button("View investment plan", type="primary", use_container_width=True):
        st.switch_page("pages/1_Growth_Analysis.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div style="margin-top: 5px;"> <br><br>', unsafe_allow_html=True)
    investing = st.toggle("Start investing", value=st.session_state.investing_mode)
    st.markdown('</div>', unsafe_allow_html=True)

st.session_state.investing_mode = investing

# ====================== ACCOUNTS ======================
st.subheader("Your accounts")
accent_color = "#008A3D" if investing else "#E60000"
revenue_text = "Invested saving" if investing else "Unused revenue"

st.markdown(f"""
    <div class="account-card">
        <h3>Private Account</h3>
        <p>Current Balance</p>
        <h2 style="margin:0; color:#333; margin:-1.5rem 0rem -1.5rem 0rem">{format_chf(12500)}</h2>
        <div class="notification" style="background: #F8F9FA; border: 1px solid #DDDDDD;">
            {revenue_text}: <strong style="color:{accent_color};">{format_chf(monthly_unused)}/month</strong><br>
            <small>12-month moving average</small>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="account-card">
        <h3>Savings Account</h3>
        <p>Current Balance</p>
        <h2 style="margin:0; color:#333; margin:-1.5rem 0rem -1.5rem 0rem">{format_chf(46000)}</h2>
        <div class="notification" style="background: #F8F9FA; border: 1px solid #DDDDDD;">
            {revenue_text}: <strong style="color:{accent_color};">{format_chf(monthly_unused)}/month</strong><br>
            <small>12-month moving average</small>
        </div>
    </div>
""", unsafe_allow_html=True)

st.caption("Fomoco • UBS-inspired • May 2026")
