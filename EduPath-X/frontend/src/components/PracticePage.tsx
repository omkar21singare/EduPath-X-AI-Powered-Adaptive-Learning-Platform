import type { Recommendation, DashboardResponse, ConceptNode } from '../types';
import { Target, ArrowDown, Sparkles, BookOpen, ChevronRight, Lock, Play } from 'lucide-react';

interface PracticePageProps {
  dashboardData: DashboardResponse | null;
  onSelectConcept: (concept: ConceptNode) => void;
  onOpenStudy: (concept: ConceptNode) => void;
  onStartRecommendation: (rec: Recommendation) => void;
}

export const PracticePage: React.FC<PracticePageProps> = ({
  dashboardData,
  onSelectConcept,
  onOpenStudy,
  onStartRecommendation
}) => {
  const rec = dashboardData?.recommendations?.[0];
  const goal = dashboardData?.goal;
  const nodes = dashboardData?.knowledge_map || [];
  const CORE_CONCEPTS = ['ARRAYS', 'LINKED_LIST', 'STACKS', 'TREES', 'GRAPHS'];
  const practiceTopics = nodes.filter(n => CORE_CONCEPTS.includes(n.code));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <Target className="w-5 h-5 text-indigo-600" /> Adaptive Practice Area
          </h2>
          <p className="text-xs text-slate-500">Deliberate practice dynamically driven by your Bayesian Knowledge Tracing state</p>
        </div>
        <span className="text-xs font-bold px-2.5 py-1 bg-indigo-50 text-indigo-700 border border-indigo-200 rounded-lg">
          Live BKT Adaptation
        </span>
      </div>

      {/* Clear Recommendation-to-Practice Transition Card (PART 9) */}
      <div className="bg-white p-6 sm:p-8 rounded-2xl shadow-sm border border-slate-100">
        {rec ? (
          <div className="max-w-2xl mx-auto space-y-6 text-center">
            {/* Stage 1: Recommendation Selected */}
            {/* Stage 1: Recommendation Selected (Technical Readout) */}
            <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 text-left shadow-lg text-slate-300 font-mono text-[11px] sm:text-xs">
              <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
                <span className="font-extrabold text-indigo-400 uppercase tracking-widest flex items-center gap-2">
                  <Sparkles className="w-4 h-4" /> BKT Policy Engine
                </span>
                <span className="font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                  v2.4_adaptive
                </span>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-slate-500">Target Concept:</span>
                  <span className="font-bold text-white text-sm bg-slate-800 px-2 py-1 rounded">{rec.concept_title} ({rec.concept_code})</span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-slate-500">Mastery P(K):</span>
                  <span className="font-bold text-indigo-300">{rec.current_mastery ?? rec.rationale?.mastery_level}%</span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-slate-500">Action Type:</span>
                  <span className="font-bold text-amber-400">{rec.action_type}</span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-slate-500">Prerequisites:</span>
                  <span className="font-bold text-emerald-400">{rec.prerequisites_met !== false ? 'SATISFIED' : 'PENDING'}</span>
                </div>

                {goal && (
                  <div className="flex justify-between items-center">
                    <span className="text-slate-500">Goal Alignment:</span>
                    <span className="font-bold text-violet-300">{goal.title} ({goal.progress_percentage}%)</span>
                  </div>
                )}
              </div>

              <div className="mt-4 pt-4 border-t border-slate-800">
                <span className="text-slate-500 block mb-1">Generated Rationale:</span>
                <p className="text-emerald-300/90 leading-relaxed italic border-l-2 border-emerald-500/30 pl-3">
                  "{rec.reason_text}"
                </p>
              </div>
            </div>

            {/* Transition Indicator */}
            <div className="flex flex-col items-center justify-center gap-1 text-slate-400">
              <ArrowDown className="w-5 h-5 text-indigo-600 animate-bounce" />
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                Question Target Selected via BKT Policy
              </span>
            </div>

            {/* Stage 2: Launch Action */}
            <div className="space-y-3">
              <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
                <button
                  onClick={() => onStartRecommendation(rec)}
                  className="w-full sm:w-auto px-8 py-3.5 bg-indigo-600 hover:bg-indigo-700 text-white font-extrabold text-sm rounded-xl shadow-lg shadow-indigo-200 transition-all flex items-center justify-center gap-2"
                >
                  <Play className="w-4 h-4 fill-current" />
                  <span>Launch {rec.concept_title} Practice Session</span>
                  <ChevronRight className="w-4 h-4" />
                </button>

                {/* Option to study instead */}
                <button
                  onClick={() => {
                    const matchNode = nodes.find(n => n.id === rec.concept_id) || {
                      id: rec.concept_id,
                      code: rec.concept_code,
                      title: rec.concept_title,
                      category: 'Data Structures',
                      mastery_percentage: rec.current_mastery || 50,
                      status: 'IN_PROGRESS',
                      is_unlocked: true,
                      prerequisites: []
                    };
                    onOpenStudy(matchNode);
                  }}
                  className="w-full sm:w-auto px-6 py-3.5 bg-white hover:bg-slate-50 text-indigo-700 border border-indigo-200 font-bold text-sm rounded-xl transition-all flex items-center justify-center gap-2 shadow-2xs"
                >
                  <BookOpen className="w-4 h-4" />
                  <span>Review Study Material First</span>
                </button>
              </div>

              <p className="text-[11px] text-slate-400">
                Every response updates Bayesian knowledge state $P(K)$ and re-calibrates subsequent recommendations.
              </p>
            </div>
          </div>
        ) : (
          <div className="text-center py-8 space-y-2">
            <p className="text-slate-600 font-semibold text-sm">No practice questions are currently available for your recommended topic.</p>
            <p className="text-slate-400 text-xs">Please explore verified study materials or choose an alternate topic below.</p>
          </div>
        )}
      </div>

      {/* Core Practice Topics Grid */}
      <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <h3 className="text-sm font-bold text-slate-800 mb-3 flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-indigo-600" />
          Curriculum Practice Topics
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
          {practiceTopics.map((topic) => {
            const isBlocked = topic.is_unlocked === false;
            return (
              <div
                key={topic.id}
                className={`p-3.5 rounded-xl border text-left transition-all flex flex-col justify-between ${
                  isBlocked
                    ? 'border-slate-200 bg-slate-50/60'
                    : 'border-slate-100 bg-slate-50 hover:bg-white hover:border-indigo-300 hover:shadow-xs'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-[10px] font-bold text-slate-400 uppercase">{topic.code}</span>
                    <span className="text-xs font-black text-indigo-600">{Math.round(topic.mastery_percentage || 0)}%</span>
                  </div>
                  <h4 className="font-bold text-slate-800 text-xs mb-2 truncate">
                    {topic.title}
                  </h4>
                  {isBlocked && (
                    <div className="text-[10px] text-rose-700 font-semibold flex items-center gap-1 mb-2">
                      <Lock className="w-3 h-3 text-rose-600" />
                      <span>Prerequisite Required</span>
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-1.5 pt-2 border-t border-slate-200/50">
                  <button
                    onClick={() => onOpenStudy(topic)}
                    className="flex-1 py-1 px-2 rounded-lg bg-white border border-slate-200 hover:bg-slate-100 text-slate-700 text-[10px] font-bold transition-colors text-center"
                  >
                    Study
                  </button>
                  <button
                    onClick={() => onSelectConcept(topic)}
                    disabled={isBlocked}
                    className="flex-1 py-1 px-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 disabled:opacity-40 disabled:cursor-not-allowed text-white text-[10px] font-bold transition-colors text-center flex items-center justify-center gap-0.5"
                  >
                    <span>Practice</span>
                    <ChevronRight className="w-3 h-3" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
