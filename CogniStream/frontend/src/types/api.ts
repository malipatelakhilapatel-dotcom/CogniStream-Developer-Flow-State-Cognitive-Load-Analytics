export interface HealthStatus {
  status: string;
  database_connected: boolean;
  engine: string;
  table_counts: Record<string, number>;
  mode: string;
}

export interface OverviewKpis {
  active_developers: number;
  observed_ide_hours: number;
  qualifying_focus_hours: number;
  avg_focus_block_minutes: number;
  potential_interruptions: number;
  estimated_context_switching_tax_pct: number;
  total_focus_blocks: number;
  qualifying_focus_blocks: number;
  period_days: number;
}

export interface Insight {
  id: string;
  type: 'positive' | 'negative' | 'warning' | 'trend' | 'info';
  title: string;
  description: string;
}

export interface OverviewResponse {
  kpis: OverviewKpis;
  insights: Insight[];
}

export interface FlowTrend {
  date: string;
  observed_ide_hours: number;
  qualifying_focus_hours: number;
  focus_blocks: number;
  interruptions: number;
  active_devs: number;
}

export interface FocusBlock {
  focus_block_id: string;
  actor_id: string;
  team_id: string;
  project_id: string | null;
  start_timestamp: string;
  end_timestamp: string;
  duration_minutes: number;
  interruption_count: number;
  is_qualifying: number;
  qualification_status: string;
}

export interface DurationBucket {
  bucket: string;
  count: number;
}

export interface FlowBlocksResponse {
  total_blocks: number;
  duration_distribution: DurationBucket[];
  blocks: FocusBlock[];
}

export interface InterruptionCategory {
  category: string;
  label: string;
  count: number;
  percentage: number;
  estimated_loss_hours: number;
}

export interface InterruptionTimelinePoint {
  date: string;
  total_interruptions: number;
  ci_cd_notification: number;
  direct_message: number;
  mention: number;
  project_switch: number;
  task_switch: number;
  other: number;
}

export interface TeamComparisonMetric {
  team_id: string;
  team_name: string;
  headcount: number;
  observed_ide_hours: number;
  qualifying_focus_hours: number;
  qualifying_hours_per_dev: number;
  interruptions_per_dev: number;
  avg_focus_block_minutes: number;
  context_switch_count: number;
  context_switching_tax_pct: number;
}

export interface ActivityEvent {
  event_id: string;
  timestamp: string;
  source: string;
  event_type: string;
  actor_id: string;
  team_id: string;
  project_id: string | null;
  interruption_category: string;
  is_potential_interruption: number;
}

export interface ActivityResponse {
  page: number;
  page_size: number;
  total_events: number;
  total_pages: number;
  events: ActivityEvent[];
}

export interface FilterOption {
  id: string;
  name: string;
}

export interface FiltersResponse {
  teams: FilterOption[];
  projects: FilterOption[];
  sources: FilterOption[];
  categories: FilterOption[];
  date_range: {
    default_start: string;
    default_end: string;
  };
}
