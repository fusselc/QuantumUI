import React from 'react';
import { ExecutionStatus } from '../types';
import { Circle, Play, AlertTriangle, CheckCircle, Clock, XCircle } from 'lucide-react';

interface StatusBadgeProps {
  status: ExecutionStatus;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'Draft':
        return { color: 'bg-slate-800 text-slate-300 border-slate-700', icon: <Circle className="w-3.5 h-3.5" /> };
      case 'Validating':
        return { color: 'bg-sky-950 text-sky-400 border-sky-800 animate-pulse', icon: <Clock className="w-3.5 h-3.5 animate-spin" /> };
      case 'Ready':
        return { color: 'bg-emerald-950 text-emerald-400 border-emerald-800', icon: <CheckCircle className="w-3.5 h-3.5" /> };
      case 'Running (Simulator)':
        return { color: 'bg-indigo-950 text-indigo-400 border-indigo-800 animate-pulse', icon: <Play className="w-3.5 h-3.5" /> };
      case 'Running (Hardware)':
        return { color: 'bg-rose-950 text-rose-400 border-rose-800 animate-pulse', icon: <Play className="w-3.5 h-3.5" /> };
      case 'Complete':
        return { color: 'bg-teal-950 text-teal-300 border-teal-800', icon: <CheckCircle className="w-3.5 h-3.5" /> };
      case 'Failed':
        return { color: 'bg-red-950 text-red-400 border-red-800', icon: <AlertTriangle className="w-3.5 h-3.5" /> };
      case 'Cancelled':
        return { color: 'bg-slate-900 text-slate-400 border-slate-800', icon: <XCircle className="w-3.5 h-3.5" /> };
      default:
        return { color: 'bg-slate-800 text-slate-300 border-slate-700', icon: <Circle className="w-3.5 h-3.5" /> };
    }
  };

  const config = getStatusConfig();

  return (
    <div
      role="status"
      aria-label={`Status: ${status}`}
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border ${config.color} transition-all`}
    >
      {config.icon}
      <span>{status}</span>
    </div>
  );
};
