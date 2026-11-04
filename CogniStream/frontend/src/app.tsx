import React, { useState, useEffect } from 'react';
import { Sidebar, NavigationTab } from './components/Sidebar';
import { Header } from './components/Header';
import { OverviewPage } from './pages/OverviewPage';
import { FlowAnalyticsPage } from './pages/FlowAnalyticsPage';
import { InterruptionsPage } from './pages/InterruptionsPage';
import { TeamComparisonPage } from './pages/TeamComparisonPage';
import { ActivityExplorerPage } from './pages/ActivityExplorerPage';
import { MethodologyPage } from './pages/MethodologyPage';
import { api } from './services/api';
import {
  HealthStatus,
  OverviewResponse,
  FlowTrend,
  FlowBlocksResponse,
  InterruptionCategory,
  InterruptionTimelinePoint,
  TeamComparisonMetric,
  ActivityEvent,
  FiltersResponse
} from './types/api';
import { AlertCircle, RefreshCw } from 'lucide-react';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<NavigationTab>('overview');
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [filters, setFilters] = useState<FiltersResponse | null>(null);
  const [selectedTeam, setSelectedTeam] = useState<string>('all');
  const [dateRange, setDateRange] = useState<string>('30d');

  // Page data states
  const [overviewData, setOverviewData] = useState<OverviewResponse | null>(null);
  const [trends, setTrends] = useState<FlowTrend[]>([]);
  const [blocksData, setBlocksData] = useState<FlowBlocksResponse | null>(null);
  const [interruptionBreakdown, setInterruptionBreakdown] = useState<InterruptionCategory[]>([]);
  const [interruptionTimeline, setInterruptionTimeline] = useState<InterruptionTimelinePoint[]>([]);
  const [teamMetrics, setTeamMetrics] = useState<TeamComparisonMetric[]>([]);
  const [recentEvents, setRecentEvents] = useState<ActivityEvent[]>([]);

  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Compute dates based on dateRange
  const getDateBounds = (range: string): { start?: string; end?: string } => {
    const end = '2026-10-25';
    if (range === '7d') return { start: '2026-10-18', end };
    if (range === '14d') return { start: '2026-10-11', end };
    return { start: '2026-09-25', end }; // 30d
  };

  const loadAllData = async (isManualRefresh = false) => {
    if (isManualRefresh) setIsRefreshing(true);
    else setIsLoading(true);
    setError(null);

    const { start, end } = getDateBounds(dateRange);
    const teamParam = selectedTeam !== 'all' ? selectedTeam : undefined;

    try {
      // 1. Health & Filters
      const [healthRes, filtersRes] = await Promise.all([
        api.getHealth().catch(() => null),
        api.getFilters().catch(() => null)
      ]);
      if (healthRes) setHealth(healthRes);
      if (filtersRes) setFilters(filtersRes);

      // 2. Overview & Trends
      const [overviewRes, trendsRes, blocksRes, intrBreakdownRes, intrTimelineRes, teamsRes, activityRes] =
        await Promise.all([
          api.getOverview(start, end, teamParam),
          api.getFlowTrends(start, end, teamParam),
          api.getFlowBlocks(start, end, teamParam),
          api.getInterruptionBreakdown(start, end, teamParam),
          api.getInterruptionTimeline(start, end, teamParam),
          api.getTeamComparison(start, end),
          api.getRecentActivity(start, end, teamParam, undefined, undefined, undefined, 1, 10)
        ]);

      setOverviewData(overviewRes);
      setTrends(trendsRes.trends || []);
      setBlocksData(blocksRes);
      setInterruptionBreakdown(intrBreakdownRes.breakdown || []);
      setInterruptionTimeline(intrTimelineRes.timeline || []);
      setTeamMetrics(teamsRes.teams || []);
      setRecentEvents(activityRes.events || []);
    } catch (err: any) {
      console.error('API Error:', err);
      setError(err?.message || 'Failed to connect to CogniStream backend service.');
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    loadAllData();
  }, [selectedTeam, dateRange]);

  const teamsList = filters?.teams || [
    { id: 'all', name: 'All Teams' },
    { id: 'team-platform', name: 'Platform Engineering' },
    { id: 'team-product', name: 'Product Engineering' },
    { id: 'team-data', name: 'Data Engineering' }
  ];

  return (
    <div className="flex min-h-screen bg-[#F8FAFC]">
      {/* Left Sidebar */}
      <Sidebar currentTab={currentTab} onSelectTab={setCurrentTab} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          health={health}
          teams={teamsList}
          selectedTeam={selectedTeam}
          onSelectTeam={setSelectedTeam}
          dateRange={dateRange}
          onSelectDateRange={setDateRange}
          onRefresh={() => loadAllData(true)}
          isRefreshing={isRefreshing}
        />

        <main className="p-8 max-w-7xl w-full mx-auto flex-1">
          {error && (
            <div className="mb-6 rounded-xl border border-rose-200 bg-rose-50 p-4 text-rose-800 text-xs flex items-center justify-between">
              <div className="flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-rose-600" />
                <span>{error}</span>
              </div>
              <button
                onClick={() => loadAllData(true)}
                className="font-medium underline hover:text-rose-950 flex items-center gap-1"
              >
                <RefreshCw className="w-3 h-3" /> Retry
              </button>
            </div>
          )}

          {currentTab === 'overview' && (
            <OverviewPage
              data={overviewData}
              trends={trends}
              interruptions={interruptionBreakdown}
              distribution={blocksData?.duration_distribution || []}
              teams={teamMetrics}
              recentEvents={recentEvents}
              isLoading={isLoading}
              onNavigate={setCurrentTab}
            />
          )}

          {currentTab === 'flow' && (
            <FlowAnalyticsPage
              blocksData={blocksData}
              trends={trends}
              isLoading={isLoading}
            />
          )}

          {currentTab === 'interruptions' && (
            <InterruptionsPage
              breakdown={interruptionBreakdown}
              timeline={interruptionTimeline}
              insights={overviewData?.insights || []}
              isLoading={isLoading}
            />
          )}

          {currentTab === 'teams' && (
            <TeamComparisonPage
              teams={teamMetrics}
              isLoading={isLoading}
            />
          )}

          {currentTab === 'activity' && (
            <ActivityExplorerPage
              teams={teamsList}
              sources={filters?.sources || []}
              categories={filters?.categories || []}
            />
          )}

          {currentTab === 'methodology' && <MethodologyPage />}
        </main>
      </div>
    </div>
  );
};

export default App;
