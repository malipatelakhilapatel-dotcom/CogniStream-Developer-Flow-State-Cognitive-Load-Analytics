import React from 'react';
import {
  BookOpen,
  CheckCircle,
  HelpCircle,
  Shield,
  Layers,
  Sparkles,
  Percent,
  Timer,
  AlertTriangle
} from 'lucide-react';

export const MethodologyPage: React.FC = () => {
  return (
    <div className="max-w-4xl space-y-10 pb-16">
      {/* Title */}
      <div>
        <h1 className="text-xl font-bold tracking-tight text-gray-950">Analytics Methodology & Assumptions</h1>
        <p className="text-sm text-gray-500 mt-1">
          Detailed documentation of session reconstruction heuristics, recovery assumptions, and metric limitations.
        </p>
      </div>

      {/* Ethical & Telemetry Disclaimer */}
      <div className="rounded-xl border border-amber-200 bg-amber-50/60 p-5 space-y-2">
        <div className="flex items-center gap-2 text-amber-900 font-semibold text-sm">
          <Shield className="w-4 h-4 text-amber-700" />
          <span>Core Principle: Observable Proxies vs. Mental States</span>
        </div>
        <p className="text-xs text-amber-900/90 leading-relaxed">
          CogniStream does <span className="font-semibold">not</span> measure subjective mental concentration, cognitive fatigue,
          or individual developer competence. All metrics measure <em>observable telemetry proxies</em>—specifically uninterrupted
          active editor time and potential communication triggers. Metrics are aggregated at the team level to diagnose workflow
          frictions such as CI/CD noise rather than monitor individuals.
        </p>
      </div>

      {/* Section 1: Session & Focus Block Reconstruction */}
      <section className="space-y-4">
        <div className="flex items-center gap-2 border-b border-gray-200 pb-2">
          <Timer className="w-5 h-5 text-indigo-600" />
          <h2 className="text-base font-bold text-gray-900">1. Session & Focus Block Reconstruction</h2>
        </div>

        <div className="text-xs text-gray-600 space-y-3 leading-relaxed">
          <p>
            Developer telemetry is ingested continuously from IDE Activity Watch as periodic heartbeat events (every 2–4 minutes of active input).
            To reconstruct coherent work blocks from discrete telemetry points:
          </p>

          <div className="rounded-lg border border-gray-200 bg-white p-4 space-y-2 font-mono text-[11px]">
            <div className="flex items-start gap-2">
              <span className="text-indigo-600 font-bold">•</span>
              <span><strong>Inactivity Threshold (15 mins):</strong> Heartbeats separated by &le; 15 minutes are merged into the same continuous session. Any gap &gt; 15 minutes automatically splits the stream into a new block.</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-indigo-600 font-bold">•</span>
              <span><strong>Explicit Session Boundaries:</strong> Explicit <code>ide_session_started</code> and <code>ide_session_ended</code> signals override heartbeat intervals.</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-indigo-600 font-bold">•</span>
              <span><strong>Qualifying Focus Threshold (90 mins):</strong> Reconstructed blocks with continuous active duration &ge; 90 minutes qualify as deep uninterrupted focus blocks. Blocks &lt; 90 minutes are classified as fragmented.</span>
            </div>
          </div>
        </div>
      </section>

      {/* Section 2: Non-Overlapping Interruption Interval Union */}
      <section className="space-y-4">
        <div className="flex items-center gap-2 border-b border-gray-200 pb-2">
          <Layers className="w-5 h-5 text-indigo-600" />
          <h2 className="text-base font-bold text-gray-900">2. Interruption Loss & Recovery Model</h2>
        </div>

        <div className="text-xs text-gray-600 space-y-3 leading-relaxed">
          <p>
            When a potential interruption event occurs, cognitive research suggests a brief period of distraction and recovery before returning to context.
            CogniStream assigns configurable nominal recovery durations based on category:
          </p>

          <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white">
            <table className="w-full text-left text-xs">
              <thead className="bg-gray-50 border-b border-gray-200 text-gray-600">
                <tr>
                  <th className="p-2.5 font-semibold">Category</th>
                  <th className="p-2.5 font-semibold">Source</th>
                  <th className="p-2.5 font-semibold text-right">Nominal Recovery</th>
                  <th className="p-2.5 font-semibold">Rationale & Trigger Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                <tr>
                  <td className="p-2.5 font-medium text-gray-900">CI/CD Notification</td>
                  <td className="p-2.5 text-gray-500">Slack Bot</td>
                  <td className="p-2.5 text-right font-mono text-indigo-600 font-semibold">12 min</td>
                  <td className="p-2.5 text-gray-500">Failed build alerts require log inspection and triage.</td>
                </tr>
                <tr>
                  <td className="p-2.5 font-medium text-gray-900">Direct Message</td>
                  <td className="p-2.5 text-gray-500">Slack</td>
                  <td className="p-2.5 text-right font-mono text-indigo-600 font-semibold">15 min</td>
                  <td className="p-2.5 text-gray-500">Personal synchronous queries demanding real-time reply.</td>
                </tr>
                <tr>
                  <td className="p-2.5 font-medium text-gray-900">Cross-Project Switch</td>
                  <td className="p-2.5 text-gray-500">IDE Telemetry</td>
                  <td className="p-2.5 text-right font-mono text-indigo-600 font-semibold">18 min</td>
                  <td className="p-2.5 text-gray-500">Switching repositories requires mental and tool reload.</td>
                </tr>
                <tr>
                  <td className="p-2.5 font-medium text-gray-900">Channel @Mention</td>
                  <td className="p-2.5 text-gray-500">Slack</td>
                  <td className="p-2.5 text-right font-mono text-indigo-600 font-semibold">10 min</td>
                  <td className="p-2.5 text-gray-500">Targeted alerts in team channels.</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="rounded-lg border border-emerald-200 bg-emerald-50/50 p-4 space-y-1">
            <h4 className="font-semibold text-emerald-950 flex items-center gap-1.5">
              <CheckCircle className="w-4 h-4 text-emerald-600" />
              <span>Interval Union: Strict Prevention of Double-Counting</span>
            </h4>
            <p className="text-emerald-900/90 text-xs">
              If multiple Slack messages arrive at 14:00, 14:02, and 14:05, nominal recovery times would sum to 45 minutes.
              CogniStream maps each event to a time range <span className="font-mono">[T, T + R]</span> and merges overlapping intervals into a unified non-overlapping set.
              This mathematically guarantees that overlapping interruptions are never double-counted.
            </p>
          </div>
        </div>
      </section>

      {/* Section 3: Context-Switching Tax */}
      <section className="space-y-4">
        <div className="flex items-center gap-2 border-b border-gray-200 pb-2">
          <Percent className="w-5 h-5 text-indigo-600" />
          <h2 className="text-base font-bold text-gray-900">3. Context-Switching Tax Formula</h2>
        </div>

        <div className="text-xs text-gray-600 space-y-3 leading-relaxed">
          <p>The Context-Switching Tax expresses the proportion of observed working time estimated to be absorbed by interruption friction:</p>

          <div className="rounded-lg border border-gray-200 bg-gray-50 p-4 text-center font-mono text-xs">
            <span className="font-bold text-indigo-700">Estimated Context-Switching Tax (%)</span> =
            <span className="inline-block mx-2 text-gray-800">
              (Total Merged Interruption Recovery Time / Total Observed Active IDE Time) &times; 100
            </span>
          </div>

          <p className="text-gray-500 italic">
            Note: If observed IDE active time is zero for a given period, the calculation returns 0.0% to avoid division-by-zero errors.
          </p>
        </div>
      </section>

      {/* Section 4: Limitations & Sources of Bias */}
      <section className="space-y-4">
        <div className="flex items-center gap-2 border-b border-gray-200 pb-2">
          <AlertTriangle className="w-5 h-5 text-amber-600" />
          <h2 className="text-base font-bold text-gray-900">4. Known Limitations & Potential Bias</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-gray-600">
          <div className="p-4 rounded-lg border border-gray-200 bg-white space-y-1">
            <h4 className="font-semibold text-gray-900">Async Notifications</h4>
            <p className="text-gray-500">
              Developers do not immediately read every Slack notification. Treating every bot alert as an active interruption represents an upper bound on potential disruption.
            </p>
          </div>

          <div className="p-4 rounded-lg border border-gray-200 bg-white space-y-1">
            <h4 className="font-semibold text-gray-900">Non-IDE Thinking Time</h4>
            <p className="text-gray-500">
              System architecture design, sketching on physical whiteboards, and reading technical RFCs take place outside the IDE and may appear as inactivity.
            </p>
          </div>

          <div className="p-4 rounded-lg border border-gray-200 bg-white space-y-1">
            <h4 className="font-semibold text-gray-900">Synthetic Fixtures</h4>
            <p className="text-gray-500">
              Current demonstration metrics are generated deterministically using realistic behavioral profiles and are explicitly labeled as synthetic demo telemetry.
            </p>
          </div>

          <div className="p-4 rounded-lg border border-gray-200 bg-white space-y-1">
            <h4 className="font-semibold text-gray-900">No Causal Claims</h4>
            <p className="text-gray-500">
              Correlation between notification spikes and split sessions highlights opportunities to tune alerts, but does not definitively prove causation.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};
