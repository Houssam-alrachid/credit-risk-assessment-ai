"""
Income-related financial calculations.

All calculations are deterministic and follow standard banking formulas.
"""

from typing import Dict, Any, Optional


def calculate_annual_income(monthly_gross: float, monthly_net: float) -> Dict[str, float]:
    """
    Calculate annual income figures.
    
    Args:
        monthly_gross: Monthly gross income
        monthly_net: Monthly net income
        
    Returns:
        Dictionary with annual_gross and annual_net
    """
    return {
        "annual_gross": monthly_gross * 12,
        "annual_net": monthly_net * 12,
    }


def calculate_disposable_income(
    monthly_net_income: float,
    essential_expenses: float = 0.0,
    existing_debt_payments: float = 0.0
) -> float:
    """
    Calculate disposable income after essential expenses and debt.
    
    Args:
        monthly_net_income: Monthly net income
        essential_expenses: Monthly essential expenses (housing, utilities, food)
        existing_debt_payments: Current monthly debt obligations
        
    Returns:
        Disposable income amount
    """
    return monthly_net_income - essential_expenses - existing_debt_payments


def calculate_max_affordable_payment(
    monthly_gross_income: float,
    existing_monthly_debt: float,
    max_dti_ratio: float = 43.0,
    housing_expense_ratio: float = 28.0
) -> Dict[str, float]:
    """
    Calculate maximum affordable monthly payment.
    
    Uses standard banking guidelines:
    - 28% rule: Housing expenses should not exceed 28% of gross income
    - 43% rule: Total debt should not exceed 43% of gross income
    
    Args:
        monthly_gross_income: Monthly gross income
        existing_monthly_debt: Current monthly debt payments
        max_dti_ratio: Maximum debt-to-income ratio (default 43%)
        housing_expense_ratio: Maximum housing expense ratio (default 28%)
        
    Returns:
        Dictionary with max_payment_dti and max_payment_housing
    """
    # Based on total DTI limit
    max_total_debt = (monthly_gross_income * max_dti_ratio) / 100
    max_payment_dti = max_total_debt - existing_monthly_debt
    
    # Based on housing expense limit
    max_payment_housing = (monthly_gross_income * housing_expense_ratio) / 100
    
    return {
        "max_payment_dti": max(0, max_payment_dti),
        "max_payment_housing": max_payment_housing,
        "recommended_max_payment": min(max_payment_dti, max_payment_housing)
    }


def perform_income_stress_test(
    monthly_gross_income: float,
    monthly_payment: float,
    income_reduction_pct: float = 20.0,
    interest_rate_increase_bps: float = 200.0,
    current_interest_rate: float = 4.0,
    loan_amount: float = 0.0,
    loan_term_months: int = 240
) -> Dict[str, Any]:
    """
    Perform affordability stress test.
    
    Tests two scenarios:
    1. Income reduction (default 20%)
    2. Interest rate increase (default +200 basis points)
    
    Args:
        monthly_gross_income: Current monthly gross income
        monthly_payment: Proposed monthly payment
        income_reduction_pct: Income reduction percentage for stress test
        interest_rate_increase_bps: Interest rate increase in basis points
        current_interest_rate: Current interest rate (annual %)
        loan_amount: Loan amount for payment recalculation
        loan_term_months: Loan term in months
        
    Returns:
        Dictionary with stress test results
    """
    # Scenario 1: Income reduction
    stressed_income = monthly_gross_income * (1 - income_reduction_pct / 100)
    income_stress_dti = (monthly_payment / stressed_income) * 100 if stressed_income > 0 else 999
    passes_income_stress = income_stress_dti <= 43.0
    
    # Scenario 2: Interest rate increase
    stressed_rate = current_interest_rate + (interest_rate_increase_bps / 100)
    
    # Recalculate payment with stressed rate if loan details provided
    if loan_amount > 0 and loan_term_months > 0:
        monthly_rate = (stressed_rate / 100) / 12
        if monthly_rate > 0:
            stressed_payment = loan_amount * (
                monthly_rate * (1 + monthly_rate) ** loan_term_months
            ) / ((1 + monthly_rate) ** loan_term_months - 1)
        else:
            stressed_payment = loan_amount / loan_term_months
    else:
        # Approximate: increase payment proportionally to rate increase
        stressed_payment = monthly_payment * (1 + (interest_rate_increase_bps / 10000))
    
    rate_stress_dti = (stressed_payment / monthly_gross_income) * 100
    passes_rate_stress = rate_stress_dti <= 43.0
    
    # Combined stress test
    combined_stressed_payment = stressed_payment
    combined_stressed_income = stressed_income
    combined_dti = (combined_stressed_payment / combined_stressed_income) * 100 if combined_stressed_income > 0 else 999
    passes_combined_stress = combined_dti <= 43.0
    
    return {
        "income_stress": {
            "stressed_income": round(stressed_income, 2),
            "dti_ratio": round(income_stress_dti, 2),
            "passes": passes_income_stress
        },
        "rate_stress": {
            "stressed_rate": round(stressed_rate, 2),
            "stressed_payment": round(stressed_payment, 2),
            "dti_ratio": round(rate_stress_dti, 2),
            "passes": passes_rate_stress
        },
        "combined_stress": {
            "stressed_income": round(combined_stressed_income, 2),
            "stressed_payment": round(combined_stressed_payment, 2),
            "dti_ratio": round(combined_dti, 2),
            "passes": passes_combined_stress
        },
        "overall_passes_stress_test": passes_income_stress and passes_rate_stress
    }


def calculate_income_stability_score(
    years_employed: float,
    employment_type: str,
    income_trend: str = "stable",
    has_multiple_sources: bool = False
) -> int:
    """
    Calculate income stability score (0-100).
    
    Args:
        years_employed: Years in current employment
        employment_type: Type of employment (employed, self_employed, contractor, etc.)
        income_trend: Income trend (growing, stable, declining)
        has_multiple_sources: Whether applicant has multiple income sources
        
    Returns:
        Stability score from 0-100
    """
    score = 50  # Base score
    
    # Employment duration
    if years_employed >= 5:
        score += 20
    elif years_employed >= 3:
        score += 15
    elif years_employed >= 1:
        score += 10
    else:
        score -= 10
    
    # Employment type
    if employment_type.lower() == "employed":
        score += 15
    elif employment_type.lower() == "self_employed":
        score += 5
    elif employment_type.lower() in ["contractor", "freelance"]:
        score -= 5
    elif employment_type.lower() in ["unemployed", "student"]:
        score -= 20
    
    # Income trend
    if income_trend.lower() == "growing":
        score += 10
    elif income_trend.lower() == "declining":
        score -= 15
    
    # Multiple income sources
    if has_multiple_sources:
        score += 5
    
    # Clamp to 0-100
    return max(0, min(100, score))
