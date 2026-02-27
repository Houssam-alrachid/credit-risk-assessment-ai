import React from 'react';
import { Building2, Shield } from 'lucide-react';

function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="bg-primary-600 p-2 rounded-lg">
              <Building2 className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Credit Risk Assessment</h1>
              <p className="text-xs text-gray-500">AI-Powered Loan Underwriting</p>
            </div>
          </div>
          
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Shield className="h-4 w-4 text-success-500" />
            <span>Basel III Compliant</span>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
