import React from 'react';
import { Template } from '../types';
import { Atom } from 'lucide-react';

interface TemplateCardProps {
  template: Template;
  isSelected: boolean;
  onSelect: (template: Template) => void;
}

export const TemplateCard: React.FC<TemplateCardProps> = ({
  template,
  isSelected,
  onSelect
}) => {
  const getDifficultyColor = () => {
    switch (template.difficulty) {
      case 'beginner':
        return 'text-emerald-400 bg-emerald-950/60 border-emerald-800/60';
      case 'intermediate':
        return 'text-amber-400 bg-amber-950/60 border-amber-800/60';
      case 'advanced':
        return 'text-purple-400 bg-purple-950/60 border-purple-800/60';
      default:
        return 'text-slate-400 bg-slate-800 border-slate-700';
    }
  };

  return (
    <div
      tabIndex={0}
      role="button"
      aria-pressed={isSelected}
      onClick={() => onSelect(template)}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onSelect(template);
        }
      }}
      className={`glass-panel p-3.5 text-left transition-all cursor-pointer border flex flex-col justify-between gap-2 ${
        isSelected
          ? 'border-cyan-400 bg-slate-900/90 shadow-lg shadow-cyan-950/40 ring-1 ring-cyan-400'
          : 'border-slate-800/80 hover:border-slate-700 bg-slate-950/40 hover:bg-slate-900/40'
      }`}
    >
      <div>
        <div className="flex items-center justify-between gap-2 mb-1.5">
          <span className="font-medium text-sm text-slate-100 flex items-center gap-1.5">
            <Atom className="w-3.5 h-3.5 text-cyan-400" />
            {template.name}
          </span>
          <span className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded border ${getDifficultyColor()}`}>
            {template.difficulty}
          </span>
        </div>
        <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
          {template.description}
        </p>
      </div>

      <div className="flex items-center justify-between text-[11px] text-slate-500 pt-1 border-t border-slate-800/60">
        <span>{template.category}</span>
        <span className="text-cyan-400 font-medium">Load Template →</span>
      </div>
    </div>
  );
};
