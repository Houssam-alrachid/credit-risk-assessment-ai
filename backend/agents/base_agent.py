"""
Base Agent Configuration
Shared configuration and utilities for all credit risk agents
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Type, Optional
from config.settings import settings
from config.logging_config import get_logger

logger = get_logger(__name__)


def get_llm(temperature: Optional[float] = None) -> ChatOpenAI:
    """
    Get configured LLM instance.
    
    Args:
        temperature: Override default temperature if needed
        
    Returns:
        Configured ChatOpenAI instance
    """
    return ChatOpenAI(
        model=settings.openai_model,
        temperature=temperature if temperature is not None else settings.openai_temperature,
        api_key=settings.openai_api_key,
        max_retries=3,
        request_timeout=60
    )


def create_agent_prompt(
    system_message: str,
    include_history: bool = False
) -> ChatPromptTemplate:
    """
    Create a standardized prompt template for agents.
    
    Args:
        system_message: The system message defining agent behavior
        include_history: Whether to include conversation history
        
    Returns:
        Configured ChatPromptTemplate
    """
    messages = [("system", system_message)]
    
    if include_history:
        messages.append(MessagesPlaceholder(variable_name="history", optional=True))
    
    messages.append(("human", "{input}"))
    
    return ChatPromptTemplate.from_messages(messages)


def create_structured_agent(
    system_message: str,
    output_model: Type[BaseModel],
    temperature: Optional[float] = None
):
    """
    Create an agent that outputs structured data.
    
    Args:
        system_message: System prompt for the agent
        output_model: Pydantic model for structured output
        temperature: Optional temperature override
        
    Returns:
        Configured chain for structured output
    """
    llm = get_llm(temperature)
    prompt = create_agent_prompt(system_message)
    
    structured_llm = llm.with_structured_output(output_model)
    
    chain = prompt | structured_llm
    
    return chain


BANKING_CONTEXT = """
You are an expert banking analyst specializing in credit risk assessment.
You operate under strict regulatory frameworks including:
- Basel III/IV capital requirements
- European Banking Authority (EBA) guidelines
- IFRS 9 provisioning standards
- Local consumer protection regulations

Your analysis must be:
- Objective and data-driven
- Compliant with fair lending practices
- Transparent and explainable
- Conservative in risk estimation
"""
