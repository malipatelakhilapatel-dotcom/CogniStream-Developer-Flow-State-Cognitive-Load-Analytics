import React from 'react';
import {
  LayoutDashboard,
  Timer,
  BellOff,
  GitCompare,
  ListOrdered,
  BookOpen,
  Cpu
} from 'lucide-react';

export type NavigationTab = 'overview' | 'flow' | 'interruptions' | 'teams' | 'activity' | 'methodology';

interface SidebarProps {
  currentTab: NavigationTab;
  onSelectTab: (tab: NavigationTab) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentTab, onSelectTab }) => {
  const navItems = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'flow', label: 'Flow Analytics', icon: Timer },
    { id: 'interruptions', label: 'Interruption Analysis', icon: BellOff },
    { id: 'teams', label: 'Team Comparison', icon: GitCompare },
    { id: 'activity', label: 'Activity Explorer', icon: ListOrdered },
    { id: 'methodology', label: 'Methodology & Bias', icon: BookOpen },
  ];

  return (
    <aside className="w-64 border-r border-gray-200 bg-white flex flex-col justify-between shrink-0 h-screen sticky top-0 select-none">
      <div>
        {/* Logo and Brand */}
        <div className="h-16 px-6 flex items-center gap-3 border-b border-gray-200">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white shadow-sm">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-base tracking-tight text-gray-900">CogniStream</span>
              <span className="text-[10px] uppercase font-bold text-indigo-600 bg-indigo-50 px-1.5 py-0.5 rounded border border-indigo-200">
                v1.0
              </span>
            </div>
            <p className="text-[11px] text-gray-500 font-medium">Flow & Cognitive Friction</p>
          </div>
        </div>

        {/* Navigation List */}
        <nav className="p-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onSelectTab(item.id as NavigationTab)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-indigo-50 text-indigo-700 font-semibold'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-600' : 'text-gray-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Info Box */}
      <div className="p-4 border-t border-gray-200 bg-gray-50/70">
        <div className="text-xs text-gray-600 space-y-1">
          <div className="font-semibold text-gray-900">Observable Telemetry Proxy</div>
          <p className="text-[11px] text-gray-500 leading-normal">
            Quantifies workflow interruption triggers and estimated recovery times. Never measures human cognitive states directly.
          </p>
        </div>
      </div>
    </aside>
  );
};
