import React, { useState } from 'react';
import { User, Briefcase, CreditCard, Home, FileText, ChevronRight, ChevronLeft } from 'lucide-react';

const STEPS = [
  { id: 'applicant', title: 'Applicant', icon: User },
  { id: 'employment', title: 'Employment', icon: Briefcase },
  { id: 'debts', title: 'Existing Debts', icon: CreditCard },
  { id: 'collateral', title: 'Collateral', icon: Home },
  { id: 'loan', title: 'Loan Request', icon: FileText },
];

const initialFormData = {
  application_id: `APP-${Date.now()}`,
  applicant: {
    first_name: '',
    last_name: '',
    date_of_birth: '',
    nationality: 'FR',
    email: '',
    phone: '',
  },
  employment: {
    employment_type: 'employed',
    employer_name: '',
    job_title: '',
    industry: '',
    years_employed: 0,
    years_in_profession: 0,
    monthly_gross_income: 0,
    monthly_net_income: 0,
    additional_income: 0,
    income_verified: false,
  },
  existing_debts: [],
  collateral: null,
  loan_request: {
    loan_purpose: 'mortgage',
    requested_amount: 0,
    requested_term_months: 240,
    preferred_payment_day: 1,
    purpose_description: '',
  },
  credit_history: {
    credit_score: 700,
    credit_score_source: 'bureau',
    accounts_open: 0,
    accounts_closed: 0,
    oldest_account_years: 0,
    recent_inquiries: 0,
    delinquencies_30_days: 0,
    delinquencies_60_days: 0,
    delinquencies_90_days: 0,
    bankruptcies: 0,
    foreclosures: 0,
    collections: 0,
  },
};

function ApplicationForm({ onSubmit, isLoading }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState(initialFormData);

  const updateFormData = (section, field, value) => {
    setFormData(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value,
      },
    }));
  };

  const handleNext = () => {
    if (currentStep < STEPS.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrev = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const loadSampleData = (type) => {
    if (type === 'good') {
      setFormData({
        ...initialFormData,
        application_id: `APP-${Date.now()}`,
        applicant: {
          first_name: 'Marie',
          last_name: 'Martin',
          date_of_birth: '1985-03-20',
          nationality: 'FR',
          email: 'marie.martin@email.com',
          phone: '+33612345678',
        },
        employment: {
          employment_type: 'employed',
          employer_name: 'BNP Paribas',
          job_title: 'Senior Financial Analyst',
          industry: 'Banking & Finance',
          years_employed: 6.5,
          years_in_profession: 12,
          monthly_gross_income: 7500,
          monthly_net_income: 5625,
          additional_income: 500,
          income_verified: true,
        },
        existing_debts: [
          {
            debt_type: 'auto_loan',
            creditor_name: 'Crédit Auto France',
            original_amount: 25000,
            current_balance: 12000,
            monthly_payment: 420,
            interest_rate: 4.5,
            remaining_months: 30,
            is_secured: true,
            payment_history: 'excellent',
          },
        ],
        collateral: {
          collateral_type: 'real_estate',
          description: 'Appartement 3 pièces, 75m², Paris 15ème',
          estimated_value: 450000,
          valuation_date: '2024-01-15',
          valuation_source: 'Expert immobilier agréé',
          encumbrances: 0,
          insurance_coverage: 450000,
        },
        loan_request: {
          loan_purpose: 'mortgage',
          requested_amount: 320000,
          requested_term_months: 240,
          preferred_payment_day: 5,
          purpose_description: 'Acquisition résidence principale',
        },
        credit_history: {
          credit_score: 745,
          credit_score_source: 'Banque de France',
          accounts_open: 4,
          accounts_closed: 2,
          oldest_account_years: 15,
          recent_inquiries: 1,
          delinquencies_30_days: 0,
          delinquencies_60_days: 0,
          delinquencies_90_days: 0,
          bankruptcies: 0,
          foreclosures: 0,
          collections: 0,
        },
      });
    } else {
      setFormData({
        ...initialFormData,
        application_id: `APP-${Date.now()}`,
        applicant: {
          first_name: 'Pierre',
          last_name: 'Dubois',
          date_of_birth: '1992-08-10',
          nationality: 'FR',
          email: 'pierre.dubois@email.com',
          phone: '+33698765432',
        },
        employment: {
          employment_type: 'contractor',
          employer_name: 'Various Clients',
          job_title: 'Freelance Developer',
          industry: 'Technology',
          years_employed: 1.5,
          years_in_profession: 3,
          monthly_gross_income: 4500,
          monthly_net_income: 3200,
          additional_income: 0,
          income_verified: false,
        },
        existing_debts: [
          {
            debt_type: 'personal_loan',
            creditor_name: 'Cofidis',
            original_amount: 15000,
            current_balance: 11000,
            monthly_payment: 350,
            interest_rate: 8.5,
            remaining_months: 36,
            is_secured: false,
            payment_history: 'fair',
          },
        ],
        collateral: null,
        loan_request: {
          loan_purpose: 'debt_consolidation',
          requested_amount: 25000,
          requested_term_months: 60,
          preferred_payment_day: 15,
          purpose_description: 'Consolidation des crédits existants',
        },
        credit_history: {
          credit_score: 580,
          credit_score_source: 'Banque de France',
          accounts_open: 5,
          accounts_closed: 1,
          oldest_account_years: 4,
          recent_inquiries: 6,
          delinquencies_30_days: 3,
          delinquencies_60_days: 1,
          delinquencies_90_days: 0,
          bankruptcies: 0,
          foreclosures: 0,
          collections: 0,
        },
      });
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Quick Load Buttons */}
      <div className="mb-6 flex gap-4 justify-center">
        <button
          type="button"
          onClick={() => loadSampleData('good')}
          className="px-4 py-2 bg-success-50 text-success-600 rounded-lg hover:bg-success-100 transition-colors text-sm font-medium"
        >
          Load Good Profile (Marie)
        </button>
        <button
          type="button"
          onClick={() => loadSampleData('risky')}
          className="px-4 py-2 bg-danger-50 text-danger-600 rounded-lg hover:bg-danger-100 transition-colors text-sm font-medium"
        >
          Load Risky Profile (Pierre)
        </button>
      </div>

      {/* Progress Steps */}
      <div className="mb-8">
        <div className="flex justify-between">
          {STEPS.map((step, index) => {
            const Icon = step.icon;
            const isActive = index === currentStep;
            const isCompleted = index < currentStep;
            
            return (
              <div
                key={step.id}
                className={`flex flex-col items-center cursor-pointer ${
                  isActive ? 'text-primary-600' : isCompleted ? 'text-success-500' : 'text-gray-400'
                }`}
                onClick={() => setCurrentStep(index)}
              >
                <div className={`w-10 h-10 rounded-full flex items-center justify-center mb-2 ${
                  isActive ? 'bg-primary-100' : isCompleted ? 'bg-success-100' : 'bg-gray-100'
                }`}>
                  <Icon className="w-5 h-5" />
                </div>
                <span className="text-xs font-medium">{step.title}</span>
              </div>
            );
          })}
        </div>
        <div className="mt-4 h-2 bg-gray-200 rounded-full">
          <div
            className="h-full bg-primary-600 rounded-full transition-all duration-300"
            style={{ width: `${((currentStep + 1) / STEPS.length) * 100}%` }}
          />
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="card">
          {/* Step 0: Applicant Info */}
          {currentStep === 0 && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold text-gray-900">Applicant Information</h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.applicant.first_name}
                    onChange={(e) => updateFormData('applicant', 'first_name', e.target.value)}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.applicant.last_name}
                    onChange={(e) => updateFormData('applicant', 'last_name', e.target.value)}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Date of Birth</label>
                  <input
                    type="date"
                    className="input-field"
                    value={formData.applicant.date_of_birth}
                    onChange={(e) => updateFormData('applicant', 'date_of_birth', e.target.value)}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Nationality</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.applicant.nationality}
                    onChange={(e) => updateFormData('applicant', 'nationality', e.target.value)}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    type="email"
                    className="input-field"
                    value={formData.applicant.email}
                    onChange={(e) => updateFormData('applicant', 'email', e.target.value)}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                  <input
                    type="tel"
                    className="input-field"
                    value={formData.applicant.phone}
                    onChange={(e) => updateFormData('applicant', 'phone', e.target.value)}
                  />
                </div>
              </div>
              
              {/* Credit History Section */}
              <h3 className="text-lg font-medium text-gray-900 mt-6">Credit History</h3>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Credit Score</label>
                  <input
                    type="number"
                    className="input-field"
                    min="300"
                    max="850"
                    value={formData.credit_history.credit_score}
                    onChange={(e) => updateFormData('credit_history', 'credit_score', parseInt(e.target.value))}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Open Accounts</label>
                  <input
                    type="number"
                    className="input-field"
                    min="0"
                    value={formData.credit_history.accounts_open}
                    onChange={(e) => updateFormData('credit_history', 'accounts_open', parseInt(e.target.value))}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Recent Inquiries</label>
                  <input
                    type="number"
                    className="input-field"
                    min="0"
                    value={formData.credit_history.recent_inquiries}
                    onChange={(e) => updateFormData('credit_history', 'recent_inquiries', parseInt(e.target.value))}
                  />
                </div>
              </div>
            </div>
          )}

          {/* Step 1: Employment */}
          {currentStep === 1 && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold text-gray-900">Employment Information</h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Employment Type</label>
                  <select
                    className="input-field"
                    value={formData.employment.employment_type}
                    onChange={(e) => updateFormData('employment', 'employment_type', e.target.value)}
                  >
                    <option value="employed">Employed</option>
                    <option value="self_employed">Self-Employed</option>
                    <option value="contractor">Contractor</option>
                    <option value="retired">Retired</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Employer Name</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.employment.employer_name}
                    onChange={(e) => updateFormData('employment', 'employer_name', e.target.value)}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Job Title</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.employment.job_title}
                    onChange={(e) => updateFormData('employment', 'job_title', e.target.value)}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Industry</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.employment.industry}
                    onChange={(e) => updateFormData('employment', 'industry', e.target.value)}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Years at Current Job</label>
                  <input
                    type="number"
                    className="input-field"
                    step="0.5"
                    min="0"
                    value={formData.employment.years_employed}
                    onChange={(e) => updateFormData('employment', 'years_employed', parseFloat(e.target.value))}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Years in Profession</label>
                  <input
                    type="number"
                    className="input-field"
                    step="0.5"
                    min="0"
                    value={formData.employment.years_in_profession}
                    onChange={(e) => updateFormData('employment', 'years_in_profession', parseFloat(e.target.value))}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Monthly Gross Income (€)</label>
                  <input
                    type="number"
                    className="input-field"
                    min="0"
                    value={formData.employment.monthly_gross_income}
                    onChange={(e) => updateFormData('employment', 'monthly_gross_income', parseFloat(e.target.value))}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Monthly Net Income (€)</label>
                  <input
                    type="number"
                    className="input-field"
                    min="0"
                    value={formData.employment.monthly_net_income}
                    onChange={(e) => updateFormData('employment', 'monthly_net_income', parseFloat(e.target.value))}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Additional Income (€)</label>
                  <input
                    type="number"
                    className="input-field"
                    min="0"
                    value={formData.employment.additional_income}
                    onChange={(e) => updateFormData('employment', 'additional_income', parseFloat(e.target.value))}
                  />
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="income_verified"
                    className="h-4 w-4 text-primary-600 rounded"
                    checked={formData.employment.income_verified}
                    onChange={(e) => updateFormData('employment', 'income_verified', e.target.checked)}
                  />
                  <label htmlFor="income_verified" className="ml-2 text-sm text-gray-700">
                    Income Verified
                  </label>
                </div>
              </div>
            </div>
          )}

          {/* Step 2: Existing Debts */}
          {currentStep === 2 && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold text-gray-900">Existing Debts</h2>
              <p className="text-gray-600 text-sm">
                {formData.existing_debts.length === 0 
                  ? 'No existing debts added. Click "Add Debt" to add one.'
                  : `${formData.existing_debts.length} debt(s) added.`
                }
              </p>
              {formData.existing_debts.map((debt, index) => (
                <div key={index} className="p-4 bg-gray-50 rounded-lg">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-medium">{debt.creditor_name}</span>
                    <span className="text-sm text-gray-500">€{debt.current_balance}</span>
                  </div>
                </div>
              ))}
              <p className="text-sm text-gray-500 italic">
                Debts are pre-loaded with sample data. In production, you would add a form to add/edit debts.
              </p>
            </div>
          )}

          {/* Step 3: Collateral */}
          {currentStep === 3 && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold text-gray-900">Collateral (Optional)</h2>
              {formData.collateral ? (
                <div className="p-4 bg-gray-50 rounded-lg">
                  <div className="flex justify-between items-center">
                    <div>
                      <span className="font-medium">{formData.collateral.description}</span>
                      <p className="text-sm text-gray-500">Type: {formData.collateral.collateral_type}</p>
                    </div>
                    <span className="text-lg font-semibold text-success-600">
                      €{formData.collateral.estimated_value?.toLocaleString()}
                    </span>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500 italic">No collateral provided</p>
              )}
            </div>
          )}

          {/* Step 4: Loan Request */}
          {currentStep === 4 && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold text-gray-900">Loan Request</h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Loan Purpose</label>
                  <select
                    className="input-field"
                    value={formData.loan_request.loan_purpose}
                    onChange={(e) => updateFormData('loan_request', 'loan_purpose', e.target.value)}
                  >
                    <option value="mortgage">Mortgage</option>
                    <option value="auto">Auto Loan</option>
                    <option value="personal">Personal Loan</option>
                    <option value="business">Business Loan</option>
                    <option value="debt_consolidation">Debt Consolidation</option>
                    <option value="home_improvement">Home Improvement</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Requested Amount (€)</label>
                  <input
                    type="number"
                    className="input-field"
                    min="1000"
                    value={formData.loan_request.requested_amount}
                    onChange={(e) => updateFormData('loan_request', 'requested_amount', parseFloat(e.target.value))}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Term (Months)</label>
                  <input
                    type="number"
                    className="input-field"
                    min="12"
                    max="480"
                    value={formData.loan_request.requested_term_months}
                    onChange={(e) => updateFormData('loan_request', 'requested_term_months', parseInt(e.target.value))}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Purpose Description</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.loan_request.purpose_description}
                    onChange={(e) => updateFormData('loan_request', 'purpose_description', e.target.value)}
                  />
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Navigation */}
        <div className="mt-6 flex justify-between">
          <button
            type="button"
            onClick={handlePrev}
            className="btn-secondary flex items-center gap-2"
            disabled={currentStep === 0}
          >
            <ChevronLeft className="w-4 h-4" />
            Previous
          </button>
          
          {currentStep < STEPS.length - 1 ? (
            <button
              type="button"
              onClick={handleNext}
              className="btn-primary flex items-center gap-2"
            >
              Next
              <ChevronRight className="w-4 h-4" />
            </button>
          ) : (
            <button
              type="submit"
              className="btn-primary flex items-center gap-2"
              disabled={isLoading}
            >
              {isLoading ? 'Processing...' : 'Submit Application'}
            </button>
          )}
        </div>
      </form>
    </div>
  );
}

export default ApplicationForm;
