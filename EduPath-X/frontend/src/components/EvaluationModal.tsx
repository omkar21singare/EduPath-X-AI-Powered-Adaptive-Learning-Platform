import React, { useState } from 'react';
import type { EvaluationResult } from '../types';
import { runEvaluation } from '../services/api';
import { FlaskConical, Zap } from 'lucide-react';

interface EvaluationModalProps {
  onClose: () => void;
}

export const EvaluationModal: React.FC<EvaluationModalProps> = ({ onClose }) => {
  const [numTrials, setNumTrials] = useState(50);
  const [daysToSimulate, setDaysToSimulate] = useState(30);
  const [result, setResult] = useState<EvaluationResult | null>(null);
  const [isRunning, setIsRunning] = useState(false);

  const handleRun = async () => {
    setIsRunning(true);
    try {
      const res = await runEvaluation(numTrials, daysToSimulate);
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-md z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl max-w-3xl w-full p-6 shadow-2xl border border-slate-100 animate-in fade-in zoom-in-95 duration-200 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-violet-600 to-purple-600 text-white flex items-center justify-center shadow-md shadow-purple-200">
              <FlaskConical className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-heading text-lg font-bold text-slate-800">Adaptive vs Fixed Scientific Evaluation Engine</h3>
              <p className="text-xs text-slate-500">Controlled Monte Carlo simulation trial comparison</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 font-bold">✕</button>
        </div>

        {/* Inputs */}
        <div className="py-4 grid grid-cols-1 md:grid-cols-3 gap-4 border-b border-slate-100">
          <div>
            <label className="text-xs font-bold text-slate-700 block mb-1">Simulation Trials</label>
            <input
              type="number"
              value={numTrials}
              onChange={(e) => setNumTrials(Number(e.target.value))}
              className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label className="text-xs font-bold text-slate-700 block mb-1">Simulated Timeline (Days)</label>
            <input
              type="number"
              value={daysToSimulate}
              onChange={(e) => setDaysToSimulate(Number(e.target.value))}
              className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div className="flex items-end">
            <button
              onClick={handleRun}
              disabled={isRunning}
              className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow-md transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
            >
              <Zap className="w-4 h-4" />
              {isRunning ? 'Running Simulation Trials...' : 'Run Comparative Experiment'}
            </button>
          </div>
        </div>

        {/* Results */}
        {result && (
          <div className="py-5 space-y-5 animate-in fade-in duration-300">
            {/* Efficiency Highlight banner */}
            <div className="bg-gradient-to-r from-emerald-500 to-teal-600 text-white p-4 rounded-2xl shadow-lg flex items-center justify-between">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider opacity-80">Efficiency Advantage</span>
                <h4 className="text-xl font-bold font-heading">
                  EduPath-X Adaptive Engine is {result.efficiency_gain_pct}% More Efficient
                </h4>
              </div>
              <div className="w-12 h-12 rounded-full bg-white/20 flex items-center justify-center font-bold text-lg">
                +{result.efficiency_gain_pct}%
              </div>
            </div>

            {/* Comparison Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Baseline Policy A */}
              <div className="p-5 rounded-2xl border border-slate-200 bg-slate-50/50 space-y-3">
                <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                  <h4 className="font-bold text-sm text-slate-800">{result.policy_fixed.name}</h4>
                  <span className="text-[10px] font-bold bg-slate-200 text-slate-700 px-2 py-0.5 rounded-full">BASELINE</span>
                </div>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-slate-500">Avg Days to Mastery:</span>
                    <span className="font-bold text-slate-800">{result.policy_fixed.avg_days_to_mastery} Days</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Avg Questions Required:</span>
                    <span className="font-bold text-slate-800">{result.policy_fixed.avg_questions_required}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">14-Day Retention Rate:</span>
                    <span className="font-bold text-slate-800">{result.policy_fixed.retention_rate_14day}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Completion Rate:</span>
                    <span className="font-bold text-slate-800">{result.policy_fixed.completion_rate_pct}%</span>
                  </div>
                </div>
              </div>

              {/* Adaptive Policy B */}
              <div className="p-5 rounded-2xl border border-indigo-200 bg-indigo-50/40 space-y-3 shadow-sm">
                <div className="flex items-center justify-between border-b border-indigo-100 pb-2">
                  <h4 className="font-bold text-sm text-indigo-900">{result.policy_adaptive.name}</h4>
                  <span className="text-[10px] font-bold bg-indigo-600 text-white px-2 py-0.5 rounded-full">PROPOSED</span>
                </div>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-indigo-700">Avg Days to Mastery:</span>
                    <span className="font-bold text-indigo-950">{result.policy_adaptive.avg_days_to_mastery} Days</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-indigo-700">Avg Questions Required:</span>
                    <span className="font-bold text-indigo-950">{result.policy_adaptive.avg_questions_required}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-indigo-700">14-Day Retention Rate:</span>
                    <span className="font-bold text-emerald-700">{result.policy_adaptive.retention_rate_14day}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-indigo-700">Completion Rate:</span>
                    <span className="font-bold text-indigo-950">{result.policy_adaptive.completion_rate_pct}%</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Scientific Conclusion */}
            <div className="p-4 rounded-2xl bg-slate-900 text-slate-100 text-xs leading-relaxed font-medium">
              <span className="text-amber-400 font-bold uppercase tracking-wider block mb-1">Empirical Synthesis Conclusion</span>
              {result.conclusion}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
