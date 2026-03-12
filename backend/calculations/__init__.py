"""
Financial calculations module for credit risk assessment.

This module provides deterministic, auditable financial calculations
separate from LLM-based qualitative analysis.
"""

from .income_calculations import (
    calculate_annual_income,
    calculate_disposable_income,
    calculate_max_affordable_payment,
    perform_income_stress_test,
)

from .debt_calculations import (
    calculate_estimated_payment,
    calculate_dti_ratio,
    calculate_dscr,
    calculate_total_monthly_debt,
    assess_debt_burden,
)

from .collateral_calculations import (
    calculate_ltv_ratio,
    calculate_liquidation_value,
    assess_collateral_quality,
)

from .risk_calculations import (
    calculate_probability_of_default,
    calculate_loss_given_default,
    calculate_expected_loss,
    calculate_risk_score,
)

# Export all functions for easy import
# The __all__ list explicitly defines which functions are publicly available 
# when someone does from calculations import *.
__all__ = [
    # Income calculations
    "calculate_annual_income",
    "calculate_disposable_income",
    "calculate_max_affordable_payment",
    "perform_income_stress_test",
    # Debt calculations
    "calculate_estimated_payment",
    "calculate_dti_ratio",
    "calculate_dscr",
    "calculate_total_monthly_debt",
    "assess_debt_burden",
    # Collateral calculations
    "calculate_ltv_ratio",
    "calculate_liquidation_value",
    "assess_collateral_quality",
    # Risk calculations
    "calculate_probability_of_default",
    "calculate_loss_given_default",
    "calculate_expected_loss",
    "calculate_risk_score",
]
