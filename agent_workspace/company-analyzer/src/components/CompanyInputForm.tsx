import React, { useState } from 'react';
import { Search, Building2 } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';

interface CompanyInputFormProps {
  onAnalyze: (companyName: string) => void;
  isLoading: boolean;
}

export const CompanyInputForm: React.FC<CompanyInputFormProps> = ({ onAnalyze, isLoading }) => {
  const [companyName, setCompanyName] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (companyName.trim()) {
      onAnalyze(companyName.trim());
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <Card className="border-0 shadow-xl bg-gradient-to-br from-slate-50 to-blue-50">
        <CardHeader className="text-center space-y-4 pb-8">
          <div className="flex justify-center">
            <div className="p-4 bg-blue-600 rounded-full">
              <Building2 className="h-8 w-8 text-white" />
            </div>
          </div>
          <CardTitle className="text-3xl font-bold text-slate-800">
            Company Analysis Platform
          </CardTitle>
          <CardDescription className="text-lg text-slate-600 max-w-2xl mx-auto">
            Get comprehensive insights into any company including financial data, market position, 
            competitive analysis, and strategic recommendations
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="company-name" className="text-sm font-medium text-slate-700">
                Company Name
              </label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                <Input
                  id="company-name"
                  type="text"
                  placeholder="Enter company name (e.g., Tesla, Apple, Microsoft)"
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                  className="pl-10 h-12 text-base border-slate-300 focus:border-blue-500 focus:ring-blue-500"
                  disabled={isLoading}
                />
              </div>
            </div>
            
            <Button
              type="submit"
              className="w-full h-12 text-base font-semibold bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-200"
              disabled={isLoading || !companyName.trim()}
            >
              {isLoading ? (
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Analyzing Company...</span>
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <Search className="h-4 w-4" />
                  <span>Start Analysis</span>
                </div>
              )}
            </Button>
          </form>
          
          <div className="bg-white rounded-lg p-4 border border-slate-200">
            <h3 className="font-semibold text-slate-800 mb-2">What you'll get:</h3>
            <ul className="text-sm text-slate-600 space-y-1">
              <li>• Comprehensive company information and structure</li>
              <li>• Detailed products and services analysis</li>
              <li>• Market comparison with key competitors</li>
              <li>• Editable fields for additional insights</li>
              <li>• Exportable analysis reports</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
