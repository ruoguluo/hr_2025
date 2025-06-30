import React, { useState } from 'react';
import { Edit2, Check, X } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { MarketComparison } from '../types/analysis';

interface MarketComparisonTableProps {
  title: string;
  data: MarketComparison;
  companyName: string;
  onUpdate: (dimension: string, column: string, value: string) => void;
  className?: string;
}

export const MarketComparisonTable: React.FC<MarketComparisonTableProps> = ({ 
  title, 
  data, 
  companyName,
  onUpdate, 
  className = '' 
}) => {
  const [editingCell, setEditingCell] = useState<{ dimension: string; column: string } | null>(null);
  const [editValue, setEditValue] = useState('');

  const startEdit = (dimension: string, column: string, currentValue: string) => {
    setEditingCell({ dimension, column });
    setEditValue(currentValue);
  };

  const saveEdit = () => {
    if (editingCell && editValue.trim()) {
      onUpdate(editingCell.dimension, editingCell.column, editValue.trim());
    }
    setEditingCell(null);
    setEditValue('');
  };

  const cancelEdit = () => {
    setEditingCell(null);
    setEditValue('');
  };

  const isPlaceholder = (value: string) => value.includes('待补充 🔘');
  const isEditing = (dimension: string, column: string) => 
    editingCell?.dimension === dimension && editingCell?.column === column;

  const columns = [
    { key: '行业常规标准', label: 'Industry Standard' },
    { key: 'target_company', label: companyName },
    { key: 'competitor_a', label: 'Competitor A' },
    { key: 'competitor_b', label: 'Competitor B' },
  ];

  return (
    <div className={`bg-white rounded-lg border border-slate-200 overflow-hidden ${className}`}>
      <div className="bg-slate-50 px-6 py-4 border-b border-slate-200">
        <h3 className="text-lg font-semibold text-slate-800">{title}</h3>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-slate-100">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Dimension
              </th>
              {columns.map((col) => (
                <th key={col.key} className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  {col.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {Object.entries(data).map(([dimension, rowData]) => (
              <tr key={dimension} className="hover:bg-slate-50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap font-medium text-slate-700">
                  {dimension}
                </td>
                {columns.map((col) => {
                  const value = rowData[col.key as keyof typeof rowData];
                  const cellKey = `${dimension}-${col.key}`;
                  
                  return (
                    <td key={col.key} className="px-6 py-4 relative group">
                      {isEditing(dimension, col.key) ? (
                        <div className="space-y-2">
                          <Input
                            value={editValue}
                            onChange={(e) => setEditValue(e.target.value)}
                            className="w-full"
                            placeholder="Enter comparison data..."
                          />
                          <div className="flex space-x-1">
                            <Button
                              size="sm"
                              onClick={saveEdit}
                              className="bg-green-600 hover:bg-green-700 h-6 px-2"
                            >
                              <Check className="h-3 w-3" />
                            </Button>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={cancelEdit}
                              className="h-6 px-2"
                            >
                              <X className="h-3 w-3" />
                            </Button>
                          </div>
                        </div>
                      ) : (
                        <div className="flex items-center justify-between">
                          <div className={`text-sm ${
                            isPlaceholder(value) 
                              ? 'text-orange-600 font-medium' 
                              : 'text-slate-600'
                          }`}>
                            {value}
                          </div>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => startEdit(dimension, col.key, value)}
                            className="ml-2 opacity-0 group-hover:opacity-100 hover:bg-blue-50 h-6 w-6 p-0"
                          >
                            <Edit2 className="h-3 w-3" />
                          </Button>
                        </div>
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
