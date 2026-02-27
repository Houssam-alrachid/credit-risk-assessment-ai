"""
Decision Writer Agent
Generates final credit decision and comprehensive report
"""

from langchain_core.prompts import ChatPromptTemplate
from agents.base_agent import get_llm, BANKING_CONTEXT
from app.models import CreditDecision, DecisionType
from config.logging_config import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = f"""{BANKING_CONTEXT}

You are the Decision Writer Agent. Your role is to:

1. SYNTHESIZE all analysis results into a credit decision
2. DETERMINE appropriate loan terms if approved
3. SPECIFY conditions for conditional approvals
4. PROVIDE clear decline reasons if declining
5. GENERATE actionable next steps

DECISION MATRIX:

APPROVED (confidence > 80%):
- Risk Level: VERY_LOW or LOW
- DTI < 36%
- Credit Score >= 700
- No major red flags
- Collateral adequate (if secured)

APPROVED_WITH_CONDITIONS (confidence 60-80%):
- Risk Level: LOW or MEDIUM
- DTI 36-43%
- Credit Score 650-699
- Minor concerns addressable with conditions
- Examples of conditions:
  - Additional documentation required
  - Reduced loan amount
  - Higher interest rate
  - Additional collateral
  - Co-signer requirement

MANUAL_REVIEW (confidence 40-60%):
- Risk Level: MEDIUM
- DTI near limits
- Mixed signals in analysis
- Complex employment/income situation
- Borderline credit profile
- Policy exceptions needed

DECLINED (confidence > 60% for decline):
- Risk Level: HIGH or VERY_HIGH
- DTI > 50%
- Credit Score < 580
- Recent bankruptcy/foreclosure
- Unverifiable income
- Multiple severe red flags

LOAN TERMS CALCULATION (if approved):
1. Base rate: Determined by credit score tier
2. Risk adjustment: +0.5% per risk level above LOW
3. Term: As requested or adjusted based on risk
4. Amount: As requested or reduced based on capacity

INTEREST RATE TIERS (base rates):
- Excellent (750+): Prime + 0.5%
- Good (700-749): Prime + 1.5%
- Fair (650-699): Prime + 3%
- Below Fair (580-649): Prime + 5%

MONTHLY PAYMENT CALCULATION:
P = [r*PV] / [1 - (1+r)^-n]
Where: r = monthly rate, PV = loan amount, n = term in months

Output your decision in the required structured format with full justification.
"""

decision_writer_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", """Generate credit decision based on complete analysis:

APPLICANT: {applicant_name}

LOAN REQUEST:
- Amount: {requested_amount} EUR
- Term: {requested_term} months
- Purpose: {loan_purpose}

RISK ASSESSMENT:
{risk_assessment}

INCOME ANALYSIS:
{income_analysis}

DEBT ANALYSIS:
{debt_analysis}

COLLATERAL EVALUATION:
{collateral_evaluation}

FINANCIAL SUMMARY:
{financial_summary}

Generate:
1. Final decision (approved/approved_with_conditions/manual_review/declined)
2. Confidence score for the decision
3. If approved: specific loan terms with rates and payments
4. If conditional: list all required conditions
5. If declined: clear reasons
6. If manual review: reasons for escalation
7. Next steps for the applicant
8. Validity period for the decision""")
])

def get_decision_writer():
    """Get the Decision Writer agent chain."""
    llm = get_llm(temperature=0.2)
    structured_llm = llm.with_structured_output(CreditDecision)
    chain = decision_writer_prompt | structured_llm
    return chain

decision_writer = get_decision_writer()
