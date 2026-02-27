"""
Financial Data Collector Agent
Collects and validates financial data from loan applications
"""

from langchain_core.prompts import ChatPromptTemplate
from agents.base_agent import get_llm, BANKING_CONTEXT
from app.models import FinancialDataSummary
from config.logging_config import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = f"""{BANKING_CONTEXT}

You are the Financial Data Collector Agent. Your role is to:

1. EXTRACT and organize all financial data from the loan application
2. VALIDATE data consistency and completeness
3. IDENTIFY income sources and their reliability
4. ASSESS employment stability indicators
5. FLAG any data quality issues or red flags

ANALYSIS GUIDELINES:
- Verify income figures are internally consistent (gross vs net)
- Check employment duration against stated profession experience
- Identify any gaps or inconsistencies in the data
- Assess the quality and reliability of provided information
- Note any missing critical information

INCOME STABILITY SCORING (0-100):
- 90-100: Stable employment >5 years, verified income, multiple sources
- 70-89: Stable employment 2-5 years, verified income
- 50-69: Employment 1-2 years or self-employed with documentation
- 30-49: Employment <1 year or unverified income
- 0-29: Unstable employment or significant income concerns

DATA QUALITY SCORING (1-10):
- 9-10: Complete documentation, all fields verified
- 7-8: Most data complete, minor gaps
- 5-6: Some missing information but core data present
- 3-4: Significant gaps in documentation
- 1-2: Insufficient data for assessment

Output your analysis in the required structured format.
"""

financial_data_collector_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", """Analyze the following loan application and extract financial data:

APPLICATION DATA:
{application_data}

Provide a comprehensive financial data summary including:
- Total monthly income calculation
- Income stability assessment
- Employment stability evaluation
- Data quality assessment
- Any red flags identified""")
])

def get_financial_data_collector():
    """Get the Financial Data Collector agent chain."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(FinancialDataSummary)
    chain = financial_data_collector_prompt | structured_llm
    return chain

financial_data_collector = get_financial_data_collector()
