"""
Pydantic Models for Credit Risk Assessment
Structured data models for loan applications, analysis, and reports
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal
from datetime import date, datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class EmploymentType(str, Enum):
    EMPLOYED = "employed"
    SELF_EMPLOYED = "self_employed"
    CONTRACTOR = "contractor"
    RETIRED = "retired"
    UNEMPLOYED = "unemployed"
    STUDENT = "student"


class LoanPurpose(str, Enum):
    MORTGAGE = "mortgage"
    AUTO = "auto"
    PERSONAL = "personal"
    BUSINESS = "business"
    EDUCATION = "education"
    DEBT_CONSOLIDATION = "debt_consolidation"
    HOME_IMPROVEMENT = "home_improvement"
    OTHER = "other"


class CollateralType(str, Enum):
    REAL_ESTATE = "real_estate"
    VEHICLE = "vehicle"
    SAVINGS = "savings"
    INVESTMENT_PORTFOLIO = "investment_portfolio"
    BUSINESS_ASSETS = "business_assets"
    NONE = "none"


class RiskLevel(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class DecisionType(str, Enum):
    APPROVED = "approved"
    APPROVED_WITH_CONDITIONS = "approved_with_conditions"
    MANUAL_REVIEW = "manual_review"
    DECLINED = "declined"


# ============================================================================
# INPUT MODELS
# ============================================================================

class ApplicantInfo(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date = Field(...)
    nationality: str = Field(default="FR")
    tax_id: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)

    @field_validator("date_of_birth")
    @classmethod
    def validate_age(cls, v: date) -> date:
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 18:
            raise ValueError("Applicant must be at least 18 years old")
        if age > 100:
            raise ValueError("Invalid date of birth")
        return v


class EmploymentInfo(BaseModel):
    employment_type: EmploymentType = Field(...)
    employer_name: Optional[str] = Field(default=None)
    job_title: Optional[str] = Field(default=None)
    industry: Optional[str] = Field(default=None)
    years_employed: float = Field(ge=0)
    years_in_profession: float = Field(ge=0)
    monthly_gross_income: float = Field(gt=0)
    monthly_net_income: float = Field(gt=0)
    additional_income: float = Field(default=0, ge=0)
    income_verified: bool = Field(default=False)


class ExistingDebt(BaseModel):
    debt_type: str = Field(...)
    creditor_name: str = Field(...)
    original_amount: float = Field(gt=0)
    current_balance: float = Field(ge=0)
    monthly_payment: float = Field(ge=0)
    interest_rate: float = Field(ge=0, le=100)
    remaining_months: int = Field(ge=0)
    is_secured: bool = Field(default=False)
    payment_history: Literal["excellent", "good", "fair", "poor"] = Field(default="good")


class CollateralInfo(BaseModel):
    collateral_type: CollateralType = Field(...)
    description: str = Field(...)
    estimated_value: float = Field(gt=0)
    valuation_date: date = Field(...)
    valuation_source: str = Field(...)
    encumbrances: float = Field(default=0, ge=0)
    insurance_coverage: Optional[float] = Field(default=None)


class LoanRequest(BaseModel):
    loan_purpose: LoanPurpose = Field(...)
    requested_amount: float = Field(gt=0)
    requested_term_months: int = Field(gt=0, le=480)
    preferred_payment_day: int = Field(default=1, ge=1, le=28)
    purpose_description: Optional[str] = Field(default=None)


class CreditHistory(BaseModel):
    credit_score: int = Field(ge=300, le=850)
    credit_score_source: str = Field(default="bureau")
    accounts_open: int = Field(ge=0)
    accounts_closed: int = Field(ge=0)
    oldest_account_years: float = Field(ge=0)
    recent_inquiries: int = Field(ge=0)
    delinquencies_30_days: int = Field(default=0, ge=0)
    delinquencies_60_days: int = Field(default=0, ge=0)
    delinquencies_90_days: int = Field(default=0, ge=0)
    bankruptcies: int = Field(default=0, ge=0)
    foreclosures: int = Field(default=0, ge=0)
    collections: int = Field(default=0, ge=0)


class LoanApplication(BaseModel):
    application_id: Optional[str] = Field(default=None)
    applicant: ApplicantInfo = Field(...)
    employment: EmploymentInfo = Field(...)
    existing_debts: List[ExistingDebt] = Field(default_factory=list)
    collateral: Optional[CollateralInfo] = Field(default=None)
    loan_request: LoanRequest = Field(...)
    credit_history: CreditHistory = Field(...)


# ============================================================================
# ANALYSIS MODELS - Agent Outputs
# ============================================================================

class FinancialDataSummary(BaseModel):
    total_monthly_income: float = Field(...)
    income_stability_score: float = Field(ge=0, le=100)
    income_sources: List[str] = Field(...)
    employment_stability: str = Field(...)
    income_trend: Literal["increasing", "stable", "decreasing"] = Field(...)
    verification_status: str = Field(...)
    red_flags: List[str] = Field(default_factory=list)
    data_quality_score: int = Field(ge=1, le=10)


class IncomeAnalysis(BaseModel):
    gross_annual_income: float = Field(...)
    net_annual_income: float = Field(...)
    income_to_expense_ratio: float = Field(...)
    disposable_income_monthly: float = Field(...)
    income_sustainability: Literal["high", "medium", "low"] = Field(...)
    income_diversification: float = Field(ge=0, le=100)
    stress_test_result: str = Field(...)
    max_affordable_payment: float = Field(...)
    analysis_notes: List[str] = Field(default_factory=list)


class DebtAnalysis(BaseModel):
    total_existing_debt: float = Field(...)
    total_monthly_debt_payments: float = Field(...)
    debt_to_income_ratio: float = Field(...)
    projected_dti_ratio: float = Field(...)
    debt_service_coverage_ratio: float = Field(...)
    utilization_rate: float = Field(ge=0, le=100)
    debt_structure_assessment: str = Field(...)
    payment_shock_risk: Literal["low", "medium", "high"] = Field(...)
    debt_consolidation_benefit: Optional[str] = Field(default=None)
    debt_red_flags: List[str] = Field(default_factory=list)


class CollateralEvaluation(BaseModel):
    collateral_present: bool = Field(...)
    collateral_type: Optional[str] = Field(default=None)
    estimated_value: float = Field(default=0)
    loan_to_value_ratio: float = Field(default=100)
    collateral_quality: Literal["excellent", "good", "fair", "poor", "none"] = Field(default="none")
    liquidation_value: float = Field(default=0)
    collateral_coverage_ratio: float = Field(default=0)
    valuation_confidence: Literal["high", "medium", "low"] = Field(default="low")
    collateral_risks: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class RiskScoreBreakdown(BaseModel):
    credit_history_score: float = Field(ge=0, le=100)
    income_stability_score: float = Field(ge=0, le=100)
    debt_burden_score: float = Field(ge=0, le=100)
    collateral_score: float = Field(ge=0, le=100)
    employment_score: float = Field(ge=0, le=100)

    @property
    def weighted_total(self) -> float:
        weights = {
            "credit_history": 0.30,
            "income_stability": 0.25,
            "debt_burden": 0.25,
            "collateral": 0.10,
            "employment": 0.10
        }
        return (
            self.credit_history_score * weights["credit_history"] +
            self.income_stability_score * weights["income_stability"] +
            self.debt_burden_score * weights["debt_burden"] +
            self.collateral_score * weights["collateral"] +
            self.employment_score * weights["employment"]
        )


class RiskAssessment(BaseModel):
    overall_risk_level: RiskLevel = Field(...)
    risk_score: int = Field(ge=0, le=100)
    probability_of_default: float = Field(ge=0, le=100)
    loss_given_default: float = Field(ge=0, le=100)
    expected_loss: float = Field(ge=0)
    score_breakdown: RiskScoreBreakdown = Field(...)
    risk_factors: List[str] = Field(...)
    mitigating_factors: List[str] = Field(...)
    regulatory_flags: List[str] = Field(default_factory=list)
    basel_risk_weight: float = Field(ge=0, le=150)


# ============================================================================
# DECISION MODELS
# ============================================================================

class LoanTerms(BaseModel):
    approved_amount: float = Field(...)
    interest_rate: float = Field(ge=0, le=100)
    term_months: int = Field(...)
    monthly_payment: float = Field(...)
    total_interest: float = Field(...)
    total_repayment: float = Field(...)
    annual_percentage_rate: float = Field(...)
    fees: float = Field(default=0)


class CreditDecision(BaseModel):
    decision: DecisionType = Field(...)
    decision_date: datetime = Field(default_factory=datetime.utcnow)
    confidence_score: float = Field(ge=0, le=100)
    approved_terms: Optional[LoanTerms] = Field(default=None)
    conditions: List[str] = Field(default_factory=list)
    decline_reasons: List[str] = Field(default_factory=list)
    manual_review_reasons: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)
    validity_days: int = Field(default=30)


# ============================================================================
# FINAL REPORT MODEL
# ============================================================================

class CreditAssessmentReport(BaseModel):
    report_id: str = Field(...)
    application_id: str = Field(...)
    report_date: datetime = Field(default_factory=datetime.utcnow)
    applicant_name: str = Field(...)
    
    financial_summary: FinancialDataSummary = Field(...)
    income_analysis: IncomeAnalysis = Field(...)
    debt_analysis: DebtAnalysis = Field(...)
    collateral_evaluation: CollateralEvaluation = Field(...)
    risk_assessment: RiskAssessment = Field(...)
    credit_decision: CreditDecision = Field(...)
    
    executive_summary: str = Field(...)
    detailed_analysis: str = Field(...)
    recommendations: List[str] = Field(...)
    
    processing_time_seconds: float = Field(...)
    trace_id: Optional[str] = Field(default=None)
    model_version: str = Field(default="1.0.0")


# ============================================================================
# API REQUEST/RESPONSE MODELS
# ============================================================================

class AssessmentRequest(BaseModel):
    application: LoanApplication = Field(...)
    fast_mode: bool = Field(default=False)
    include_detailed_report: bool = Field(default=True)


class AssessmentResponse(BaseModel):
    success: bool = Field(...)
    report: Optional[CreditAssessmentReport] = Field(default=None)
    error: Optional[str] = Field(default=None)
    processing_time_seconds: float = Field(...)
    trace_url: Optional[str] = Field(default=None)


class HealthResponse(BaseModel):
    status: str = Field(...)
    version: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ProgressUpdate(BaseModel):
    status: str = Field(...)
    progress: int = Field(ge=0, le=100)
    stage: str = Field(...)
    data: Optional[dict] = Field(default=None)
