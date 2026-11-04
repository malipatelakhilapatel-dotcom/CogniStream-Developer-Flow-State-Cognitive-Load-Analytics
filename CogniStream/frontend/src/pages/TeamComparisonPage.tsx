import React from 'react';
import { TeamComparisonMetric } from '../types/api';
import { Users, Sparkles, Bell, Zap, Info, Shield } from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell
} from 'recharts';

interface TeamComparisonPageProps {
  teams: TeamComparisonMetric[];
  isLoading: boolean;
}

export const TeamComparisonPage: React.FC<TeamComparisonPageProps> = ({ teams, isLoading }) => {
  if (isLoading) {
    return (
      <div className="p-12 flex justify-center items-center">
        <div className="w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const teamColors: Record<string, string> = {
    'team-platform': '#4F46E5',
    'team-product': '#0D9488',
    'team-data': '#F59E0B'
  };

  return (
    <div className="space-y-8">
      {/* Title */}
      <div>
        <h1 className="text-xl font-bold tracking-tight text-gray-950">Team Flow Comparison</h1>
        <p className="text-sm text-gray-500 mt-1">
          Normalized focus capacity and friction tax across engineering organizations.
        </p>
      </div>

      {/* Normalization & Ethical Disclaimer */}
      <div className="rounded-xl border border-gray-200 bg-white p-4 text-xs text-gray-600 flex items-start gap-3">
        <Shield className="w-5 h-5 text-indigo-600 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <p className="font-semibold text-gray-900">Per-Developer Normalization & Team Integrity</p>
          <p className="text-gray-500 leading-relaxed">
            Metrics are normalized by active headcount to avoid size bias. CogniStream strictly avoids ranking individual engineers
            or generating individual productivity scores. Telemetry is intended solely to diagnose organizational friction and notification policies.
          </p>
        </div>
      </div>

      {/* Visual Comparison Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Qualifying Focus Hours per Developer */}
        <div className="rounded-xl border border-gray-200 bg-white p-5">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h3 className="text-sm font-bold text-gray-900">Qualifying Focus Hours / Developer</h3>
              <p className="text-xs text-gray-500">Average deep focus hours per engineer over period</p>
            </div>
            <Sparkles className="w-4 h-4 text-indigo-600" />
          </div>

          <div className="h-[220px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={teams} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
                <XAxis dataKey="team_name" tick={{ fontSize: 11, fill: '#64748B' }} tickLine={false} axisLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#64748B' }} tickLine={false} axisLine={false} unit="h" />
                <Tooltip />
                <Bar dataKey="qualifying_hours_per_dev" radius={[4, 4, 0, 0]}>
                  {teams.map((t) => (
                    <Cell key={t.team_id} fill={teamColors[t.team_id] || '#4F46E5'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Potential Interruptions per Developer */}
        <div className="rounded-xl border border-gray-200 bg-white p-5">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h3 className="text-sm font-bold text-gray-900">Interruptions / Developer</h3>
              <p className="text-xs text-gray-500">Average external interruption events per engineer</p>
            </div>
            <Bell className="w-4 h-4 text-amber-600" />
          </div>

          <div className="h-[220px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={teams} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
                <XAxis dataKey="team_name" tick={{ fontSize: 11, fill: '#64748B' }} tickLine={false} axisLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#64748B' }} tickLine={false} axisLine={false} />
                <Tooltip />
                <Bar dataKey="interruptions_per_dev" fill="#F59E0B" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Comprehensive Comparison Table */}
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        <h3 className="text-sm font-bold text-gray-900 mb-1">Detailed Team Telemetry Matrix</h3>
        <p className="text-xs text-gray-500 mb-4">
          Holistic view of observed activity, qualifying focus, context switching, and estimated workflow friction tax.
        </p>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-gray-100 text-gray-500 bg-gray-50/50">
                <th className="py-2.5 px-3 font-semibold">Team Name</th>
                <th className="py-2.5 px-3 font-semibold text-right">Headcount</th>
                <th className="py-2.5 px-3 font-semibold text-right">Total IDE Hours</th>
                <th className="py-2.5 px-3 font-semibold text-right">Qual. Focus Hours</th>
                <th className="py-2.5 px-3 font-semibold text-right">Focus / Dev</th>
                <th className="py-2.5 px-3 font-semibold text-right">Interrupts / Dev</th>
                <th className="py-2.5 px-3 font-semibold text-right">Avg Block</th>
                <th className="py-2.5 px-3 font-semibold text-right">Context Switches</th>
                <th className="py-2.5 px-3 font-semibold text-right">Friction Tax</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {teams.map((tm) => (
                <tr key={tm.team_id} className="hover:bg-gray-50/60">
                  <td className="py-3 px-3 font-semibold text-gray-900 flex items-center gap-2">
                    <span
                      className="w-2.5 h-2.5 rounded-full"
                      style={{ backgroundColor: teamColors[tm.team_id] || '#4F46E5' }}
                    />
                    <span>{tm.team_name}</span>
                  </td>
                  <td className="py-3 px-3 text-right font-mono text-gray-600">{tm.headcount}</td>
                  <td className="py-3 px-3 text-right text-gray-700">{tm.observed_ide_hours} hrs</td>
                  <td className="py-3 px-3 text-right font-medium text-gray-900">{tm.qualifying_focus_hours} hrs</td>
                  <td className="py-3 px-3 text-right font-semibold text-indigo-600">
                    {tm.qualifying_hours_per_dev} hrs
                  </td>
                  <td className="py-3 px-3 text-right text-gray-700">{tm.interruptions_per_dev}</td>
                  <td className="py-3 px-3 text-right text-gray-700">{tm.avg_focus_block_minutes}m</td>
                  <td className="py-3 px-3 text-right font-mono text-gray-600">{tm.context_switch_count}</td>
                  <td className="py-3 px-3 text-right">
                    <span
                      className={`inline-block px-2 py-0.5 rounded-md font-mono font-medium ${
                        tm.context_switching_tax_pct > 20
                          ? 'bg-rose-50 text-rose-700 border border-rose-200'
                          : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                      }`}
                    >
                      {tm.context_switching_tax_pct}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
