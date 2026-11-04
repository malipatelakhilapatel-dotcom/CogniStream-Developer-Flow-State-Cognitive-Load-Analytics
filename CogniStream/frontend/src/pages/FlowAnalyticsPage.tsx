import React, { useState } from 'react';
import { FlowBlocksResponse, FlowTrend } from '../types/api';
import {
  Clock,
  Sparkles,
  Info,
  Calendar,
  CheckCircle2,
  Filter
} from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar,
  Cell
} from 'recharts';

interface FlowAnalyticsPageProps {
  blocksData: FlowBlocksResponse | null;
  trends: FlowTrend[];
  isLoading: boolean;
}

export const FlowAnalyticsPage: React.FC<FlowAnalyticsPageProps> = ({
  blocksData,
  trends,
  isLoading
}) => {
  const [qualifyingOnly, setQualifyingOnly] = useState<boolean>(false);

  if (isLoading || !blocksData) {
    return (
      <div className="p-12 flex justify-center items-center">
        <div className="w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const { total_blocks, duration_distribution, blocks } = blocksData;

  const filteredBlocks = qualifyingOnly
    ? blocks.filter((b) => b.is_qualifying === 1)
    : blocks;

  const qualifyingCount = blocks.filter((b) => b.is_qualifying === 1).length;
  const qualPct = total_blocks > 0 ? Math.round((qualifyingCount / total_blocks) * 100) : 0;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold tracking-tight text-gray-950">Flow Analytics & Focus Blocks</h1>
        <p className="text-sm text-gray-500 mt-1">
          Detailed inspection of reconstructed developer sessions and qualifying uninterrupted focus periods.
        </p>
      </div>

      {/* Methodology Banner */}
      <div className="rounded-xl border border-indigo-100 bg-indigo-50/40 p-4 text-xs text-indigo-900 flex items-start gap-3">
        <Info className="w-5 h-5 text-indigo-600 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <p className="font-semibold text-indigo-950">Focus Block Reconstruction Methodology</p>
          <p className="text-indigo-800/90 leading-relaxed">
            Continuous IDE telemetry heartbeats are clustered into active blocks. Any gap exceeding the configurable
            <span className="font-semibold"> 15-minute inactivity threshold</span> splits sessions. Blocks with duration
            <span className="font-semibold"> ≥ 90 minutes</span> are classified as <em>Qualifying Focus</em>. This serves as an
            observable behavioral proxy rather than a direct measurement of subjective mental states.
          </p>
        </div>
      </div>

      {/* Primary Charts: Trends & Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Daily Focus Trajectory (7 cols) */}
        <div className="lg:col-span-7 rounded-xl border border-gray-200 bg-white p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-gray-900">Daily Focus Volume</h3>
              <p className="text-xs text-gray-500">Continuous IDE activity hours vs qualifying focus hours</p>
            </div>
            <div className="flex items-center gap-3 text-xs">
              <span className="flex items-center gap-1.5 text-gray-600">
                <span className="w-2.5 h-2.5 rounded bg-indigo-200" />
                IDE Active
              </span>
              <span className="flex items-center gap-1.5 text-indigo-700 font-medium">
                <span className="w-2.5 h-2.5 rounded bg-indigo-600" />
                Qualifying (≥90m)
              </span>
            </div>
          </div>

          <div className="h-[260px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trends} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
                <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#64748B' }} tickLine={false} axisLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#64748B' }} tickLine={false} axisLine={false} unit="h" />
                <Tooltip />
                <Area type="monotone" dataKey="observed_ide_hours" stroke="#818CF8" fill="#EEF2FF" />
                <Area type="monotone" dataKey="qualifying_focus_hours" stroke="#4F46E5" fill="#C7D2FE" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Duration Distribution (5 cols) */}
        <div className="lg:col-span-5 rounded-xl border border-gray-200 bg-white p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-gray-900">Duration Distribution</h3>
              <p className="text-xs text-gray-500">{qualifyingCount} of {total_blocks} blocks ({qualPct}%) qualify</p>
            </div>
            <span className="text-xs bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded font-medium border border-indigo-200">
              Target: ≥90m
            </span>
          </div>

          <div className="h-[260px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={duration_distribution} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
                <XAxis dataKey="bucket" tick={{ fontSize: 11, fill: '#64748B' }} tickLine={false} axisLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#64748B' }} tickLine={false} axisLine={false} />
                <Tooltip />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {duration_distribution.map((entry, index) => (
                    <Cell
                      key={`flow-cell-${index}`}
                      fill={entry.bucket.includes('90') || entry.bucket.includes('120') ? '#4F46E5' : '#CBD5E1'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Focus Blocks Exploration Table */}
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
          <div>
            <h3 className="text-sm font-bold text-gray-900">Reconstructed Focus Blocks</h3>
            <p className="text-xs text-gray-500">Inspecting longest active blocks with mapped potential interruptions</p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setQualifyingOnly(!qualifyingOnly)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
                qualifyingOnly
                  ? 'bg-indigo-600 text-white border-indigo-600'
                  : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'
              }`}
            >
              <Filter className="w-3.5 h-3.5" />
              <span>{qualifyingOnly ? 'Showing Qualifying Only (≥90m)' : 'All Focus Blocks'}</span>
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-gray-100 text-gray-500 bg-gray-50/50">
                <th className="py-2.5 px-3 font-semibold">Block ID</th>
                <th className="py-2.5 px-3 font-semibold">Developer</th>
                <th className="py-2.5 px-3 font-semibold">Team</th>
                <th className="py-2.5 px-3 font-semibold">Project</th>
                <th className="py-2.5 px-3 font-semibold">Start Time</th>
                <th className="py-2.5 px-3 font-semibold text-right">Duration</th>
                <th className="py-2.5 px-3 font-semibold text-right">Interrupts</th>
                <th className="py-2.5 px-3 font-semibold text-center">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {filteredBlocks.slice(0, 20).map((b) => (
                <tr key={b.focus_block_id} className="hover:bg-gray-50/60 transition-colors">
                  <td className="py-2.5 px-3 font-mono text-gray-600 text-[11px]">{b.focus_block_id}</td>
                  <td className="py-2.5 px-3 font-medium text-gray-900">{b.actor_id}</td>
                  <td className="py-2.5 px-3 text-gray-600">{b.team_id.replace('team-', '')}</td>
                  <td className="py-2.5 px-3 text-gray-600 font-mono text-[11px]">
                    {b.project_id || <span className="text-gray-400 italic">None</span>}
                  </td>
                  <td className="py-2.5 px-3 text-gray-500 font-mono text-[11px]">
                    {b.start_timestamp.replace('T', ' ').slice(0, 16)}
                  </td>
                  <td className="py-2.5 px-3 text-right font-semibold text-gray-900">
                    {Math.round(b.duration_minutes)}m
                  </td>
                  <td className="py-2.5 px-3 text-right font-mono text-gray-600">
                    {b.interruption_count}
                  </td>
                  <td className="py-2.5 px-3 text-center">
                    {b.is_qualifying === 1 ? (
                      <span className="inline-flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-medium">
                        <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                        Qualifying (≥90m)
                      </span>
                    ) : (
                      <span className="inline-flex items-center text-[11px] px-2 py-0.5 rounded-full bg-gray-100 text-gray-600">
                        Fragmented
                      </span>
                    )}
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
