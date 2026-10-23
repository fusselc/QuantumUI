import React, { useState } from 'react';
import { Eye, List } from 'lucide-react';

interface CircuitVisualizerProps {
  code: string;
  circuitDescription?: string;
}

export const CircuitVisualizer: React.FC<CircuitVisualizerProps> = ({
  code,
  circuitDescription
}) => {
  const [showAltText, setShowAltText] = useState(false);

  // Extract simple gate representations
  const parseGates = () => {
    const lines = code.split('\n');
    const gates: Array<{ type: string; qubit: string; target?: string }> = [];

    lines.forEach((line) => {
      const trimmed = line.trim();
      if (trimmed.includes('.h(')) {
        const m = trimmed.match(/\.h\((\d+)\)/);
        if (m) gates.push({ type: 'H', qubit: `q[${m[1]}]` });
      } else if (trimmed.includes('.x(')) {
        const m = trimmed.match(/\.x\((\d+)\)/);
        if (m) gates.push({ type: 'X', qubit: `q[${m[1]}]` });
      } else if (trimmed.includes('.p(')) {
        const m = trimmed.match(/\.p\([^,]+,\s*(\d+)\)/);
        if (m) gates.push({ type: 'P(θ)', qubit: `q[${m[1]}]` });
      } else if (trimmed.includes('.cx(')) {
        const m = trimmed.match(/\.cx\((\d+),\s*(\d+)\)/);
        if (m) gates.push({ type: 'CNOT', qubit: `q[${m[1]}]`, target: `q[${m[2]}]` });
      } else if (trimmed.includes('.measure')) {
        gates.push({ type: 'M', qubit: 'All Qubits' });
      }
    });
    return gates;
  };

  const parsedGates = parseGates();

  return (
    <div className="glass-panel p-4 flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Eye className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-semibold text-slate-200">Interactive Circuit Board</h3>
        </div>
        <button
          type="button"
          onClick={() => setShowAltText(!showAltText)}
          className="text-xs text-slate-400 hover:text-cyan-300 flex items-center gap-1 border border-slate-700 rounded px-2 py-0.5 transition-all"
          aria-expanded={showAltText}
        >
          <List className="w-3.5 h-3.5" />
          {showAltText ? 'View Schematic' : 'Text Alternative (WCAG)'}
        </button>
      </div>

      {showAltText ? (
        <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-xs text-slate-300 space-y-2">
          <p className="font-medium text-cyan-400">Screen-Reader Accessible Operation Breakdown:</p>
          <p className="leading-relaxed">{circuitDescription || 'Qubits initialized to ground state |0>. Gates applied in chronological sequence followed by computational basis measurement.'}</p>
        </div>
      ) : (
        <div className="bg-slate-950/90 p-4 rounded-lg border border-slate-800/80 overflow-x-auto custom-scrollbar min-h-[110px] flex items-center">
          {parsedGates.length === 0 ? (
            <span className="text-xs text-slate-500 italic">No quantum gates detected in code yet.</span>
          ) : (
            <div className="flex items-center gap-3 min-w-max">
              <div className="px-2 py-1 bg-slate-900 text-slate-400 rounded text-[11px] font-mono border border-slate-800">
                |0⟩ Init
              </div>
              {parsedGates.map((gate, i) => (
                <React.Fragment key={i}>
                  <div className="h-[2px] w-6 bg-slate-700" />
                  <div className={`px-2.5 py-1.5 rounded text-xs font-mono font-bold shadow flex flex-col items-center justify-center min-w-[36px] ${
                    gate.type === 'H' ? 'bg-cyan-900/80 text-cyan-300 border border-cyan-700' :
                    gate.type === 'CNOT' ? 'bg-purple-900/80 text-purple-300 border border-purple-700' :
                    gate.type === 'M' ? 'bg-emerald-900/80 text-emerald-300 border border-emerald-700' :
                    'bg-slate-800 text-slate-200 border border-slate-700'
                  }`}>
                    <span>{gate.type}</span>
                    <span className="text-[9px] font-normal text-slate-400">{gate.qubit}</span>
                  </div>
                </React.Fragment>
              ))}
              <div className="h-[2px] w-6 bg-slate-700" />
              <div className="px-2 py-1 bg-slate-900 text-emerald-400 rounded text-[11px] font-mono border border-slate-800">
                Measure ⚡
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
