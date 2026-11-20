import React from 'react';
import { Play, FastForward, RotateCcw, Sparkles, FlaskConical } from 'lucide-react';

interface SimulationBarProps {
  currentDay: number;
  selectedProfile: string;
  setSelectedProfile: (p: string) => void;
  onSimulateDays: (days: number) => void;
  onResetSimulation: () => void;
  onStartGuidedDemo: () => void;
  onOpenEvaluation: () => void;
  isLoading: boolean;
}

export const SimulationBar: React.FC<SimulationBarProps> = ({
  currentDay,
  selectedProfile,
  setSelectedProfile,
  onSimulateDays,
  onResetSimulation,
  onStartGuidedDemo,
  onOpenEvaluation,
  isLoading
}) => {
  return (
    <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white px-6 py-3 border-b border-indigo-950 flex flex-wrap items-center justify-between gap-4 shadow-lg sticky top-0 z-30">
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 px-3 py-1 bg-indigo-500/20 border border-indigo-400/30 rounded-full text-xs font-semibold text-indigo-300">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          Mode B: Timeline Simulation
        </div>
        <div className="text-xs text-slate-300 font-medium">
          Simulated Day: <span className="font-bold text-white text-sm bg-slate-800 px-2.5 py-0.5 rounded-lg border border-slate-700">Day {currentDay}</span>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        {/* Profile selector */}
        <select
          value={selectedProfile}
          onChange={(e) => setSelectedProfile(e.target.value)}
          className="bg-slate-800 text-slate-200 text-xs font-medium px-3 py-1.5 rounded-lg border border-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <option value="Balanced learner">Balanced Learner</option>
          <option value="Strong learner">Strong Learner</option>
          <option value="Struggling with Trees">Struggling with Trees</option>
          <option value="Inconsistent learner">Inconsistent Learner</option>
        </select>

        {/* Action Buttons */}
        <button
          onClick={() => onSimulateDays(1)}
          disabled={isLoading}
          className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg transition-colors shadow-sm disabled:opacity-50"
        >
          <Play className="w-3.5 h-3.5" />
          Simulate 1 Day
        </button>

        <button
          onClick={() => onSimulateDays(7)}
          disabled={isLoading}
          className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 bg-indigo-700 hover:bg-indigo-600 text-white rounded-lg transition-colors shadow-sm disabled:opacity-50"
        >
          <FastForward className="w-3.5 h-3.5" />
          +7 Days
        </button>

        <button
          onClick={() => onSimulateDays(30)}
          disabled={isLoading}
          className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 bg-indigo-800 hover:bg-indigo-700 text-white rounded-lg transition-colors shadow-sm disabled:opacity-50"
        >
          <FastForward className="w-3.5 h-3.5" />
          +30 Days
        </button>

        <button
          onClick={onResetSimulation}
          disabled={isLoading}
          className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition-colors border border-slate-700 disabled:opacity-50"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          Reset
        </button>

        <div className="h-4 w-px bg-slate-800 mx-1"></div>

        <button
          onClick={onStartGuidedDemo}
          className="flex items-center gap-1.5 text-xs font-bold px-3 py-1.5 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-white rounded-lg transition-all shadow-md shadow-amber-900/20"
        >
          <Sparkles className="w-3.5 h-3.5" />
          Guided Demo
        </button>

        <button
          onClick={onOpenEvaluation}
          className="flex items-center gap-1.5 text-xs font-bold px-3 py-1.5 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 text-white rounded-lg transition-all shadow-md shadow-purple-900/20"
        >
          <FlaskConical className="w-3.5 h-3.5" />
          Evaluation Engine
        </button>
      </div>
    </div>
  );
};
