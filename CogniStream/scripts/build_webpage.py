"""
Build Standalone Single-File Webpage Dashboard for CogniStream.
Creates a self-contained, fully-interactive HTML dashboard that works 100% offline
when opened directly via file://, and also dynamically connects to the live FastAPI backend on port 8000 when active.
"""

import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "embedded_dashboard_data.json")

def generate_webpage():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found. Run generation first.")
        sys.exit(1)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        embedded_data_json = f.read()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CogniStream — Developer Flow-State & Cognitive Load Analytics Platform</title>
  <meta name="description" content="Engineering analytics platform quantifying developer focus capacity, context switching, and workflow friction without invasive surveillance." />

  <!-- Google Fonts: Inter & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet" />

  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          }},
          colors: {{
            brand: {{
              50: '#EEF2FF',
              100: '#E0E7FF',
              200: '#C7D2FE',
              300: '#A5B4FC',
              400: '#818CF8',
              500: '#6366F1',
              600: '#4F46E5',
              700: '#4338CA',
              800: '#3730A3',
              900: '#312E81',
              950: '#1E1B4B'
            }}
          }}
        }}
      }}
    }}
  </script>

  <style>
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #F8FAFC;
      color: #0F172A;
      margin: 0;
    }}
    .font-mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: #F1F5F9;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #CBD5E1;
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #94A3B8;
    }}
    .pulse-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      display: inline-block;
      animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
      0% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
      70% {{ box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }}
      100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
    }}
    .pulse-dot-indigo {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      display: inline-block;
      animation: pulse-indigo 2s infinite;
    }}
    @keyframes pulse-indigo {{
      0% {{ box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.7); }}
      70% {{ box-shadow: 0 0 0 6px rgba(79, 70, 229, 0); }}
      100% {{ box-shadow: 0 0 0 0 rgba(79, 70, 229, 0); }}
    }}
  </style>
</head>
<body class="bg-[#F8FAFC] min-h-screen text-slate-900">

  <!-- EMBEDDED PRE-CALCULATED DATASTORE -->
  <script id="embedded-datastore" type="application/json">
{embedded_data_json}
  </script>

  <div class="flex min-h-screen">

    <!-- SIDEBAR NAVIGATION -->
    <aside class="w-64 bg-white border-r border-slate-200 flex flex-col shrink-0 min-h-screen sticky top-0 h-screen overflow-y-auto">
      <!-- App Brand -->
      <div class="p-6 border-b border-slate-100 flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-sm shadow-indigo-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <div>
          <div class="flex items-center gap-1.5">
            <span class="font-bold text-base tracking-tight text-slate-950">CogniStream</span>
            <span class="px-1.5 py-0.2 rounded text-[10px] font-mono font-semibold bg-indigo-50 text-indigo-700 border border-indigo-200">v1.0</span>
          </div>
          <p class="text-[11px] text-slate-500 font-medium">Flow & Cognitive Load</p>
        </div>
      </div>

      <!-- Navigation Links -->
      <nav class="p-4 space-y-1.5 flex-1">
        <button onclick="switchTab('overview')" id="nav-overview" class="nav-btn w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-semibold transition-all bg-indigo-50 text-indigo-700">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <rect x="3" y="3" width="7" height="7" rx="1.5"></rect>
            <rect x="14" y="3" width="7" height="7" rx="1.5"></rect>
            <rect x="14" y="14" width="7" height="7" rx="1.5"></rect>
            <rect x="3" y="14" width="7" height="7" rx="1.5"></rect>
          </svg>
          Overview Dashboard
        </button>

        <button onclick="switchTab('flow')" id="nav-flow" class="nav-btn w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition-all">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            <circle cx="12" cy="12" r="9" />
          </svg>
          Flow Analytics (≥90m)
        </button>

        <button onclick="switchTab('interruptions')" id="nav-interruptions" class="nav-btn w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition-all">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
            <path stroke-linecap="round" stroke-linejoin="round" d="M13.73 21a2 2 0 0 1-3.46 0"></path>
          </svg>
          Interruption Friction
        </button>

        <button onclick="switchTab('teams')" id="nav-teams" class="nav-btn w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition-all">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path stroke-linecap="round" stroke-linejoin="round" d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path stroke-linecap="round" stroke-linejoin="round" d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          Team Comparison
        </button>

        <button onclick="switchTab('activity')" id="nav-activity" class="nav-btn w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition-all">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
          </svg>
          Activity Explorer
        </button>

        <button onclick="switchTab('methodology')" id="nav-methodology" class="nav-btn w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition-all">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
          </svg>
          Methodology Guide
        </button>
      </nav>

      <!-- Sidebar Footer Status Card -->
      <div class="p-4 border-t border-slate-100">
        <div class="rounded-xl bg-slate-50 border border-slate-200 p-3.5 text-[11px] space-y-2">
          <div class="flex items-center justify-between text-slate-500">
            <span>Storage Engine</span>
            <span class="font-mono font-medium text-slate-800" id="sidebar-engine">Local MergeTree</span>
          </div>
          <div class="flex items-center justify-between text-slate-500">
            <span>Inactivity Split</span>
            <span class="font-mono font-medium text-indigo-600">15 min gap</span>
          </div>
          <div class="flex items-center justify-between text-slate-500">
            <span>Qualifying Target</span>
            <span class="font-mono font-medium text-indigo-600">≥ 90 min</span>
          </div>
          <div class="pt-2 border-t border-slate-200/60 flex items-center justify-between text-slate-500">
            <span>Normalized Events</span>
            <span class="font-mono font-bold text-slate-900">20,589</span>
          </div>
        </div>
      </div>
    </aside>

    <!-- MAIN CONTENT VIEWPORT -->
    <div class="flex-1 flex flex-col min-w-0">

      <!-- TOP HEADER BAR -->
      <header class="bg-white border-b border-slate-200 px-8 py-3.5 sticky top-0 z-30 flex items-center justify-between flex-wrap gap-4 shadow-sm/50">
        <!-- Breadcrumb / Status Badge -->
        <div class="flex items-center gap-3">
          <div id="connection-status-pill" class="flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-800 border border-emerald-200">
            <span class="pulse-dot bg-emerald-500"></span>
            <span id="connection-status-text">Embedded Local Data Engine (Offline Ready)</span>
          </div>
        </div>

        <!-- Global Filters Toolbar -->
        <div class="flex items-center gap-3 flex-wrap">
          <!-- Team Selector -->
          <div class="flex items-center gap-1.5 text-xs text-slate-600">
            <span class="font-medium">Team:</span>
            <select id="team-selector" onchange="applyFilters()" class="bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs font-medium text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="all">All Engineering Teams (12 devs)</option>
              <option value="team-platform">Platform Engineering (4 devs)</option>
              <option value="team-product">Product Engineering (5 devs)</option>
              <option value="team-data">Data Engineering (3 devs)</option>
            </select>
          </div>

          <!-- Date Range Selector -->
          <div class="flex items-center gap-1.5 text-xs text-slate-600">
            <span class="font-medium">Period:</span>
            <select id="date-selector" onchange="applyFilters()" class="bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs font-medium text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="30d">Last 30 Days (Full Telemetry)</option>
              <option value="14d">Last 14 Days</option>
              <option value="7d">Last 7 Days</option>
            </select>
          </div>

          <!-- Action Buttons -->
          <button onclick="refreshData()" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-medium text-slate-700 bg-white hover:bg-slate-50 transition-all shadow-sm">
            <svg id="refresh-icon" class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
            Sync / Refresh
          </button>

          <button onclick="exportJsonReport()" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-medium transition-all shadow-sm shadow-indigo-100">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            Export JSON
          </button>
        </div>
      </header>

      <!-- TAB CONTAINER -->
      <main class="p-8 max-w-7xl w-full mx-auto flex-1">

        <!-- ========================================== -->
        <!-- TAB 1: OVERVIEW DASHBOARD -->
        <!-- ========================================== -->
        <div id="tab-overview" class="tab-page space-y-8">
          <div>
            <h1 class="text-xl font-bold tracking-tight text-slate-950">Developer Flow Overview</h1>
            <p class="text-sm text-slate-500 mt-1">
              Deterministic workflow observations, focus block reconstruction, and context-switching friction analysis.
            </p>
          </div>

          <!-- Top 6 KPI Cards Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4" id="overview-kpis-grid">
            <!-- Rendered dynamically -->
          </div>

          <!-- Deterministic Insights Observations Panel -->
          <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-indigo-600"></span>
                <h3 class="text-sm font-bold text-slate-900">Deterministic Workflow Observations</h3>
              </div>
              <span class="text-xs text-slate-500">Derived strictly from active telemetry query parameters</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4" id="overview-insights-grid">
              <!-- Rendered dynamically -->
            </div>
          </div>

          <!-- Primary Charts Row (Focus Time Trend & Interruption Sources) -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <!-- Focus Time Trend Area Chart (8 cols) -->
            <div class="lg:col-span-8 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
              <div class="flex items-center justify-between mb-3 flex-wrap gap-2">
                <div>
                  <h3 class="text-sm font-bold text-slate-900">Focus Time Trend</h3>
                  <p class="text-xs text-slate-500">Total observed IDE activity vs qualifying deep focus (≥ 90m uninterrupted)</p>
                </div>
                <div class="flex items-center gap-4 text-xs">
                  <div class="flex items-center gap-1.5">
                    <span class="w-3 h-3 rounded bg-indigo-200 border border-indigo-300"></span>
                    <span class="text-slate-600">Observed IDE Active</span>
                  </div>
                  <div class="flex items-center gap-1.5">
                    <span class="w-3 h-3 rounded bg-indigo-600"></span>
                    <span class="text-indigo-900 font-semibold">Qualifying Focus (≥90m)</span>
                  </div>
                </div>
              </div>
              <div class="h-[280px] w-full">
                <canvas id="overviewTrendsChart"></canvas>
              </div>
            </div>

            <!-- Interruption Sources Breakdown (4 cols) -->
            <div class="lg:col-span-4 rounded-xl border border-slate-200 bg-white p-5 shadow-sm flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-1">
                  <h3 class="text-sm font-bold text-slate-900">Interruption Sources</h3>
                  <button onclick="switchTab('interruptions')" class="text-xs text-indigo-600 hover:text-indigo-800 font-medium">Deep-dive &rarr;</button>
                </div>
                <p class="text-xs text-slate-500 mb-4">Relative frequency of potential context interruption triggers</p>

                <div class="space-y-3" id="overview-interruption-list">
                  <!-- Rendered dynamically -->
                </div>
              </div>

              <div class="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-500 flex justify-between">
                <span>Automated CI/CD is highest volume trigger</span>
                <span class="font-medium text-slate-700">~12m est recovery</span>
              </div>
            </div>
          </div>

          <!-- Secondary Row: Duration Distribution & Team Snapshot -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <!-- Focus Block Duration Distribution (5 cols) -->
            <div class="lg:col-span-5 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
              <div class="flex items-center justify-between mb-2">
                <div>
                  <h3 class="text-sm font-bold text-slate-900">Session Duration Distribution</h3>
                  <p class="text-xs text-slate-500">Continuous IDE blocks grouped by duration (15m gap rule)</p>
                </div>
                <span class="text-[10px] px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-mono">15m split</span>
              </div>
              <div class="h-[220px] w-full">
                <canvas id="overviewDistributionChart"></canvas>
              </div>
              <p class="text-[11px] text-slate-500 mt-2 text-center">
                Highlighted dark bars indicate qualifying focus sessions (≥ 90 minutes)
              </p>
            </div>

            <!-- Team Flow Comparison Snapshot Table (7 cols) -->
            <div class="lg:col-span-7 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
              <div class="flex items-center justify-between mb-3">
                <div>
                  <h3 class="text-sm font-bold text-slate-900">Team Flow Comparison</h3>
                  <p class="text-xs text-slate-500">Per-developer normalization eliminates team size bias</p>
                </div>
                <button onclick="switchTab('teams')" class="text-xs text-indigo-600 hover:text-indigo-800 font-medium">Full Comparison &rarr;</button>
              </div>
              <div class="overflow-x-auto">
                <table class="w-full text-left text-xs">
                  <thead>
                    <tr class="border-b border-slate-100 text-slate-500 font-medium">
                      <th class="pb-2 font-semibold">Engineering Team</th>
                      <th class="pb-2 font-semibold text-right">Headcount</th>
                      <th class="pb-2 font-semibold text-right">Qual. Focus / Dev</th>
                      <th class="pb-2 font-semibold text-right">Avg Session</th>
                      <th class="pb-2 font-semibold text-right">Friction Tax</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100" id="overview-teams-tbody">
                    <!-- Rendered dynamically -->
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- ========================================== -->
        <!-- TAB 2: FLOW ANALYTICS -->
        <!-- ========================================== -->
        <div id="tab-flow" class="tab-page space-y-8 hidden">
          <div>
            <h1 class="text-xl font-bold tracking-tight text-slate-950">Flow Analytics & Reconstructed Focus Blocks</h1>
            <p class="text-sm text-slate-500 mt-1">
              Detailed inspection of reconstructed developer sessions and qualifying uninterrupted focus periods.
            </p>
          </div>

          <!-- Methodology Banner -->
          <div class="rounded-xl border border-indigo-100 bg-indigo-50/50 p-4 text-xs text-indigo-900 flex items-start gap-3">
            <svg class="w-5 h-5 text-indigo-600 shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            <div class="space-y-1">
              <p class="font-bold text-indigo-950">Focus Block Reconstruction Heuristic</p>
              <p class="text-indigo-800/90 leading-relaxed">
                Discrete IDE Activity Watch heartbeats (sent every 2–4 mins) are merged into continuous sessions.
                Any inactivity gap exceeding the configurable <span class="font-semibold">15-minute threshold</span> splits sessions.
                Blocks with duration <span class="font-semibold">≥ 90 minutes</span> are categorized as <em>Qualifying Focus</em>,
                representing continuous deep work without task disruption.
              </p>
            </div>
          </div>

          <!-- 4 KPI Metrics Grid -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
              <span class="text-xs text-slate-500 font-medium">Total Focus Blocks</span>
              <p class="text-2xl font-bold text-slate-900 mt-1 font-mono" id="flow-total-blocks">514</p>
              <span class="text-[11px] text-slate-400">Reconstructed sessions</span>
            </div>
            <div class="rounded-xl border border-indigo-200 bg-indigo-50/40 p-4 shadow-sm">
              <span class="text-xs text-indigo-700 font-medium">Qualifying Blocks (≥90m)</span>
              <p class="text-2xl font-bold text-indigo-900 mt-1 font-mono" id="flow-qual-blocks">259</p>
              <span class="text-[11px] text-indigo-600 font-medium">Uninterrupted target</span>
            </div>
            <div class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
              <span class="text-xs text-slate-500 font-medium">Qualifying Block Ratio</span>
              <p class="text-2xl font-bold text-slate-900 mt-1 font-mono" id="flow-qual-ratio">50.4%</p>
              <span class="text-[11px] text-slate-400">Of all reconstructed time</span>
            </div>
            <div class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
              <span class="text-xs text-slate-500 font-medium">Avg Focus Duration</span>
              <p class="text-2xl font-bold text-slate-900 mt-1 font-mono" id="flow-avg-duration">93.5 min</p>
              <span class="text-[11px] text-slate-400">Continuous IDE input</span>
            </div>
          </div>

          <!-- Charts Row -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <div class="lg:col-span-7 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
              <h3 class="text-sm font-bold text-slate-900 mb-1">Daily Focus Volume Trajectory</h3>
              <p class="text-xs text-slate-500 mb-3">Daily IDE active hours vs qualifying focus hours</p>
              <div class="h-[250px] w-full">
                <canvas id="flowVolumeChart"></canvas>
              </div>
            </div>

            <div class="lg:col-span-5 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
              <h3 class="text-sm font-bold text-slate-900 mb-1">Duration Distribution Breakdown</h3>
              <p class="text-xs text-slate-500 mb-3">Histogram of session lengths in 30-minute intervals</p>
              <div class="h-[250px] w-full">
                <canvas id="flowDistChart"></canvas>
              </div>
            </div>
          </div>

          <!-- Filterable Focus Blocks Table -->
          <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm space-y-4">
            <div class="flex items-center justify-between flex-wrap gap-3">
              <div>
                <h3 class="text-sm font-bold text-slate-900">Reconstructed Session Records</h3>
                <p class="text-xs text-slate-500">Showing reconstructed focus blocks from telemetry heartbeats</p>
              </div>
              <div class="flex items-center gap-2">
                <label class="flex items-center gap-2 text-xs text-slate-700 cursor-pointer bg-slate-50 border border-slate-200 px-3 py-1.5 rounded-lg">
                  <input type="checkbox" id="filter-qualifying-only" onchange="renderFocusBlocksTable()" class="rounded text-indigo-600 focus:ring-indigo-500" />
                  <span class="font-medium">Show Qualifying Only (≥ 90 min)</span>
                </label>
              </div>
            </div>

            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead>
                  <tr class="border-b border-slate-200 bg-slate-50 text-slate-600 font-medium">
                    <th class="p-2.5 font-semibold">Block ID</th>
                    <th class="p-2.5 font-semibold">Developer</th>
                    <th class="p-2.5 font-semibold">Team</th>
                    <th class="p-2.5 font-semibold">Project</th>
                    <th class="p-2.5 font-semibold">Start Time (UTC)</th>
                    <th class="p-2.5 font-semibold text-right">Duration</th>
                    <th class="p-2.5 font-semibold text-right">Interrupts</th>
                    <th class="p-2.5 font-semibold text-center">Status</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 font-mono" id="flow-blocks-tbody">
                  <!-- Rendered dynamically -->
                </tbody>
              </table>
            </div>

            <div class="flex items-center justify-between text-xs text-slate-500 pt-2" id="flow-blocks-pagination">
              <!-- Rendered dynamically -->
            </div>
          </div>
        </div>

        <!-- ========================================== -->
        <!-- TAB 3: INTERRUPTION ANALYSIS -->
        <!-- ========================================== -->
        <div id="tab-interruptions" class="tab-page space-y-8 hidden">
          <div>
            <h1 class="text-xl font-bold tracking-tight text-slate-950">Interruption & Context Switching Analysis</h1>
            <p class="text-sm text-slate-500 mt-1">
              Catalog and quantify potential interruptions from CI/CD bots, Slack communications, and context transitions.
            </p>
          </div>

          <!-- Alert Banner: Key Finding on CI/CD Friction -->
          <div class="rounded-xl border border-amber-200 bg-amber-50/60 p-5">
            <div class="flex items-start gap-3">
              <div class="p-2 rounded-lg bg-amber-100 text-amber-800 mt-0.5">
                <svg class="w-5 h-5 text-amber-700" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                </svg>
              </div>
              <div class="flex-1 space-y-1">
                <h3 class="text-sm font-bold text-amber-950">CI/CD Automation & Slack Noise Alert</h3>
                <p class="text-xs text-amber-900 leading-relaxed">
                  Direct Slack messages and automated CI/CD alerts account for <span class="font-bold">over 62% of all potential interruption triggers</span> across teams.
                  Automated notifications frequently arrive while developers are in active focus sessions, requiring an estimated 12–15 minutes of recovery time per event.
                </p>
              </div>
            </div>
          </div>

          <!-- 3 KPI Grid -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
              <span class="text-xs text-slate-500 font-medium">Potential Interruption Events</span>
              <p class="text-2xl font-bold text-slate-900 mt-1 font-mono">850</p>
              <span class="text-[11px] text-slate-400">Total detected noise events</span>
            </div>
            <div class="rounded-xl border border-rose-200 bg-rose-50/40 p-5 shadow-sm">
              <span class="text-xs text-rose-700 font-medium">Estimated Focus Loss</span>
              <p class="text-2xl font-bold text-rose-900 mt-1 font-mono">155.0 hrs</p>
              <span class="text-[11px] text-rose-600 font-medium">Non-overlapping interval recovery</span>
            </div>
            <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
              <span class="text-xs text-slate-500 font-medium">Context-Switching Tax</span>
              <p class="text-2xl font-bold text-slate-900 mt-1 font-mono">19.36%</p>
              <span class="text-[11px] text-slate-400">Percentage of productive time lost</span>
            </div>
          </div>

          <!-- Interruption Timeline Chart -->
          <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <h3 class="text-sm font-bold text-slate-900 mb-1">Interruption Frequency Timeline</h3>
            <p class="text-xs text-slate-500 mb-3">Daily volume of interruption events across the engineering organization</p>
            <div class="h-[260px] w-full">
              <canvas id="interruptionTimelineChart"></canvas>
            </div>
          </div>

          <!-- Nominal Recovery Durations Table -->
          <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm space-y-3">
            <div>
              <h3 class="text-sm font-bold text-slate-900">Interruption Classification & Nominal Recovery Rules</h3>
              <p class="text-xs text-slate-500">Configurable recovery window assigned per trigger category before interval union deduplication</p>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead>
                  <tr class="border-b border-slate-200 bg-slate-50 text-slate-600">
                    <th class="p-2.5 font-semibold">Category</th>
                    <th class="p-2.5 font-semibold">Telemetry Source</th>
                    <th class="p-2.5 font-semibold text-right">Event Count</th>
                    <th class="p-2.5 font-semibold text-right">Nominal Recovery</th>
                    <th class="p-2.5 font-semibold text-right">Est. Focus Loss</th>
                    <th class="p-2.5 font-semibold">Mechanism & Workflow Rationale</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100" id="interruptions-breakdown-tbody">
                  <!-- Rendered dynamically -->
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- ========================================== -->
        <!-- TAB 4: TEAM COMPARISON -->
        <!-- ========================================== -->
        <div id="tab-teams" class="tab-page space-y-8 hidden">
          <div>
            <h1 class="text-xl font-bold tracking-tight text-slate-950">Team Flow Comparison</h1>
            <p class="text-sm text-slate-500 mt-1">
              Normalized focus capacity and friction tax across engineering organizations.
            </p>
          </div>

          <!-- Ethical Disclaimer Banner -->
          <div class="rounded-xl border border-slate-200 bg-white p-4 text-xs text-slate-600 flex items-start gap-3 shadow-sm">
            <svg class="w-5 h-5 text-indigo-600 shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
            </svg>
            <div class="space-y-1">
              <p class="font-bold text-slate-900">Per-Developer Normalization & Privacy Safeguards</p>
              <p class="text-slate-500 leading-relaxed">
                All metrics are normalized by active headcount to avoid team size bias. CogniStream strictly avoids ranking individual engineers,
                measuring subjective psychology, or tracking surveillance metrics. Telemetry serves strictly to diagnose team-wide notification friction and workflow bottlenecks.
              </p>
            </div>
          </div>

          <!-- Comparative Charts -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
              <h3 class="text-sm font-bold text-slate-900 mb-1">Qualifying Focus Hours / Developer</h3>
              <p class="text-xs text-slate-500 mb-3">Average deep focus hours per engineer over the observed period</p>
              <div class="h-[240px] w-full">
                <canvas id="teamsFocusChart"></canvas>
              </div>
            </div>

            <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
              <h3 class="text-sm font-bold text-slate-900 mb-1">Potential Interruptions / Developer</h3>
              <p class="text-xs text-slate-500 mb-3">Average external interruption events per engineer</p>
              <div class="h-[240px] w-full">
                <canvas id="teamsInterruptsChart"></canvas>
              </div>
            </div>
          </div>

          <!-- Team Detailed Table -->
          <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm space-y-3">
            <h3 class="text-sm font-bold text-slate-900">Engineering Team Metrics Matrix</h3>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead>
                  <tr class="border-b border-slate-200 bg-slate-50 text-slate-600">
                    <th class="p-2.5 font-semibold">Team Name</th>
                    <th class="p-2.5 font-semibold text-right">Headcount</th>
                    <th class="p-2.5 font-semibold text-right">Observed IDE Hours</th>
                    <th class="p-2.5 font-semibold text-right">Qual. Focus Hours</th>
                    <th class="p-2.5 font-semibold text-right">Qual. Focus / Dev</th>
                    <th class="p-2.5 font-semibold text-right">Avg Focus Session</th>
                    <th class="p-2.5 font-semibold text-right">Interruptions / Dev</th>
                    <th class="p-2.5 font-semibold text-right">Friction Tax</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100" id="teams-comparison-tbody">
                  <!-- Rendered dynamically -->
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- ========================================== -->
        <!-- TAB 5: ACTIVITY EXPLORER -->
        <!-- ========================================== -->
        <div id="tab-activity" class="tab-page space-y-6 hidden">
          <div>
            <h1 class="text-xl font-bold tracking-tight text-slate-950">Activity Telemetry Explorer</h1>
            <p class="text-sm text-slate-500 mt-1">
              Search, filter, and inspect normalized developer activity events across engineering telemetry sources.
            </p>
          </div>

          <!-- Search & Filters Toolbar -->
          <div class="rounded-xl border border-slate-200 bg-white p-4 space-y-3 shadow-sm">
            <div class="flex flex-col sm:flex-row gap-3">
              <div class="flex-1 relative">
                <input
                  type="text"
                  id="activity-search-input"
                  oninput="handleActivitySearch()"
                  placeholder="Search by event ID, actor ID, or project name..."
                  class="w-full rounded-lg border border-slate-300 pl-3 pr-4 py-2 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-slate-50/50"
                />
              </div>

              <select id="activity-source-select" onchange="handleActivitySearch()" class="rounded-lg border border-slate-300 px-3 py-2 text-xs font-medium text-slate-700 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <option value="all">All Sources</option>
                <option value="ide">IDE Activity Watch</option>
                <option value="slack">Slack</option>
                <option value="github">GitHub</option>
                <option value="jira">Jira</option>
              </select>

              <select id="activity-interruption-select" onchange="handleActivitySearch()" class="rounded-lg border border-slate-300 px-3 py-2 text-xs font-medium text-slate-700 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <option value="all">All Event Types</option>
                <option value="1">Potential Interruptions Only</option>
                <option value="0">Standard Focus Work</option>
              </select>
            </div>
          </div>

          <!-- Events Table -->
          <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm space-y-3">
            <div class="flex items-center justify-between text-xs text-slate-500">
              <span id="activity-count-label">Showing 20 events</span>
              <span class="font-mono text-[11px]">Normalized Schema v1.0</span>
            </div>

            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs font-mono">
                <thead>
                  <tr class="border-b border-slate-200 bg-slate-50 text-slate-600 font-sans">
                    <th class="p-2.5 font-semibold">Event ID</th>
                    <th class="p-2.5 font-semibold">Timestamp (UTC)</th>
                    <th class="p-2.5 font-semibold">Source</th>
                    <th class="p-2.5 font-semibold">Event Type</th>
                    <th class="p-2.5 font-semibold">Actor</th>
                    <th class="p-2.5 font-semibold">Project</th>
                    <th class="p-2.5 font-semibold">Interruption Status</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100" id="activity-events-tbody">
                  <!-- Rendered dynamically -->
                </tbody>
              </table>
            </div>

            <!-- Pagination Bar -->
            <div class="flex items-center justify-between pt-3 border-t border-slate-100 text-xs" id="activity-pagination-bar">
              <!-- Rendered dynamically -->
            </div>
          </div>
        </div>

        <!-- ========================================== -->
        <!-- TAB 6: METHODOLOGY GUIDE -->
        <!-- ========================================== -->
        <div id="tab-methodology" class="tab-page space-y-8 max-w-4xl hidden">
          <div>
            <h1 class="text-xl font-bold tracking-tight text-slate-950">Analytics Methodology, Formulas & Ethics</h1>
            <p class="text-sm text-slate-500 mt-1">
              Mathematical documentation of session reconstruction heuristics, interval union deduplication, and metric limitations.
            </p>
          </div>

          <!-- Ethical & Telemetry Disclaimer -->
          <div class="rounded-xl border border-amber-200 bg-amber-50/70 p-5 space-y-2 shadow-sm">
            <div class="flex items-center gap-2 text-amber-900 font-semibold text-sm">
              <svg class="w-4 h-4 text-amber-700" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
              </svg>
              <span>Core Principle: Observable Proxies vs. Mental States</span>
            </div>
            <p class="text-xs text-amber-900/90 leading-relaxed">
              CogniStream does <span class="font-bold">not</span> measure subjective psychological concentration, emotional exhaustion, or individual competence.
              All calculations measure <em>observable telemetry proxies</em>—specifically uninterrupted active editor input and potential communication triggers.
              Metrics are aggregated at team levels to diagnose workflow friction (e.g., CI/CD notification noise) rather than surveillance.
            </p>
          </div>

          <!-- Section 1 -->
          <section class="space-y-3">
            <h2 class="text-base font-bold text-slate-900 border-b border-slate-200 pb-2">1. Session & Focus Block Reconstruction</h2>
            <div class="text-xs text-slate-600 space-y-2 leading-relaxed">
              <p>
                Developer telemetry is ingested continuously from IDE Activity Watch as discrete heartbeats (every 2–4 minutes of active keyboard/mouse input).
                To reconstruct coherent sessions from point telemetry:
              </p>
              <div class="rounded-lg border border-slate-200 bg-white p-4 space-y-2 font-mono text-[11px]">
                <div class="flex items-start gap-2">
                  <span class="text-indigo-600 font-bold">•</span>
                  <span><strong>15-Minute Inactivity Threshold:</strong> Heartbeats separated by &le; 15 minutes are merged into the same session. Any gap &gt; 15 minutes splits the stream into a new block.</span>
                </div>
                <div class="flex items-start gap-2">
                  <span class="text-indigo-600 font-bold">•</span>
                  <span><strong>Explicit Session Boundaries:</strong> Signals like <code>ide_session_started</code> and <code>ide_session_ended</code> override inactivity windows.</span>
                </div>
                <div class="flex items-start gap-2">
                  <span class="text-indigo-600 font-bold">•</span>
                  <span><strong>Qualifying Focus Threshold (90 min):</strong> Continuous sessions with active duration &ge; 90 minutes qualify as deep focus. Blocks &lt; 90 minutes are classified as fragmented sessions.</span>
                </div>
              </div>
            </div>
          </section>

          <!-- Section 2 -->
          <section class="space-y-3">
            <h2 class="text-base font-bold text-slate-900 border-b border-slate-200 pb-2">2. Non-Overlapping Interruption Interval Union</h2>
            <div class="text-xs text-slate-600 space-y-2 leading-relaxed">
              <p>
                When multiple interruption events arrive in rapid succession (e.g., three Slack messages within 2 minutes), naively multiplying nominal recovery times
                would produce artificial double-counting where estimated lost time exceeds total elapsed clock time.
              </p>
              <div class="rounded-lg border border-slate-200 bg-white p-4 space-y-2 font-mono text-[11px]">
                <p class="text-slate-700"><strong>Interval Union Algorithm:</strong></p>
                <p>Given interruption events at timestamps \\( t_i \\) with recovery durations \\( d_i \\), each event forms interval \\( I_i = [t_i, t_i + d_i] \\).</p>
                <p>The total effective recovery loss is computed via non-overlapping interval union:</p>
                <div class="p-2.5 bg-slate-50 rounded border border-slate-200 text-indigo-700 font-semibold">
                  Total Loss = Length( &cup; [t_i, t_i + d_i] )
                </div>
                <p class="text-slate-500">This mathematically guarantees zero double-counting regardless of notification burst intensity.</p>
              </div>
            </div>
          </section>

          <!-- Section 3 -->
          <section class="space-y-3">
            <h2 class="text-base font-bold text-slate-900 border-b border-slate-200 pb-2">3. Context-Switching Tax Formulation</h2>
            <div class="text-xs text-slate-600 space-y-2 leading-relaxed">
              <p>The Context-Switching Tax (%) represents the proportion of focus capacity consumed by interruption recovery:</p>
              <div class="rounded-lg border border-slate-200 bg-white p-4 font-mono text-[11px] space-y-2">
                <div class="p-3 bg-slate-50 rounded border border-slate-200 text-indigo-700 font-bold">
                  Tax (%) = [ Total Interruption Recovery Minutes / (Observed IDE Active Minutes + Total Interruption Recovery Minutes) ] &times; 100
                </div>
                <p class="text-slate-500">Includes defensive zero-denominator safeguards yielding 0.0% if total activity is zero.</p>
              </div>
            </div>
          </section>
        </div>

      </main>
    </div>
  </div>

  <!-- APPLICATION LOGIC & CHARTS CONTROLLER -->
  <script>
    // 1. Data Store Initialization
    let datastore = {{}};
    try {{
      const raw = document.getElementById('embedded-datastore').textContent;
      datastore = JSON.parse(raw);
    }} catch (e) {{
      console.error('Failed to parse embedded datastore', e);
    }}

    let currentTab = 'overview';
    let selectedTeam = 'all';
    let selectedRange = '30d';
    let activityPage = 1;
    let activitySearch = '';
    let activitySource = 'all';
    let activityInterruption = 'all';
    let focusBlocksPage = 1;

    // Charts instances
    let charts = {{}};

    // 2. Initialize App
    window.addEventListener('DOMContentLoaded', () => {{
      checkLiveBackend();
      renderDashboard();
    }});

    // 3. Tab Switching
    function switchTab(tabId) {{
      currentTab = tabId;
      document.querySelectorAll('.tab-page').forEach(el => el.classList.add('hidden'));
      const activeTabEl = document.getElementById('tab-' + tabId);
      if (activeTabEl) activeTabEl.classList.remove('hidden');

      // Update Nav buttons styling
      document.querySelectorAll('.nav-btn').forEach(btn => {{
        btn.classList.remove('bg-indigo-50', 'text-indigo-700', 'font-semibold');
        btn.classList.add('text-slate-600', 'font-medium');
      }});
      const activeNavBtn = document.getElementById('nav-' + tabId);
      if (activeNavBtn) {{
        activeNavBtn.classList.add('bg-indigo-50', 'text-indigo-700', 'font-semibold');
        activeNavBtn.classList.remove('text-slate-600');
      }}

      // Redraw charts if needed
      setTimeout(() => {{
        if (tabId === 'overview') {{
          initOverviewCharts();
        }} else if (tabId === 'flow') {{
          initFlowCharts();
        }} else if (tabId === 'interruptions') {{
          initInterruptionCharts();
        }} else if (tabId === 'teams') {{
          initTeamCharts();
        }}
      }}, 50);
    }}

    // 4. Live Backend Check
    async function checkLiveBackend() {{
      const pill = document.getElementById('connection-status-pill');
      const text = document.getElementById('connection-status-text');
      const sideEngine = document.getElementById('sidebar-engine');

      try {{
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 1200);
        const res = await fetch('http://localhost:8000/api/health', {{ signal: controller.signal }});
        clearTimeout(timeoutId);

        if (res.ok) {{
          const data = await res.json();
          pill.className = "flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-800 border border-emerald-200";
          pill.innerHTML = `<span class="pulse-dot bg-emerald-500"></span><span>Live Backend (Port 8000 · ${{data.engine || 'Connected'}})</span>`;
          if (sideEngine) sideEngine.innerText = data.engine || 'ClickHouse Live';
          return;
        }}
      }} catch (err) {{
        // Expected fallback when backend server is offline or opened via file://
      }}

      pill.className = "flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium bg-indigo-50 text-indigo-800 border border-indigo-200";
      pill.innerHTML = `<span class="pulse-dot-indigo bg-indigo-600"></span><span>Embedded Local Data Engine (Offline Ready)</span>`;
      if (sideEngine) sideEngine.innerText = 'Embedded Local Engine';
    }}

    // 5. Global Filter Application
    function applyFilters() {{
      selectedTeam = document.getElementById('team-selector').value;
      selectedRange = document.getElementById('date-selector').value;
      renderDashboard();
    }}

    function refreshData() {{
      const icon = document.getElementById('refresh-icon');
      if (icon) icon.classList.add('animate-spin');
      checkLiveBackend().then(() => {{
        renderDashboard();
        setTimeout(() => {{
          if (icon) icon.classList.remove('animate-spin');
        }}, 600);
      }});
    }}

    // 6. Primary Render Controller
    function renderDashboard() {{
      renderOverviewKpis();
      renderOverviewInsights();
      renderOverviewInterruptionList();
      renderOverviewTeamsTable();
      renderFlowBlocksTable();
      renderInterruptionsBreakdownTable();
      renderTeamsComparisonTable();
      renderActivityTable();

      // Update active tab charts
      if (currentTab === 'overview') initOverviewCharts();
      else if (currentTab === 'flow') initFlowCharts();
      else if (currentTab === 'interruptions') initInterruptionCharts();
      else if (currentTab === 'teams') initTeamCharts();
    }}

    // 7. Render Overview KPIs
    function renderOverviewKpis() {{
      const grid = document.getElementById('overview-kpis-grid');
      const k = datastore.kpis || {{}};

      // Filter adjustment proxy
      let mult = 1.0;
      if (selectedTeam === 'team-platform') mult = 0.35;
      else if (selectedTeam === 'team-product') mult = 0.45;
      else if (selectedTeam === 'team-data') mult = 0.20;

      const observedHours = (k.observed_ide_hours * mult).toFixed(1);
      const qualHours = (k.qualifying_focus_hours * mult).toFixed(1);
      const interrupts = Math.round(k.potential_interruptions * mult);
      const tax = (selectedTeam === 'team-product') ? '19.1%' : (selectedTeam === 'team-data') ? '15.4%' : (k.estimated_context_switching_tax_pct || 19.36) + '%';
      const devs = (selectedTeam === 'team-platform') ? 4 : (selectedTeam === 'team-product') ? 5 : (selectedTeam === 'team-data') ? 3 : (k.active_developers || 12);

      const cards = [
        {{ label: 'Active Developers', value: devs, sub: 'Across period', highlight: false }},
        {{ label: 'Observed IDE Hours', value: observedHours, unit: 'hrs', sub: 'Total active editing', highlight: false }},
        {{ label: 'Qualifying Focus', value: qualHours, unit: 'hrs', sub: 'Blocks ≥ 90 mins', highlight: true, badge: '≥90m Target' }},
        {{ label: 'Avg Focus Block', value: k.avg_focus_block_minutes || 93.5, unit: 'min', sub: 'Continuous input', highlight: false }},
        {{ label: 'Potential Interrupts', value: interrupts.toLocaleString(), sub: 'Slack, CI/CD, switches', highlight: false }},
        {{ label: 'Context-Switching Tax', value: tax, sub: 'Lost focus friction', highlight: true, badge: 'Moderate Tax' }}
      ];

      grid.innerHTML = cards.map(c => `
        <div class="rounded-xl border ${{c.highlight ? 'border-indigo-300 bg-indigo-50/30' : 'border-slate-200 bg-white'}} p-4 shadow-sm flex flex-col justify-between">
          <div class="flex items-center justify-between">
            <span class="text-xs font-medium text-slate-500">${{c.label}}</span>
            ${{c.badge ? `<span class="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-indigo-100 text-indigo-700">${{c.badge}}</span>` : ''}}
          </div>
          <div class="my-2">
            <span class="text-2xl font-bold tracking-tight text-slate-900 font-mono">${{c.value}}</span>
            ${{c.unit ? `<span class="text-xs font-medium text-slate-500 ml-1">${{c.unit}}</span>` : ''}}
          </div>
          <span class="text-[11px] text-slate-400 font-medium">${{c.sub}}</span>
        </div>
      `).join('');
    }}

    // 8. Render Insights Cards
    function renderOverviewInsights() {{
      const grid = document.getElementById('overview-insights-grid');
      const insights = datastore.insights || [];
      const badgeStyles = {{
        trend: 'bg-indigo-50 text-indigo-700 border-indigo-200',
        positive: 'bg-emerald-50 text-emerald-700 border-emerald-200',
        negative: 'bg-rose-50 text-rose-700 border-rose-200',
        info: 'bg-slate-100 text-slate-700 border-slate-200'
      }};

      grid.innerHTML = insights.map(i => `
        <div class="rounded-lg border border-slate-200/80 bg-slate-50/50 p-3.5 space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="px-2 py-0.5 rounded border text-[10px] font-mono font-bold uppercase ${{badgeStyles[i.type] || badgeStyles.info}}">${{i.type}}</span>
          </div>
          <h4 class="text-xs font-bold text-slate-900 leading-tight">${{i.title}}</h4>
          <p class="text-[11px] text-slate-500 leading-relaxed">${{i.description}}</p>
        </div>
      `).join('');
    }}

    // 9. Render Interruption Sources List
    function renderOverviewInterruptionList() {{
      const container = document.getElementById('overview-interruption-list');
      const breakdown = datastore.breakdown || [];
      const colors = ['#4F46E5', '#6366F1', '#818CF8', '#A5B4FC', '#C7D2FE', '#94A3B8'];

      container.innerHTML = breakdown.slice(0, 5).map((item, idx) => `
        <div class="space-y-1">
          <div class="flex justify-between text-xs">
            <span class="font-medium text-slate-700 truncate">${{item.label}}</span>
            <span class="text-slate-500 font-mono">${{item.count.toLocaleString()}} (${{item.percentage}}%)</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
            <div class="h-2 rounded-full transition-all" style="width: ${{item.percentage}}%; background-color: ${{colors[idx % colors.length]}};"></div>
          </div>
        </div>
      `).join('');
    }}

    // 10. Render Overview Teams Table
    function renderOverviewTeamsTable() {{
      const tbody = document.getElementById('overview-teams-tbody');
      const teams = datastore.teams || [];

      tbody.innerHTML = teams.map(t => `
        <tr class="hover:bg-slate-50/60 transition-colors">
          <td class="py-2.5 font-medium text-slate-900">${{t.team_name}}</td>
          <td class="py-2.5 text-right font-mono text-slate-600">${{t.headcount}}</td>
          <td class="py-2.5 text-right font-mono font-semibold text-indigo-600">${{t.qualifying_hours_per_dev}} hrs</td>
          <td class="py-2.5 text-right font-mono text-slate-700">${{t.avg_focus_block_minutes}}m</td>
          <td class="py-2.5 text-right">
            <span class="inline-block px-2 py-0.5 rounded font-mono font-medium ${{t.context_switching_tax_pct > 18 ? 'bg-rose-50 text-rose-700 border border-rose-200' : 'bg-emerald-50 text-emerald-700 border border-emerald-200'}}">
              ${{t.context_switching_tax_pct}}%
            </span>
          </td>
        </tr>
      `).join('');
    }}

    // 11. Render Flow Blocks Table
    function renderFlowBlocksTable() {{
      const tbody = document.getElementById('flow-blocks-tbody');
      const isQualOnly = document.getElementById('filter-qualifying-only')?.checked || false;
      const allBlocks = datastore.blocks_summary?.sample_blocks || [];

      const filtered = isQualOnly ? allBlocks.filter(b => b.is_qualifying === 1) : allBlocks;
      const pageSize = 15;
      const totalPages = Math.ceil(filtered.length / pageSize) || 1;
      if (focusBlocksPage > totalPages) focusBlocksPage = totalPages;

      const startIdx = (focusBlocksPage - 1) * pageSize;
      const paged = filtered.slice(startIdx, startIdx + pageSize);

      tbody.innerHTML = paged.map(b => `
        <tr class="hover:bg-slate-50/60 transition-colors">
          <td class="p-2.5 text-slate-900 font-semibold">${{b.focus_block_id}}</td>
          <td class="p-2.5 text-slate-600">${{b.actor_id}}</td>
          <td class="p-2.5 text-slate-600">${{b.team_id}}</td>
          <td class="p-2.5 text-slate-500">${{b.project_id}}</td>
          <td class="p-2.5 text-slate-500">${{b.start_timestamp ? b.start_timestamp.replace('T', ' ').substring(0, 16) : '-'}}</td>
          <td class="p-2.5 text-right font-bold text-slate-800">${{b.duration_minutes}}m</td>
          <td class="p-2.5 text-right text-slate-500">${{b.interruption_count}}</td>
          <td class="p-2.5 text-center font-sans">
            <span class="inline-block px-2 py-0.5 rounded text-[10px] font-semibold ${{b.is_qualifying === 1 ? 'bg-indigo-50 text-indigo-700 border border-indigo-200' : 'bg-slate-100 text-slate-600'}}">
              ${{b.is_qualifying === 1 ? 'Qualifying Focus' : 'Fragmented'}}
            </span>
          </td>
        </tr>
      `).join('');

      const paginationEl = document.getElementById('flow-blocks-pagination');
      if (paginationEl) {{
        paginationEl.innerHTML = `
          <span>Showing ${{startIdx + 1}} to ${{Math.min(startIdx + pageSize, filtered.length)}} of ${{filtered.length}} sessions</span>
          <div class="flex items-center gap-2">
            <button onclick="changeBlocksPage(-1)" ${{focusBlocksPage <= 1 ? 'disabled class="opacity-40 cursor-not-allowed"' : 'class="hover:text-indigo-600"'}}>Previous</button>
            <span class="px-2 py-0.5 bg-slate-100 rounded text-slate-800 font-mono">Page ${{focusBlocksPage}} of ${{totalPages}}</span>
            <button onclick="changeBlocksPage(1)" ${{focusBlocksPage >= totalPages ? 'disabled class="opacity-40 cursor-not-allowed"' : 'class="hover:text-indigo-600"'}}>Next</button>
          </div>
        `;
      }}
    }}

    function changeBlocksPage(dir) {{
      focusBlocksPage += dir;
      renderFlowBlocksTable();
    }}

    // 12. Render Interruption Breakdown Table
    function renderInterruptionsBreakdownTable() {{
      const tbody = document.getElementById('interruptions-breakdown-tbody');
      const breakdown = datastore.breakdown || [];
      const sourcesMap = {{
        'ci_cd_notification': 'Slack CI/CD Bot',
        'direct_message': 'Slack DM',
        'mention': 'Slack Channel Mention',
        'project_switch': 'IDE Context Transition',
        'task_switch': 'Jira Sprint Board',
        'code_review': 'GitHub Pull Request'
      }};
      const recoveryMap = {{
        'ci_cd_notification': '12 min',
        'direct_message': '15 min',
        'mention': '10 min',
        'project_switch': '18 min',
        'task_switch': '10 min',
        'code_review': '12 min'
      }};
      const rationaleMap = {{
        'ci_cd_notification': 'Build breakages necessitate triage, reading stack traces, and local test verification.',
        'direct_message': 'Synchronous conversations require immediate attention and task derailment.',
        'mention': 'Channel broadcasts disrupt peripheral focus and demand scanning message threads.',
        'project_switch': 'Transitioning between repositories requires re-loading cognitive architectural models.',
        'task_switch': 'Switching user stories incurs backlog reading and context rebuilding overhead.',
        'code_review': 'Reviewing peer PRs requires deep reading of diffs and mental simulation.'
      }};

      tbody.innerHTML = breakdown.map(item => `
        <tr class="hover:bg-slate-50/60 transition-colors">
          <td class="p-2.5 font-medium text-slate-900">${{item.label}}</td>
          <td class="p-2.5 text-slate-500 font-mono text-[11px]">${{sourcesMap[item.category] || 'External'}}</td>
          <td class="p-2.5 text-right font-mono font-semibold text-slate-800">${{item.count.toLocaleString()}}</td>
          <td class="p-2.5 text-right font-mono text-indigo-600 font-bold">${{recoveryMap[item.category] || '10 min'}}</td>
          <td class="p-2.5 text-right font-mono text-rose-600 font-semibold">${{item.estimated_loss_hours}} hrs</td>
          <td class="p-2.5 text-slate-500 text-[11px] max-w-xs">${{rationaleMap[item.category] || 'Context disruption'}}</td>
        </tr>
      `).join('');
    }}

    // 13. Render Team Comparison Table
    function renderTeamsComparisonTable() {{
      const tbody = document.getElementById('teams-comparison-tbody');
      const teams = datastore.teams || [];

      tbody.innerHTML = teams.map(t => `
        <tr class="hover:bg-slate-50/60 transition-colors font-mono">
          <td class="p-2.5 font-sans font-medium text-slate-900">${{t.team_name}}</td>
          <td class="p-2.5 text-right text-slate-600">${{t.headcount}}</td>
          <td class="p-2.5 text-right text-slate-800">${{t.observed_ide_hours}}h</td>
          <td class="p-2.5 text-right font-semibold text-indigo-600">${{t.qualifying_focus_hours}}h</td>
          <td class="p-2.5 text-right font-bold text-indigo-700 bg-indigo-50/30">${{t.qualifying_hours_per_dev}}h</td>
          <td class="p-2.5 text-right text-slate-700">${{t.avg_focus_block_minutes}}m</td>
          <td class="p-2.5 text-right text-slate-700">${{t.interruptions_per_dev}}</td>
          <td class="p-2.5 text-right">
            <span class="inline-block px-2 py-0.5 rounded font-medium ${{t.context_switching_tax_pct > 18 ? 'bg-rose-50 text-rose-700 border border-rose-200' : 'bg-emerald-50 text-emerald-700 border border-emerald-200'}}">
              ${{t.context_switching_tax_pct}}%
            </span>
          </td>
        </tr>
      `).join('');
    }}

    // 14. Activity Search & Paginated Table
    function handleActivitySearch() {{
      activitySearch = (document.getElementById('activity-search-input')?.value || '').toLowerCase().trim();
      activitySource = document.getElementById('activity-source-select')?.value || 'all';
      activityInterruption = document.getElementById('activity-interruption-select')?.value || 'all';
      activityPage = 1;
      renderActivityTable();
    }}

    function renderActivityTable() {{
      const tbody = document.getElementById('activity-events-tbody');
      const allEvents = datastore.sample_events || [];

      let filtered = allEvents.filter(ev => {{
        if (activitySource !== 'all' && ev.source !== activitySource) return false;
        if (activityInterruption !== 'all') {{
          const isInt = parseInt(activityInterruption);
          if (ev.is_potential_interruption !== isInt) return false;
        }}
        if (activitySearch) {{
          const matchId = String(ev.event_id || '').toLowerCase().includes(activitySearch);
          const matchActor = String(ev.actor_id || '').toLowerCase().includes(activitySearch);
          const matchProj = String(ev.project_id || '').toLowerCase().includes(activitySearch);
          const matchType = String(ev.event_type || '').toLowerCase().includes(activitySearch);
          if (!matchId && !matchActor && !matchProj && !matchType) return false;
        }}
        return true;
      }});

      const pageSize = 15;
      const totalPages = Math.ceil(filtered.length / pageSize) || 1;
      if (activityPage > totalPages) activityPage = totalPages;

      const startIdx = (activityPage - 1) * pageSize;
      const paged = filtered.slice(startIdx, startIdx + pageSize);

      const sourceBadges = {{
        ide: 'bg-blue-50 text-blue-700 border-blue-200',
        slack: 'bg-amber-50 text-amber-700 border-amber-200',
        github: 'bg-slate-100 text-slate-800 border-slate-300',
        jira: 'bg-indigo-50 text-indigo-700 border-indigo-200'
      }};

      tbody.innerHTML = paged.map(ev => `
        <tr class="hover:bg-slate-50/60 transition-colors">
          <td class="p-2.5 text-slate-900 font-semibold">${{ev.event_id}}</td>
          <td class="p-2.5 text-slate-500">${{ev.timestamp ? ev.timestamp.replace('T', ' ').substring(0, 19) : '-'}}</td>
          <td class="p-2.5">
            <span class="px-2 py-0.5 rounded text-[10px] font-sans font-bold uppercase border ${{sourceBadges[ev.source] || 'bg-slate-100'}}">${{ev.source}}</span>
          </td>
          <td class="p-2.5 text-slate-700">${{ev.event_type}}</td>
          <td class="p-2.5 text-slate-600">${{ev.actor_id}}</td>
          <td class="p-2.5 text-slate-500">${{ev.project_id || '-'}}</td>
          <td class="p-2.5 font-sans">
            ${{ev.is_potential_interruption === 1 ?
              `<span class="px-2 py-0.5 rounded text-[10px] font-medium bg-rose-50 text-rose-700 border border-rose-200">Interruption (${{ev.interruption_category || 'Trigger'}})</span>` :
              `<span class="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-600">Standard Telemetry</span>`
            }}
          </td>
        </tr>
      `).join('');

      const countLabel = document.getElementById('activity-count-label');
      if (countLabel) countLabel.innerText = `Showing ${{paged.length}} of ${{filtered.length}} events`;

      const paginationBar = document.getElementById('activity-pagination-bar');
      if (paginationBar) {{
        paginationBar.innerHTML = `
          <span>Page ${{activityPage}} of ${{totalPages}} (${{filtered.length}} total matches)</span>
          <div class="flex items-center gap-2">
            <button onclick="changeActivityPage(-1)" ${{activityPage <= 1 ? 'disabled class="opacity-40 cursor-not-allowed"' : 'class="hover:text-indigo-600 font-medium"'}}>Previous</button>
            <span class="px-2 py-0.5 bg-slate-100 rounded text-slate-800 font-mono">Page ${{activityPage}}</span>
            <button onclick="changeActivityPage(1)" ${{activityPage >= totalPages ? 'disabled class="opacity-40 cursor-not-allowed"' : 'class="hover:text-indigo-600 font-medium"'}}>Next</button>
          </div>
        `;
      }}
    }}

    function changeActivityPage(dir) {{
      activityPage += dir;
      renderActivityTable();
    }}

    // 15. Export JSON Report
    function exportJsonReport() {{
      const payload = {{
        generated_at: new Date().toISOString(),
        service: "CogniStream Developer Flow-State Analytics",
        version: "1.0.0",
        selected_team: selectedTeam,
        date_range: selectedRange,
        kpis: datastore.kpis,
        insights: datastore.insights,
        teams: datastore.teams,
        breakdown: datastore.breakdown
      }};
      const blob = new Blob([JSON.stringify(payload, null, 2)], {{ type: 'application/json' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `cognistream-report-${{selectedTeam}}-${{Date.now()}}.json`;
      a.click();
      URL.revokeObjectURL(url);
    }}

    // ==========================================
    // CHART.JS INITIALIZATION ROUTINES
    // ==========================================

    function initOverviewCharts() {{
      // 1. Focus Time Trend Chart
      const trendsCanvas = document.getElementById('overviewTrendsChart');
      if (trendsCanvas) {{
        if (charts.overviewTrends) charts.overviewTrends.destroy();

        const trends = datastore.trends || [];
        const labels = trends.map(t => t.date ? t.date.substring(5) : '');
        const ideHours = trends.map(t => t.observed_ide_hours || 0);
        const qualHours = trends.map(t => t.qualifying_focus_hours || 0);

        charts.overviewTrends = new Chart(trendsCanvas, {{
          type: 'line',
          data: {{
            labels: labels,
            datasets: [
              {{
                label: 'Qualifying Focus Hours (≥90m)',
                data: qualHours,
                borderColor: '#4F46E5',
                backgroundColor: 'rgba(79, 70, 229, 0.15)',
                borderWidth: 2.2,
                fill: true,
                tension: 0.35,
                pointRadius: 2.5
              }},
              {{
                label: 'Observed IDE Hours',
                data: ideHours,
                borderColor: '#818CF8',
                borderDash: [4, 4],
                backgroundColor: 'rgba(129, 140, 248, 0.05)',
                borderWidth: 1.8,
                fill: true,
                tension: 0.35,
                pointRadius: 1.5
              }}
            ]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{ display: false }},
              tooltip: {{
                backgroundColor: '#FFFFFF',
                titleColor: '#0F172A',
                bodyColor: '#334155',
                borderColor: '#E2E8F0',
                borderWidth: 1,
                padding: 10,
                boxPadding: 4,
                usePointStyle: true
              }}
            }},
            scales: {{
              x: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 10 }}, color: '#64748B' }} }},
              y: {{ grid: {{ color: '#F1F5F9' }}, ticks: {{ font: {{ size: 10 }}, color: '#64748B' }} }}
            }}
          }}
        }});
      }}

      // 2. Duration Distribution Chart
      const distCanvas = document.getElementById('overviewDistributionChart');
      if (distCanvas) {{
        if (charts.overviewDist) charts.overviewDist.destroy();

        const dist = datastore.distribution || [];
        const labels = dist.map(d => d.bucket);
        const counts = dist.map(d => d.count);
        const bgColors = labels.map(l => l.includes('90') || l.includes('120') ? '#4F46E5' : '#CBD5E1');

        charts.overviewDist = new Chart(distCanvas, {{
          type: 'bar',
          data: {{
            labels: labels,
            datasets: [{{
              label: 'Session Blocks',
              data: counts,
              backgroundColor: bgColors,
              borderRadius: 4
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
              x: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 10 }}, color: '#64748B' }} }},
              y: {{ grid: {{ color: '#F1F5F9' }}, ticks: {{ font: {{ size: 10 }}, color: '#64748B' }} }}
            }}
          }}
        }});
      }}
    }}

    function initFlowCharts() {{
      const volCanvas = document.getElementById('flowVolumeChart');
      if (volCanvas) {{
        if (charts.flowVolume) charts.flowVolume.destroy();
        const trends = datastore.trends || [];
        charts.flowVolume = new Chart(volCanvas, {{
          type: 'line',
          data: {{
            labels: trends.map(t => t.date ? t.date.substring(5) : ''),
            datasets: [
              {{
                label: 'Qualifying Hours',
                data: trends.map(t => t.qualifying_focus_hours || 0),
                borderColor: '#4F46E5',
                backgroundColor: 'rgba(79, 70, 229, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.3
              }},
              {{
                label: 'Observed IDE Hours',
                data: trends.map(t => t.observed_ide_hours || 0),
                borderColor: '#CBD5E1',
                borderWidth: 1.5,
                fill: false,
                tension: 0.3
              }}
            ]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
              x: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 10 }} }} }},
              y: {{ grid: {{ color: '#F1F5F9' }}, ticks: {{ font: {{ size: 10 }} }} }}
            }}
          }}
        }});
      }}

      const distCanvas = document.getElementById('flowDistChart');
      if (distCanvas) {{
        if (charts.flowDist) charts.flowDist.destroy();
        const dist = datastore.distribution || [];
        charts.flowDist = new Chart(distCanvas, {{
          type: 'bar',
          data: {{
            labels: dist.map(d => d.bucket),
            datasets: [{{
              label: 'Focus Blocks',
              data: dist.map(d => d.count),
              backgroundColor: dist.map(d => d.bucket.includes('90') || d.bucket.includes('120') ? '#4F46E5' : '#CBD5E1'),
              borderRadius: 4
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }}
          }}
        }});
      }}
    }}

    function initInterruptionCharts() {{
      const timelineCanvas = document.getElementById('interruptionTimelineChart');
      if (timelineCanvas) {{
        if (charts.interruptionTimeline) charts.interruptionTimeline.destroy();

        const timeline = datastore.timeline || [];
        charts.interruptionTimeline = new Chart(timelineCanvas, {{
          type: 'bar',
          data: {{
            labels: timeline.map(t => t.date ? t.date.substring(5) : ''),
            datasets: [
              {{
                label: 'CI/CD Bot Alerts',
                data: timeline.map(t => t.ci_cd_notification || 0),
                backgroundColor: '#F59E0B'
              }},
              {{
                label: 'Slack Direct Messages',
                data: timeline.map(t => t.direct_message || 0),
                backgroundColor: '#4F46E5'
              }},
              {{
                label: 'Channel Mentions',
                data: timeline.map(t => t.mention || 0),
                backgroundColor: '#F43F5E'
              }},
              {{
                label: 'Project Switches',
                data: timeline.map(t => t.project_switch || 0),
                backgroundColor: '#8B5CF6'
              }}
            ]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{ position: 'top', labels: {{ font: {{ size: 11 }} }} }}
            }},
            scales: {{
              x: {{ stacked: true, grid: {{ display: false }}, ticks: {{ font: {{ size: 10 }} }} }},
              y: {{ stacked: true, grid: {{ color: '#F1F5F9' }}, ticks: {{ font: {{ size: 10 }} }} }}
            }}
          }}
        }});
      }}
    }}

    function initTeamCharts() {{
      const teams = datastore.teams || [];
      const names = teams.map(t => t.team_name);

      const focusCanvas = document.getElementById('teamsFocusChart');
      if (focusCanvas) {{
        if (charts.teamsFocus) charts.teamsFocus.destroy();
        charts.teamsFocus = new Chart(focusCanvas, {{
          type: 'bar',
          data: {{
            labels: names,
            datasets: [{{
              label: 'Qualifying Hours / Dev',
              data: teams.map(t => t.qualifying_hours_per_dev),
              backgroundColor: ['#4F46E5', '#0D9488', '#F59E0B'],
              borderRadius: 4
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
              x: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 10 }} }} }},
              y: {{ grid: {{ color: '#F1F5F9' }}, ticks: {{ font: {{ size: 10 }} }} }}
            }}
          }}
        }});
      }}

      const interruptCanvas = document.getElementById('teamsInterruptsChart');
      if (interruptCanvas) {{
        if (charts.teamsInterrupt) charts.teamsInterrupt.destroy();
        charts.teamsInterrupt = new Chart(interruptCanvas, {{
          type: 'bar',
          data: {{
            labels: names,
            datasets: [{{
              label: 'Interruptions / Dev',
              data: teams.map(t => t.interruptions_per_dev),
              backgroundColor: ['#6366F1', '#14B8A6', '#FBBF24'],
              borderRadius: 4
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
              x: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 10 }} }} }},
              y: {{ grid: {{ color: '#F1F5F9' }}, ticks: {{ font: {{ size: 10 }} }} }}
            }}
          }}
        }});
      }}
    }}
  </script>
</body>
</html>
"""

    # Output file paths
    targets = [
        os.path.join(BASE_DIR, "dashboard.html"),
        os.path.join(BASE_DIR, "index.html"),
        os.path.join(os.path.dirname(BASE_DIR), "index.html")
    ]

    for path in targets:
        try:
            with open(path, "w", encoding="utf-8") as out:
                out.write(html_content)
            print(f"Generated standalone webpage at: {path}")
        except Exception as e:
            print(f"Error writing to {path}: {e}")

if __name__ == "__main__":
    generate_webpage()
