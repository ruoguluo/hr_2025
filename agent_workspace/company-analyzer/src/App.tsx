import React, { useState } from 'react';
import { CompanyInputForm } from './components/CompanyInputForm';
import { AnalysisResults } from './components/AnalysisResults';
import { AnalysisResult, AnalysisState } from './types/analysis';
import { analysisService } from './services/analysisService';
import { Toaster } from './components/ui/toaster';
import { useToast } from './hooks/use-toast';

function App() {
  const [analysisState, setAnalysisState] = useState<AnalysisState>({
    isLoading: false,
    error: null,
    result: null
  });
  
  const { toast } = useToast();

  const handleAnalyze = async (companyName: string) => {
    setAnalysisState({ isLoading: true, error: null, result: null });
    
    try {
      const result = await analysisService.analyzeCompany(companyName);
      setAnalysisState({ isLoading: false, error: null, result });
      
      toast({
        title: "Analysis Complete",
        description: `Successfully analyzed ${companyName}. You can now edit fields and export the report.`,
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Analysis failed';
      setAnalysisState({ isLoading: false, error: errorMessage, result: null });
      
      toast({
        title: "Analysis Failed",
        description: errorMessage,
        variant: "destructive",
      });
    }
  };

  const handleUpdate = async (section: string, field: string, value: string) => {
    if (!analysisState.result) return;

    try {
      // Update local state immediately for better UX
      const updatedResult = { ...analysisState.result };
      if (section === 'company_info') {
        updatedResult.company_info = { ...updatedResult.company_info, [field]: value };
      } else if (section === 'products_services') {
        updatedResult.products_services = { ...updatedResult.products_services, [field]: value };
      }
      
      setAnalysisState(prev => ({ ...prev, result: updatedResult }));
      
      // Try to update on backend
      await analysisService.updateField(section, field, value);
      
      toast({
        title: "Field Updated",
        description: `Successfully updated "${field}"`,
      });
    } catch (error) {
      toast({
        title: "Update Failed",
        description: "Failed to save the update, but local changes are preserved.",
        variant: "destructive",
      });
    }
  };

  const handleMarketUpdate = async (dimension: string, column: string, value: string) => {
    if (!analysisState.result) return;

    try {
      // Update local state immediately
      const updatedResult = { ...analysisState.result };
      updatedResult.market_comparison = {
        ...updatedResult.market_comparison,
        [dimension]: {
          ...updatedResult.market_comparison[dimension as keyof typeof updatedResult.market_comparison],
          [column]: value
        }
      };
      
      setAnalysisState(prev => ({ ...prev, result: updatedResult }));
      
      // Try to update on backend
      await analysisService.updateField('market_comparison', `${dimension}.${column}`, value);
      
      toast({
        title: "Comparison Updated",
        description: `Successfully updated ${dimension} - ${column}`,
      });
    } catch (error) {
      toast({
        title: "Update Failed",
        description: "Failed to save the update, but local changes are preserved.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-slate-800 mb-4">
            Enterprise Company Analysis Platform
          </h1>
          <p className="text-lg text-slate-600 max-w-3xl mx-auto">
            Comprehensive business intelligence and competitive analysis for strategic decision making
          </p>
        </header>

        {/* Main Content */}
        {!analysisState.result ? (
          <div className="flex justify-center">
            <CompanyInputForm 
              onAnalyze={handleAnalyze} 
              isLoading={analysisState.isLoading} 
            />
          </div>
        ) : (
          <div className="space-y-6">
            {/* Back to Search */}
            <div className="flex justify-center mb-8">
              <button
                onClick={() => setAnalysisState({ isLoading: false, error: null, result: null })}
                className="text-blue-600 hover:text-blue-800 font-medium"
              >
                ← Analyze Another Company
              </button>
            </div>
            
            {/* Results */}
            <AnalysisResults 
              result={analysisState.result}
              onUpdate={handleUpdate}
              onMarketUpdate={handleMarketUpdate}
            />
          </div>
        )}

        {/* Error Display */}
        {analysisState.error && (
          <div className="max-w-2xl mx-auto mt-8">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <h3 className="text-red-800 font-semibold mb-2">Analysis Error</h3>
              <p className="text-red-700">{analysisState.error}</p>
            </div>
          </div>
        )}
      </div>
      
      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 mt-16">
        <div className="container mx-auto px-4 py-6">
          <div className="text-center text-slate-600">
            <p>© 2025 Company Analysis Platform. Professional business intelligence solutions.</p>
          </div>
        </div>
      </footer>
      
      <Toaster />
    </div>
  );
}

export default App;
