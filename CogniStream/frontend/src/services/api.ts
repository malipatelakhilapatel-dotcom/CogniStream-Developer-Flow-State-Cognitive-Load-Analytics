import {
  HealthStatus,
  OverviewResponse,
  FlowTrend,
  FlowBlocksResponse,
  InterruptionCategory,
  InterruptionTimelinePoint,
  TeamComparisonMetric,
  ActivityResponse,
  FiltersResponse
} from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

function buildQuery(params: Record<string, string | number | undefined | null>): string {
  const parts: string[] = [];
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== '') {
      parts.push(`${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`);
    }
  }
  return parts.length > 0 ? `?${parts.join('&')}` : '';
}

export const api = {
  async getHealth(): Promise<HealthStatus> {
    const res = await fetch(`${API_BASE_URL}/health`);
    if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
    return res.json();
  },

  async getFilters(): Promise<FiltersResponse> {
    const res = await fetch(`${API_BASE_URL}/filters`);
    if (!res.ok) throw new Error(`Filters fetch failed: ${res.statusText}`);
    return res.json();
  },

  async getOverview(startDate?: string, endDate?: string, teamId?: string): Promise<OverviewResponse> {
    const q = buildQuery({ start_date: startDate, end_date: endDate, team_id: teamId });
    const res = await fetch(`${API_BASE_URL}/overview${q}`);
    if (!res.ok) throw new Error(`Overview fetch failed: ${res.statusText}`);
    return res.json();
  },

  async getFlowBlocks(
    startDate?: string,
    endDate?: string,
    teamId?: string,
    projectId?: string,
    isQualifying?: number
  ): Promise<FlowBlocksResponse> {
    const q = buildQuery({
      start_date: startDate,
      end_date: endDate,
      team_id: teamId,
      project_id: projectId,
      is_qualifying: isQualifying
    });
    const res = await fetch(`${API_BASE_URL}/flow/blocks${q}`);
    if (!res.ok) throw new Error(`Flow blocks fetch failed: ${res.statusText}`);
    return res.json();
  },

  async getFlowTrends(startDate?: string, endDate?: string, teamId?: string): Promise<{ trends: FlowTrend[] }> {
    const q = buildQuery({ start_date: startDate, end_date: endDate, team_id: teamId });
    const res = await fetch(`${API_BASE_URL}/flow/trends${q}`);
    if (!res.ok) throw new Error(`Flow trends fetch failed: ${res.statusText}`);
    return res.json();
  },

  async getInterruptionBreakdown(
    startDate?: string,
    endDate?: string,
    teamId?: string
  ): Promise<{ breakdown: InterruptionCategory[] }> {
    const q = buildQuery({ start_date: startDate, end_date: endDate, team_id: teamId });
    const res = await fetch(`${API_BASE_URL}/interruptions/breakdown${q}`);
    if (!res.ok) throw new Error(`Interruption breakdown fetch failed: ${res.statusText}`);
    return res.json();
  },

  async getInterruptionTimeline(
    startDate?: string,
    endDate?: string,
    teamId?: string
  ): Promise<{ timeline: InterruptionTimelinePoint[] }> {
    const q = buildQuery({ start_date: startDate, end_date: endDate, team_id: teamId });
    const res = await fetch(`${API_BASE_URL}/interruptions/timeline${q}`);
    if (!res.ok) throw new Error(`Interruption timeline fetch failed: ${res.statusText}`);
    return res.json();
  },

  async getTeamComparison(startDate?: string, endDate?: string): Promise<{ teams: TeamComparisonMetric[] }> {
    const q = buildQuery({ start_date: startDate, end_date: endDate });
    const res = await fetch(`${API_BASE_URL}/teams/comparison${q}`);
    if (!res.ok) throw new Error(`Team comparison fetch failed: ${res.statusText}`);
    return res.json();
  },

  async getRecentActivity(
    startDate?: string,
    endDate?: string,
    teamId?: string,
    source?: string,
    category?: string,
    search?: string,
    page: number = 1,
    pageSize: number = 25
  ): Promise<ActivityResponse> {
    const q = buildQuery({
      start_date: startDate,
      end_date: endDate,
      team_id: teamId,
      source: source,
      category: category,
      search: search,
      page: page,
      page_size: pageSize
    });
    const res = await fetch(`${API_BASE_URL}/activity/recent${q}`);
    if (!res.ok) throw new Error(`Activity fetch failed: ${res.statusText}`);
    return res.json();
  }
};
