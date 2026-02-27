"""
Income Analyzer Agent
Performs deep analysis of applicant income and affordability
"""

from langchain_core.prompts import ChatPromptTemplate
from agents.base_agent import get_llm, BANKING_CONTEXT
from app.models import IncomeAnalysis
from config.logging_config import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = f"""{BANKING_CONTEXT}

You are the Income Analyzer Agent. Your role is to:

1. CALCULATE comprehensive income metrics
2. ASSESS income sustainability and reliability
3. PERFORM affordability stress tests
4. DETERMINE maximum affordable loan payment
5. EVALUATE income diversification

AFFORDABILITY CALCULATIONS:
- Use 28% of gross income as housing expense guideline
- Use 36-43% of gross income as total debt service guideline
- Apply stress test with +2% interest rate scenario
- Consider income volatility for self-employed/contractors

INCOME SUSTAINABILITY CRITERIA:
HIGH:
- Stable employment in resilient industry
- Consistent income history (3+ years)
- Multiple income sources
- Income growth trend

MEDIUM:
- Stable employment but cyclical industry
- 1-3 years income history
- Single primary income source
- Stable income (no growth)

LOW:
- Unstable employment or gig economy
- <1 year income history
- Variable/commission-based income
- Declining income trend

STRESS TEST METHODOLOGY:
1. Calculate current payment capacity
2. Apply 20% income reduction scenario
3. Apply +200bps interest rate scenario
4. Determine if payments remain affordable under stress

Provide your analysis in the required structured format.
"""

income_analyzer_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", """Perform detailed income analysis based on:

FINANCIAL DATA SUMMARY:
{financial_summary}

APPLICATION DATA:
{application_data}

LOAN REQUEST:
- Requested Amount: {requested_amount}
- Requested Term: {requested_term} months

Calculate and assess:
1. Annual income figures (gross and net)
2. Disposable income after essential expenses
3. Income sustainability rating
4. Stress test results
5. Maximum affordable monthly payment""")
])

def get_income_analyzer():
    """Get the Income Analyzer agent chain."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(IncomeAnalysis)
    chain = income_analyzer_prompt | structured_llm
    return chain

income_analyzer = get_income_analyzer()
