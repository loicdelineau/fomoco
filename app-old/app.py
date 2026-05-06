import streamlit as st
from calculations import risk_band, future_value_annuity
from visualizations import create_growth_chart

# ====================== UBS-STYLE CONFIG ======================
st.set_page_config(
    page_title="Fomoco • UBS",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded"
)

# UBS Brand Colors
ubs_red = "#E20613"
ubs_dark = "#1E1E1E"
ubs_gray = "#F5F5F5"

# Enhanced CSS for perfect readability
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #FFFFFF;
    }}
    .main .block-container {{
        padding-top: 2rem;
        max-width: 720px;
    }}
    h1 {{
        color: {ubs_red} !important;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 700;
    }}
    
    /* SIDEBAR - High contrast */
    .stSidebar {{
        background-color: {ubs_gray};
    }}
    .stSidebar .stMarkdown, .stSidebar label, .stSidebar p {{
        color: {ubs_dark} !important;
        font-weight: 500;
    }}
    .stSlider label, .stSelectbox label {{
        color: {ubs_dark} !important;
        font-size: 1.05rem !important;
        font-weight: 600;
    }}
    
    /* Make slider values and selectbox text darker */
    .stSlider .stMarkdown, .stSelectbox div[data-baseweb="select"] {{
        color: {ubs_dark} !important;
    }}
    
    /* Info box - maximum readability */
    .info-box {{
        background-color: #F8F9FA;
        padding: 1.6rem;
        border-radius: 12px;
        border-left: 6px solid #E20613;
        margin: 25px 0;
        color: #1E1E1E !important;
        font-size: 1.05rem;
        line-height: 1.55;
    }}
    </style>
""", unsafe_allow_html=True)

# ====================== HEADER ======================
st.markdown(f"""
    <div style="text-align: center; padding: 1rem 0 2rem 0;">
        <h1 style="margin:0; font-size: 2.8rem; color: {ubs_red};">FOMOCO</h1>
        <p style="color: #444; margin: 0.2rem 0 0 0; font-size: 1.15rem;">
            See what you're missing out on
        </p>
    </div>
""", unsafe_allow_html=True)

# ====================== SIDEBAR ======================
st.sidebar.markdown("### Your Investment Plan")
monthly = st.sidebar.slider("Monthly investment ($)", 0, 1000, 200, step=25)

basket_option = st.sidebar.selectbox(
    "Investment basket",
    ["Conservative (bonds)", "Balanced (60/40)", "Aggressive (stocks)"]
)

horizon = st.sidebar.slider("Time horizon (years)", 10, 40, 20, step=5)

baskets = {
    "Conservative (bonds)": {"rate": 5.0,  "vol": 4.0},
    "Balanced (60/40)":     {"rate": 8.0,  "vol": 9.0},
    "Aggressive (stocks)":  {"rate": 12.0, "vol": 18.0},
}

params = baskets[basket_option]
annual_rate = params["rate"]

# ====================== CALCULATIONS ======================
years_list = list(range(1, horizon + 1))
lower, expected, upper = risk_band(monthly, horizon, params["rate"], params["vol"])

# ====================== CHART ======================
fig = create_growth_chart(
    years_list, lower, expected, upper, monthly, basket_option, annual_rate
)
st.plotly_chart(fig, use_container_width=True)

# ====================== UBS HIGHLIGHT CARD ======================
final_value = expected[-1]
bank_final = future_value_annuity(monthly, horizon, 0.25)[-1]

st.markdown(f"""
    <div style="background: linear-gradient(135deg, #E20613, #B0000F); 
                color: white; 
                padding: 2rem; 
                border-radius: 16px; 
                text-align: center; 
                box-shadow: 0 8px 20px rgba(226,6,19,0.3);
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
        <p style="margin:0; font-size: 1.1rem; opacity: 0.95;">
            In {horizon} years you could have
        </p>
        <h2 style="margin: 0.5rem 0; font-size: 3.2rem; font-weight: 700;">
            ${final_value:,.0f}
        </h2>
        <p style="margin:0; font-size: 1.3rem; opacity: 0.95;">
            instead of <span style="text-decoration: line-through; opacity: 0.85;">${bank_final:,.0f}</span>
        </p>
        <p style="margin-top: 1rem; font-size: 1rem; opacity: 0.9;">
            investing ${monthly}/month in <strong>{basket_option}</strong>
        </p>
    </div>
""", unsafe_allow_html=True)

# ====================== INFO BOX (Fixed Readability) ======================
st.markdown(f"""
    <div class="info-box">
        <strong>Green curve</strong> — Expected investment growth<br>
        <strong>Red dashed curve</strong> — Bank account at 0.25%<br>
        <strong>Orange band</strong> — Realistic risk range
    </div>
""", unsafe_allow_html=True)

st.caption("Fomoco — Making compound interest visible • May 2026")
