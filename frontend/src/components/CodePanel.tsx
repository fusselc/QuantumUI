import React, { useState } from 'react';
import { Code, Copy, Check, ShieldCheck, RefreshCw } from 'lucide-react';
import { ValidationReport } from '../types';

interface CodePanelProps {
  code: string;
  isUserEdited: boolean;
  onCodeChange: (newCode: string) => void;
  onValidate: () => void;
  validationReport?: ValidationReport;
  isLoading: boolean;
}

export const CodePanel: React.FC<CodePanelProps> = ({
  code,
  isUserEdited,
  onCodeChange,
  onValidate,
  validationReport,
  isLoading
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="glass-panel p-4 flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Code className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-semibold text-slate-200">Generated Qiskit Code</h3>
          <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full border ${
            isUserEdited
              ? 'bg-amber-950 text-amber-300 border-amber-700'
              : 'bg-sky-950 text-sky-300 border-sky-700'
          }`}>
            {isUserEdited ? 'Edited by You' : 'AI-Generated Draft'}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={onValidate}
            disabled={isLoading}
            className="text-xs text-slate-300 hover:text-cyan-400 bg-slate-900 border border-slate-700 rounded px-2.5 py-1 flex items-center gap-1 transition-all"
            title="Re-validate Python syntax and quantum circuit"
          >
            <RefreshCw className={`w-3 h-3 ${isLoading ? 'animate-spin' : ''}`} />
            Re-Validate
          </button>
          <button
            type="button"
            onClick={handleCopy}
            className="text-xs text-slate-300 hover:text-cyan-400 bg-slate-900 border border-slate-700 rounded px-2.5 py-1 flex items-center gap-1 transition-all"
          >
            {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
            {copied ? 'Copied' : 'Copy'}
          </button>
        </div>
      </div>

      <div className="relative rounded-lg overflow-hidden border border-slate-800 bg-slate-950 font-mono text-xs">
        <textarea
          value={code}
          onChange={(e) => onCodeChange(e.target.value)}
          rows={7}
          spellCheck={false}
          className="w-full p-3 bg-transparent text-cyan-200 focus:outline-none custom-scrollbar leading-relaxed resize-none"
        />
      </div>

      {validationReport && (
        <div className={`p-2.5 rounded-md text-xs border flex items-start gap-2 ${
          validationReport.is_valid
            ? 'bg-emerald-950/40 text-emerald-300 border-emerald-800/60'
            : 'bg-rose-950/40 text-rose-300 border-rose-800/60'
        }`}>
          <ShieldCheck className="w-4 h-4 flex-shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold">
              {validationReport.is_valid ? 'Static AST Validation Passed' : 'Validation Issues Detected'}:
            </span>
            {validationReport.is_valid ? (
              <span className="ml-1 text-slate-300">Syntax verified, imports safe, zero offensive patterns.</span>
            ) : (
              <ul className="list-disc list-inside mt-1 space-y-0.5 text-rose-200">
                {validationReport.errors.map((err, i) => (
                  <li key={i}>{err}</li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
