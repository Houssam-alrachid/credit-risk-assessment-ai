"""
FastAPI Application - Credit Risk Assessment AI
Main entry point for the REST API
"""

import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
import json
from datetime import datetime
from typing import Optional

from app.models import (
    AssessmentRequest,
    AssessmentResponse,
    HealthResponse,
    LoanApplication,
    ProgressUpdate
)
from services.credit_assessment_service import credit_assessment_service
from config.settings import settings
from config.logging_config import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"LangSmith tracing: {settings.langsmith_tracing_enabled}")
    yield
    logger.info("Shutting down application")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    ## Credit Risk Assessment AI
    
    Multi-agent system for automated loan underwriting using LangGraph and LangSmith.
    
    ### Features
    - **Automated Credit Analysis**: 6 specialized AI agents analyze loan applications
    - **Risk Scoring**: Comprehensive risk assessment with PD/LGD calculations
    - **Regulatory Compliance**: Basel III/IV compliant risk weights
    - **Full Traceability**: LangSmith integration for complete observability
    
    ### Workflow
    1. Financial Data Collection
    2. Income Analysis
    3. Debt Analysis
    4. Collateral Evaluation
    5. Risk Scoring
    6. Decision Writing
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for container orchestration"""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.utcnow()
    )


@app.post("/api/v1/assess", response_model=AssessmentResponse, tags=["Assessment"])
async def assess_credit_risk(request: AssessmentRequest):
    """
    Perform complete credit risk assessment on a loan application.
    
    This endpoint triggers the full multi-agent workflow:
    1. Financial data collection and validation
    2. Income analysis and affordability assessment
    3. Debt analysis and DTI calculation
    4. Collateral evaluation (if applicable)
    5. Risk scoring and PD/LGD estimation
    6. Final credit decision generation
    
    Returns a comprehensive report with decision, terms, and detailed analysis.
    """
    logger.info(f"Received assessment request for application: {request.application.application_id}")
    
    validation = credit_assessment_service.validate_application(request.application)
    if not validation["valid"]:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid application",
                "issues": validation["issues"]
            }
        )
    
    if validation["warnings"]:
        logger.warning(f"Application warnings: {validation['warnings']}")
    
    response = await credit_assessment_service.assess_credit_risk(request)
    
    if not response.success:
        raise HTTPException(
            status_code=500,
            detail={"error": response.error}
        )
    
    return response


@app.post("/api/v1/assess/stream", tags=["Assessment"])
async def assess_credit_risk_streaming(request: AssessmentRequest):
    """
    Perform credit risk assessment with Server-Sent Events (SSE) for progress updates.
    
    Returns a stream of progress updates as the assessment progresses through each stage.
    """
    logger.info(f"Received streaming assessment request")
    
    validation = credit_assessment_service.validate_application(request.application)
    if not validation["valid"]:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid application",
                "issues": validation["issues"]
            }
        )
    
    async def event_generator():
        async for update in credit_assessment_service.assess_credit_risk_streaming(request):
            yield f"data: {json.dumps(update.model_dump())}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


@app.post("/api/v1/validate", tags=["Validation"])
async def validate_application(application: LoanApplication):
    """
    Validate a loan application without performing full assessment.
    
    Useful for pre-flight checks before submitting for full assessment.
    """
    validation = credit_assessment_service.validate_application(application)
    return validation


@app.get("/api/v1/config", tags=["Configuration"])
async def get_configuration():
    """Get current API configuration (non-sensitive)"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "model": settings.openai_model,
        "langsmith_enabled": settings.langsmith_tracing_enabled,
        "langsmith_project": settings.langsmith_project if settings.langsmith_tracing_enabled else None,
        "max_dti_ratio": settings.max_dti_ratio,
        "credit_score_range": {
            "min": settings.min_credit_score,
            "max": settings.max_credit_score
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
