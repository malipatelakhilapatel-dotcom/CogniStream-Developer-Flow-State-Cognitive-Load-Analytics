import React from 'react';
import { InterruptionCategory, InterruptionTimelinePoint, Insight } from '../types/api';
import { InsightCard } from '../components/InsightCard';
import {
  BellOff,
  AlertTriangle,
  Bot,
  MessageSquare,
  ArrowRightLeft,
  GitPullRequest,
  CheckCircle,
  Clock,
  ShieldCheck
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from 'recharts';

interface InterruptionsPageProps {
  breakdown: InterruptionCategory[];
  timeline: InterruptionTimelinePoint[];
  insights: Insight[];
  isLoading: boolean;
}

export const InterruptionsPage: React.FC<InterruptionsPageProps> = ({
  breakdown,
  timeline,
  insights,
  isLoading
}) => {
  if (isLoading) {
    return (
      <div className="p-12 flex justify-center items-center">
        <div className="w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const totalInterruptions = breakdown.reduce((acc, curr) => acc + curr.count, 0);
  const totalEstLossHours = breakdown.reduce((acc, curr) => acc + curr.estimated_loss_hours, 0);

  const cicdItem = breakdown.find((b) => b.category === 'ci_cd_notification');
  const cicdPct = cicdItem ? cicdItem.percentage : 0;
  const cicdCount = cicdItem ? cicdItem.count : 0;

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'ci_cd_notification':
        return <Bot className="w-4 h-4 text-amber-600" />;
      case 'direct_message':
        return <MessageSquare className="w-4 h-4 text-indigo-600" />;
      case 'mention':
        return <BellOff className="w-4 h-4 text-rose-600" />;
      case 'project_switch':
        return <ArrowRightLeft className="w-4 h-4 text-purple-600" />;
      case 'code_review':
        return <GitPullRequest className="w-4 h-4 text-blue-600" />;
      default:
        return <Clock className="w-4 h-4 text-gray-500" />;
    }
  };

  return (
    <div className="space-y-8">
      {/* Title */}
      <div>
        <h1 className="text-xl font-bold tracking-tight text-gray-950">Interruption Analysis</h1>
        <p className="text-sm text-gray-500 mt-1">
          Catalog and quantify potential interruptions from CI/CD bots, Slack communications, and context transitions.
        </p>
      </div>

      {/* Top Banner: Key Findings on CI/CD Friction */}
      <div className="rounded-xl border border-amber-200 bg-amber-50/50 p-5">
        <div className="flex items-start gap-3">
          <div className="p-2 rounded-lg bg-amber-100 text-amber-800 mt-0.5">
            <AlertTriangle className="w-5 h-5 text-amber-700" />
          </div>
          <div className="flex-1 space-y-1">
            <h3 className="text-sm font-bold text-amber-950">
              CI/CD Automation Friction Alert
            </h3>
            <p className="text-xs text-amber-900 leading-relaxed">
              Automated build alerts and CI/CD bot notifications account for <span className="font-bold">{cicdCount.toLocaleString()} events ({cicdPct}% of all potential interruptions)</span>.
              Frequent build notifications during working hours trigger recurring context switching. Adjusting notification channel policies could preserve substantial uninterrupted focus.
            </p>
          </div>
        </div>
      </div>

      {/* Primary KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="rounded-xl border border-gray-200 bg-white p-5">
          <span className="text-xs font-semibold uppercase text-gray-500">Total Potential Interruptions</span>
          <div className="text-2xl font-bold text-gray-900 mt-2">{totalInterruptions.toLocaleString()}</div>
          <p className="text-xs text-gray-500 mt-1">Across 30 days of observed telemetry</p>
        </div>

        <div className="rounded-xl border border-gray-200 bg-white p-5">
          <span className="text-xs font-semibold uppercase text-gray-500">Estimated Associated Focus Loss</span>
          <div className="text-2xl font-bold text-gray-900 mt-2">{Math.round(totalEstLossHours)} hrs</div>
          <p className="text-xs text-gray-500 mt-1">Non-overlapping interval recovery estimate</p>
        </div>

        <div className="rounded-xl border border-gray-200 bg-white p-5">
          <span className="text-xs font-semibold uppercase text-gray-500">Recovery Model Guarantee</span>
          <div className="text-2xl font-bold text-emerald-600 mt-2 flex items-center gap-1.5">
            <ShieldCheck className="w-6 h-6" /> Zero Overlap
          </div>
          <p className="text-xs text-gray-500 mt-1">Interval union prevents double-counting recovery windows</p>
        </div>
      </div>

      {/* Interruption Timeline Chart */}
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-gray-900">Interruption Timeline by Category</h3>
            <p className="text-xs text-gray-500">Daily event volume segmented by interruption trigger</p>
          </div>
        </div>

        <div className="h-[280px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={timeline} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
              <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#64748B' }} tickLine={false} axisLine={false} />
              <YAxis tick={{ fontSize: 11, fill: '#64748B' }} tickLine={false} axisLine={false} />
              <Tooltip />
              <Legend wrapperStyle={{ fontSize: 11 }} />
              <Bar dataKey="ci_cd_notification" name="CI/CD Alerts" fill="#F59E0B" stackId="a" />
              <Bar dataKey="direct_message" name="Slack DMs" fill="#4F46E5" stackId="a" />
              <Bar dataKey="mention" name="Mentions" fill="#EF4444" stackId="a" />
              <Bar dataKey="project_switch" name="Project Switches" fill="#8B5CF6" stackId="a" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Category Breakdown Table */}
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        <h3 className="text-sm font-bold text-gray-900 mb-1">Interruption Category Breakdown</h3>
        <p className="text-xs text-gray-500 mb-4">
          Estimated recovery time assumptions: CI/CD (12m), Direct Message (15m), Mentions (10m), Switches (18m).
        </p>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-gray-100 text-gray-500 bg-gray-50/50">
                <th className="py-2.5 px-3 font-semibold">Category</th>
                <th className="py-2.5 px-3 font-semibold text-right">Event Count</th>
                <th className="py-2.5 px-3 font-semibold text-right">Proportion</th>
                <th className="py-2.5 px-3 font-semibold text-right">Est. Focus Loss</th>
                <th className="py-2.5 px-3 font-semibold text-right">Assumed Recovery</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {breakdown.map((item) => (
                <tr key={item.category} className="hover:bg-gray-50/60">
                  <td className="py-3 px-3 font-medium text-gray-900 flex items-center gap-2">
                    {getCategoryIcon(item.category)}
                    <span>{item.label}</span>
                  </td>
                  <td className="py-3 px-3 text-right font-mono font-medium text-gray-800">
                    {item.count.toLocaleString()}
                  </td>
                  <td className="py-3 px-3 text-right text-gray-600">
                    {item.percentage}%
                  </td>
                  <td className="py-3 px-3 text-right font-semibold text-indigo-600">
                    {Math.round(item.estimated_loss_hours)} hrs
                  </td>
                  <td className="py-3 px-3 text-right font-mono text-gray-500">
                    {item.category === 'ci_cd_notification'
                      ? '12m'
                      : item.category === 'direct_message'
                      ? '15m'
                      : item.category === 'project_switch'
                      ? '18m'
                      : '10m'}
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
