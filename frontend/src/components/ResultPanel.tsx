import React, { useState } from 'react';
import { BarChart3, BookOpen, Clock, Activity } from 'lucide-react';
import { ExecutionResult, ExplanationByLevel } from '../types';

interface ResultPanelProps {
  result?: ExecutionResult;
  explanation?: ExplanationByLevel;
}

export const ResultPanel: React.FC<ResultPanelProps> = ({
  result,
  explanation
}) => {
  const [level, setLevel] = useState<'beginner' | 'intermediate' | 'technical'>('beginner');

  if (!result || !result.raw_result) {
    return (
      <div className="glass-panel p-6 text-center text-slate-500 text-xs italic">
        Run the experiment to observe measurement outcomes and plain-language quantum explanations.
      </div>
    );
  }

  const rawCounts = result.raw_result;
  const totalShots = Object.values(rawCounts).reduce((a, b) => a + b, 0);

  return (
    <div className="glass-panel p-4 flex flex-col gap-4">
      {/* Header with Telemetry */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-semibold text-slate-200">Measurement Outcomes (Histogram)</h3>
        </div>
        <div className="flex items-center gap-3 text-xs text-slate-400">
          <span className="flex items-center gap-1">
            <Clock className="w-3.5 h-3.5 text-slate-500" />
            {result.execution_time_ms} ms
          </span>
          <span className="flex items-center gap-1">
            <Activity className="w-3.5 h-3.5 text-emerald-400" />
            {totalShots} shots
          </span>
        </div>
      </div>

      {/* Visual Histogram Bars */}
      <div className="space-y-2 bg-slate-950 p-4 rounded-lg border border-slate-800/80">
        {Object.entries(rawCounts).map(([state, count]) => {
          const pct = ((count / totalShots) * 100).toFixed(1);
          return (
            <div key={state} className="space-y-1">
              <div className="flex justify-between text-xs font-mono">
                <span className="text-cyan-300 font-bold">|{state}⟩</span>
                <span className="text-slate-400">{count} shots ({pct}%)</span>
              </div>
              <div className="w-full h-3 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
                <div
                  className="h-full bg-gradient-to-r from-cyan-500 to-sky-400 transition-all duration-500"
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* 3-Level Explanation Engine */}
      {explanation && (
        <div className="flex flex-col gap-2 pt-2 border-t border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-200 flex items-center gap-1.5">
              <BookOpen className="w-4 h-4 text-purple-400" />
              AI Explanation Layer:
            </span>
            <div className="inline-flex rounded-lg bg-slate-900 p-0.5 border border-slate-800">
              {(['beginner', 'intermediate', 'technical'] as const).map((lvl) => (
                <button
                  key={lvl}
                  type="button"
                  onClick={() => setLevel(lvl)}
                  className={`text-[11px] font-medium px-2.5 py-0.5 rounded capitalize transition-all ${
                    level === lvl
                      ? 'bg-cyan-600 text-white shadow'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {lvl}
                </button>
              ))}
            </div>
          </div>

          <div className="bg-slate-950/80 p-3.5 rounded-lg border border-slate-800/80 text-xs text-slate-300 leading-relaxed">
            {explanation[level]}
          </div>
        </div>
      )}
    </div>
  );
};
