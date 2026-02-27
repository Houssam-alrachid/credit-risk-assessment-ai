import React from 'react';
import { 
  CheckCircle, XCircle, AlertTriangle, Clock, 
  TrendingUp, TrendingDown, Shield, FileText,
  ArrowLeft, Download, Percent, DollarSign
} from 'lucide-react';
import { 
  RadialBarChart, RadialBar, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip
} from 'recharts';

function ResultsDashboard({ result, onNewAssessment }) {
  const report = result?.report;
  
  if (!report) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No assessment data available</p>
      </div>
    );
  }

  const decision = report.credit_decision;
  const risk = report.risk_assessment;
  const income = report.income_analysis;
  const debt = report.debt_analysis;
  const collateral = report.collateral_evaluation;

  const getDecisionColor = (dec) => {
    switch (dec) {
      case 'approved': return 'text-success-600 bg-success-50';
      case 'approved_with_conditions': return 'text-warning-600 bg-warning-50';
      case 'declined': return 'text-danger-600 bg-danger-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const getDecisionIcon = (dec) => {
    switch (dec) {
      case 'approved': return CheckCircle;
      case 'approved_with_conditions': return AlertTriangle;
      case 'declined': return XCircle;
      default: return Clock;
    }
  };

  const getRiskColor = (level) => {
    switch (level) {
      case 'very_low':
      case 'low': return 'text-success-600';
      case 'medium': return 'text-warning-600';
      case 'high':
      case 'very_high': return 'text-danger-600';
      default: return 'text-gray-600';
    }
  };

  const DecisionIcon = getDecisionIcon(decision.decision);

  const scoreData = risk.score_breakdown ? [
    { name: 'Credit History', value: risk.score_breakdown.credit_history_score, fill: '#3b82f6' },
    { name: 'Income Stability', value: risk.score_breakdown.income_stability_score, fill: '#22c55e' },
    { name: 'Debt Burden', value: risk.score_breakdown.debt_burden_score, fill: '#f59e0b' },
    { name: 'Collateral', value: risk.score_breakdown.collateral_score, fill: '#8b5cf6' },
    { name: 'Employment', value: risk.score_breakdown.employment_score, fill: '#06b6d4' },
  ] : [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <button
          onClick={onNewAssessment}
          className="btn-secondary flex items-center gap-2"
        >
          <ArrowLeft className="w-4 h-4" />
          New Assessment
        </button>
        <div className="text-sm text-gray-500">
          Report ID: {report.report_id}
        </div>
      </div>

      {/* Decision Card */}
      <div className={`card ${getDecisionColor(decision.decision)} border-2`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="p-3 rounded-full bg-white/50">
              <DecisionIcon className="w-8 h-8" />
            </div>
            <div>
              <h2 className="text-2xl font-bold uppercase">
                {decision.decision.replace(/_/g, ' ')}
              </h2>
              <p className="text-sm opacity-80">
                Applicant: {report.applicant_name}
              </p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold">{decision.confidence_score}%</div>
            <div className="text-sm opacity-80">Confidence</div>
          </div>
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-4 gap-4">
        <div className="card">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary-100 rounded-lg">
              <Shield className="w-5 h-5 text-primary-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">Risk Score</p>
              <p className={`text-xl font-bold ${getRiskColor(risk.overall_risk_level)}`}>
                {risk.risk_score}/100
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-warning-100 rounded-lg">
              <Percent className="w-5 h-5 text-warning-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">DTI Ratio</p>
              <p className="text-xl font-bold text-gray-900">
                {(debt.projected_dti_ratio * 100).toFixed(1)}%
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-danger-100 rounded-lg">
              <TrendingDown className="w-5 h-5 text-danger-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">Default Prob.</p>
              <p className="text-xl font-bold text-gray-900">
                {(risk.probability_of_default).toFixed(2)}%
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-success-100 rounded-lg">
              <DollarSign className="w-5 h-5 text-success-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">Max Payment</p>
              <p className="text-xl font-bold text-gray-900">
                €{income.max_affordable_payment?.toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Approved Terms (if applicable) */}
      {decision.approved_terms && (
        <div className="card bg-success-50 border-success-200">
          <h3 className="text-lg font-semibold text-success-800 mb-4">Approved Loan Terms</h3>
          <div className="grid grid-cols-4 gap-6">
            <div>
              <p className="text-sm text-success-600">Amount</p>
              <p className="text-2xl font-bold text-success-800">
                €{decision.approved_terms.approved_amount?.toLocaleString()}
              </p>
            </div>
            <div>
              <p className="text-sm text-success-600">Interest Rate</p>
              <p className="text-2xl font-bold text-success-800">
                {decision.approved_terms.interest_rate}%
              </p>
            </div>
            <div>
              <p className="text-sm text-success-600">Monthly Payment</p>
              <p className="text-2xl font-bold text-success-800">
                €{decision.approved_terms.monthly_payment?.toLocaleString()}
              </p>
            </div>
            <div>
              <p className="text-sm text-success-600">Term</p>
              <p className="text-2xl font-bold text-success-800">
                {decision.approved_terms.term_months} months
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Score Breakdown Chart */}
      <div className="grid grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Score Breakdown</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={scoreData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 100]} />
              <YAxis dataKey="name" type="category" width={120} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="value" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Financial Summary</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-gray-600">Annual Gross Income</span>
              <span className="font-semibold">€{income.gross_annual_income?.toLocaleString()}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-gray-600">Annual Net Income</span>
              <span className="font-semibold">€{income.net_annual_income?.toLocaleString()}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-gray-600">Total Existing Debt</span>
              <span className="font-semibold">€{debt.total_existing_debt?.toLocaleString()}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-gray-600">Monthly Debt Payments</span>
              <span className="font-semibold">€{debt.total_monthly_debt_payments?.toLocaleString()}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-gray-600">Collateral Value</span>
              <span className="font-semibold">
                {collateral.collateral_present 
                  ? `€${collateral.estimated_value?.toLocaleString()}`
                  : 'None'
                }
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Risk Factors & Mitigating Factors */}
      <div className="grid grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-danger-600 mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5" />
            Risk Factors
          </h3>
          <ul className="space-y-2">
            {risk.risk_factors?.map((factor, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                <XCircle className="w-4 h-4 text-danger-500 flex-shrink-0 mt-0.5" />
                {factor}
              </li>
            ))}
          </ul>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-success-600 mb-4 flex items-center gap-2">
            <CheckCircle className="w-5 h-5" />
            Mitigating Factors
          </h3>
          <ul className="space-y-2">
            {risk.mitigating_factors?.map((factor, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                <CheckCircle className="w-4 h-4 text-success-500 flex-shrink-0 mt-0.5" />
                {factor}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Conditions or Decline Reasons */}
      {decision.conditions?.length > 0 && (
        <div className="card border-warning-200 bg-warning-50">
          <h3 className="text-lg font-semibold text-warning-800 mb-4">Conditions</h3>
          <ul className="space-y-2">
            {decision.conditions.map((condition, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-warning-700">
                <AlertTriangle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                {condition}
              </li>
            ))}
          </ul>
        </div>
      )}

      {decision.decline_reasons?.length > 0 && (
        <div className="card border-danger-200 bg-danger-50">
          <h3 className="text-lg font-semibold text-danger-800 mb-4">Decline Reasons</h3>
          <ul className="space-y-2">
            {decision.decline_reasons.map((reason, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-danger-700">
                <XCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                {reason}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendations */}
      {report.recommendations?.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Recommendations
          </h3>
          <ul className="space-y-2">
            {report.recommendations.map((rec, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                <TrendingUp className="w-4 h-4 text-primary-500 flex-shrink-0 mt-0.5" />
                {rec}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Processing Info */}
      <div className="text-center text-sm text-gray-500 space-y-1">
        <p>Processing Time: {report.processing_time_seconds?.toFixed(2)}s</p>
        <p>Trace ID: {report.trace_id}</p>
        <p>Model Version: {report.model_version}</p>
      </div>
    </div>
  );
}

export default ResultsDashboard;
