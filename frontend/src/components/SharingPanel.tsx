import React from 'react';
import { Share2, Download, ExternalLink, ShieldCheck } from 'lucide-react';
import { SharingState } from '../types';

interface SharingPanelProps {
  experimentId: string;
  sharingState: SharingState;
  onUpdateSharing: (newSharing: Partial<SharingState>) => void;
  onExportNotebook: () => void;
  onOpenColab: () => void;
}

export const SharingPanel: React.FC<SharingPanelProps> = ({
  experimentId: _experimentId,
  sharingState,
  onUpdateSharing,
  onExportNotebook,
  onOpenColab
}) => {
  return (
    <div className="glass-panel p-4 flex flex-col gap-3">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2.5">
        <div className="flex items-center gap-2">
          <Share2 className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-semibold text-slate-200">Export & Open Science</h3>
        </div>
        <span className="text-[11px] text-emerald-400 flex items-center gap-1 font-medium">
          <ShieldCheck className="w-3.5 h-3.5" />
          100% Private by Default
        </span>
      </div>

      {/* Export Buttons */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        <button
          type="button"
          onClick={onExportNotebook}
          className="flex items-center justify-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 rounded-lg p-2 text-xs font-medium transition-all"
        >
          <Download className="w-3.5 h-3.5 text-cyan-400" />
          Download Jupyter (.ipynb)
        </button>

        <button
          type="button"
          onClick={onOpenColab}
          className="flex items-center justify-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 rounded-lg p-2 text-xs font-medium transition-all"
        >
          <ExternalLink className="w-3.5 h-3.5 text-amber-400" />
          Launch in Google Colab
        </button>
      </div>

      {/* Independent Sharing Toggles */}
      <div className="pt-2 space-y-2 border-t border-slate-800 text-xs">
        <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wide">
          Opt-In Community Sharing (Independent Controls):
        </span>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
          <label className="flex items-center gap-2 p-2 bg-slate-950/60 rounded border border-slate-800/80 cursor-pointer hover:border-slate-700">
            <input
              type="checkbox"
              checked={sharingState.dataset}
              onChange={(e) => onUpdateSharing({ dataset: e.target.checked })}
              className="rounded bg-slate-900 border-slate-700 text-cyan-500 focus:ring-cyan-500"
            />
            <span className="text-slate-300">Contribute to Public Dataset</span>
          </label>

          <label className="flex items-center gap-2 p-2 bg-slate-950/60 rounded border border-slate-800/80 cursor-pointer hover:border-slate-700">
            <input
              type="checkbox"
              checked={sharingState.social}
              onChange={(e) => onUpdateSharing({ social: e.target.checked })}
              className="rounded bg-slate-900 border-slate-700 text-cyan-500 focus:ring-cyan-500"
            />
            <span className="text-slate-300">Generate Social Media Card</span>
          </label>
        </div>
      </div>
    </div>
  );
};
