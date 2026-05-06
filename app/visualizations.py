import plotly.graph_objects as go
from calculations import future_value_annuity


def create_growth_chart(years_list, lower, expected, upper, monthly, basket_name, rate, initial=0):
    """
    UBS-style growth chart with support for Initial Investment
    """
    fig = go.Figure()

    # === RISK BAND (UBS red tint) ===
    fig.add_trace(go.Scatter(
        x=years_list, y=upper,
        fill=None, mode='lines', line_color='rgba(0,0,0,0)',
        name='Upper bound'
    ))
    fig.add_trace(go.Scatter(
        x=years_list, y=lower,
        fill='tonexty', mode='lines',
        fillcolor='rgba(226, 6, 19, 0.15)',   # UBS red light band
        line_color='rgba(0,0,0,0)',
        name='Risk range'
    ))

    # === MAIN INVESTMENT CURVE (Professional Green) ===
    fig.add_trace(go.Scatter(
        x=years_list,
        y=expected,
        mode='lines+markers',
        name=f'Investment Growth ({rate}%)',
        line=dict(color='#00A86B', width=5),
        marker=dict(size=8, color='#00A86B'),
        hovertemplate="Year %{x}<br>Value: $%{y:,.0f}<extra></extra>"
    ))

    # === BANK ACCOUNT CURVE (UBS Red dashed) ===
    bank_rate = 0.25
    bank_values = future_value_annuity(monthly, max(years_list), bank_rate, initial)

    fig.add_trace(go.Scatter(
        x=years_list,
        y=bank_values,
        mode='lines+markers',
        name='Bank Account (0.25%)',
        line=dict(color='#E20613', width=3, dash='dash'),
        marker=dict(size=6, color='#E20613'),
        hovertemplate="Year %{x}<br>Value: $%{y:,.0f}<extra></extra>"
    ))

    # === CHART TITLE & LAYOUT ===
    initial_text = f" + CHF {initial:,.0f} initial" if initial > 0 else ""
    
    fig.update_layout(
        title=dict(
            text=f"Your Money in {max(years_list)} Years{initial_text}",
            font=dict(size=24, family="Helvetica Neue, Arial", color="#1E1E1E"),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Years",
            title_font=dict(size=16, color="#1E1E1E"),
            tickfont=dict(size=14, color="#1E1E1E"),
            gridcolor='rgba(0,0,0,0.06)'
        ),
        yaxis=dict(
            title="Portfolio Value (CHF)",
            title_font=dict(size=16, color="#1E1E1E"),
            tickfont=dict(size=14, color="#1E1E1E"),
            tickprefix="CHF ",
            gridcolor='rgba(0,0,0,0.06)'
        ),
        hovermode="x unified",
        template="plotly_white",
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        legend=dict(
            yanchor="top", y=0.98, xanchor="left", x=0.02,
            bgcolor="rgba(255,255,255,0.98)",
            bordercolor="#E5E5E5",
            borderwidth=1,
            font=dict(size=13, color="#1E1E1E")
        ),
        margin=dict(l=20, r=20, t=80, b=60),
        height=520
    )

    fig.update_xaxes(showgrid=True, zeroline=False, showline=True, linewidth=1, linecolor='#E5E5E5')
    fig.update_yaxes(showgrid=True, zeroline=False, showline=True, linewidth=1, linecolor='#E5E5E5')

    return fig
