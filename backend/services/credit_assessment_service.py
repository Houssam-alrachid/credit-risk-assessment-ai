"""
Credit Assessment Service
Business logic layer for credit risk assessment operations
"""

import uuid
import os
from datetime import datetime
from typing import Optional, AsyncGenerator, Dict, Any

from graphs.credit_assessment_graph import CreditAssessmentGraph
from app.models import (
    LoanApplication,
    CreditAssessmentReport,
    AssessmentRequest,
    AssessmentResponse,
    ProgressUpdate
)
from config.settings import settings
from config.logging_config import get_logger

logger = get_logger(__name__)


class CreditAssessmentService:
    """
    Service layer for credit risk assessment operations.
    Handles business logic, tracing setup, and error handling.
    """
    
    def __init__(self):
        self.graph = CreditAssessmentGraph()
        self._setup_langsmith()
    
    def _setup_langsmith(self):
        """Configure LangSmith tracing if enabled"""
        if settings.langsmith_tracing_enabled and settings.langsmith_api_key:
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
            os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project
            logger.info(f"LangSmith tracing enabled for project: {settings.langsmith_project}")
        else:
            os.environ["LANGCHAIN_TRACING_V2"] = "false"
            logger.info("LangSmith tracing disabled")
    
    def _generate_trace_id(self) -> str:
        """Generate unique trace ID for LangSmith"""
        return f"credit-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
    
    def _get_trace_url(self, trace_id: str) -> Optional[str]:
        """Get LangSmith trace URL if tracing is enabled"""
        if settings.langsmith_tracing_enabled and settings.langsmith_api_key:
            return f"https://smith.langchain.com/o/{settings.langsmith_project}/projects/p/{trace_id}"
        return None
    
    async def assess_credit_risk(
        self,
        request: AssessmentRequest
    ) -> AssessmentResponse:
        """
        Perform complete credit risk assessment.
        
        Args:
            request: Assessment request containing loan application
            
        Returns:
            Assessment response with report or error
        """
        start_time = datetime.utcnow()
        trace_id = self._generate_trace_id()
        
        logger.info(f"Starting credit assessment - trace_id: {trace_id}")
        
        try:
            application = request.application
            if not application.application_id:
                application.application_id = str(uuid.uuid4())
            
            report = await self.graph.run(
                application=application,
                trace_id=trace_id
            )
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            logger.info(
                f"Credit assessment completed - "
                f"application_id: {application.application_id}, "
                f"decision: {report.credit_decision.decision.value}, "
                f"time: {processing_time:.2f}s"
            )
            
            return AssessmentResponse(
                success=True,
                report=report,
                processing_time_seconds=processing_time,
                trace_url=self._get_trace_url(trace_id)
            )
            
        except Exception as e:
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            logger.error(f"Credit assessment failed: {str(e)}", exc_info=True)
            
            return AssessmentResponse(
                success=False,
                error=str(e),
                processing_time_seconds=processing_time,
                trace_url=self._get_trace_url(trace_id)
            )
    
    async def assess_credit_risk_streaming(
        self,
        request: AssessmentRequest
    ) -> AsyncGenerator[ProgressUpdate, None]:
        """
        Perform credit risk assessment with streaming progress updates.
        
        Args:
            request: Assessment request containing loan application
            
        Yields:
            Progress updates during assessment
        """
        trace_id = self._generate_trace_id()
        
        yield ProgressUpdate(
            status="Initializing credit assessment...",
            progress=0,
            stage="init",
            data={"trace_id": trace_id}
        )
        
        try:
            application = request.application
            if not application.application_id:
                application.application_id = str(uuid.uuid4())
            
            yield ProgressUpdate(
                status="Collecting financial data...",
                progress=10,
                stage="financial_data"
            )
            
            report = await self.graph.run(
                application=application,
                trace_id=trace_id
            )
            
            yield ProgressUpdate(
                status="Assessment complete!",
                progress=100,
                stage="complete",
                data={
                    "decision": report.credit_decision.decision.value,
                    "confidence": report.credit_decision.confidence_score,
                    "risk_level": report.risk_assessment.overall_risk_level.value,
                    "report_id": report.report_id
                }
            )
            
        except Exception as e:
            logger.error(f"Streaming assessment failed: {str(e)}", exc_info=True)
            yield ProgressUpdate(
                status=f"Assessment failed: {str(e)}",
                progress=0,
                stage="error",
                data={"error": str(e)}
            )
    
    def validate_application(self, application: LoanApplication) -> Dict[str, Any]:
        """
        Validate loan application before processing.
        
        Args:
            application: Loan application to validate
            
        Returns:
            Validation result with any issues found
        """
        issues = []
        warnings = []
        
        if application.loan_request.requested_amount <= 0:
            issues.append("Requested amount must be positive")
        
        if application.loan_request.requested_term_months <= 0:
            issues.append("Requested term must be positive")
        
        if application.employment.monthly_net_income > application.employment.monthly_gross_income:
            issues.append("Net income cannot exceed gross income")
        
        if application.credit_history.credit_score < 300 or application.credit_history.credit_score > 850:
            issues.append("Credit score must be between 300 and 850")
        
        dti_estimate = 0
        monthly_income = application.employment.monthly_gross_income
        if monthly_income > 0:
            total_debt_payments = sum(d.monthly_payment for d in application.existing_debts)
            dti_estimate = total_debt_payments / monthly_income
            
            if dti_estimate > 0.6:
                warnings.append(f"High existing DTI ratio: {dti_estimate:.1%}")
        
        if application.credit_history.bankruptcies > 0:
            warnings.append("Applicant has bankruptcy history")
        
        if application.credit_history.delinquencies_90_days > 0:
            warnings.append("Applicant has 90+ day delinquencies")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }


credit_assessment_service = CreditAssessmentService()
