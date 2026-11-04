import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { ActivityResponse, FilterOption } from '../types/api';
import {
  Search,
  Filter,
  ChevronLeft,
  ChevronRight,
  Activity,
  Calendar,
  Layers,
  Database,
  Tag
} from 'lucide-react';

interface ActivityExplorerPageProps {
  teams: FilterOption[];
  sources: FilterOption[];
  categories: FilterOption[];
}

export const ActivityExplorerPage: React.FC<ActivityExplorerPageProps> = ({
  teams,
  sources,
  categories
}) => {
  const [data, setData] = useState<ActivityResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [search, setSearch] = useState<string>('');
  const [selectedTeam, setSelectedTeam] = useState<string>('all');
  const [selectedSource, setSelectedSource] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [page, setPage] = useState<number>(1);
  const pageSize = 20;

  const loadEvents = async () => {
    setIsLoading(true);
    try {
      const res = await api.getRecentActivity(
        undefined,
        undefined,
        selectedTeam !== 'all' ? selectedTeam : undefined,
        selectedSource !== 'all' ? selectedSource : undefined,
        selectedCategory !== 'all' ? selectedCategory : undefined,
        search.trim() || undefined,
        page,
        pageSize
      );
      setData(res);
    } catch (err) {
      console.error('Failed to load activity events:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, [page, selectedTeam, selectedSource, selectedCategory]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    loadEvents();
  };

  const getSourceBadge = (source: string) => {
    switch (source) {
      case 'ide':
        return <span className="bg-blue-50 text-blue-700 border border-blue-200 px-2 py-0.5 rounded font-mono text-[10px] uppercase">IDE</span>;
      case 'slack':
        return <span className="bg-amber-50 text-amber-700 border border-amber-200 px-2 py-0.5 rounded font-mono text-[10px] uppercase">Slack</span>;
      case 'github':
        return <span className="bg-gray-100 text-gray-800 border border-gray-300 px-2 py-0.5 rounded font-mono text-[10px] uppercase">GitHub</span>;
      case 'jira':
        return <span className="bg-indigo-50 text-indigo-700 border border-indigo-200 px-2 py-0.5 rounded font-mono text-[10px] uppercase">Jira</span>;
      default:
        return <span className="bg-gray-50 text-gray-600 px-2 py-0.5 rounded font-mono text-[10px] uppercase">{source}</span>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h1 className="text-xl font-bold tracking-tight text-gray-950">Activity Explorer</h1>
        <p className="text-sm text-gray-500 mt-1">
          Search, filter, and inspect normalized developer activity events across engineering telemetry sources.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="rounded-xl border border-gray-200 bg-white p-4 space-y-3">
        <form onSubmit={handleSearchSubmit} className="flex flex-col sm:flex-row gap-3">
          <div className="flex-1 relative">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search by event ID, actor ID, or project..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-2 text-xs border border-gray-200 rounded-lg focus:outline-none focus:border-indigo-500 bg-gray-50/50"
            />
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {/* Team Filter */}
            <select
              value={selectedTeam}
              onChange={(e) => { setSelectedTeam(e.target.value); setPage(1); }}
              className="text-xs bg-gray-50 border border-gray-200 rounded-lg px-2.5 py-2 font-medium text-gray-700 focus:outline-none"
            >
              <option value="all">All Teams</option>
              {teams.filter(t => t.id !== 'all').map((t) => (
                <option key={t.id} value={t.id}>{t.name}</option>
              ))}
            </select>

            {/* Source Filter */}
            <select
              value={selectedSource}
              onChange={(e) => { setSelectedSource(e.target.value); setPage(1); }}
              className="text-xs bg-gray-50 border border-gray-200 rounded-lg px-2.5 py-2 font-medium text-gray-700 focus:outline-none"
            >
              <option value="all">All Sources</option>
              {sources.filter(s => s.id !== 'all').map((s) => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>

            {/* Category Filter */}
            <select
              value={selectedCategory}
              onChange={(e) => { setSelectedCategory(e.target.value); setPage(1); }}
              className="text-xs bg-gray-50 border border-gray-200 rounded-lg px-2.5 py-2 font-medium text-gray-700 focus:outline-none"
            >
              <option value="all">All Categories</option>
              {categories.filter(c => c.id !== 'all').map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>

            <button
              type="submit"
              className="px-3.5 py-2 rounded-lg bg-indigo-600 text-white text-xs font-semibold hover:bg-indigo-700 transition-colors"
            >
              Apply Filter
            </button>
          </div>
        </form>
      </div>

      {/* Table Container */}
      <div className="rounded-xl border border-gray-200 bg-white overflow-hidden">
        {isLoading ? (
          <div className="p-12 flex justify-center items-center">
            <div className="w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : !data || data.events.length === 0 ? (
          <div className="p-12 text-center text-gray-500">
            <Activity className="w-8 h-8 text-gray-300 mx-auto mb-2" />
            <p className="text-sm font-medium">No activity events found</p>
            <p className="text-xs text-gray-400 mt-1">Try broadening your search query or filter selections.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-gray-100 text-gray-500 bg-gray-50/70">
                  <th className="py-2.5 px-3.5 font-semibold">Event ID</th>
                  <th className="py-2.5 px-3.5 font-semibold">Timestamp (UTC)</th>
                  <th className="py-2.5 px-3.5 font-semibold">Source</th>
                  <th className="py-2.5 px-3.5 font-semibold">Event Type</th>
                  <th className="py-2.5 px-3.5 font-semibold">Actor ID</th>
                  <th className="py-2.5 px-3.5 font-semibold">Team</th>
                  <th className="py-2.5 px-3.5 font-semibold">Project</th>
                  <th className="py-2.5 px-3.5 font-semibold">Interruption Type</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50 font-mono">
                {data.events.map((ev) => (
                  <tr key={ev.event_id} className="hover:bg-gray-50/60 font-sans">
                    <td className="py-2.5 px-3.5 font-mono text-[11px] text-gray-600">{ev.event_id}</td>
                    <td className="py-2.5 px-3.5 font-mono text-[11px] text-gray-500">
                      {ev.timestamp.replace('T', ' ').slice(0, 19)}
                    </td>
                    <td className="py-2.5 px-3.5">{getSourceBadge(ev.source)}</td>
                    <td className="py-2.5 px-3.5 font-medium text-gray-800">{ev.event_type}</td>
                    <td className="py-2.5 px-3.5 font-mono text-[11px] text-gray-700">{ev.actor_id}</td>
                    <td className="py-2.5 px-3.5 text-gray-600">{ev.team_id.replace('team-', '')}</td>
                    <td className="py-2.5 px-3.5 font-mono text-[11px] text-gray-500">
                      {ev.project_id || '-'}
                    </td>
                    <td className="py-2.5 px-3.5">
                      {ev.is_potential_interruption === 1 ? (
                        <span className="inline-block px-2 py-0.5 rounded text-[10px] font-medium bg-rose-50 text-rose-700 border border-rose-200">
                          {ev.interruption_category}
                        </span>
                      ) : (
                        <span className="text-gray-400 text-[11px] font-mono">none</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination Bar */}
        {data && data.total_pages > 1 && (
          <div className="p-3.5 border-t border-gray-100 bg-gray-50/50 flex items-center justify-between text-xs">
            <span className="text-gray-500">
              Showing page <span className="font-semibold text-gray-900">{data.page}</span> of{' '}
              <span className="font-semibold text-gray-900">{data.total_pages}</span> ({data.total_events.toLocaleString()} total events)
            </span>

            <div className="flex items-center gap-1.5">
              <button
                disabled={data.page <= 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                className="p-1.5 rounded-lg border border-gray-200 bg-white hover:bg-gray-50 disabled:opacity-40 transition-colors"
              >
                <ChevronLeft className="w-3.5 h-3.5" />
              </button>
              <span className="px-2 font-mono font-medium text-gray-700">{data.page}</span>
              <button
                disabled={data.page >= data.total_pages}
                onClick={() => setPage((p) => Math.min(data.total_pages, p + 1))}
                className="p-1.5 rounded-lg border border-gray-200 bg-white hover:bg-gray-50 disabled:opacity-40 transition-colors"
              >
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
