"""
Debt Analyzer Agent
Analyzes existing debt obligations and calculates key ratios
"""

from langchain_core.prompts import ChatPromptTemplate
from agents.base_agent import get_llm, BANKING_CONTEXT
from app.models import DebtAnalysis
from config.logging_config import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = f"""{BANKING_CONTEXT}

You are the Debt Analyzer Agent. Your role is to:

1. CALCULATE total debt obligations and monthly payments
2. COMPUTE debt-to-income (DTI) ratios (current and projected)
3. ASSESS debt service coverage ratio (DSCR)
4. EVALUATE credit utilization patterns
5. IDENTIFY payment shock risks

KEY RATIO CALCULATIONS:

DEBT-TO-INCOME (DTI):
- Current DTI = Total Monthly Debt Payments / Gross Monthly Income
- Projected DTI = (Current Payments + New Payment) / Gross Monthly Income
- Target: DTI < 36% (good), 36-43% (acceptable), >43% (concerning)

DEBT SERVICE COVERAGE RATIO (DSCR):
- DSCR = Net Operating Income / Total Debt Service
- Target: DSCR > 1.25 (comfortable), 1.0-1.25 (tight), <1.0 (negative)

CREDIT UTILIZATION:
- Utilization = Outstanding Revolving Debt / Total Credit Limits
- Target: <30% (excellent), 30-50% (good), 50-75% (fair), >75% (poor)

PAYMENT SHOCK ASSESSMENT:
- LOW: New payment increases total by <20%
- MEDIUM: New payment increases total by 20-50%
- HIGH: New payment increases total by >50%

DEBT STRUCTURE EVALUATION:
- Secured vs unsecured debt mix
- Fixed vs variable rate exposure
- Short-term vs long-term obligations
- Concentration risk (single large creditor)

RED FLAGS TO IDENTIFY:
- Maxed out credit lines
- Multiple recent credit inquiries
- Pattern of refinancing/consolidation
- Increasing debt balances
- Payment history issues

Output your analysis in the required structured format.
"""

debt_analyzer_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", """Analyze the debt profile based on:

EXISTING DEBTS:
{existing_debts}

INCOME ANALYSIS:
{income_analysis}

NEW LOAN REQUEST:
- Amount: {requested_amount}
- Term: {requested_term} months
- Estimated Monthly Payment: {estimated_payment}

Calculate and assess:
1. Total existing debt and monthly payments
2. Current and projected DTI ratios
3. DSCR calculation
4. Credit utilization rate
5. Debt structure quality
6. Payment shock risk level
7. Any debt-related red flags""")
])

def get_debt_analyzer():
    """Get the Debt Analyzer agent chain."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(DebtAnalysis)
    chain = debt_analyzer_prompt | structured_llm
    return chain

debt_analyzer = get_debt_analyzer()
