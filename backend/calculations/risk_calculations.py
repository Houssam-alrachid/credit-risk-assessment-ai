"""
Risk-related financial calculations.

All calculations are deterministic and follow Basel III and standard banking formulas.
"""

from typing import Dict, Any, Optional
import math


def calculate_probability_of_default(
    credit_score: int,
    dti_ratio: float,
    employment_years: float,
    payment_history_score: int = 100,
    debt_burden_level: str = "moderate"
) -> float:
    """
    Calculate Probability of Default (PD) using a scoring model.
    
    PD is estimated based on:
    - Credit score (40% weight)
    - DTI ratio (25% weight)
    - Employment stability (15% weight)
    - Payment history (10% weight)
    - Debt burden (10% weight)
    
    Args:
        credit_score: Credit score (300-850)
        dti_ratio: Debt-to-Income ratio (%)
        employment_years: Years in current employment
        payment_history_score: Payment history score (0-100)
        debt_burden_level: Debt burden level
        
    Returns:
        Probability of Default as percentage (0-100)
    """
    # Credit score component (40% weight)
    if credit_score >= 750:
        credit_component = 2.0
    elif credit_score >= 700:
        credit_component = 5.0
    elif credit_score >= 650:
        credit_component = 10.0
    elif credit_score >= 600:
        credit_component = 20.0
    elif credit_score >= 550:
        credit_component = 35.0
    else:
        credit_component = 50.0
    
    # DTI component (25% weight)
    if dti_ratio < 20:
        dti_component = 2.0
    elif dti_ratio < 28:
        dti_component = 5.0
    elif dti_ratio < 36:
        dti_component = 12.0
    elif dti_ratio < 43:
        dti_component = 25.0
    else:
        dti_component = 40.0
    
    # Employment stability component (15% weight)
    if employment_years >= 5:
        employment_component = 2.0
    elif employment_years >= 3:
        employment_component = 5.0
    elif employment_years >= 1:
        employment_component = 10.0
    else:
        employment_component = 20.0
    
    # Payment history component (10% weight)
    payment_component = (100 - payment_history_score) / 5
    
    # Debt burden component (10% weight)
    debt_burden_scores = {
        "low": 2.0,
        "moderate": 8.0,
        "high": 18.0,
        "very_high": 30.0
    }
    debt_component = debt_burden_scores.get(debt_burden_level.lower(), 15.0)
    
    # Weighted average
    pd = (
        credit_component * 0.40 +
        dti_component * 0.25 +
        employment_component * 0.15 +
        payment_component * 0.10 +
        debt_component * 0.10
    )
    
    # Clamp to 0.1-99% (never 0 or 100)
    return max(0.1, min(99.0, pd))


def calculate_loss_given_default(
    ltv_ratio: float,
    collateral_quality: str,
    recovery_rate: float = 70.0,
    has_guarantor: bool = False
) -> float:
    """
    Calculate Loss Given Default (LGD).
    
    LGD = 100% - Recovery Rate
    
    Recovery rate depends on:
    - LTV ratio
    - Collateral quality
    - Presence of guarantor
    
    Args:
        ltv_ratio: Loan-to-Value ratio (%)
        collateral_quality: Quality of collateral
        recovery_rate: Base recovery rate from collateral (%)
        has_guarantor: Whether loan has a guarantor
        
    Returns:
        Loss Given Default as percentage (0-100)
    """
    # Base recovery from collateral
    base_recovery = recovery_rate
    
    # Adjust for LTV
    if ltv_ratio < 60:
        ltv_adjustment = 10  # Better recovery
    elif ltv_ratio < 75:
        ltv_adjustment = 5
    elif ltv_ratio < 85:
        ltv_adjustment = 0
    elif ltv_ratio < 95:
        ltv_adjustment = -10
    else:
        ltv_adjustment = -20
    
    # Adjust for collateral quality
    quality_adjustments = {
        "excellent": 15,
        "good": 10,
        "acceptable": 0,
        "weak": -10,
        "poor": -20
    }
    quality_adjustment = quality_adjustments.get(collateral_quality.lower(), 0)
    
    # Guarantor adjustment
    guarantor_adjustment = 10 if has_guarantor else 0
    
    # Total recovery rate
    total_recovery = base_recovery + ltv_adjustment + quality_adjustment + guarantor_adjustment
    total_recovery = max(10, min(95, total_recovery))  # Clamp 10-95%
    
    # LGD is inverse of recovery
    lgd = 100 - total_recovery
    
    return max(5.0, min(90.0, lgd))


def calculate_expected_loss(
    loan_amount: float,
    probability_of_default: float,
    loss_given_default: float,
    exposure_at_default: Optional[float] = None
) -> Dict[str, float]:
    """
    Calculate Expected Loss (EL).
    
    EL = PD × LGD × EAD
    
    Where:
    - PD = Probability of Default (%)
    - LGD = Loss Given Default (%)
    - EAD = Exposure at Default (loan amount if not specified)
    
    Args:
        loan_amount: Loan amount
        probability_of_default: PD as percentage
        loss_given_default: LGD as percentage
        exposure_at_default: EAD (defaults to loan_amount)
        
    Returns:
        Dictionary with expected loss calculations
    """
    ead = exposure_at_default if exposure_at_default is not None else loan_amount
    
    # Convert percentages to decimals
    pd_decimal = probability_of_default / 100
    lgd_decimal = loss_given_default / 100
    
    # Calculate expected loss
    expected_loss = ead * pd_decimal * lgd_decimal
    expected_loss_pct = (expected_loss / loan_amount) * 100 if loan_amount > 0 else 0
    
    return {
        "expected_loss_amount": round(expected_loss, 2),
        "expected_loss_percentage": round(expected_loss_pct, 2),
        "probability_of_default": round(probability_of_default, 2),
        "loss_given_default": round(loss_given_default, 2),
        "exposure_at_default": round(ead, 2)
    }


def calculate_risk_score(
    probability_of_default: float,
    loss_given_default: float,
    dti_ratio: float,
    ltv_ratio: float,
    credit_score: int,
    income_stability_score: int = 50,
    collateral_quality_score: int = 50
) -> Dict[str, Any]:
    """
    Calculate overall risk score (0-100).
    
    Lower score = higher risk
    Higher score = lower risk
    
    Components:
    - PD impact (30% weight)
    - LGD impact (20% weight)
    - DTI ratio (15% weight)
    - LTV ratio (15% weight)
    - Credit score (10% weight)
    - Income stability (5% weight)
    - Collateral quality (5% weight)
    
    Args:
        probability_of_default: PD percentage
        loss_given_default: LGD percentage
        dti_ratio: DTI ratio percentage
        ltv_ratio: LTV ratio percentage
        credit_score: Credit score (300-850)
        income_stability_score: Income stability (0-100)
        collateral_quality_score: Collateral quality (0-100)
        
    Returns:
        Dictionary with risk score and level
    """
    # PD component (inverse - lower PD = higher score)
    pd_score = max(0, 100 - probability_of_default)
    
    # LGD component (inverse - lower LGD = higher score)
    lgd_score = max(0, 100 - loss_given_default)
    
    # DTI component
    if dti_ratio < 20:
        dti_score = 100
    elif dti_ratio < 28:
        dti_score = 85
    elif dti_ratio < 36:
        dti_score = 70
    elif dti_ratio < 43:
        dti_score = 50
    else:
        dti_score = 25
    
    # LTV component
    if ltv_ratio < 60:
        ltv_score = 100
    elif ltv_ratio < 75:
        ltv_score = 85
    elif ltv_ratio < 85:
        ltv_score = 70
    elif ltv_ratio < 95:
        ltv_score = 50
    else:
        ltv_score = 25
    
    # Credit score component (normalize to 0-100)
    credit_normalized = ((credit_score - 300) / (850 - 300)) * 100
    credit_normalized = max(0, min(100, credit_normalized))
    
    # Weighted average
    risk_score = (
        pd_score * 0.30 +
        lgd_score * 0.20 +
        dti_score * 0.15 +
        ltv_score * 0.15 +
        credit_normalized * 0.10 +
        income_stability_score * 0.05 +
        collateral_quality_score * 0.05
    )
    
    # Determine risk level
    if risk_score >= 80:
        risk_level = "low"
    elif risk_score >= 65:
        risk_level = "moderate"
    elif risk_score >= 50:
        risk_level = "elevated"
    elif risk_score >= 35:
        risk_level = "high"
    else:
        risk_level = "very_high"
    
    return {
        "risk_score": round(risk_score, 2),
        "overall_risk_level": risk_level,
        "component_scores": {
            "pd_score": round(pd_score, 2),
            "lgd_score": round(lgd_score, 2),
            "dti_score": round(dti_score, 2),
            "ltv_score": round(ltv_score, 2),
            "credit_score": round(credit_normalized, 2),
            "income_stability_score": round(income_stability_score, 2),
            "collateral_quality_score": round(collateral_quality_score, 2)
        }
    }


def calculate_capital_requirement(
    loan_amount: float,
    risk_weight: float,
    minimum_capital_ratio: float = 8.0
) -> Dict[str, float]:
    """
    Calculate regulatory capital requirement (Basel III).
    
    Capital Requirement = Loan Amount × Risk Weight × Minimum Capital Ratio
    
    Risk weights:
    - Low risk (AAA-AA): 20%
    - Medium risk (A-BBB): 50%
    - High risk (BB-B): 100%
    - Very high risk (CCC and below): 150%
    
    Args:
        loan_amount: Loan amount
        risk_weight: Risk weight percentage (20, 50, 100, 150)
        minimum_capital_ratio: Minimum capital ratio (default 8%)
        
    Returns:
        Dictionary with capital requirements
    """
    risk_weighted_assets = loan_amount * (risk_weight / 100)
    capital_required = risk_weighted_assets * (minimum_capital_ratio / 100)
    
    return {
        "loan_amount": round(loan_amount, 2),
        "risk_weight": risk_weight,
        "risk_weighted_assets": round(risk_weighted_assets, 2),
        "minimum_capital_ratio": minimum_capital_ratio,
        "capital_required": round(capital_required, 2)
    }
