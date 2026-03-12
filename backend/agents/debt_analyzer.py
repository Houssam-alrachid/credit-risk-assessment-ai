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

1. INTERPRET pre-calculated debt metrics
2. ASSESS debt burden sustainability (qualitative)
3. EVALUATE debt management behavior
4. IDENTIFY payment patterns and risks
5. ANALYZE debt structure quality and composition

NOTE: Mathematical calculations (DTI, DSCR, debt totals) are provided to you 
pre-calculated. Focus on QUALITATIVE analysis:
- Debt composition quality (secured vs unsecured, rates)
- Payment history patterns and behavior
- Debt management strategy assessment
- Future debt trajectory and risks
- Credit utilization strategy

DTI RATIO INTERPRETATION:
EXCELLENT: < 20%
GOOD: 20-28%
ACCEPTABLE: 28-36%
HIGH: 36-43%
VERY HIGH: > 43%

DSCR (Debt Service Coverage Ratio) INTERPRETATION:
STRONG: > 2.0
GOOD: 1.5-2.0
ACCEPTABLE: 1.25-1.5
WEAK: 1.0-1.25
CRITICAL: < 1.0

QUALITATIVE ASSESSMENT FOCUS:

DEBT STRUCTURE EVALUATION:
- Secured vs unsecured debt mix quality
- Fixed vs variable rate exposure risks
- Short-term vs long-term obligation balance
- Concentration risk (single large creditor)
- Debt diversification strategy

PAYMENT BEHAVIOR PATTERNS:
- Payment history consistency
- Refinancing/consolidation patterns
- Credit line management
- Debt balance trends

RED FLAGS TO IDENTIFY:
- Maxed out credit lines
- Multiple recent credit inquiries
- Pattern of frequent refinancing
- Increasing debt balances without income growth
- Payment history issues or late payments

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

PRE-CALCULATED METRICS (use these, do not recalculate):
{calculations}

Your task is QUALITATIVE ANALYSIS:
1. Assess debt composition quality (types, rates, terms)
2. Evaluate payment history and behavior patterns
3. Analyze debt management strategy
4. Identify payment shock risks
5. Assess credit utilization strategy
6. Evaluate debt structure sustainability
7. Identify debt-related red flags and risks

IMPORTANT: Use the pre-calculated DTI, DSCR, and debt totals. Focus on 
interpreting them and providing qualitative insights about debt management, 
composition quality, and sustainability.""")
])

def get_debt_analyzer():
    """Get the Debt Analyzer agent chain."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(DebtAnalysis)
    chain = debt_analyzer_prompt | structured_llm
    return chain

debt_analyzer = get_debt_analyzer()
