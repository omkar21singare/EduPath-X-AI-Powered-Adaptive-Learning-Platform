import type { Recommendation } from '../types';
import { Target, Zap, Brain, ArrowDown, ShieldCheck, AlertCircle, HelpCircle } from 'lucide-react';

interface Props {
  recommendations?: Recommendation[];
}

export function AdaptiveVisualizer({ recommendations }: Props) {
  const rec = recommendations && recommendations.length > 0 ? recommendations[0] : null;

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 h-full flex flex-col justify-between">
      <div>
        {/* Header with Mode indicator */}
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2">
            <Brain className="w-5 h-5 text-indigo-600" />
            Why this question?
          </h3>
          <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
            Live Production BKT
          </span>
        </div>

        {rec ? (
          <div className="space-y-4">
            {/* Goal Connection (PART 4) */}
            <div className="p-3 bg-indigo-50/70 border border-indigo-100 rounded-xl text-xs flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Target className="w-4 h-4 text-indigo-600 shrink-0" />
                <div>
                  <span className="text-[10px] font-bold text-indigo-500 uppercase block">Active Goal</span>
                  <span className="font-extrabold text-slate-800">
                    {rec.active_goal ? `${rec.active_goal.goal_name} (Target: ${rec.active_goal.target_mastery}%)` : 'No active goal'}
                  </span>
                </div>
              </div>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md ${rec.active_goal ? 'bg-indigo-100 text-indigo-800' : 'bg-slate-100 text-slate-500'}`}>
                {rec.active_goal ? (rec.active_goal.is_direct_goal_concept ? 'Direct Target' : 'Curriculum Prereq') : 'General Study'}
              </span>
            </div>

            {/* Core Recommendation State Grid (PART 2) */}
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                <span className="text-[10px] text-slate-400 uppercase font-bold block mb-1">Selected Concept</span>
                <span className="font-extrabold text-slate-800 text-sm truncate block">{rec.concept_title || 'Not available'}</span>
                <span className="text-[10px] text-slate-500 font-semibold">{rec.concept_code || ''}</span>
              </div>

              <div className="bg-emerald-50/60 p-3 rounded-xl border border-emerald-100">
                <span className="text-[10px] text-emerald-600 uppercase font-bold block mb-1">Current BKT Mastery</span>
                <span className="font-extrabold text-emerald-800 text-sm block">
                  {rec.current_mastery !== undefined ? `${rec.current_mastery}%` : rec.rationale?.mastery_level !== undefined ? `${rec.rationale.mastery_level}%` : 'Not available'}
                </span>
                <span className="text-[10px] text-emerald-600 font-semibold">P(Know) Posterior</span>
              </div>

              <div className="bg-amber-50/60 p-3 rounded-xl border border-amber-100">
                <span className="text-[10px] text-amber-600 uppercase font-bold block mb-1">Recommended Action</span>
                <span className="font-extrabold text-amber-800 text-sm block">{rec.action_type || 'Not available'}</span>
                <span className="text-[10px] text-amber-600 font-semibold">Adaptive Policy</span>
              </div>

              <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                <span className="text-[10px] text-slate-400 uppercase font-bold block mb-1">Target Difficulty</span>
                <span className="font-extrabold text-slate-800 text-sm block">{rec.target_difficulty || 'Medium'}</span>
                <span className="text-[10px] text-slate-500 font-semibold">Item Calibration</span>
              </div>
            </div>

            {/* Prerequisites & Reason (PART 2 & 4) */}
            <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-100 space-y-2">
              <div className="flex items-center justify-between text-[11px]">
                <span className="font-bold text-slate-500 uppercase tracking-wider text-[10px]">Prerequisites</span>
                <span className={`font-bold flex items-center gap-1 ${rec.prerequisites_met !== false ? 'text-emerald-600' : 'text-amber-600'}`}>
                  {rec.prerequisites_met !== false ? (
                    <>
                      <ShieldCheck className="w-3.5 h-3.5" /> Satisfied ✓
                    </>
                  ) : (
                    <>
                      <AlertCircle className="w-3.5 h-3.5" /> Pending Prerequisites
                    </>
                  )}
                </span>
              </div>

              <div className="pt-2 border-t border-slate-200/60">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Why this recommendation?</span>
                <p className="text-xs text-slate-700 leading-relaxed font-medium italic">
                  "{rec.reason_text || 'Recommendation explanation unavailable.'}"
                </p>
              </div>
            </div>

            {/* Decision Chain (PART 3) */}
            <div className="p-3 bg-gradient-to-r from-slate-50 to-indigo-50/40 rounded-xl border border-slate-100">
              <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider mb-2 text-center flex items-center justify-center gap-1">
                <Zap className="w-3 h-3 text-indigo-500" /> Decision Pipeline Flow
              </div>
              <div className="flex items-center justify-between text-[10px] font-extrabold text-slate-600">
                <div className="text-center px-1">
                  <div className="text-slate-400 font-normal">State</div>
                  <div className="text-indigo-600 font-bold">{rec.current_mastery ?? rec.rationale?.mastery_level}%</div>
                </div>
                <ArrowDown className="w-3 h-3 text-slate-300 -rotate-90 shrink-0" />
                <div className="text-center px-1">
                  <div className="text-slate-400 font-normal">Prereqs</div>
                  <div className="text-emerald-600 font-bold">{rec.prerequisites_met !== false ? 'Met ✓' : 'Wait'}</div>
                </div>
                <ArrowDown className="w-3 h-3 text-slate-300 -rotate-90 shrink-0" />
                <div className="text-center px-1">
                  <div className="text-slate-400 font-normal">Action</div>
                  <div className="text-amber-600 font-bold">{rec.action_type}</div>
                </div>
                <ArrowDown className="w-3 h-3 text-slate-300 -rotate-90 shrink-0" />
                <div className="text-center px-1">
                  <div className="text-slate-400 font-normal">Difficulty</div>
                  <div className="text-slate-800 font-bold">{rec.target_difficulty || 'Medium'}</div>
                </div>
                <ArrowDown className="w-3 h-3 text-slate-300 -rotate-90 shrink-0" />
                <div className="text-center px-1">
                  <div className="text-slate-400 font-normal">Question</div>
                  <div className="text-indigo-700 font-bold truncate max-w-[65px]">{rec.concept_code}</div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center p-8 text-center text-slate-400 space-y-2">
            <HelpCircle className="w-8 h-8 text-slate-300" />
            <p className="text-xs font-semibold">Recommendation explanation unavailable.</p>
            <p className="text-[11px] text-slate-400">Complete an activity or set a learning goal to generate recommendations.</p>
          </div>
        )}
      </div>

      {/* Footer Disclaimer (PART 10) */}
      <div className="pt-3 border-t border-slate-100 text-[10px] text-slate-400 flex items-center justify-between">
        <span>Source: BKT Bayesian Knowledge Tracing</span>
        <span className="italic">Offline experiments separate</span>
      </div>
    </div>
  );
}
