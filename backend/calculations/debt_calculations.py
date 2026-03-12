"""
Debt-related financial calculations.

All calculations are deterministic and follow standard banking formulas.
"""

from typing import Dict, List, Any


def calculate_estimated_payment(
    amount: float,
    term_months: int,
    rate: float = 0.05
) -> float:
    """
    Calculate estimated monthly payment using amortization formula.
    
    Args:
        amount: Loan amount
        term_months: Loan term in months
        rate: Annual interest rate (default 0.05 = 5%)
        
    Returns:
        Monthly payment amount
    """
    monthly_rate = rate / 12
    if monthly_rate == 0:
        return amount / term_months
    payment = (monthly_rate * amount) / (1 - (1 + monthly_rate) ** -term_months)
    return round(payment, 2)


def calculate_total_monthly_debt(debts: List[Dict[str, Any]]) -> float:
    """
    Calculate total monthly debt payments.
    
    Args:
        debts: List of debt dictionaries with 'monthly_payment' field
        
    Returns:
        Total monthly debt payment
    """
    return sum(debt.get("monthly_payment", 0) for debt in debts)


def calculate_dti_ratio(
    total_monthly_debt: float,
    monthly_gross_income: float
) -> float:
    """
    Calculate Debt-to-Income (DTI) ratio.
    
    DTI = (Total Monthly Debt Payments / Monthly Gross Income) × 100
    
    Args:
        total_monthly_debt: Total monthly debt payments
        monthly_gross_income: Monthly gross income
        
    Returns:
        DTI ratio as percentage
    """
    if monthly_gross_income <= 0:
        return 999.0  # Invalid/infinite DTI
    
    return (total_monthly_debt / monthly_gross_income) * 100


def calculate_dscr(
    monthly_net_income: float,
    total_monthly_debt: float
) -> float:
    """
    Calculate Debt Service Coverage Ratio (DSCR).
    
    DSCR = Monthly Net Income / Total Monthly Debt Payments
    
    A DSCR > 1.0 means income exceeds debt obligations.
    
    Args:
        monthly_net_income: Monthly net income
        total_monthly_debt: Total monthly debt payments
        
    Returns:
        DSCR ratio
    """
    if total_monthly_debt <= 0:
        return 999.0  # No debt, infinite coverage
    
    return monthly_net_income / total_monthly_debt


def assess_debt_burden(dti_ratio: float, dscr: float) -> Dict[str, Any]:
    """
    Assess debt burden level based on DTI and DSCR.
    
    DTI Guidelines:
    - Excellent: < 20%
    - Good: 20-28%
    - Acceptable: 28-36%
    - High: 36-43%
    - Very High: > 43%
    
    DSCR Guidelines:
    - Strong: > 2.0
    - Good: 1.5-2.0
    - Acceptable: 1.25-1.5
    - Weak: 1.0-1.25
    - Critical: < 1.0
    
    Args:
        dti_ratio: Debt-to-Income ratio
        dscr: Debt Service Coverage Ratio
        
    Returns:
        Dictionary with burden assessment
    """
    # DTI Assessment
    if dti_ratio < 20:
        dti_level = "excellent"
        dti_score = 100
    elif dti_ratio < 28:
        dti_level = "good"
        dti_score = 85
    elif dti_ratio < 36:
        dti_level = "acceptable"
        dti_score = 70
    elif dti_ratio < 43:
        dti_level = "high"
        dti_score = 50
    else:
        dti_level = "very_high"
        dti_score = 25
    
    # DSCR Assessment
    if dscr >= 2.0:
        dscr_level = "strong"
        dscr_score = 100
    elif dscr >= 1.5:
        dscr_level = "good"
        dscr_score = 85
    elif dscr >= 1.25:
        dscr_level = "acceptable"
        dscr_score = 70
    elif dscr >= 1.0:
        dscr_level = "weak"
        dscr_score = 50
    else:
        dscr_level = "critical"
        dscr_score = 25
    
    # Overall assessment
    overall_score = (dti_score + dscr_score) / 2
    
    if overall_score >= 85:
        overall_level = "low"
    elif overall_score >= 70:
        overall_level = "moderate"
    elif overall_score >= 50:
        overall_level = "high"
    else:
        overall_level = "very_high"
    
    return {
        "dti_assessment": {
            "level": dti_level,
            "score": dti_score
        },
        "dscr_assessment": {
            "level": dscr_level,
            "score": dscr_score
        },
        "overall_debt_burden": overall_level,
        "overall_score": round(overall_score, 2)
    }


def calculate_debt_utilization(
    total_debt_balance: float,
    total_credit_limit: float
) -> float:
    """
    Calculate credit utilization ratio.
    
    Args:
        total_debt_balance: Total outstanding debt balance
        total_credit_limit: Total available credit limit
        
    Returns:
        Utilization ratio as percentage
    """
    if total_credit_limit <= 0:
        return 0.0
    
    return (total_debt_balance / total_credit_limit) * 100


def project_debt_payoff(
    debt_balance: float,
    monthly_payment: float,
    annual_interest_rate: float
) -> Dict[str, Any]:
    """
    Project debt payoff timeline.
    
    Args:
        debt_balance: Current debt balance
        monthly_payment: Monthly payment amount
        annual_interest_rate: Annual interest rate (%)
        
    Returns:
        Dictionary with payoff projection
    """
    if monthly_payment <= 0:
        return {
            "months_to_payoff": 999,
            "total_interest_paid": 0,
            "total_amount_paid": debt_balance
        }
    
    monthly_rate = (annual_interest_rate / 100) / 12
    balance = debt_balance
    months = 0
    total_interest = 0
    
    # Cap at 600 months (50 years) to prevent infinite loops
    max_months = 600
    
    while balance > 0 and months < max_months:
        interest_charge = balance * monthly_rate
        principal_payment = monthly_payment - interest_charge
        
        if principal_payment <= 0:
            # Payment doesn't cover interest
            return {
                "months_to_payoff": 999,
                "total_interest_paid": 0,
                "total_amount_paid": 0,
                "error": "Payment insufficient to cover interest"
            }
        
        balance -= principal_payment
        total_interest += interest_charge
        months += 1
    
    return {
        "months_to_payoff": months,
        "years_to_payoff": round(months / 12, 1),
        "total_interest_paid": round(total_interest, 2),
        "total_amount_paid": round(debt_balance + total_interest, 2)
    }
