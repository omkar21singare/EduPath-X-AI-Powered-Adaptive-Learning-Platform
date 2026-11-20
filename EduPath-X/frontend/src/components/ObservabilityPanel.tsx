
export function ObservabilityPanel({ dashboardData }: any) {
  return (
    <div className="bg-slate-900 p-8 rounded-2xl shadow-xl mt-8 text-slate-300">
      <div className="flex items-center justify-between mb-8">
        <h3 className="text-xl font-bold text-white tracking-tight">Research / Experimental Observability</h3>
        <div className="flex gap-3">
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-bold uppercase tracking-wider">
            PHASE 2 — Production Adaptive
          </span>
          <span className="px-3 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-full text-xs font-bold uppercase tracking-wider">
            PHASE 3B — Offline Research
          </span>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Phase 3B Research Summary */}
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
          <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-4">Final True Mastery Comparison</h4>
          <div className="space-y-4">
            <div className="flex justify-between items-center text-sm">
              <span className="font-semibold">Fast Profile</span>
              <div className="text-right">
                <div><span className="text-slate-400">Phase 2:</span> <span className="text-white">0.833</span></div>
                <div><span className="text-slate-400">Phase 3B IRT:</span> <span className="text-white">0.827</span></div>
              </div>
            </div>
            <div className="flex justify-between items-center text-sm border-t border-slate-700/50 pt-4">
              <span className="font-semibold">Average Profile</span>
              <div className="text-right">
                <div><span className="text-slate-400">Phase 2:</span> <span className="text-white">0.740</span></div>
                <div><span className="text-slate-400">Phase 3B IRT:</span> <span className="text-white">0.744</span></div>
              </div>
            </div>
            <div className="flex justify-between items-center text-sm border-t border-slate-700/50 pt-4">
              <span className="font-semibold">Struggling Profile</span>
              <div className="text-right">
                <div><span className="text-slate-400">Phase 2:</span> <span className="text-white">0.608</span></div>
                <div><span className="text-slate-400">Phase 3B IRT:</span> <span className="text-white">0.604</span></div>
              </div>
            </div>
          </div>
        </div>

        {/* Item Exposure Analysis */}
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
          <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-4">Item Exposure Analysis</h4>
          <div className="space-y-4">
            <div className="text-sm">
              <div className="font-bold text-emerald-400 mb-1">Phase 2 Adaptive</div>
              <div className="flex justify-between"><span className="text-slate-400">Mean unique questions:</span> <span className="text-white font-mono">25.5</span></div>
              <div className="flex justify-between"><span className="text-slate-400">Repetition rate:</span> <span className="text-white font-mono">35%</span></div>
            </div>
            <div className="text-sm border-t border-slate-700/50 pt-4">
              <div className="font-bold text-indigo-400 mb-1">Phase 3B IRT Adaptive</div>
              <div className="flex justify-between"><span className="text-slate-400">Mean unique questions:</span> <span className="text-white font-mono">12.5</span></div>
              <div className="flex justify-between"><span className="text-slate-400">Repetition rate:</span> <span className="text-white font-mono">67%</span></div>
            </div>
          </div>
          <div className="mt-4 p-3 bg-slate-900/80 rounded-lg text-xs italic text-slate-400 border border-slate-700/30">
            Phase 3B concentrated practice on fewer items because unrestricted nearest-difficulty matching allowed repeated selection of the same item.
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* IRT Visual Explanation */}
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
          <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-4 flex items-center justify-between">
            BKT → IRT Bridge
            <span className="px-2 py-0.5 bg-rose-500/10 text-rose-400 rounded text-[10px] uppercase border border-rose-500/20">Offline Experimental Bridge</span>
          </h4>
          <div className="flex items-center justify-between text-xs font-bold text-slate-400 mb-4 bg-slate-900 p-4 rounded-lg">
            <span>BKT Mastery</span>
            <span>→</span>
            <span>logit(P)</span>
            <span>→</span>
            <span>Calibrated Map</span>
            <span>→</span>
            <span className="text-indigo-400">IRT θ Estimate</span>
          </div>
          <div className="text-center font-mono text-sm text-slate-300 bg-slate-900/50 py-3 rounded-lg border border-slate-700/30">
            θ = 0.610 × logit(P(L)) - 0.431
          </div>
        </div>

        {/* Live System State Placeholder */}
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
          <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-4 flex items-center justify-between">
            Live Production State
            <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded text-[10px] uppercase border border-emerald-500/20">Active</span>
          </h4>
          <div className="space-y-3 text-sm">
             <div className="flex justify-between items-center bg-slate-900 p-3 rounded-lg">
              <span className="text-slate-400 font-medium">Concept Mastery (Global)</span>
              <span className="font-mono text-white">
                {dashboardData?.kpis?.overall_progress ? (dashboardData.kpis.overall_progress + '%') : 'Not available'}
              </span>
            </div>
            <div className="flex justify-between items-center bg-slate-900 p-3 rounded-lg">
              <span className="text-slate-400 font-medium">Estimated IRT Ability (θ)</span>
              <span className="font-mono text-slate-500 italic">Offline experiment</span>
            </div>
            <div className="flex justify-between items-center bg-slate-900 p-3 rounded-lg">
              <span className="text-slate-400 font-medium">Current Item Difficulty (b)</span>
              <span className="font-mono text-slate-500 italic">Offline experiment</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
