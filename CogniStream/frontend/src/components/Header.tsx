import React from 'react';
import { Database, RefreshCw, Calendar, Users, ShieldAlert } from 'lucide-react';
import { HealthStatus, FilterOption } from '../types/api';

interface HeaderProps {
  health: HealthStatus | null;
  teams: FilterOption[];
  selectedTeam: string;
  onSelectTeam: (teamId: string) => void;
  dateRange: string;
  onSelectDateRange: (range: string) => void;
  onRefresh: () => void;
  isRefreshing: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  health,
  teams,
  selectedTeam,
  onSelectTeam,
  dateRange,
  onSelectDateRange,
  onRefresh,
  isRefreshing
}) => {
  return (
    <header className="h-16 border-b border-gray-200 bg-white px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center gap-4">
        {/* Synthetic Demo Data Pill */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-medium">
          <ShieldAlert className="w-3.5 h-3.5 text-amber-600" />
          <span>SYNTHETIC DEMO DATA</span>
        </div>

        {/* Database Engine Indicator */}
        <div className="hidden md:flex items-center gap-2 text-xs text-gray-500 border-l border-gray-200 pl-4">
          <Database className="w-3.5 h-3.5 text-gray-400" />
          <span>Storage:</span>
          <span className="font-medium text-gray-800">
            {health?.database_connected ? 'ClickHouse MergeTree' : 'Embedded Local Engine'}
          </span>
          <span
            className={`w-2 h-2 rounded-full ${
              health?.database_connected ? 'bg-emerald-500' : 'bg-blue-500'
            }`}
            title={health?.database_connected ? 'Online ClickHouse instance' : 'Local verified data engine active'}
          />
        </div>
      </div>

      {/* Global Dashboard Filters */}
      <div className="flex items-center gap-3">
        {/* Team Selector */}
        <div className="flex items-center gap-1.5 bg-gray-50 border border-gray-200 rounded-lg px-2.5 py-1.5 text-xs text-gray-700">
          <Users className="w-3.5 h-3.5 text-gray-400" />
          <select
            value={selectedTeam}
            onChange={(e) => onSelectTeam(e.target.value)}
            className="bg-transparent font-medium text-gray-800 focus:outline-none cursor-pointer"
          >
            {teams.map((t) => (
              <option key={t.id} value={t.id}>
                {t.name}
              </option>
            ))}
          </select>
        </div>

        {/* Date Range Selector */}
        <div className="flex items-center gap-1.5 bg-gray-50 border border-gray-200 rounded-lg px-2.5 py-1.5 text-xs text-gray-700">
          <Calendar className="w-3.5 h-3.5 text-gray-400" />
          <select
            value={dateRange}
            onChange={(e) => onSelectDateRange(e.target.value)}
            className="bg-transparent font-medium text-gray-800 focus:outline-none cursor-pointer"
          >
            <option value="30d">Last 30 Days (Complete Demo Period)</option>
            <option value="14d">Last 14 Days</option>
            <option value="7d">Last 7 Days</option>
          </select>
        </div>

        {/* Refresh Button */}
        <button
          onClick={onRefresh}
          disabled={isRefreshing}
          className="p-1.5 text-gray-500 hover:text-gray-900 hover:bg-gray-100 rounded-lg border border-gray-200 transition-colors disabled:opacity-50"
          title="Refresh Telemetry Metrics"
        >
          <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin text-indigo-600' : ''}`} />
        </button>
      </div>
    </header>
  );
};
