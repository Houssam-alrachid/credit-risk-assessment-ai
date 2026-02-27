"""
LangGraph Credit Assessment Orchestration
Defines the multi-agent workflow for credit risk assessment
"""

import asyncio
import uuid
import json
from datetime import datetime
from typing import TypedDict, Annotated, Optional, Dict, Any, List
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage

from agents.financial_data_collector import financial_data_collector
from agents.income_analyzer import income_analyzer
from agents.debt_analyzer import debt_analyzer
from agents.collateral_evaluator import collateral_evaluator
from agents.risk_scorer import risk_scorer
from agents.decision_writer import decision_writer

from app.models import (
    LoanApplication,
    FinancialDataSummary,
    IncomeAnalysis,
    DebtAnalysis,
    CollateralEvaluation,
    RiskAssessment,
    CreditDecision,
    CreditAssessmentReport,
    ProgressUpdate
)
from config.logging_config import get_logger

logger = get_logger(__name__)


class CreditAssessmentState(TypedDict):
    """State schema for the credit assessment workflow"""
    application: Dict[str, Any]
    application_id: str
    
    financial_summary: Optional[Dict[str, Any]]
    income_analysis: Optional[Dict[str, Any]]
    debt_analysis: Optional[Dict[str, Any]]
    collateral_evaluation: Optional[Dict[str, Any]]
    risk_assessment: Optional[Dict[str, Any]]
    credit_decision: Optional[Dict[str, Any]]
    
    current_stage: str
    progress: int
    errors: List[str]
    start_time: float
    
    messages: Annotated[List[Any], add_messages]


def calculate_estimated_payment(amount: float, term_months: int, rate: float = 0.05) -> float:
    """Calculate estimated monthly payment using amortization formula"""
    monthly_rate = rate / 12
    if monthly_rate == 0:
        return amount / term_months
    payment = (monthly_rate * amount) / (1 - (1 + monthly_rate) ** -term_months)
    return round(payment, 2)


class CreditAssessmentGraph:
    """
    LangGraph-based orchestrator for credit risk assessment.
    Implements hybrid sequential/parallel workflow.
    """
    
    def __init__(self):
        self.graph = None
        self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(CreditAssessmentState)
        
        workflow.add_node("collect_financial_data", self._collect_financial_data)
        workflow.add_node("analyze_income", self._analyze_income)
        workflow.add_node("analyze_debt", self._analyze_debt)
        workflow.add_node("evaluate_collateral", self._evaluate_collateral)
        workflow.add_node("calculate_risk", self._calculate_risk)
        workflow.add_node("write_decision", self._write_decision)
        
        workflow.add_edge(START, "collect_financial_data")
        workflow.add_edge("collect_financial_data", "analyze_income")
        workflow.add_edge("analyze_income", "analyze_debt")
        workflow.add_edge("analyze_debt", "evaluate_collateral")
        workflow.add_edge("evaluate_collateral", "calculate_risk")
        workflow.add_edge("calculate_risk", "write_decision")
        workflow.add_edge("write_decision", END)
        
        self.graph = workflow.compile()
    
    async def _collect_financial_data(self, state: CreditAssessmentState) -> Dict[str, Any]:
        """Node: Collect and validate financial data"""
        logger.info(f"[{state['application_id']}] Collecting financial data...")
        
        try:
            app = state["application"]
            application_data = json.dumps(app, indent=2, default=str)
            
            result = await financial_data_collector.ainvoke({
                "application_data": application_data
            })
            
            return {
                "financial_summary": result.model_dump(),
                "current_stage": "financial_data_collected",
                "progress": 20,
                "messages": [AIMessage(content=f"Financial data collected: stability score {result.income_stability_score}")]
            }
        except Exception as e:
            logger.error(f"Error collecting financial data: {e}")
            return {
                "errors": state.get("errors", []) + [f"Financial data collection failed: {str(e)}"],
                "current_stage": "error"
            }
    
    async def _analyze_income(self, state: CreditAssessmentState) -> Dict[str, Any]:
        """Node: Analyze income and affordability"""
        logger.info(f"[{state['application_id']}] Analyzing income...")
        
        try:
            app = state["application"]
            loan_request = app.get("loan_request", {})
            
            result = await income_analyzer.ainvoke({
                "financial_summary": json.dumps(state["financial_summary"], default=str),
                "application_data": json.dumps(app, default=str),
                "requested_amount": loan_request.get("requested_amount", 0),
                "requested_term": loan_request.get("requested_term_months", 0)
            })
            
            return {
                "income_analysis": result.model_dump(),
                "current_stage": "income_analyzed",
                "progress": 35,
                "messages": [AIMessage(content=f"Income analyzed: max affordable payment {result.max_affordable_payment} EUR")]
            }
        except Exception as e:
            logger.error(f"Error analyzing income: {e}")
            return {
                "errors": state.get("errors", []) + [f"Income analysis failed: {str(e)}"],
                "current_stage": "error"
            }
    
    async def _analyze_debt(self, state: CreditAssessmentState) -> Dict[str, Any]:
        """Node: Analyze existing debt obligations"""
        logger.info(f"[{state['application_id']}] Analyzing debt...")
        
        try:
            app = state["application"]
            loan_request = app.get("loan_request", {})
            existing_debts = app.get("existing_debts", [])
            
            requested_amount = loan_request.get("requested_amount", 0)
            requested_term = loan_request.get("requested_term_months", 12)
            estimated_payment = calculate_estimated_payment(requested_amount, requested_term)
            
            result = await debt_analyzer.ainvoke({
                "existing_debts": json.dumps(existing_debts, default=str),
                "income_analysis": json.dumps(state["income_analysis"], default=str),
                "requested_amount": requested_amount,
                "requested_term": requested_term,
                "estimated_payment": estimated_payment
            })
            
            return {
                "debt_analysis": result.model_dump(),
                "current_stage": "debt_analyzed",
                "progress": 50,
                "messages": [AIMessage(content=f"Debt analyzed: DTI {result.debt_to_income_ratio:.1%}, projected {result.projected_dti_ratio:.1%}")]
            }
        except Exception as e:
            logger.error(f"Error analyzing debt: {e}")
            return {
                "errors": state.get("errors", []) + [f"Debt analysis failed: {str(e)}"],
                "current_stage": "error"
            }
    
    async def _evaluate_collateral(self, state: CreditAssessmentState) -> Dict[str, Any]:
        """Node: Evaluate collateral"""
        logger.info(f"[{state['application_id']}] Evaluating collateral...")
        
        try:
            app = state["application"]
            loan_request = app.get("loan_request", {})
            collateral = app.get("collateral")
            
            collateral_info = json.dumps(collateral, default=str) if collateral else "No collateral provided - unsecured loan"
            
            result = await collateral_evaluator.ainvoke({
                "collateral_info": collateral_info,
                "requested_amount": loan_request.get("requested_amount", 0),
                "loan_purpose": loan_request.get("loan_purpose", "other"),
                "requested_term": loan_request.get("requested_term_months", 0)
            })
            
            return {
                "collateral_evaluation": result.model_dump(),
                "current_stage": "collateral_evaluated",
                "progress": 65,
                "messages": [AIMessage(content=f"Collateral evaluated: quality={result.collateral_quality}, LTV={result.loan_to_value_ratio:.1f}%")]
            }
        except Exception as e:
            logger.error(f"Error evaluating collateral: {e}")
            return {
                "errors": state.get("errors", []) + [f"Collateral evaluation failed: {str(e)}"],
                "current_stage": "error"
            }
    
    async def _calculate_risk(self, state: CreditAssessmentState) -> Dict[str, Any]:
        """Node: Calculate comprehensive risk score"""
        logger.info(f"[{state['application_id']}] Calculating risk score...")
        
        try:
            app = state["application"]
            loan_request = app.get("loan_request", {})
            credit_history = app.get("credit_history", {})
            
            result = await risk_scorer.ainvoke({
                "financial_summary": json.dumps(state["financial_summary"], default=str),
                "income_analysis": json.dumps(state["income_analysis"], default=str),
                "debt_analysis": json.dumps(state["debt_analysis"], default=str),
                "collateral_evaluation": json.dumps(state["collateral_evaluation"], default=str),
                "credit_history": json.dumps(credit_history, default=str),
                "requested_amount": loan_request.get("requested_amount", 0),
                "requested_term": loan_request.get("requested_term_months", 0),
                "loan_purpose": loan_request.get("loan_purpose", "other")
            })
            
            return {
                "risk_assessment": result.model_dump(),
                "current_stage": "risk_calculated",
                "progress": 80,
                "messages": [AIMessage(content=f"Risk calculated: {result.overall_risk_level.value}, PD={result.probability_of_default:.1f}%")]
            }
        except Exception as e:
            logger.error(f"Error calculating risk: {e}")
            return {
                "errors": state.get("errors", []) + [f"Risk calculation failed: {str(e)}"],
                "current_stage": "error"
            }
    
    async def _write_decision(self, state: CreditAssessmentState) -> Dict[str, Any]:
        """Node: Write final credit decision"""
        logger.info(f"[{state['application_id']}] Writing decision...")
        
        try:
            app = state["application"]
            applicant = app.get("applicant", {})
            loan_request = app.get("loan_request", {})
            
            applicant_name = f"{applicant.get('first_name', '')} {applicant.get('last_name', '')}".strip()
            
            result = await decision_writer.ainvoke({
                "applicant_name": applicant_name,
                "requested_amount": loan_request.get("requested_amount", 0),
                "requested_term": loan_request.get("requested_term_months", 0),
                "loan_purpose": loan_request.get("loan_purpose", "other"),
                "risk_assessment": json.dumps(state["risk_assessment"], default=str),
                "income_analysis": json.dumps(state["income_analysis"], default=str),
                "debt_analysis": json.dumps(state["debt_analysis"], default=str),
                "collateral_evaluation": json.dumps(state["collateral_evaluation"], default=str),
                "financial_summary": json.dumps(state["financial_summary"], default=str)
            })
            
            return {
                "credit_decision": result.model_dump(),
                "current_stage": "decision_complete",
                "progress": 100,
                "messages": [AIMessage(content=f"Decision: {result.decision.value} (confidence: {result.confidence_score:.0f}%)")]
            }
        except Exception as e:
            logger.error(f"Error writing decision: {e}")
            return {
                "errors": state.get("errors", []) + [f"Decision writing failed: {str(e)}"],
                "current_stage": "error"
            }
    
    async def run(self, application: LoanApplication, trace_id: Optional[str] = None) -> CreditAssessmentReport:
        """
        Execute the credit assessment workflow.
        
        Args:
            application: Complete loan application
            trace_id: Optional trace ID for LangSmith
            
        Returns:
            Complete credit assessment report
        """
        start_time = datetime.utcnow()
        application_id = application.application_id or str(uuid.uuid4())
        
        logger.info(f"Starting credit assessment for application {application_id}")
        
        initial_state: CreditAssessmentState = {
            "application": application.model_dump(),
            "application_id": application_id,
            "financial_summary": None,
            "income_analysis": None,
            "debt_analysis": None,
            "collateral_evaluation": None,
            "risk_assessment": None,
            "credit_decision": None,
            "current_stage": "started",
            "progress": 0,
            "errors": [],
            "start_time": start_time.timestamp(),
            "messages": [HumanMessage(content=f"Starting credit assessment for {application_id}")]
        }
        
        config = {"configurable": {"thread_id": application_id}}
        if trace_id:
            config["metadata"] = {"trace_id": trace_id}
        
        final_state = await self.graph.ainvoke(initial_state, config=config)
        
        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds()
        
        applicant = application.applicant
        applicant_name = f"{applicant.first_name} {applicant.last_name}"
        
        report = CreditAssessmentReport(
            report_id=str(uuid.uuid4()),
            application_id=application_id,
            report_date=end_time,
            applicant_name=applicant_name,
            financial_summary=FinancialDataSummary(**final_state["financial_summary"]),
            income_analysis=IncomeAnalysis(**final_state["income_analysis"]),
            debt_analysis=DebtAnalysis(**final_state["debt_analysis"]),
            collateral_evaluation=CollateralEvaluation(**final_state["collateral_evaluation"]),
            risk_assessment=RiskAssessment(**final_state["risk_assessment"]),
            credit_decision=CreditDecision(**final_state["credit_decision"]),
            executive_summary=self._generate_executive_summary(final_state),
            detailed_analysis=self._generate_detailed_analysis(final_state),
            recommendations=self._generate_recommendations(final_state),
            processing_time_seconds=processing_time,
            trace_id=trace_id
        )
        
        logger.info(f"Credit assessment completed for {application_id} in {processing_time:.2f}s")
        
        return report
    
    def _generate_executive_summary(self, state: Dict[str, Any]) -> str:
        """Generate executive summary from state"""
        decision = state.get("credit_decision", {})
        risk = state.get("risk_assessment", {})
        income = state.get("income_analysis", {})
        debt = state.get("debt_analysis", {})
        
        decision_type = decision.get("decision", "unknown")
        risk_level = risk.get("overall_risk_level", "unknown")
        dti = debt.get("projected_dti_ratio", 0)
        
        return f"""
## Executive Summary

**Decision:** {decision_type.upper()}
**Risk Level:** {risk_level}
**Confidence:** {decision.get('confidence_score', 0):.0f}%

### Key Metrics
- Projected DTI: {dti:.1%}
- Risk Score: {risk.get('risk_score', 0)}/100
- Probability of Default: {risk.get('probability_of_default', 0):.2f}%
- Max Affordable Payment: €{income.get('max_affordable_payment', 0):,.2f}

### Summary
This application has been assessed using automated credit risk analysis. 
The decision is based on comprehensive evaluation of income stability, 
debt obligations, collateral coverage, and overall creditworthiness.
"""
    
    def _generate_detailed_analysis(self, state: Dict[str, Any]) -> str:
        """Generate detailed analysis narrative"""
        financial = state.get("financial_summary", {})
        income = state.get("income_analysis", {})
        debt = state.get("debt_analysis", {})
        collateral = state.get("collateral_evaluation", {})
        risk = state.get("risk_assessment", {})
        
        return f"""
## Detailed Analysis

### Income Assessment
- Gross Annual Income: €{income.get('gross_annual_income', 0):,.2f}
- Net Annual Income: €{income.get('net_annual_income', 0):,.2f}
- Income Stability Score: {financial.get('income_stability_score', 0)}/100
- Income Sustainability: {income.get('income_sustainability', 'N/A')}
- Stress Test Result: {income.get('stress_test_result', 'N/A')}

### Debt Profile
- Total Existing Debt: €{debt.get('total_existing_debt', 0):,.2f}
- Monthly Debt Payments: €{debt.get('total_monthly_debt_payments', 0):,.2f}
- Current DTI: {debt.get('debt_to_income_ratio', 0):.1%}
- Projected DTI: {debt.get('projected_dti_ratio', 0):.1%}
- DSCR: {debt.get('debt_service_coverage_ratio', 0):.2f}

### Collateral Assessment
- Collateral Present: {'Yes' if collateral.get('collateral_present') else 'No'}
- Collateral Quality: {collateral.get('collateral_quality', 'N/A')}
- LTV Ratio: {collateral.get('loan_to_value_ratio', 100):.1f}%
- Liquidation Value: €{collateral.get('liquidation_value', 0):,.2f}

### Risk Profile
- Overall Risk Level: {risk.get('overall_risk_level', 'N/A')}
- Risk Score: {risk.get('risk_score', 0)}/100
- PD: {risk.get('probability_of_default', 0):.2f}%
- LGD: {risk.get('loss_given_default', 0):.1f}%
- Expected Loss: €{risk.get('expected_loss', 0):,.2f}
"""
    
    def _generate_recommendations(self, state: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        decision = state.get("credit_decision", {})
        risk = state.get("risk_assessment", {})
        collateral = state.get("collateral_evaluation", {})
        
        recommendations.extend(decision.get("next_steps", []))
        recommendations.extend(collateral.get("recommendations", []))
        
        if risk.get("risk_score", 0) > 60:
            recommendations.append("Consider requiring additional collateral or guarantor")
        
        if not recommendations:
            recommendations.append("No additional recommendations at this time")
        
        return recommendations
