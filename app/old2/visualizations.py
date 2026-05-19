import plotly.graph_objects as go
from calculations import future_value_annuity


def create_growth_chart(years_list, lower, expected, upper, monthly, basket_name, rate, initial=0):
    """Clean, mobile-friendly UBS-style chart"""
    
    fig = go.Figure()

    # Risk band
    fig.add_trace(go.Scatter(
        x=years_list, y=upper,
        fill=None, mode='lines', line_color='rgba(0,0,0,0)',
        name='Upper bound'
    ))
    fig.add_trace(go.Scatter(
        x=years_list, y=lower,
        fill='tonexty', mode='lines',
        fillcolor='rgba(226, 6, 19, 0.16)',   # Soft UBS red
        line_color='rgba(0,0,0,0)',
        name='Risk range'
    ))

    # Investment growth (green)
    fig.add_trace(go.Scatter(
        x=years_list,
        y=expected,
        mode='lines+markers',
        name=f'Investment ({rate}%)',
        line=dict(color='#00A86B', width=4.5),
        marker=dict(size=6),
        hovertemplate="Year %{x}<br>CHF %{y:,.0f}<extra></extra>"
    ))

    # Bank account (red dashed)
    bank_values = future_value_annuity(monthly, max(years_list), 0.25, initial)
    fig.add_trace(go.Scatter(
        x=years_list,
        y=bank_values,
        mode='lines+markers',
        name='Bank (0.25%)',
        line=dict(color='#E20613', width=3, dash='dash'),
        marker=dict(size=5),
        hovertemplate="Year %{x}<br>CHF %{y:,.0f}<extra></extra>"
    ))

    # Title with initial amount
    initial_text = f" + CHF {initial:,.0f}" if initial > 0 else ""
    
    fig.update_layout(
        title=dict(
            text=f"Projected Value in {max(years_list)} Years{initial_text}",
            font=dict(size=20, color="#1E1E1E"),
            x=0.5,
            xanchor="center"
        ),
        xaxis=dict(
            title="Years to Retirement",
            title_font=dict(size=14),
            tickfont=dict(size=13)
        ),
        yaxis=dict(
            title="Portfolio Value (CHF)",
            title_font=dict(size=14),
            tickfont=dict(size=13),
            tickprefix="CHF "
        ),
        hovermode="x unified",
        template="plotly_white",
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.02,
            font=dict(size=12.5, color="#444444"),
            bgcolor="rgba(255,255,255,0.95)"
        ),
        height=520,           # Good height for phone
        margin=dict(l=30, r=30, t=70, b=50)
    )

    return fig
