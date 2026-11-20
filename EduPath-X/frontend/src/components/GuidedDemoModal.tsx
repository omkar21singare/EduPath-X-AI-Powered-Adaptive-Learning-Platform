import React, { useState } from 'react';
import { Sparkles, ArrowRight } from 'lucide-react';
import { simulateDays, runEvaluation } from '../services/api';

interface GuidedDemoModalProps {
  onClose: () => void;
  onRefreshDashboard: () => void;
}

export const GuidedDemoModal: React.FC<GuidedDemoModalProps> = ({ onClose, onRefreshDashboard }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [isProcessing, setIsProcessing] = useState(false);
  const [evalResults, setEvalResults] = useState<any>(null);

  const steps = [
    {
      step: 1,
      title: "1. Initial Learner State Inspection",
      description: "Learner 'Aarav Sharma' enters the platform. The system inspects baseline knowledge states: Arrays (91% Mastered), Trees (54% Weak), DFS (37% Weak).",
      actionLabel: "Proceed to Session Launch"
    },
    {
      step: 2,
      title: "2. Adaptive Learning Session Launch",
      description: "Student attempts Tree Traversal practice questions. The Bayesian Knowledge Tracing engine evaluates responses in real-time.",
      actionLabel: "Simulate Student Interaction"
    },
    {
      step: 3,
      title: "3. AI Misconception & Weakness Detection",
      description: "System identifies 3 consecutive incorrect attempts in Tree Traversal order. P(K_Trees) drops from 54% to 42%.",
      actionLabel: "Generate Dynamic Recommendation"
    },
    {
      step: 4,
      title: "4. Targeted Revision Recommendation",
      description: "Recommendation Engine overrides linear advancement and outputs: 'REVISE Tree Traversal Fundamentals'. Rationale: 42% accuracy across recent attempts.",
      actionLabel: "Complete Revision Material"
    },
    {
      step: 5,
      title: "5. Verified Educational Study & Practice",
      description: "Learner studies concise explanation backed by MIT OpenCourseWare 6.006 and completes 4 targeted practice problems.",
      actionLabel: "Execute BKT Knowledge Update"
    },
    {
      step: 6,
      title: "6. Knowledge Model Update & Graph Transition",
      description: "Correct responses boost Bayesian probability P(K_Trees) from 42% → 78%. Prerequisite for Graph Traversal (DFS) is now SATISFIED!",
      actionLabel: "Simulate 7-Day Fast-Forward"
    },
    {
      step: 7,
      title: "7. Long-Term Accelerated Timeline Simulation",
      description: "Fast-forward 7 days of simulated daily study. Dashboard KPI cards, streak counts, and concept states update naturally from accumulated data.",
      actionLabel: "Run Adaptive vs Fixed Evaluation"
    },
    {
      step: 8,
      title: "8. Scientific Research Comparison",
      description: "Empirical evaluation comparing Fixed Linear Curriculum vs EduPath-X Adaptive Engine across 50 simulation trials.",
      actionLabel: "Finish Guided Presentation"
    }
  ];

  const handleNextStep = async () => {
    if (currentStep === 6) {
      setIsProcessing(true);
      await simulateDays(7, "Balanced learner", 1);
      onRefreshDashboard();
      setIsProcessing(false);
      setCurrentStep(7);
    } else if (currentStep === 7) {
      setIsProcessing(true);
      const res = await runEvaluation(20, 30);
      setEvalResults(res);
      setIsProcessing(false);
      setCurrentStep(8);
    } else if (currentStep < steps.length) {
      setCurrentStep(prev => prev + 1);
    } else {
      onClose();
    }
  };

  const activeStepInfo = steps[currentStep - 1];

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-md z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl max-w-2xl w-full p-6 shadow-2xl border border-slate-100 animate-in fade-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-amber-500 to-orange-500 text-white flex items-center justify-center shadow-md shadow-amber-200">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-heading text-lg font-bold text-slate-800">Guided Presentation Demo</h3>
              <p className="text-xs text-slate-500">Step {currentStep} of {steps.length} — Interactive Live Product Flow</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 font-bold">✕</button>
        </div>

        {/* Progress bar */}
        <div className="w-full bg-slate-100 rounded-full h-1.5 my-4">
          <div
            className="bg-amber-500 h-1.5 rounded-full transition-all duration-300"
            style={{ width: `${(currentStep / steps.length) * 100}%` }}
          ></div>
        </div>

        {/* Step details */}
        <div className="py-4 space-y-4">
          <h4 className="font-heading text-base font-bold text-slate-900">{activeStepInfo.title}</h4>
          <p className="text-xs text-slate-600 leading-relaxed bg-slate-50 p-4 rounded-2xl border border-slate-100">
            {activeStepInfo.description}
          </p>

          {/* Special view for step 8 */}
          {currentStep === 8 && evalResults && (
            <div className="p-4 bg-indigo-50/70 rounded-2xl border border-indigo-100 space-y-3 text-xs">
              <span className="font-bold text-indigo-900 text-xs uppercase tracking-wider block">Empirical Experiment Results</span>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-white p-3 rounded-xl border border-slate-200">
                  <span className="text-[10px] text-slate-400 font-bold block uppercase">Fixed Baseline</span>
                  <span className="text-sm font-bold text-slate-700">{evalResults.policy_fixed.avg_questions_required} questions</span>
                  <p className="text-[10px] text-slate-500">{evalResults.policy_fixed.retention_rate_14day}% retention</p>
                </div>
                <div className="bg-indigo-600 text-white p-3 rounded-xl shadow-md">
                  <span className="text-[10px] text-indigo-200 font-bold block uppercase">EduPath-X Adaptive</span>
                  <span className="text-sm font-bold">{evalResults.policy_adaptive.avg_questions_required} questions</span>
                  <p className="text-[10px] text-indigo-100">{evalResults.policy_adaptive.retention_rate_14day}% retention</p>
                </div>
              </div>
              <p className="text-indigo-900 font-medium text-[11px] pt-1">{evalResults.conclusion}</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
          <button
            onClick={() => setCurrentStep(prev => Math.max(1, prev - 1))}
            disabled={currentStep === 1 || isProcessing}
            className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-xl disabled:opacity-40"
          >
            ← Previous Step
          </button>

          <button
            onClick={handleNextStep}
            disabled={isProcessing}
            className="px-6 py-2.5 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-white font-bold text-xs rounded-xl shadow-md transition-all flex items-center gap-1.5 disabled:opacity-50"
          >
            <span>{isProcessing ? 'Executing System Logic...' : activeStepInfo.actionLabel}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
