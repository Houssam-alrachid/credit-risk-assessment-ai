import React, { useState } from 'react';
import Header from './components/Header';
import ApplicationForm from './components/ApplicationForm';
import ResultsDashboard from './components/ResultsDashboard';
import LoadingOverlay from './components/LoadingOverlay';
import { assessCreditRisk } from './api/creditApi';

function App() {
  const [currentView, setCurrentView] = useState('form');
  const [isLoading, setIsLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('');
  const [assessmentResult, setAssessmentResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (applicationData) => {
    setIsLoading(true);
    setError(null);
    setLoadingMessage('Initializing credit assessment...');

    try {
      const result = await assessCreditRisk(applicationData, (progress) => {
        setLoadingMessage(progress.message || 'Processing...');
      });

      setAssessmentResult(result);
      setCurrentView('results');
    } catch (err) {
      setError(err.message || 'Assessment failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewAssessment = () => {
    setAssessmentResult(null);
    setCurrentView('form');
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 bg-danger-50 border border-danger-200 text-danger-700 px-4 py-3 rounded-lg">
            <p className="font-medium">Error</p>
            <p className="text-sm">{error}</p>
          </div>
        )}

        {currentView === 'form' && (
          <ApplicationForm onSubmit={handleSubmit} isLoading={isLoading} />
        )}

        {currentView === 'results' && assessmentResult && (
          <ResultsDashboard 
            result={assessmentResult} 
            onNewAssessment={handleNewAssessment}
          />
        )}
      </main>

      {isLoading && <LoadingOverlay message={loadingMessage} />}
    </div>
  );
}

export default App;
