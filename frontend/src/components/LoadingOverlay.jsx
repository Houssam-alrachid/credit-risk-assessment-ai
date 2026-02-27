import React from 'react';
import { Loader2, Brain } from 'lucide-react';

function LoadingOverlay({ message }) {
  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full mx-4">
        <div className="flex flex-col items-center">
          <div className="relative mb-6">
            <div className="bg-primary-100 p-4 rounded-full">
              <Brain className="h-12 w-12 text-primary-600" />
            </div>
            <Loader2 className="absolute -bottom-1 -right-1 h-6 w-6 text-primary-600 animate-spin" />
          </div>
          
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Analyzing Application
          </h3>
          
          <p className="text-gray-600 text-center mb-4">
            {message}
          </p>
          
          <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
            <div className="bg-primary-600 h-full rounded-full animate-pulse" style={{ width: '60%' }} />
          </div>
          
          <p className="text-xs text-gray-400 mt-4">
            6 AI agents analyzing your application...
          </p>
        </div>
      </div>
    </div>
  );
}

export default LoadingOverlay;
