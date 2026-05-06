import numpy as np

def future_value_annuity(monthly: float, years: int, annual_rate: float) -> np.ndarray:
    """Return array of portfolio values at the end of each year"""
    months = np.arange(1, years * 12 + 1)
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        return monthly * months / 12
    fv = monthly * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    return fv[11::12]

def risk_band(monthly: float, years: int, annual_rate: float, volatility: float):
    """Improved risk bands"""
    # Use more realistic downside: expected minus a portion of volatility
    lower_rate = annual_rate - 0.8 * volatility   # Not full volatility (more realistic)
    # Prevent crazy negative rates for lower bound
    lower_rate = max(lower_rate, -2.0)
    
    lower = future_value_annuity(monthly, years, lower_rate)
    expected = future_value_annuity(monthly, years, annual_rate)
    upper = future_value_annuity(monthly, years, annual_rate + volatility)
    
    return lower, expected, upper
