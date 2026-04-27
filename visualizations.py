import plotly.graph_objects as go
from calculations import future_value_annuity

def create_growth_chart(years_list, lower, expected, upper, monthly, basket_name):
    fig = go.Figure()

    # Risk shaded area
    fig.add_trace(go.Scatter(
        x=years_list, y=upper,
        fill=None, mode='lines', line_color='rgba(0,0,0,0)',
        name='Upper risk'
    ))
    fig.add_trace(go.Scatter(
        x=years_list, y=lower,
        fill='tonexty', mode='lines',
        fillcolor='rgba(255,165,0,0.2)', line_color='rgba(0,0,0,0)',
        name='Lower risk'
    ))

    # Main expected growth curve
    fig.add_trace(go.Scatter(
        x=years_list, y=expected,
        mode='lines+markers',
        name=f'Expected growth ({basket_name})',
        line=dict(color='#00cc66', width=4),
        marker=dict(size=10)
    ))

    # Red comparison dot/line for "what if you invested less/more"
    # (here we show a lazy $50/month baseline so the red dot moves up/down when you change slider)
    lazy_expected = future_value_annuity(50, max(years_list), 4.0)  # 4% savings account
    fig.add_trace(go.Scatter(
        x=years_list, y=lazy_expected,
        mode='lines+markers',
        name='If you only saved $50/mo (bank)',
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
