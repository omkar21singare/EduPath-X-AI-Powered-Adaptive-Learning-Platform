import React, { useState } from 'react';
import type { GoalData, ConceptNode } from '../types';
import { Target, CheckCircle2, RefreshCw, Plus, Sparkles, X } from 'lucide-react';
import { createOrUpdateGoal, submitGoalProgress } from '../services/api';
import { AnimatedNumber } from './AnimatedNumber';

interface GoalWidgetProps {
  goal?: GoalData;
  concepts?: ConceptNode[];
  onRefreshDashboard?: () => void;
}

export const GoalWidget: React.FC<GoalWidgetProps> = ({
  goal,
  concepts = [],
  onRefreshDashboard
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [selectedConceptId, setSelectedConceptId] = useState<number>(3); // Default to Arrays (ID 3)
  const [targetMasteryPct, setTargetMasteryPct] = useState<number>(80);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [syncFeedback, setSyncFeedback] = useState<string | null>(null);

  // Filter concepts that have practice questions or are unlocked
  const practiceableConcepts = concepts.length > 0
    ? concepts.filter(c => [3, 4, 5, 9, 12].includes(c.id))
    : [
        { id: 3, title: 'Arrays & Strings' },
        { id: 4, title: 'Linked Lists' },
        { id: 5, title: 'Stacks & Queues' },
        { id: 9, title: 'Binary Search Trees' },
        { id: 12, title: 'Graph Representations' },
      ];

  const currentMastery = goal?.current_mastery ? Math.round(goal.current_mastery * 100) : 10;
  const targetMastery = goal?.target_mastery ? Math.round(goal.target_mastery * 100) : 80;
  const progressPct = goal?.progress_percentage ?? Math.min(100, Math.round((currentMastery / targetMastery) * 100));
  const remainingPoints = goal?.remaining_percentage_points ?? Math.max(0, targetMastery - currentMastery);
  const isCompleted = goal?.status === 'COMPLETED' || currentMastery >= targetMastery;

  // Handle repeated progress submission
  const handleProgressSubmit = async () => {
    if (!goal?.id) {
      if (onRefreshDashboard) onRefreshDashboard();
      return;
    }
    try {
      setIsSubmitting(true);
      const updated = await submitGoalProgress(goal.id);
      setSyncFeedback(`Synced! Mastery: ${Math.round(updated.current_mastery * 100)}% (${updated.progress_percentage}% towards target)`);
      setTimeout(() => setSyncFeedback(null), 3500);
      if (onRefreshDashboard) onRefreshDashboard();
    } catch (err) {
      console.error('Failed to submit progress:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle goal creation or update
  const handleSaveGoal = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsSubmitting(true);
      const targetVal = targetMasteryPct / 100.0;
      await createOrUpdateGoal(selectedConceptId, targetVal);
      setIsEditing(false);
      setSyncFeedback('Goal updated successfully!');
      setTimeout(() => setSyncFeedback(null), 3000);
      if (onRefreshDashboard) onRefreshDashboard();
    } catch (err) {
      console.error('Failed to save goal:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col justify-between h-full relative">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
            <Target className="w-4 h-4 text-indigo-600" /> My Learning Goal
          </span>
          <div className="flex items-center gap-2">
            <span
              className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wide flex items-center gap-1 ${
                isCompleted
                  ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                  : 'bg-indigo-50 text-indigo-700 border border-indigo-200'
              }`}
            >
              {isCompleted ? <CheckCircle2 className="w-3 h-3" /> : null}
              {isCompleted ? 'COMPLETED' : 'ACTIVE'}
            </span>
            <button
              onClick={() => setIsEditing(true)}
              className="text-slate-400 hover:text-indigo-600 text-xs font-semibold p-1 hover:bg-slate-50 rounded-lg transition-colors"
              title="Set or update goal"
            >
              <Plus className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Goal Title */}
        <h4 className="font-heading text-base font-extrabold text-slate-800 mb-4">
          {goal?.title || 'Master Arrays & Strings'}
        </h4>

        {/* Metric Badges */}
        <div className="grid grid-cols-2 gap-2 mb-4 text-xs">
          <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
            <span className="text-[10px] text-slate-400 uppercase font-bold block mb-0.5">Current Mastery</span>
            <span className="text-sm font-extrabold text-slate-800">{currentMastery}%</span>
          </div>
          <div className="bg-indigo-50/60 p-2.5 rounded-xl border border-indigo-100">
            <span className="text-[10px] text-indigo-500 uppercase font-bold block mb-0.5">Target</span>
            <span className="text-sm font-extrabold text-indigo-700">{targetMastery}%</span>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="space-y-1.5 mb-3">
          <div className="flex justify-between items-center text-xs">
            <span className="font-bold text-slate-600">Goal Progress</span>
            <span className="font-extrabold text-indigo-600"><AnimatedNumber value={progressPct} />%</span>
          </div>
          <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-1000 ease-out ${
                isCompleted
                  ? 'bg-emerald-500'
                  : 'bg-gradient-to-r from-indigo-500 to-violet-600'
              }`}
              style={{ width: `${Math.min(100, Math.max(5, progressPct))}%` }}
            ></div>
          </div>
        </div>

        {/* Status text */}
        <p className="text-xs text-slate-500">
          {isCompleted ? (
            <span className="text-emerald-600 font-bold flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" /> Target achieved! Great job!
            </span>
          ) : (
            <span>
              <strong className="text-slate-700">{remainingPoints} percentage points</strong> remaining
            </span>
          )}
        </p>

        {syncFeedback && (
          <div className="mt-2 p-2 bg-emerald-50 border border-emerald-200 rounded-lg text-[11px] text-emerald-800 font-semibold animate-in fade-in duration-150">
            {syncFeedback}
          </div>
        )}
      </div>

      {/* Action Footer */}
      <div className="pt-3 border-t border-slate-100 mt-4 flex items-center justify-between gap-2">
        <button
          onClick={handleProgressSubmit}
          disabled={isSubmitting}
          className="flex-1 py-2 px-3 bg-slate-50 hover:bg-indigo-50 text-indigo-700 hover:text-indigo-800 border border-slate-200 hover:border-indigo-200 text-xs font-bold rounded-xl transition-all flex items-center justify-center gap-1.5 shadow-sm disabled:opacity-50"
          title="Submit repeated progress updates without duplicating records"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isSubmitting ? 'animate-spin' : ''}`} />
          {isSubmitting ? 'Syncing BKT...' : 'Submit Progress'}
        </button>
        <button
          onClick={() => setIsEditing(true)}
          className="py-2 px-3 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-xl transition-colors shadow-sm shadow-indigo-100"
        >
          Change Goal
        </button>
      </div>

      {/* Goal Edit / Create Modal */}
      {isEditing && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-sm w-full p-6 shadow-2xl border border-slate-100 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-xl bg-indigo-100 text-indigo-600 flex items-center justify-center">
                  <Sparkles className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="font-heading text-base font-bold text-slate-800">Set Learning Goal</h3>
                  <p className="text-xs text-slate-500">Pick a concept and target mastery</p>
                </div>
              </div>
              <button
                onClick={() => setIsEditing(false)}
                className="text-slate-400 hover:text-slate-600 text-sm font-bold w-7 h-7 flex items-center justify-center rounded-full hover:bg-slate-100"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleSaveGoal} className="space-y-4">
              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1.5">
                  Select Topic
                </label>
                <select
                  value={selectedConceptId}
                  onChange={(e) => setSelectedConceptId(Number(e.target.value))}
                  className="w-full p-2.5 border border-slate-200 rounded-xl text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
                >
                  {practiceableConcepts.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.title}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <div className="flex justify-between items-center mb-1.5">
                  <label className="text-xs font-bold text-slate-700">Target Mastery</label>
                  <span className="text-xs font-extrabold text-indigo-600">{targetMasteryPct}%</span>
                </div>
                <input
                  type="range"
                  min="50"
                  max="95"
                  step="5"
                  value={targetMasteryPct}
                  onChange={(e) => setTargetMasteryPct(Number(e.target.value))}
                  className="w-full accent-indigo-600 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-slate-400 font-semibold mt-1">
                  <span>50% (Basic)</span>
                  <span>80% (Proficient)</span>
                  <span>95% (Mastery)</span>
                </div>
              </div>

              <div className="pt-2 flex gap-2">
                <button
                  type="button"
                  onClick={() => setIsEditing(false)}
                  className="flex-1 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="flex-1 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-xl shadow-md transition-colors disabled:opacity-50"
                >
                  {isSubmitting ? 'Saving...' : 'Save Goal'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
