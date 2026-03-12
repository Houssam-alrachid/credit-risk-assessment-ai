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

1. INTERPRET pre-calculated collateral metrics
2. ASSESS collateral quality and marketability (qualitative)
3. EVALUATE title, legal, and insurance considerations
4. IDENTIFY market conditions and liquidation risks
5. PROVIDE collateral improvement recommendations

NOTE: Mathematical calculations (LTV ratio, liquidation value, coverage ratios) 
are provided to you pre-calculated. Focus on QUALITATIVE analysis:
- Collateral marketability and demand
- Title clarity and legal encumbrances
- Market conditions and volatility
- Liquidation timeline and process
- Insurance adequacy
- Alternative collateral options

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

QUALITATIVE ASSESSMENT FOCUS:
- Collateral marketability and demand
- Title clarity and legal encumbrances
- Market conditions and volatility
- Liquidation timeline and process complexity
- Insurance coverage adequacy
- Environmental or legal risks
- Geographic market concentration
- Alternative collateral options
- Valuation confidence and uncertainty

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

PRE-CALCULATED METRICS (use these, do not recalculate):
{calculations}

Your task is QUALITATIVE ANALYSIS:
1. Assess collateral marketability and liquidity
2. Evaluate title clarity and legal considerations
3. Analyze market conditions and demand
4. Assess liquidation timeline and process complexity
5. Evaluate insurance coverage adequacy
6. Identify valuation risks and uncertainties
7. Provide recommendations for collateral improvement
8. Suggest alternative collateral if applicable

IMPORTANT: Use the pre-calculated LTV ratio, liquidation value, and coverage ratios. 
Focus on interpreting them and providing qualitative insights about marketability, 
legal considerations, and market conditions.""")
])

def get_collateral_evaluator():
    """Get the Collateral Evaluator agent chain."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(CollateralEvaluation)
    chain = collateral_evaluator_prompt | structured_llm
    return chain

collateral_evaluator = get_collateral_evaluator()
