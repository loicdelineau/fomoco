import plotly.graph_objects as go
from calculations import future_value_annuity

def create_growth_chart(years_list, lower, expected, upper, monthly, basket_name, rate):
    fig = go.Figure()

    # Risk shaded area (orange)
    fig.add_trace(go.Scatter(
        x=years_list, y=upper,
        fill=None, mode='lines', line_color='rgba(0,0,0,0)',
        name='Upper risk'
    ))
    fig.add_trace(go.Scatter(
        x=years_list, y=lower,
        fill='tonexty', mode='lines',
        fillcolor='rgba(255,165,0,0.25)', 
        line_color='rgba(0,0,0,0)',
        name='Lower risk'
    ))

    # === GREEN CURVE - Investment ===
    fig.add_trace(go.Scatter(
        x=years_list, y=expected,
        mode='lines+markers',
        name=f'Investment ({rate}%)',
        line=dict(color='#00cc66', width=4),
        marker=dict(size=10)
    ))

    # === RED CURVE - Bank account (0.25%) ===
    bank_rate = 0.25
    bank_values = future_value_annuity(monthly, max(years_list), bank_rate)
    
    fig.add_trace(go.Scatter(
        x=years_list, y=bank_values,
        mode='lines+markers',
        name='Bank account (0.25%)',
        line=dict(color='#ff4444', width=3, dash='dash'),
        marker=dict(size=8, color='#ff4444')
    ))

    fig.update_layout(
        title=f"Fomoco – Your money in {max(years_list)} years",
        xaxis_title="Years",
        yaxis_title="Portfolio Value ($)",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    return fig
