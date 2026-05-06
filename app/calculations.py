import numpy as np

def future_value_annuity(monthly: float, years: int, annual_rate: float, initial: float = 0.0) -> np.ndarray:
    """Return array of portfolio values at the end of each year, including initial lump sum"""
    months = np.arange(1, years * 12 + 1)
    monthly_rate = annual_rate / 12 / 100
    
    # Future value of monthly contributions
    if monthly_rate == 0:
        fv_monthly = monthly * months / 12
    else:
        fv_monthly = monthly * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    
    # Future value of initial investment
    fv_initial = initial * (1 + monthly_rate) ** months
    
    # Total portfolio value
    total_fv = fv_initial + fv_monthly
    
    # Return only end-of-year values
    return total_fv[11::12]


def risk_band(monthly: float, years: int, annual_rate: float, volatility: float, initial: float = 0.0):
    """Improved risk bands including initial investment"""
    lower_rate = annual_rate - 0.8 * volatility
    lower_rate = max(lower_rate, -2.0)  # Prevent crazy negative rates
    
    lower = future_value_annuity(monthly, years, lower_rate, initial)
    expected = future_value_annuity(monthly, years, annual_rate, initial)
    upper = future_value_annuity(monthly, years, annual_rate + volatility, initial)
    
    return lower, expected, upper
