import React, { useState } from 'react';
import { Play, Cpu, AlertTriangle } from 'lucide-react';
import { ExecutionConfig, ProviderInfo } from '../types';

interface ExecutionControlBarProps {
  config: ExecutionConfig;
  providers: ProviderInfo[];
  onConfigChange: (newConfig: ExecutionConfig) => void;
  onExecute: (hardwareToken?: string) => void;
  isLoading: boolean;
}

export const ExecutionControlBar: React.FC<ExecutionControlBarProps> = ({
  config,
  providers,
  onConfigChange,
  onExecute,
  isLoading
}) => {
  const [showHardwareModal, setShowHardwareModal] = useState(false);
  const [confirmChecked, setConfirmChecked] = useState(false);

  const isHardware = config.backend_id !== 'aer_simulator';

  const handleRunClick = () => {
    if (isHardware) {
      setShowHardwareModal(true);
    } else {
      onExecute();
    }
  };

  const handleConfirmHardware = () => {
    setShowHardwareModal(false);
    onExecute('user-confirmed-hardware-token-v1');
  };

  return (
    <div className="glass-panel p-4 flex flex-col md:flex-row items-center justify-between gap-4 border-t-2 border-t-cyan-500/60">
      {/* Backend Selector */}
      <div className="flex items-center gap-3 w-full md:w-auto">
        <label className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
          <Cpu className="w-4 h-4 text-cyan-400" />
          Target Backend:
        </label>
        <select
          value={config.backend_id}
          onChange={(e) => onConfigChange({ ...config, backend_id: e.target.value })}
          disabled={isLoading}
          className="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-1.5 focus:border-cyan-400 focus:outline-none"
        >
          {providers.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name} {p.type === 'hardware' ? '(Physical QPU)' : '(Simulator)'}
            </option>
          ))}
        </select>
      </div>

      {/* Shots Control */}
      <div className="flex items-center gap-3 w-full md:w-auto">
        <label className="text-xs font-semibold text-slate-300">Shots (Trials):</label>
        <input
          type="number"
          value={config.shots}
          min={100}
          max={10000}
          step={256}
          onChange={(e) => onConfigChange({ ...config, shots: parseInt(e.target.value) || 1024 })}
          disabled={isLoading}
          className="w-24 bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-2.5 py-1.5 focus:border-cyan-400 focus:outline-none"
        />
      </div>

      {/* Primary Run Action */}
      <button
        type="button"
        onClick={handleRunClick}
        disabled={isLoading}
        className={`w-full md:w-auto inline-flex items-center justify-center gap-2 font-bold text-xs px-6 py-2.5 rounded-lg shadow-lg transition-all ${
          isHardware
            ? 'bg-gradient-to-r from-rose-600 to-pink-600 hover:from-rose-500 hover:to-pink-500 text-white shadow-rose-950/40'
            : 'bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white shadow-emerald-950/40'
        } disabled:opacity-50 disabled:cursor-not-allowed`}
      >
        <Play className={`w-4 h-4 fill-current ${isLoading ? 'animate-spin' : ''}`} />
        {isLoading ? 'Running Experiment...' : isHardware ? 'Run on Quantum Hardware' : 'Run on Simulator (Default)'}
      </button>

      {/* Hardware Safety Confirmation Modal */}
      {showHardwareModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="glass-panel max-w-md w-full p-6 border-rose-500/60 shadow-2xl bg-slate-950 flex flex-col gap-4">
            <div className="flex items-center gap-2 text-rose-400 font-bold text-base">
              <AlertTriangle className="w-5 h-5" />
              Confirm Real Quantum Hardware Execution
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              You are about to queue a quantum circuit on a physical Quantum Processing Unit (<strong>{config.backend_id}</strong>).
              Real quantum devices are subject to cloud queues and environmental noise (T1/T2 thermal decoherence).
            </p>

            <div className="bg-slate-900 p-3 rounded border border-slate-800 text-xs text-slate-400 space-y-1">
              <div>• Shots: {config.shots}</div>
              <div>• Execution primitive: Sampler</div>
              <div>• Cloud Queue: Active</div>
            </div>

            <label className="flex items-center gap-2 text-xs text-slate-200 cursor-pointer pt-2">
              <input
                type="checkbox"
                checked={confirmChecked}
                onChange={(e) => setConfirmChecked(e.target.checked)}
                className="rounded bg-slate-900 border-slate-700 text-rose-500 focus:ring-rose-500"
              />
              <span>I understand that real hardware is experimental and noisy.</span>
            </label>

            <div className="flex justify-end gap-2 pt-3 border-t border-slate-800">
              <button
                type="button"
                onClick={() => setShowHardwareModal(false)}
                className="px-3 py-1.5 text-xs text-slate-300 hover:text-white bg-slate-900 rounded-lg border border-slate-700"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleConfirmHardware}
                disabled={!confirmChecked}
                className="px-4 py-1.5 text-xs font-bold text-white bg-rose-600 hover:bg-rose-500 rounded-lg shadow-lg disabled:opacity-40 disabled:cursor-not-allowed"
              >
                Confirm Hardware Run
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
