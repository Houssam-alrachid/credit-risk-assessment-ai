"""
LangGraph Credit Assessment Orchestration
Defines the multi-agent workflow for credit risk assessment
1. User calls: graph.run(loan_application)
   ↓
2. run() creates initial_state with all fields
   ↓
3. run() calls: self.graph.ainvoke(initial_state)
   ↓
4. LangGraph executes workflow:
   START → collect_financial_data
   ↓
5. LangGraph automatically calls:
   _collect_financial_data(state=current_state)
   ↓
6. Node returns dict with updates:
   {"financial_summary": {...}, "progress": 20}
   ↓
7. LangGraph merges updates into state
   ↓
8. Updated state flows to next nodes (income, debt, collateral)
   ↓
9. Each node receives updated state automatically
"""

import uuid
import json
from datetime import datetime
from typing import TypedDict, Annotated, Optional, Dict, Any, List
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage

from agents import (
    financial_data_collector,
    income_analyzer,
    debt_analyzer,
    collateral_evaluator,
    risk_scorer,
    decision_writer
)
from calculations import (
    calculate_annual_income,
    calculate_max_affordable_payment,
    perform_income_stress_test,
    calculate_estimated_payment,
    calculate_dti_ratio,
    calculate_dscr,
    calculate_total_monthly_debt,
    assess_debt_burden,
    calculate_ltv_ratio,
    calculate_liquidation_value,
    assess_collateral_quality,
    calculate_collateral_coverage,
    calculate_probability_of_default,
    calculate_loss_given_default,
    calculate_expected_loss,
    calculate_risk_score,
)

from app.models import (
    LoanApplication,
    FinancialDataSummary,
    IncomeAnalysis,
    DebtAnalysis,
    CollateralEvaluation,
    RiskAssessment,
    CreditDecision,
    CreditAssessmentReport
)
from config.logging_config import get_logger
from monitoring.metrics import (
    track_workflow_duration,
    track_node_duration
)

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
    
    messages: Annotated[List[Any], add_messages] # LangGraph message accumulator (reducer)


class CreditAssessmentGraph:
    """
    LangGraph-based orchestrator for credit risk assessment.
    Implements parallel workflow: collect → [income, debt, collateral] → risk → decision
    """
    
    def __init__(self):
        self.graph = None
        self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow with parallel architecture"""
        workflow = StateGraph(CreditAssessmentState)
        
        # Add all nodes
        workflow.add_node("collect_financial_data", self._collect_financial_data)
        workflow.add_node("analyze_income", self._analyze_income)
        workflow.add_node("analyze_debt", self._analyze_debt)
        workflow.add_node("evaluate_collateral", self._evaluate_collateral)
        workflow.add_node("sync_parallel_analyses", self._sync_parallel_analyses)
        workflow.add_node("calculate_risk", self._calculate_risk)
        workflow.add_node("write_decision", self._write_decision)
        
        # Sequential: START → collect_financial_data
        workflow.add_edge(START, "collect_financial_data")
        
        # Parallel: collect_financial_data → [income, debt, collateral]
        workflow.add_edge("collect_financial_data", "analyze_income")
        workflow.add_edge("collect_financial_data", "analyze_debt")
        workflow.add_edge("collect_financial_data", "evaluate_collateral")
        
        # Synchronization: [income, debt, collateral] → sync
        workflow.add_edge("analyze_income", "sync_parallel_analyses")
        workflow.add_edge("analyze_debt", "sync_parallel_analyses")
        workflow.add_edge("evaluate_collateral", "sync_parallel_analyses")
        
        # Sequential: sync → risk → decision → END
        workflow.add_edge("sync_parallel_analyses", "calculate_risk")
        workflow.add_edge("calculate_risk", "write_decision")
        workflow.add_edge("write_decision", END)
        
        self.graph = workflow.compile()
    
    @track_node_duration("collect_financial_data") # Decorator for timing and metrics
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
                "financial_summary": result.model_dump(), # Convert Pydantic model to dict
                "current_stage": "financial_data_collected",
                "progress": 20,
                # income_stability_score is generated by the financial_data_collector agent via prompt rules as part of a Pydantic output (FinancialDataSummary)
                "messages": [AIMessage(content=f"Financial data collected: stability score {result.income_stability_score}")]
            }
        except Exception as e:
            logger.error(f"Error collecting financial data: {e}")
            return {
                "errors": state.get("errors", []) + [f"Financial data collection failed: {str(e)}"],
                "current_stage": "error"
            }
    
    @track_node_duration("analyze_income")
    async def _analyze_income(self, state: CreditAssessmentState) -> Dict[str, Any]:
        """Node: Analyze income and affordability (runs in parallel)"""
        logger.info(f"[{state['application_id']}] Analyzing income (parallel execution)...")
        
        try:
            app = state["application"]
            financial_summary = state.get("financial_summary", {}) 
            
            # Extract data
            employment = app.get("employment", {})
            loan_request = app.get("loan_request", {})
            monthly_gross = employment.get("monthly_gross_income", 0)
            monthly_net = employment.get("monthly_net_income", 0)
            requested_amount = loan_request.get("requested_amount", 0)
            requested_term = loan_request.get("requested_term_months", 240)
            
            # Perform Python calculations
            annual_income = calculate_annual_income(monthly_gross, monthly_net)
            
            # Calculate existing debt (will be 0 if no debts yet)
            existing_debts = app.get("debts", [])
            existing_monthly_debt = calculate_total_monthly_debt(existing_debts)
            
            max_payment = calculate_max_affordable_payment(
                monthly_gross,
                existing_monthly_debt
            )
            
            # Estimate monthly payment for stress test
            estimated_payment = calculate_estimated_payment(
                requested_amount,
                requested_term,
                rate=0.04  # 4% default rate
            ) if requested_amount > 0 and requested_term > 0 else 0
            
            stress_test = perform_income_stress_test(
                monthly_gross,
                estimated_payment,
                loan_amount=requested_amount,
                loan_term_months=requested_term
            )
            
            # Pass calculations to LLM for qualitative analysis
            result = await income_analyzer.ainvoke({
                "financial_summary": json.dumps(financial_summary, indent=2, default=str),
                "application_data": json.dumps(app, indent=2, default=str),
                "requested_amount": requested_amount,
                "requested_term": requested_term,
                "calculations": json.dumps({
                    "annual_income": annual_income,
                    "max_affordable_payment": max_payment,
                    "stress_test_results": stress_test
                }, indent=2)
            })
            
            # Merge calculations with LLM analysis
            income_analysis = result.model_dump()
            income_analysis["calculations"] = {
                "annual_gross_income": annual_income["annual_gross"],
                "annual_net_income": annual_income["annual_net"],
                "max_affordable_payment": max_payment["recommended_max_payment"],
                "stress_test_passed": stress_test["overall_passes_stress_test"]
            }
            
            return {
                "income_analysis": income_analysis,
                "current_stage": "income_analyzed",
                "progress": 40,
                "messages": [AIMessage(content=f"Income analyzed: sustainability {result.income_sustainability}")]
            }
        except Exception as e:
            logger.error(f"Error analyzing income: {e}")
            return {
                "errors": state.get("errors", []) + [f"Income analysis failed: {str(e)}"],
                "current_stage": "error"
            }
    
    @track_node_duration("analyze_debt")
    async def _analyze_debt(self, state: CreditAssessmentState) -> Dict[str, Any]:
        """Node: Analyze existing debt obligations (runs in parallel)"""
        logger.info(f"[{state['application_id']}] Analyzing debt (parallel)...")
        
        try:
            app = state["application"]
            loan_request = app.get("loan_request", {})
            employment = app.get("employment", {})
            existing_debts = app.get("debts", [])
            
            requested_amount = loan_request.get("requested_amount", 0)
            requested_term = loan_request.get("requested_term_months", 12)
            estimated_payment = calculate_estimated_payment(requested_amount, requested_term)
            
            # Extract income data
            monthly_gross = employment.get("monthly_gross_income", 0)
            monthly_net = employment.get("monthly_net_income", 0)
            
            # Perform Python calculations
            total_monthly_debt = calculate_total_monthly_debt(existing_debts)
            current_dti = calculate_dti_ratio(total_monthly_debt, monthly_gross)
            projected_dti = calculate_dti_ratio(total_monthly_debt + estimated_payment, monthly_gross)
            dscr = calculate_dscr(monthly_net, total_monthly_debt)
            debt_burden = assess_debt_burden(current_dti, dscr)
            
            # Calculate credit utilization if available
            total_balance = sum(d.get("balance", 0) for d in existing_debts if d.get("type") in ["credit_card", "line_of_credit"])
            total_limit = sum(d.get("credit_limit", 0) for d in existing_debts if d.get("credit_limit", 0) > 0)
            utilization = (total_balance / total_limit * 100) if total_limit > 0 else 0
            
            # Pass calculations to LLM for qualitative analysis
            result = await debt_analyzer.ainvoke({
                "existing_debts": json.dumps(existing_debts, default=str),
                "income_analysis": json.dumps(state.get("financial_summary", {}), default=str),
                "requested_amount": requested_amount,
                "requested_term": requested_term,
                "estimated_payment": estimated_payment,
                "calculations": json.dumps({
                    "total_monthly_debt": total_monthly_debt,
                    "current_dti_ratio": current_dti,
                    "projected_dti_ratio": projected_dti,
                    "dscr": dscr,
                    "debt_burden_assessment": debt_burden,
                    "credit_utilization": utilization
                }, indent=2)
            })
            
            # Merge calculations with LLM analysis
            debt_analysis = result.model_dump()
            debt_analysis["calculations"] = {
                "total_monthly_debt": total_monthly_debt,
                "current_dti_ratio": current_dti,
                "projected_dti_ratio": projected_dti,
                "dscr": dscr,
                "debt_burden_level": debt_burden["overall_debt_burden"],
                "credit_utilization": utilization
            }
            
            return {
                "debt_analysis": debt_analysis,
                "messages": [AIMessage(content=f"Debt analyzed: DTI {current_dti:.1f}%, projected {projected_dti:.1f}%")]
            }
        except Exception as e:
            logger.error(f"Error analyzing debt: {e}")
            return {
                "errors": state.get("errors", []) + [f"Debt analysis failed: {str(e)}"],
                "current_stage": "error"
            }
    
    @track_node_duration("evaluate_collateral")
    async def _evaluate_collateral(self, state: CreditAssessmentState) -> Dict[str, Any]:
        """Node: Evaluate collateral (runs in parallel)"""
        logger.info(f"[{state['application_id']}] Evaluating collateral (parallel)...")
        
        try:
            app = state["application"]
            loan_request = app.get("loan_request", {})
            collateral = app.get("collateral")
            requested_amount = loan_request.get("requested_amount", 0)
            
            # Perform Python calculations if collateral exists
            if collateral:
                collateral_value = collateral.get("estimated_value", 0)
                collateral_type = collateral.get("type", "other")
                condition = collateral.get("condition", "good")
                has_insurance = collateral.get("has_insurance", False)
                has_clear_title = collateral.get("clear_title", True)
                
                # Calculate LTV
                ltv = calculate_ltv_ratio(requested_amount, collateral_value)
                
                # Calculate liquidation value
                liquidation = calculate_liquidation_value(collateral_value, collateral_type, condition)
                
                # Assess collateral quality
                quality = assess_collateral_quality(
                    ltv,
                    collateral_type,
                    has_insurance,
                    has_clear_title,
                    collateral.get("marketability", "good")
                )
                
                # Calculate coverage
                coverage = calculate_collateral_coverage(
                    requested_amount,
                    liquidation["liquidation_value"]
                )
                
                calculations = {
                    "ltv_ratio": ltv,
                    "liquidation_value": liquidation["liquidation_value"],
                    "liquidation_discount": liquidation["liquidation_discount"],
                    "recovery_rate": liquidation["recovery_rate"],
                    "quality_score": quality["quality_score"],
                    "overall_quality": quality["overall_quality"],
                    "coverage_ratio": coverage["coverage_ratio"],
                    "meets_coverage_requirement": coverage["meets_requirement"]
                }
                
                collateral_info = json.dumps(collateral, default=str)
            else:
                # Unsecured loan
                calculations = {
                    "ltv_ratio": 100.0,
                    "liquidation_value": 0,
                    "quality_score": 0,
                    "overall_quality": "none",
                    "coverage_ratio": 0,
                    "meets_coverage_requirement": False
                }
                collateral_info = "No collateral provided - unsecured loan"
            
            # Pass calculations to LLM for qualitative analysis
            result = await collateral_evaluator.ainvoke({
                "collateral_info": collateral_info,
                "requested_amount": requested_amount,
                "loan_purpose": loan_request.get("loan_purpose", "other"),
                "requested_term": loan_request.get("requested_term_months", 0),
                "calculations": json.dumps(calculations, indent=2)
            })
            
            # Merge calculations with LLM analysis
            collateral_evaluation = result.model_dump()
            collateral_evaluation["calculations"] = calculations
            
            return {
                "collateral_evaluation": collateral_evaluation,
                "messages": [AIMessage(content=f"Collateral evaluated: quality={calculations.get('overall_quality', 'none')}, LTV={calculations['ltv_ratio']:.1f}%")]
            }
        except Exception as e:
            logger.error(f"Error evaluating collateral: {e}")
            return {
                "errors": state.get("errors", []) + [f"Collateral evaluation failed: {str(e)}"],
                "current_stage": "error"
            }
    
    @track_node_duration("sync_parallel_analyses")
    async def _sync_parallel_analyses(self, state: CreditAssessmentState) -> Dict[str, Any]:
        """Node: Synchronization point after parallel analyses complete"""
        logger.info(f"[{state['application_id']}] Synchronizing parallel analyses...")
        
        # Check if all parallel analyses completed successfully
        if state.get("income_analysis") and state.get("debt_analysis") and state.get("collateral_evaluation"):
            logger.info(f"[{state['application_id']}] All parallel analyses completed successfully")
            return {
                "current_stage": "parallel_analyses_complete",
                "progress": 60,
                "messages": [AIMessage(content="Parallel analyses synchronized: income, debt, and collateral evaluations complete")]
            }
        else:
            logger.warning(f"[{state['application_id']}] Some parallel analyses may have failed")
            return {
                "current_stage": "parallel_analyses_complete",
                "progress": 60
            }
    
    @track_node_duration("calculate_risk")
    async def _calculate_risk(self, state: CreditAssessmentState) -> Dict[str, Any]:
        """Node: Calculate comprehensive risk metrics"""
        logger.info(f"[{state['application_id']}] Calculating risk scores...")
        
        try:
            app = state["application"]
            loan_request = app.get("loan_request", {})
            credit_history = app.get("credit_history", {})
            employment = app.get("employment", {})
            
            # Extract data from previous analyses
            income_analysis = state.get("income_analysis", {})
            debt_analysis = state.get("debt_analysis", {})
            collateral_evaluation = state.get("collateral_evaluation", {})
            
            # Get calculations from previous nodes
            income_calcs = income_analysis.get("calculations", {})
            debt_calcs = debt_analysis.get("calculations", {})
            collateral_calcs = collateral_evaluation.get("calculations", {})
            
            # Extract key metrics
            credit_score = credit_history.get("credit_score", 650)
            dti_ratio = debt_calcs.get("current_dti_ratio", 0)
            ltv_ratio = collateral_calcs.get("ltv_ratio", 100)
            employment_years = employment.get("years_with_current_employer", 0)
            
            # Get income and collateral quality scores
            income_stability_score = income_calcs.get("stability_score", 50)
            collateral_quality_score = collateral_calcs.get("quality_score", 0)
            
            # Perform Python calculations
            pd = calculate_probability_of_default(
                credit_score,
                dti_ratio,
                employment_years,
                payment_history_score=100,  # Could extract from credit_history
                debt_burden_level=debt_calcs.get("debt_burden_level", "moderate")
            )
            
            lgd = calculate_loss_given_default(
                ltv_ratio,
                collateral_calcs.get("overall_quality", "none"),
                recovery_rate=collateral_calcs.get("recovery_rate", 70.0),
                has_guarantor=False
            )
            
            requested_amount = loan_request.get("requested_amount", 0)
            el = calculate_expected_loss(requested_amount, pd, lgd)
            
            risk = calculate_risk_score(
                pd,
                lgd,
                dti_ratio,
                ltv_ratio,
                credit_score,
                income_stability_score,
                collateral_quality_score
            )
            
            calculations = {
                "probability_of_default": pd,
                "loss_given_default": lgd,
                "expected_loss_amount": el["expected_loss_amount"],
                "expected_loss_percentage": el["expected_loss_percentage"],
                "risk_score": risk["risk_score"],
                "overall_risk_level": risk["overall_risk_level"],
                "component_scores": risk["component_scores"]
            }
            
            # Pass calculations to LLM for qualitative analysis
            result = await risk_scorer.ainvoke({
                "financial_summary": json.dumps(state["financial_summary"], default=str),
                "income_analysis": json.dumps(income_analysis, default=str),
                "debt_analysis": json.dumps(debt_analysis, default=str),
                "collateral_evaluation": json.dumps(collateral_evaluation, default=str),
                "credit_history": json.dumps(credit_history, default=str),
                "requested_amount": requested_amount,
                "requested_term": loan_request.get("requested_term_months", 0),
                "loan_purpose": loan_request.get("loan_purpose", "other"),
                "calculations": json.dumps(calculations, indent=2)
            })
            
            # Merge calculations with LLM analysis
            risk_assessment = result.model_dump()
            risk_assessment["calculations"] = calculations
            
            return {
                "risk_assessment": risk_assessment,
                "current_stage": "risk_calculated",
                "progress": 80,
                "messages": [AIMessage(content=f"Risk calculated: {risk['overall_risk_level']}, PD={pd:.1f}%")]
            }
        except Exception as e:
            logger.error(f"Error calculating risk: {e}")
            return {
                "errors": state.get("errors", []) + [f"Risk calculation failed: {str(e)}"],
                "current_stage": "error"
            }
    
    @track_node_duration("write_decision")
    async def _write_decision(self, state: CreditAssessmentState) -> Dict[str, Any]:
        """Node: Generate final credit decision"""
        logger.info(f"[{state['application_id']}] Writing credit decision...")
        
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
    
    @track_workflow_duration
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
