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

1. INTERPRET pre-calculated risk metrics (PD, LGD, EL, risk score)
2. ASSESS risk factors and their interactions (qualitative)
3. IDENTIFY mitigating and aggravating circumstances
4. EVALUATE risk trends and trajectories
5. PROVIDE risk mitigation recommendations

NOTE: Mathematical calculations (PD, LGD, EL, risk score, Basel weights) 
are provided to you pre-calculated. Focus on QUALITATIVE analysis:
- Risk factor interpretation and interactions
- Mitigating circumstances assessment
- Aggravating factors identification
- Risk trend analysis
- Comparative risk assessment
- Risk mitigation strategies

RISK LEVEL INTERPRETATION:
- VERY_LOW: Minimal default risk, strong creditworthiness
- LOW: Below-average risk, good credit profile
- MEDIUM: Average risk, acceptable with monitoring
- HIGH: Above-average risk, requires mitigation
- VERY_HIGH: Significant default risk, careful consideration needed

QUALITATIVE ASSESSMENT FOCUS:
- Risk factor interactions and compounding effects
- Mitigating circumstances (guarantors, insurance, etc.)
- Aggravating factors (industry downturn, market conditions)
- Risk trajectory (improving, stable, deteriorating)
- Comparative risk assessment vs portfolio
- Risk mitigation strategies and recommendations
- Regulatory considerations and flags
- Basel III capital requirement implications

Output your complete risk assessment in the required format.
"""

risk_scorer_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", """Perform comprehensive risk assessment based on all analyses:

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

PRE-CALCULATED METRICS (use these, do not recalculate):
{calculations}

Your task is QUALITATIVE ANALYSIS:
1. Interpret the calculated risk score and its components
2. Assess interactions between risk factors
3. Identify key risk drivers and their severity
4. Evaluate mitigating circumstances and their impact
5. Identify aggravating factors
6. Assess risk trajectory (improving/stable/deteriorating)
7. Provide risk mitigation recommendations
8. Identify regulatory considerations

IMPORTANT: Use the pre-calculated PD, LGD, EL, and risk scores. Focus on 
interpreting them and providing qualitative insights about risk factors, 
mitigating circumstances, and risk management strategies.""")
])

def get_risk_scorer():
    """Get the Risk Scorer agent chain."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(RiskAssessment)
    chain = risk_scorer_prompt | structured_llm
    return chain

risk_scorer = get_risk_scorer()
