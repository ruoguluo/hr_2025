import React, { useState } from 'react';
import { Edit2, Check, X } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';

interface EditableTableProps {
  title: string;
  data: Record<string, string> | { [key: string]: string };
  onUpdate: (field: string, value: string) => void;
  className?: string;
}

export const EditableTable: React.FC<EditableTableProps> = ({ 
  title, 
  data, 
  onUpdate, 
  className = '' 
}) => {
  const [editingField, setEditingField] = useState<string | null>(null);
  const [editValue, setEditValue] = useState('');

  const startEdit = (field: string, currentValue: string) => {
    setEditingField(field);
    setEditValue(currentValue);
  };

  const saveEdit = () => {
    if (editingField && editValue.trim()) {
      onUpdate(editingField, editValue.trim());
    }
    setEditingField(null);
    setEditValue('');
  };

  const cancelEdit = () => {
    setEditingField(null);
    setEditValue('');
  };

  const isPlaceholder = (value: string) => value.includes('待补充 🔘');

  return (
    <div className={`bg-white rounded-lg border border-slate-200 overflow-hidden ${className}`}>
      <div className="bg-slate-50 px-6 py-4 border-b border-slate-200">
        <h3 className="text-lg font-semibold text-slate-800">{title}</h3>
      </div>
      
      <div className="divide-y divide-slate-100">
        {Object.entries(data).map(([field, value]) => (
          <div key={field} className="px-6 py-4 hover:bg-slate-50 transition-colors">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="font-medium text-slate-700 mb-1">{field}</div>
                
                {editingField === field ? (
                  <div className="space-y-2">
                    {field.toLowerCase().includes('notes') || 
                     field.toLowerCase().includes('strategy') || 
                     field.toLowerCase().includes('differentiation') ? (
                      <Textarea
                        value={editValue}
                        onChange={(e) => setEditValue(e.target.value)}
                        className="w-full"
                        rows={3}
                        placeholder="Enter detailed information..."
                      />
                    ) : (
                      <Input
                        value={editValue}
                        onChange={(e) => setEditValue(e.target.value)}
                        className="w-full"
                        placeholder="Enter information..."
                      />
                    )}
                    <div className="flex space-x-2">
                      <Button
                        size="sm"
                        onClick={saveEdit}
                        className="bg-green-600 hover:bg-green-700"
                      >
                        <Check className="h-3 w-3 mr-1" />
                        Save
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={cancelEdit}
                      >
                        <X className="h-3 w-3 mr-1" />
                        Cancel
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="flex items-center justify-between">
                    <div className={`text-slate-600 ${
                      isPlaceholder(value) 
                        ? 'text-orange-600 font-medium' 
                        : ''
                    }`}>
                      {value}
                    </div>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => startEdit(field, value)}
                      className="ml-2 opacity-0 group-hover:opacity-100 hover:bg-blue-50"
                    >
                      <Edit2 className="h-3 w-3" />
                    </Button>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
