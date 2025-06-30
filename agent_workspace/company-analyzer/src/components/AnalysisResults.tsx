import React from 'react';
import { Download, Calendar, ExternalLink, FileText } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { EditableTable } from './EditableTable';
import { MarketComparisonTable } from './MarketComparisonTable';
import { AnalysisResult } from '../types/analysis';
import { analysisService } from '../services/analysisService';

interface AnalysisResultsProps {
  result: AnalysisResult;
  onUpdate: (section: string, field: string, value: string) => void;
  onMarketUpdate: (dimension: string, column: string, value: string) => void;
}

export const AnalysisResults: React.FC<AnalysisResultsProps> = ({ 
  result, 
  onUpdate,
  onMarketUpdate 
}) => {
  const handleExport = async () => {
    try {
      const report = await analysisService.exportAnalysis(result);
      
      // Create and download the report
      const blob = new Blob([report], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${result.company_name}_analysis_report.md`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Export failed:', error);
    }
  };

  const incompletePlaceholders = [
    ...Object.values(result.company_info),
    ...Object.values(result.products_services),
    ...Object.values(result.market_comparison).flatMap(item => Object.values(item))
  ].filter(value => String(value).includes('待补充 🔘')).length;

  return (
    <div className="w-full max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <Card className="border-0 shadow-lg bg-gradient-to-r from-blue-600 to-blue-700 text-white">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl font-bold text-white">
                Analysis Results: {result.company_name}
              </CardTitle>
              <div className="flex items-center space-x-4 mt-2 text-blue-100">
                <div className="flex items-center space-x-1">
                  <Calendar className="h-4 w-4" />
                  <span className="text-sm">Generated: {result.analysis_timestamp}</span>
                </div>
                {incompletePlaceholders > 0 && (
                  <div className="flex items-center space-x-1">
                    <FileText className="h-4 w-4" />
                    <span className="text-sm">{incompletePlaceholders} fields need completion</span>
                  </div>
                )}
              </div>
            </div>
            <Button 
              onClick={handleExport}
              variant="secondary"
              className="bg-white text-blue-600 hover:bg-blue-50"
            >
              <Download className="h-4 w-4 mr-2" />
              Export Report
            </Button>
          </div>
        </CardHeader>
      </Card>

      {/* Progress Indicator */}
      {incompletePlaceholders > 0 && (
        <Card className="border-orange-200 bg-orange-50">
          <CardContent className="pt-6">
            <div className="flex items-center space-x-4">
              <div className="flex-1">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-orange-800">
                    Analysis Completion Progress
                  </span>
                  <span className="text-sm text-orange-600">
                    {((67 - incompletePlaceholders) / 67 * 100).toFixed(0)}% Complete
                  </span>
                </div>
                <div className="w-full bg-orange-200 rounded-full h-2">
                  <div 
                    className="bg-orange-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(67 - incompletePlaceholders) / 67 * 100}%` }}
                  />
                </div>
              </div>
            </div>
            <p className="text-sm text-orange-700 mt-2">
              Click the edit icons to fill in the fields marked with 【待补充 🔘】 for a complete analysis.
            </p>
          </CardContent>
        </Card>
      )}

      {/* Company Information Table */}
      <EditableTable
        title="📌 Company Information"
        data={result.company_info}
        onUpdate={(field, value) => onUpdate('company_info', field, value)}
        className="shadow-md"
      />

      {/* Products & Services Table */}
      <EditableTable
        title="📋 Products & Services Information"
        data={result.products_services}
        onUpdate={(field, value) => onUpdate('products_services', field, value)}
        className="shadow-md"
      />

      {/* Market Comparison Table */}
      <MarketComparisonTable
        title="📊 Market Comparison Analysis"
        data={result.market_comparison}
        companyName={result.company_name}
        onUpdate={onMarketUpdate}
        className="shadow-md"
      />

      {/* Research Sources */}
      <Card className="shadow-md">
        <CardHeader>
          <CardTitle className="text-lg">📚 Research Sources</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {result.research_sources.map((source, index) => (
              <div key={index} className="flex items-center space-x-2 p-3 bg-slate-50 rounded-lg">
                <ExternalLink className="h-4 w-4 text-slate-500" />
                <span className="text-sm text-slate-700">{source}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Tips */}
      <Card className="border-blue-200 bg-blue-50">
        <CardContent className="pt-6">
          <h4 className="font-semibold text-blue-800 mb-2">💡 Analysis Tips</h4>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>• Click any field with 【待补充 🔘】 to add specific information</li>
            <li>• Use the export function to generate a comprehensive report</li>
            <li>• Market comparison data helps identify competitive positioning</li>
            <li>• Keep information updated as new data becomes available</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
};
