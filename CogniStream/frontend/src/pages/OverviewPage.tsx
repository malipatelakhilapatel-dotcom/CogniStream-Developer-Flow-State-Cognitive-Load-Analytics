import React from 'react';
import {
  Users,
  Clock,
  Sparkles,
  Zap,
  Bell,
  Percent,
  ArrowRight
} from 'lucide-react';
import { KpiCard } from '../components/KpiCard';
import { InsightCard } from '../components/InsightCard';
import {
  OverviewResponse,
  FlowTrend,
  InterruptionCategory,
  DurationBucket,
  TeamComparisonMetric,
  ActivityEvent
} from '../types/api';
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

interface OverviewPageProps {
  data: OverviewResponse | null;
  trends: FlowTrend[];
  interruptions: InterruptionCategory[];
  distribution: DurationBucket[];
  teams: TeamComparisonMetric[];
  recentEvents: ActivityEvent[];
  isLoading: boolean;
  onNavigate: (tab: any) => void;
}

export const OverviewPage: React.FC<OverviewPageProps> = ({
  data,
  trends,
  interruptions,
  distribution,
  teams,
  recentEvents,
  isLoading,
  onNavigate
}) => {
  if (isLoading || !data) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[400px]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin" />
          <p className="text-sm text-gray-500 font-medium">Aggregating telemetry events...</p>
        </div>
      </div>
    );
  }

  const { kpis, insights } = data;

  const barColors = ['#4F46E5', '#6366F1', '#818CF8', '#A5B4FC', '#C7D2FE', '#94A3B8'];

  return (
    <div className="space-y-8">
      {/* Title & Subtitle */}
      <div>
        <h1 className="text-xl font-bold tracking-tight text-gray-950">Developer Flow Overview</h1>
        <p className="text-sm text-gray-500 mt-1">
          Understand focus patterns, context switches, and workflow friction across engineering teams.
        </p>
      </div>

      {/* Row of 6 KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <KpiCard
          label="Active Developers"
          value={kpis.active_developers}
          subtitle={`Across ${kpis.period_days} observed days`}
          icon={Users}
        />
        <KpiCard
          label="Observed IDE Hours"
          value={kpis.observed_ide_hours}
          unit="hrs"
          subtitle="Total telemetry activity"
          icon={Clock}
        />
        <KpiCard
          label="Qualifying Focus"
          value={kpis.qualifying_focus_hours}
          unit="hrs"
          subtitle="Blocks ≥ 90 minutes"
          icon={Sparkles}
          highlight={true}
          badge={{ text: '≥90m Target', variant: 'positive' }}
        />
        <KpiCard
          label="Avg Focus Block"
          value={kpis.avg_focus_block_minutes}
          unit="min"
          subtitle={`${kpis.total_focus_blocks} total sessions`}
          icon={Zap}
        />
        <KpiCard
          label="Potential Interrupts"
          value={kpis.potential_interruptions.toLocaleString()}
          subtitle="Slack, CI/CD, switches"
          icon={Bell}
        />
        <KpiCard
          label="Context-Switching Tax"
          value={`${kpis.estimated_context_switching_tax_pct}%`}
          subtitle="Estimated time lost to friction"
          icon={Percent}
          highlight={kpis.estimated_context_switching_tax_pct > 20}
          badge={{
            text: kpis.estimated_context_switching_tax_pct > 20 ? 'Elevated Friction' : 'Moderate',
            variant: kpis.estimated_context_switching_tax_pct > 20 ? 'negative' : 'neutral'
          }}
        />
      </div>

      {/* Actionable Insights Panel */}
      {insights && insights.length > 0 && (
        <div className="rounded-xl border border-gray-200 bg-white p-5">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-indigo-600" />
              <h3 className="text-sm font-bold text-gray-900">Deterministic Workflow Observations</h3>
            </div>
            <span className="text-xs text-gray-500">Derived strictly from active query results</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {insights.map((ins) => (
              <InsightCard key={ins.id} insight={ins} />
            ))}
          </div>
        </div>
      )}

      {/* Primary Analytics Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Focus Time Trend Chart (8 cols) */}
        <div className="lg:col-span-8 rounded-xl border border-gray-200 bg-white p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-gray-900">Focus Time Trend</h3>
              <p className="text-xs text-gray-500">
                Observed IDE active hours vs qualifying focus hours (≥90m uninterrupted)
              </p>
            </div>
            <div className="flex items-center gap-4 text-xs">
              <div className="flex items-center gap-1.5">
                <span className="w-3 h-3 rounded bg-indigo-200 border border-indigo-400" />
                <span className="text-gray-600">Total IDE Active Hours</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="w-3 h-3 rounded bg-indigo-600" />
                <span className="text-gray-900 font-medium">Qualifying Focus Hours</span>
              </div>
            </div>
          </div>

          <div className="h-[280px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trends} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="ideHours" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#818CF8" stopOpacity={0.2} />
                    <stop offset="95%" stopColor="#818CF8" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="qualHours" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#4F46E5" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#4F46E5" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
                <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#64748B' }} tickLine={false} axisLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#64748B' }} tickLine={false} axisLine={false} unit="h" />
                <Tooltip
                  content={({ active, payload, label }) => {
                    if (active && payload && payload.length) {
                      return (
                        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-sm text-xs">
                          <p className="font-semibold text-gray-900 mb-1">{label}</p>
                          <p className="text-indigo-600 font-medium">
                            Qualifying Focus: {payload[0].value} hrs
                          </p>
                          <p className="text-gray-500">
                            Observed IDE: {payload[1].value} hrs
                          </p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="qualifying_focus_hours"
                  stroke="#4F46E5"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#qualHours)"
                />
                <Area
                  type="monotone"
                  dataKey="observed_ide_hours"
                  stroke="#818CF8"
                  strokeWidth={1.5}
                  strokeDasharray="4 4"
                  fillOpacity={1}
                  fill="url(#ideHours)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Interruption Sources Breakdown (4 cols) */}
        <div className="lg:col-span-4 rounded-xl border border-gray-200 bg-white p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-bold text-gray-900">Interruption Sources</h3>
              <button
                onClick={() => onNavigate('interruptions')}
                className="text-xs text-indigo-600 hover:text-indigo-800 font-medium flex items-center gap-1"
              >
                Deep-dive <ArrowRight className="w-3 h-3" />
              </button>
            </div>
            <p className="text-xs text-gray-500 mb-4">Relative frequency of potential interruption events</p>

            <div className="space-y-3">
              {interruptions.slice(0, 5).map((item, idx) => (
                <div key={item.category} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="font-medium text-gray-700 truncate max-w-[180px]">{item.label}</span>
                    <span className="text-gray-500">
                      {item.count.toLocaleString()} ({item.percentage}%)
                    </span>
                  </div>
                  <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                    <div
                      className="h-2 rounded-full transition-all"
                      style={{
                        width: `${item.percentage}%`,
                        backgroundColor: barColors[idx % barColors.length]
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-gray-100 text-[11px] text-gray-500 flex justify-between">
            <span>Automated CI/CD is highest volume trigger</span>
            <span className="font-medium text-gray-700">~12m est recovery</span>
          </div>
        </div>
      </div>

      {/* Secondary Row: Focus Distribution & Team Snapshot */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Daily Focus Block Distribution (5 cols) */}
        <div className="lg:col-span-5 rounded-xl border border-gray-200 bg-white p-5">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h3 className="text-sm font-bold text-gray-900">Session Duration Distribution</h3>
              <p className="text-xs text-gray-500">Count of continuous focus blocks grouped by duration</p>
            </div>
            <span className="text-[11px] px-2 py-0.5 rounded bg-gray-100 text-gray-600 font-mono">
              15m split rule
            </span>
          </div>

          <div className="h-[220px] w-full mt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={distribution} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
                <XAxis dataKey="bucket" tick={{ fontSize: 11, fill: '#64748B' }} tickLine={false} axisLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#64748B' }} tickLine={false} axisLine={false} />
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      return (
                        <div className="bg-white p-2.5 border border-gray-200 rounded-lg shadow-sm text-xs">
                          <p className="font-semibold text-gray-900">{payload[0].payload.bucket}</p>
                          <p className="text-indigo-600">{payload[0].value} blocks</p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {distribution.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={entry.bucket.includes('90') || entry.bucket.includes('120') ? '#4F46E5' : '#CBD5E1'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="text-[11px] text-gray-500 mt-2 text-center">
            Highlighted bars represent qualifying deep focus blocks (≥ 90 minutes)
          </p>
        </div>

        {/* Team Comparison Snapshot (7 cols) */}
        <div className="lg:col-span-7 rounded-xl border border-gray-200 bg-white p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-gray-900">Team Flow Comparison</h3>
              <p className="text-xs text-gray-500">Normalized metrics per developer avoid team size bias</p>
            </div>
            <button
              onClick={() => onNavigate('teams')}
              className="text-xs text-indigo-600 hover:text-indigo-800 font-medium flex items-center gap-1"
            >
              Full Comparison <ArrowRight className="w-3 h-3" />
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-gray-100 text-gray-500">
                  <th className="pb-2 font-semibold">Team</th>
                  <th className="pb-2 font-semibold text-right">Headcount</th>
                  <th className="pb-2 font-semibold text-right">Qual. Focus / Dev</th>
                  <th className="pb-2 font-semibold text-right">Avg Block</th>
                  <th className="pb-2 font-semibold text-right">Friction Tax</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {teams.map((tm) => (
                  <tr key={tm.team_id} className="hover:bg-gray-50/50">
                    <td className="py-2.5 font-medium text-gray-900">{tm.team_name}</td>
                    <td className="py-2.5 text-right text-gray-600 font-mono">{tm.headcount}</td>
                    <td className="py-2.5 text-right font-medium text-indigo-600">
                      {tm.qualifying_hours_per_dev} hrs
                    </td>
                    <td className="py-2.5 text-right text-gray-700">{tm.avg_focus_block_minutes}m</td>
                    <td className="py-2.5 text-right">
                      <span
                        className={`inline-block px-1.5 py-0.5 rounded font-mono font-medium ${
                          tm.context_switching_tax_pct > 20
                            ? 'bg-rose-50 text-rose-700'
                            : 'bg-emerald-50 text-emerald-700'
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
    </div>
  );
};
