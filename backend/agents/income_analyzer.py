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

1. INTERPRET pre-calculated income metrics
2. ASSESS income sustainability and reliability (qualitative)
3. EVALUATE income diversification and stability
4. IDENTIFY income-related risks and opportunities
5. PROVIDE recommendations based on calculations

NOTE: Mathematical calculations (annual income, max affordable payment, stress tests) 
are provided to you pre-calculated. Focus on QUALITATIVE analysis:
- Income source quality and stability
- Employment sector resilience
- Income growth potential
- Seasonal or cyclical risks
- Self-employment considerations

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

QUALITATIVE ASSESSMENT FOCUS:
- Employment sector resilience and outlook
- Income source diversification
- Seasonal or cyclical income patterns
- Income growth trajectory and potential
- Self-employment or contractor considerations
- Industry-specific risks

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

PRE-CALCULATED METRICS (use these, do not recalculate):
{calculations}

Your task is QUALITATIVE ANALYSIS:
1. Assess income source quality and sustainability
2. Evaluate employment stability and sector resilience
3. Identify income-related risks (seasonality, volatility, etc.)
4. Assess income growth potential
5. Provide recommendations based on the calculations provided

IMPORTANT: Use the pre-calculated values. Focus on interpreting them and providing 
qualitative insights about income stability, reliability, and sustainability.""")
])

def get_income_analyzer():
    """Get the Income Analyzer agent chain."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(IncomeAnalysis)
    chain = income_analyzer_prompt | structured_llm
    return chain

income_analyzer = get_income_analyzer()
