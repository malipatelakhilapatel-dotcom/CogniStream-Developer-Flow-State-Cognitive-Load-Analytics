import React from 'react';
import { LucideIcon } from 'lucide-react';

interface KpiCardProps {
  label: string;
  value: string | number;
  unit?: string;
  subtitle: string;
  icon: LucideIcon;
  badge?: {
    text: string;
    variant: 'positive' | 'negative' | 'neutral';
  };
  highlight?: boolean;
}

export const KpiCard: React.FC<KpiCardProps> = ({
  label,
  value,
  unit,
  subtitle,
  icon: Icon,
  badge,
  highlight = false
}) => {
  return (
    <div
      className={`rounded-xl border bg-white p-5 transition-shadow hover:shadow-sm ${
        highlight ? 'border-indigo-200 bg-gradient-to-b from-indigo-50/20 to-white' : 'border-gray-200'
      }`}
    >
      <div className="flex items-center justify-between text-gray-500 mb-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">{label}</span>
        <div className={`p-1.5 rounded-lg ${highlight ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-600'}`}>
          <Icon className="w-4 h-4" />
        </div>
      </div>

      <div className="flex items-baseline gap-1.5 mb-1">
        <span className="text-2xl font-bold tracking-tight text-gray-900">{value}</span>
        {unit && <span className="text-sm font-medium text-gray-500">{unit}</span>}
      </div>

      <div className="flex items-center justify-between mt-2 pt-2 border-t border-gray-100">
        <span className="text-xs text-gray-500">{subtitle}</span>
        {badge && (
          <span
            className={`text-xs px-1.5 py-0.5 rounded font-medium ${
              badge.variant === 'positive'
                ? 'bg-emerald-50 text-emerald-700'
                : badge.variant === 'negative'
                ? 'bg-rose-50 text-rose-700'
                : 'bg-gray-100 text-gray-600'
            }`}
          >
            {badge.text}
          </span>
        )}
      </div>
    </div>
  );
};
