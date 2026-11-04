import React from 'react';
import { Insight } from '../types/api';
import { AlertCircle, TrendingUp, CheckCircle, Info, AlertTriangle } from 'lucide-react';

interface InsightCardProps {
  insight: Insight;
}

export const InsightCard: React.FC<InsightCardProps> = ({ insight }) => {
  const config = {
    positive: {
      border: 'border-emerald-200 bg-emerald-50/40 text-emerald-900',
      icon: CheckCircle,
      iconColor: 'text-emerald-600',
      badge: 'bg-emerald-100 text-emerald-800'
    },
    negative: {
      border: 'border-rose-200 bg-rose-50/40 text-rose-900',
      icon: AlertCircle,
      iconColor: 'text-rose-600',
      badge: 'bg-rose-100 text-rose-800'
    },
    warning: {
      border: 'border-amber-200 bg-amber-50/40 text-amber-900',
      icon: AlertTriangle,
      iconColor: 'text-amber-600',
      badge: 'bg-amber-100 text-amber-800'
    },
    trend: {
      border: 'border-indigo-200 bg-indigo-50/40 text-indigo-900',
      icon: TrendingUp,
      iconColor: 'text-indigo-600',
      badge: 'bg-indigo-100 text-indigo-800'
    },
    info: {
      border: 'border-slate-200 bg-slate-50/40 text-slate-900',
      icon: Info,
      iconColor: 'text-slate-600',
      badge: 'bg-slate-100 text-slate-800'
    }
  }[insight.type] || {
    border: 'border-gray-200 bg-gray-50 text-gray-900',
    icon: Info,
    iconColor: 'text-gray-600',
    badge: 'bg-gray-100 text-gray-800'
  };

  const Icon = config.icon;

  return (
    <div className={`p-4 rounded-xl border ${config.border} flex items-start gap-3 transition-colors`}>
      <div className="mt-0.5">
        <Icon className={`w-5 h-5 ${config.iconColor}`} />
      </div>
      <div className="flex-1">
        <div className="flex items-center justify-between mb-1">
          <h4 className="text-sm font-semibold">{insight.title}</h4>
          <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full uppercase tracking-wider ${config.badge}`}>
            {insight.type}
          </span>
        </div>
        <p className="text-xs leading-relaxed text-gray-600">{insight.description}</p>
      </div>
    </div>
  );
};
