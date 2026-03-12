"""
Collateral-related financial calculations.

All calculations are deterministic and follow standard banking formulas.
"""

from typing import Dict, Any, Optional


def calculate_ltv_ratio(
    loan_amount: float,
    collateral_value: float
) -> float:
    """
    Calculate Loan-to-Value (LTV) ratio.
    
    LTV = (Loan Amount / Collateral Value) × 100
    
    Args:
        loan_amount: Requested loan amount
        collateral_value: Appraised collateral value
        
    Returns:
        LTV ratio as percentage
    """
    if collateral_value <= 0:
        return 999.0  # Invalid LTV
    
    return (loan_amount / collateral_value) * 100


def calculate_liquidation_value(
    market_value: float,
    collateral_type: str,
    condition: str = "good"
) -> Dict[str, float]:
    """
    Calculate liquidation value based on collateral type and condition.
    
    Liquidation discounts:
    - Real Estate: 15-30% discount
    - Vehicles: 25-40% discount
    - Equipment: 30-50% discount
    - Securities: 5-15% discount
    - Other: 40-60% discount
    
    Args:
        market_value: Current market value
        collateral_type: Type of collateral
        condition: Condition (excellent, good, fair, poor)
        
    Returns:
        Dictionary with liquidation values
    """
    # Base discount by collateral type
    type_discounts = {
        "real_estate": 0.20,
        "residential_property": 0.20,
        "commercial_property": 0.25,
        "vehicle": 0.30,
        "equipment": 0.40,
        "securities": 0.10,
        "inventory": 0.50,
        "other": 0.50
    }
    
    # Condition adjustments
    condition_adjustments = {
        "excellent": -0.05,  # Better condition = less discount
        "good": 0.00,
        "fair": 0.10,
        "poor": 0.20
    }
    
    base_discount = type_discounts.get(collateral_type.lower(), 0.50)
    condition_adjustment = condition_adjustments.get(condition.lower(), 0.00)
    
    total_discount = min(0.80, base_discount + condition_adjustment)  # Cap at 80% discount
    
    liquidation_value = market_value * (1 - total_discount)
    conservative_value = market_value * (1 - min(0.90, total_discount + 0.10))  # Extra conservative
    
    return {
        "market_value": round(market_value, 2),
        "liquidation_discount": round(total_discount * 100, 2),
        "liquidation_value": round(liquidation_value, 2),
        "conservative_value": round(conservative_value, 2),
        "recovery_rate": round((1 - total_discount) * 100, 2)
    }


def assess_collateral_quality(
    ltv_ratio: float,
    collateral_type: str,
    has_insurance: bool = False,
    has_clear_title: bool = True,
    marketability: str = "good"
) -> Dict[str, Any]:
    """
    Assess overall collateral quality.
    
    LTV Guidelines:
    - Excellent: < 60%
    - Good: 60-75%
    - Acceptable: 75-85%
    - High Risk: 85-95%
    - Very High Risk: > 95%
    
    Args:
        ltv_ratio: Loan-to-Value ratio
        collateral_type: Type of collateral
        has_insurance: Whether collateral is insured
        has_clear_title: Whether title is clear
        marketability: How easily collateral can be sold
        
    Returns:
        Dictionary with quality assessment
    """
    score = 50  # Base score
    
    # LTV assessment
    if ltv_ratio < 60:
        ltv_quality = "excellent"
        score += 30
    elif ltv_ratio < 75:
        ltv_quality = "good"
        score += 20
    elif ltv_ratio < 85:
        ltv_quality = "acceptable"
        score += 10
    elif ltv_ratio < 95:
        ltv_quality = "high_risk"
        score -= 10
    else:
        ltv_quality = "very_high_risk"
        score -= 30
    
    # Collateral type preference
    preferred_types = ["real_estate", "residential_property", "securities"]
    if collateral_type.lower() in preferred_types:
        score += 10
    
    # Insurance
    if has_insurance:
        score += 10
    else:
        score -= 5
    
    # Title clarity
    if not has_clear_title:
        score -= 20
    
    # Marketability
    marketability_scores = {
        "excellent": 15,
        "good": 10,
        "fair": 0,
        "poor": -15
    }
    score += marketability_scores.get(marketability.lower(), 0)
    
    # Clamp to 0-100
    final_score = max(0, min(100, score))
    
    # Overall quality
    if final_score >= 80:
        overall_quality = "excellent"
    elif final_score >= 65:
        overall_quality = "good"
    elif final_score >= 50:
        overall_quality = "acceptable"
    elif final_score >= 35:
        overall_quality = "weak"
    else:
        overall_quality = "poor"
    
    return {
        "ltv_quality": ltv_quality,
        "overall_quality": overall_quality,
        "quality_score": final_score,
        "has_insurance": has_insurance,
        "has_clear_title": has_clear_title,
        "marketability": marketability
    }


def calculate_collateral_coverage(
    loan_amount: float,
    liquidation_value: float,
    required_coverage: float = 1.2
) -> Dict[str, Any]:
    """
    Calculate collateral coverage ratio.
    
    Coverage Ratio = Liquidation Value / Loan Amount
    
    Typically require 1.2x coverage (120%) for adequate protection.
    
    Args:
        loan_amount: Loan amount
        liquidation_value: Estimated liquidation value
        required_coverage: Required coverage ratio (default 1.2)
        
    Returns:
        Dictionary with coverage analysis
    """
    if loan_amount <= 0:
        return {
            "coverage_ratio": 0,
            "meets_requirement": False,
            "shortfall": 0
        }
    
    coverage_ratio = liquidation_value / loan_amount
    meets_requirement = coverage_ratio >= required_coverage
    shortfall = max(0, (required_coverage * loan_amount) - liquidation_value)
    
    return {
        "coverage_ratio": round(coverage_ratio, 2),
        "required_coverage": required_coverage,
        "meets_requirement": meets_requirement,
        "shortfall": round(shortfall, 2),
        "excess_coverage": round(max(0, liquidation_value - (required_coverage * loan_amount)), 2)
    }
