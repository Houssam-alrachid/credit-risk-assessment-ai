"""
Application Settings
Centralized configuration management using Pydantic Settings
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    All sensitive data should be provided via environment variables.
    """
    
    # API Configuration
    app_name: str = Field(default="Credit Risk Assessment AI", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8080, description="API port")
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., description="OpenAI API key")
    openai_model: str = Field(default="gpt-4o", description="OpenAI model to use")
    openai_temperature: float = Field(default=0.1, description="Model temperature for consistency")
    
    # LangSmith Configuration (Observability)
    langsmith_api_key: Optional[str] = Field(default=None, description="LangSmith API key for tracing")
    langsmith_project: str = Field(default="credit-risk-assessment", description="LangSmith project name")
    langsmith_tracing_enabled: bool = Field(default=True, description="Enable LangSmith tracing")
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=100, description="Max requests per minute")
    rate_limit_tokens: int = Field(default=100000, description="Max tokens per minute")
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format: json or text")
    
    # Security
    cors_origins: str = Field(default="*", description="Allowed CORS origins (comma-separated)")
    api_key_header: str = Field(default="X-API-Key", description="API key header name")
    
    # Credit Assessment Configuration
    min_credit_score: int = Field(default=300, description="Minimum credit score")
    max_credit_score: int = Field(default=850, description="Maximum credit score")
    default_currency: str = Field(default="EUR", description="Default currency")
    max_dti_ratio: float = Field(default=0.43, description="Maximum debt-to-income ratio")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Using lru_cache ensures settings are only loaded once.
    """
    return Settings()


# Global settings instance
settings = get_settings()
