"""
Risk Scorer Agent
Calculates comprehensive risk scores and probability of default
"""

from langchain_core.prompts import ChatPromptTemplate
from agents.base_agent import get_llm, BANKING_CONTEXT
from app.models import RiskAssessment
from config.logging_config import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = f"""{BANKING_CONTEXT}

You are the Risk Scorer Agent. Your role is to:

1. CALCULATE comprehensive risk score (0-100, higher = riskier)
2. ESTIMATE probability of default (PD)
3. ESTIMATE loss given default (LGD)
4. COMPUTE expected loss
5. ASSIGN regulatory risk classification

RISK SCORE COMPONENTS (weights):
- Credit History (30%): Based on credit score, payment history, delinquencies
- Income Stability (25%): Based on employment, income consistency
- Debt Burden (25%): Based on DTI, DSCR, utilization
- Collateral (10%): Based on LTV, collateral quality
- Employment (10%): Based on job stability, industry

COMPONENT SCORING (0-100, where 100 = best/lowest risk):

CREDIT HISTORY SCORE:
- Credit score mapping: (credit_score - 300) / 5.5
- Adjust for: delinquencies (-10 per 30-day), bankruptcies (-30), collections (-15)

INCOME STABILITY SCORE:
- Use income_stability_score from financial analysis
- Adjust for: income trend (+10 increasing, -10 decreasing)

DEBT BURDEN SCORE:
- DTI < 30%: 90-100
- DTI 30-36%: 70-89
- DTI 36-43%: 50-69
- DTI 43-50%: 30-49
- DTI > 50%: 0-29

COLLATERAL SCORE:
- LTV < 60%: 90-100
- LTV 60-80%: 70-89
- LTV 80-90%: 50-69
- LTV 90-100%: 30-49
- No collateral/LTV > 100%: 20-29

PROBABILITY OF DEFAULT (PD) ESTIMATION:
Based on risk score:
- Score 0-20: PD 0.5-1%
- Score 21-40: PD 1-3%
- Score 41-60: PD 3-7%
- Score 61-80: PD 7-15%
- Score 81-100: PD 15-30%

LOSS GIVEN DEFAULT (LGD):
- Secured with excellent collateral: 20-30%
- Secured with good collateral: 30-45%
- Secured with fair collateral: 45-60%
- Unsecured: 60-80%

EXPECTED LOSS = PD × LGD × Exposure at Default (EAD)

RISK LEVEL CLASSIFICATION:
- VERY_LOW: Score 0-20
- LOW: Score 21-40
- MEDIUM: Score 41-60
- HIGH: Score 61-80
- VERY_HIGH: Score 81-100

BASEL RISK WEIGHT (for regulatory capital):
- Retail exposures: 75% standard
- Residential mortgage: 35% (LTV<80%), 50% (LTV 80-90%), 75% (LTV>90%)
- High-risk: 150%

Output your complete risk assessment in the required format.
"""

risk_scorer_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", """Calculate comprehensive risk assessment based on all analyses:

FINANCIAL SUMMARY:
{financial_summary}

INCOME ANALYSIS:
{income_analysis}

DEBT ANALYSIS:
{debt_analysis}

COLLATERAL EVALUATION:
{collateral_evaluation}

CREDIT HISTORY:
{credit_history}

LOAN DETAILS:
- Amount: {requested_amount}
- Term: {requested_term} months
- Purpose: {loan_purpose}

Provide:
1. Overall risk level and score
2. Component score breakdown
3. Probability of default estimate
4. Loss given default estimate
5. Expected loss calculation
6. Key risk factors
7. Mitigating factors
8. Regulatory flags
9. Basel risk weight""")
])

def get_risk_scorer():
    """Get the Risk Scorer agent chain."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(RiskAssessment)
    chain = risk_scorer_prompt | structured_llm
    return chain

risk_scorer = get_risk_scorer()
