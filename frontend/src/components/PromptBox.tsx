import React from 'react';
import { Sparkles, ArrowRight } from 'lucide-react';

interface PromptBoxProps {
  promptText: string;
  onPromptChange: (text: string) => void;
  onSubmit: () => void;
  suggestionChips: string[];
  isLoading: boolean;
}

export const PromptBox: React.FC<PromptBoxProps> = ({
  promptText,
  onPromptChange,
  onSubmit,
  suggestionChips,
  isLoading
}) => {
  return (
    <div className="glass-panel p-4 flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <label htmlFor="nl-prompt" className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-cyan-400" />
          Describe your quantum experiment in plain English
        </label>
        <span className="text-xs text-slate-400">No programming required</span>
      </div>

      <div className="relative">
        <textarea
          id="nl-prompt"
          value={promptText}
          onChange={(e) => onPromptChange(e.target.value)}
          placeholder="e.g. Create a 2-qubit circuit, put qubit 0 into superposition, entangle it with qubit 1, and measure both."
          rows={3}
          disabled={isLoading}
          className="w-full bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-sm text-slate-100 placeholder-slate-500 focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition-all resize-none"
        />
      </div>

      {suggestionChips.length > 0 && (
        <div className="flex flex-wrap items-center gap-2 pt-1">
          <span className="text-xs text-slate-400">Suggestions:</span>
          {suggestionChips.map((chip, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => onPromptChange(chip)}
              className="text-xs bg-slate-900 hover:bg-slate-800 text-cyan-300 border border-slate-700/60 hover:border-cyan-500/40 rounded-md px-2.5 py-1 transition-all focus:outline-none focus:ring-2 focus:ring-cyan-400"
            >
              {chip}
            </button>
          ))}
        </div>
      )}

      <div className="flex justify-end">
        <button
          type="button"
          onClick={onSubmit}
          disabled={isLoading || !promptText.trim()}
          className="inline-flex items-center gap-2 bg-gradient-to-r from-cyan-600 to-sky-600 hover:from-cyan-500 hover:to-sky-500 text-white font-medium text-xs px-4 py-2 rounded-lg shadow-lg shadow-cyan-900/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Translating to Qiskit...' : 'Generate Circuit'}
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
