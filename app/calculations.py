import numpy as np

def compound_future_value(monthly: float, years: int, annual_rate: float = 8.0, initial: float = 0.0) -> float:
    """Future value with monthly contributions + initial lump sum"""
    if years <= 0:
        return initial
    months = years * 12
    monthly_rate = annual_rate / 12 / 100
    
    fv_initial = initial * (1 + monthly_rate) ** months
    
    if monthly_rate == 0:
        fv_monthly = monthly * months
    else:
        fv_monthly = monthly * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    
    return fv_initial + fv_monthly


def calculate_lost_revenue(monthly_unused: float, months_without_investing: int, years_to_retirement: int, rate: float = 8.0):
    """Calculate total lost revenue + potential upside"""
    monthly_rate = rate / 12 / 100
    total_lost = 0.0
    
    for i in range(months_without_investing):
        months_remaining = years_to_retirement * 12 - i
        total_lost += monthly_unused * ((1 + monthly_rate) ** months_remaining)
    
    # Potential if starting today
    lump_sum_today = monthly_unused * months_without_investing
    fv_lump = lump_sum_today * (1 + monthly_rate) ** (years_to_retirement * 12)
    fv_monthly = compound_future_value(monthly_unused, years_to_retirement, rate)
    
    return round(total_lost), round(fv_lump + fv_monthly)


def future_value_annuity(monthly: float, years: int, annual_rate: float, initial: float = 0.0):
    """Legacy function for charts"""
    return np.array([compound_future_value(monthly, y, annual_rate, initial) 
                     for y in range(1, years + 1)])


def risk_band(monthly: float, years: int, annual_rate: float, volatility: float, initial: float = 0.0):
    """Risk bands for the growth chart"""
    lower_rate = max(annual_rate - 0.8 * volatility, -2.0)
    
    lower = future_value_annuity(monthly, years, lower_rate, initial)
    expected = future_value_annuity(monthly, years, annual_rate, initial)
    upper = future_value_annuity(monthly, years, annual_rate + volatility, initial)
    
    return lower, expected, upper
