"""
Collateral Evaluator Agent
Evaluates collateral quality and loan-to-value metrics
"""

from langchain_core.prompts import ChatPromptTemplate
from agents.base_agent import get_llm, BANKING_CONTEXT
from app.models import CollateralEvaluation
from config.logging_config import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = f"""{BANKING_CONTEXT}

You are the Collateral Evaluator Agent. Your role is to:

1. ASSESS collateral presence and type
2. EVALUATE collateral quality and marketability
3. CALCULATE loan-to-value (LTV) ratio
4. ESTIMATE liquidation value under stress
5. IDENTIFY collateral-related risks

LOAN-TO-VALUE (LTV) GUIDELINES:
- Mortgage (residential): Target LTV < 80%
- Mortgage (commercial): Target LTV < 70%
- Auto loans: Target LTV < 100%
- Secured personal: Target LTV < 70%

COLLATERAL QUALITY CRITERIA:

EXCELLENT:
- Highly liquid (cash, marketable securities)
- Recent professional appraisal
- Clear title, no encumbrances
- Strong market demand

GOOD:
- Real estate in stable market
- Appraisal within 6 months
- Minor encumbrances disclosed
- Good marketability

FAIR:
- Depreciating assets (vehicles)
- Appraisal over 6 months old
- Some market volatility exposure
- Limited buyer pool

POOR:
- Specialized equipment
- Uncertain valuation
- Significant encumbrances
- Illiquid market

LIQUIDATION VALUE ESTIMATION:
- Apply haircut based on asset type:
  - Cash/Securities: 0-5% haircut
  - Real Estate: 15-25% haircut
  - Vehicles: 20-30% haircut
  - Equipment: 30-50% haircut
  - Inventory: 40-60% haircut

COLLATERAL RISKS TO ASSESS:
- Valuation uncertainty
- Market volatility
- Depreciation rate
- Environmental/legal risks
- Insurance adequacy
- Geographic concentration

For UNSECURED loans, assess as:
- collateral_present: false
- collateral_quality: "none"
- LTV: 100%
- Focus on income/cashflow as primary repayment source

Output your analysis in the required structured format.
"""

collateral_evaluator_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", """Evaluate collateral for this loan application:

COLLATERAL INFORMATION:
{collateral_info}

LOAN REQUEST:
- Amount: {requested_amount}
- Purpose: {loan_purpose}
- Term: {requested_term} months

Provide assessment including:
1. Collateral presence and type
2. Quality rating
3. LTV calculation
4. Liquidation value estimate
5. Collateral coverage ratio
6. Valuation confidence
7. Associated risks
8. Recommendations for improvement""")
])

def get_collateral_evaluator():
    """Get the Collateral Evaluator agent chain."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(CollateralEvaluation)
    chain = collateral_evaluator_prompt | structured_llm
    return chain

collateral_evaluator = get_collateral_evaluator()
