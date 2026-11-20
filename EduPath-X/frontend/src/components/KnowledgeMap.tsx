import { useState, useEffect, useRef } from 'react';
import type { ConceptNode } from '../types';
import { BookOpen, CheckCircle, Lock, TrendingUp, AlertTriangle, Target, ChevronRight, Sparkles, Play } from 'lucide-react';
import { AnimatedNumber } from './AnimatedNumber';

interface KnowledgeMapProps {
  nodes: ConceptNode[];
  onSelectConcept: (concept: ConceptNode) => void;
  onOpenStudy?: (concept: ConceptNode) => void;
  activeGoal?: any;
}

export function KnowledgeMap({ nodes, onSelectConcept, onOpenStudy, activeGoal }: KnowledgeMapProps) {
  const [selectedNode, setSelectedNode] = useState<ConceptNode | null>(null);
  
  // Track previous unlock states for animation
  const prevUnlockStates = useRef<Record<number, boolean>>({});
  const [justUnlocked, setJustUnlocked] = useState<Record<number, boolean>>({});

  useEffect(() => {
    const newlyUnlocked: Record<number, boolean> = {};
    nodes.forEach(node => {
      const wasLocked = prevUnlockStates.current[node.id] === false;
      const isNowUnlocked = node.is_unlocked !== false;
      if (wasLocked && isNowUnlocked) {
        newlyUnlocked[node.id] = true;
      }
      prevUnlockStates.current[node.id] = node.is_unlocked !== false;
    });
    
    if (Object.keys(newlyUnlocked).length > 0) {
      setJustUnlocked(newlyUnlocked);
      const timer = setTimeout(() => setJustUnlocked({}), 3000);
      return () => clearTimeout(timer);
    }
  }, [nodes]);

  const getStatusDetails = (mastery: number) => {
    if (mastery < 50) return { label: 'REVISION', difficulty: 'Easy', color: 'bg-rose-100 text-rose-700 border-rose-200', icon: <AlertTriangle className="w-4 h-4" /> };
    if (mastery < 80) return { label: 'PRACTICE', difficulty: 'Medium', color: 'bg-amber-100 text-amber-700 border-amber-200', icon: <TrendingUp className="w-4 h-4" /> };
    if (mastery <= 90) return { label: 'CHALLENGE', difficulty: 'Hard', color: 'bg-indigo-100 text-indigo-700 border-indigo-200', icon: <BookOpen className="w-4 h-4" /> };
    return { label: 'ADVANCE', difficulty: 'Advanced', color: 'bg-emerald-100 text-emerald-700 border-emerald-200', icon: <CheckCircle className="w-4 h-4" /> };
  };

  const CORE_CONCEPTS = ['ALG_THINK', 'ARRAYS', 'LINKED_LIST', 'STACKS', 'TREES', 'GRAPHS'];
  const visibleNodes = nodes.filter(n => CORE_CONCEPTS.includes(n.code));

  const activeInspectionNode = selectedNode || visibleNodes.find(n => n.code === 'ARRAYS') || visibleNodes[0];
  const nodeStatus = activeInspectionNode ? getStatusDetails(activeInspectionNode.mastery_percentage || 0) : null;
  const isGoalTopic = activeGoal && activeInspectionNode && activeGoal.concept_id === activeInspectionNode.id;

  // Prerequisite blocking check (PART B & P)
  const isPrereqBlocked = activeInspectionNode?.is_unlocked === false;
  const prereqFailures = activeInspectionNode?.prerequisite_details?.filter(p => !p.is_met) || [];
  const hasPracticeQuestions = (activeInspectionNode?.question_count ?? 0) > 0 || ['ARRAYS', 'LINKED_LIST', 'STACKS', 'TREES', 'GRAPHS'].includes(activeInspectionNode?.code || '');
  const isPracticeDisabled = isPrereqBlocked || !hasPracticeQuestions;

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 h-full flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-bold text-slate-800">Concept Mastery Map</h3>
            <p className="text-xs text-slate-500">Interactive curriculum graph with continuous Bayesian Knowledge Tracing</p>
          </div>
          <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-100">
            6 Core Curriculum Topics
          </span>
        </div>

        {/* Nodes Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 mb-6">
          {visibleNodes.map((node) => {
            const { label, color, icon } = getStatusDetails(node.mastery_percentage || 0);
            const isSelected = activeInspectionNode?.id === node.id;
            const isBlocked = node.is_unlocked === false;
            const hasQuestions = (node.question_count ?? 0) > 0 || ['ARRAYS', 'LINKED_LIST', 'STACKS', 'TREES', 'GRAPHS'].includes(node.code);

            const isJustUnlocked = !!justUnlocked[node.id];

            return (
              <button
                key={node.id}
                onClick={() => setSelectedNode(node)}
                className={`p-3.5 rounded-xl border-2 text-left transition-all duration-300 relative focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 ${
                  isJustUnlocked ? 'animate-in zoom-in spin-in-2 duration-700 shadow-xl ring-2 ring-emerald-400 z-10 ' : ''
                }${
                  isSelected
                    ? 'border-indigo-600 bg-indigo-50/40 shadow-md ring-1 ring-indigo-600'
                    : isBlocked
                    ? 'border-slate-200 bg-slate-50/60 cursor-not-allowed hover:bg-slate-100'
                    : 'border-slate-100 hover:border-indigo-300 bg-slate-50/70 hover:bg-white hover:-translate-y-1 hover:shadow-lg cursor-pointer'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className={`p-1.5 rounded-lg transition-colors duration-500 ${isBlocked ? 'bg-rose-100 text-rose-700' : isJustUnlocked ? 'bg-emerald-100 text-emerald-600' : color}`}>
                    {isBlocked ? <Lock className="w-3.5 h-3.5" /> : isJustUnlocked ? <Sparkles className="w-3.5 h-3.5 animate-pulse" /> : icon}
                  </div>
                  <div className="flex items-center gap-1">
                    {!hasQuestions && (
                      <span className="text-[9px] font-bold px-1.5 py-0.5 rounded bg-amber-100 text-amber-800">
                        Study Only
                      </span>
                    )}
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">{node.code}</span>
                  </div>
                </div>

                <h4 className="font-bold text-slate-800 text-xs mb-1 truncate">{node.title}</h4>

                <div className="mt-2">
                  <div className="flex justify-between text-[11px] mb-1">
                    <span className="font-semibold text-slate-500">Mastery</span>
                    <span className="font-extrabold text-indigo-600"><AnimatedNumber value={node.mastery_percentage || 0} />%</span>
                  </div>
                  <div className="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden">
                    <div
                      className="bg-indigo-600 h-1.5 rounded-full transition-all duration-1000 ease-out"
                      style={{ width: `${Math.max(5, node.mastery_percentage || 0)}%` }}
                    ></div>
                  </div>
                </div>

                <div className="mt-2 flex items-center justify-between text-[10px] font-bold uppercase tracking-wider text-slate-500">
                  <span>
                    {isBlocked ? 'LOCKED' : (node.mastery_percentage || 0) < 50 ? 'REVISION RECOMMENDED' : `Action: ${label}`}
                  </span>
                  {activeGoal && activeGoal.concept_id === node.id && (
                    <span className="text-indigo-600 flex items-center gap-0.5 font-bold">
                      <Target className="w-3 h-3" /> Goal
                    </span>
                  )}
                </div>
              </button>
            );
          })}
        </div>

        {/* Selected Concept Deep-Dive Inspection Card (PART B, C, D, P) */}
        {activeInspectionNode && nodeStatus && (
          <div className="p-4 bg-slate-50 border border-slate-200/80 rounded-2xl animate-in fade-in duration-150">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-indigo-600"></span>
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Concept Inspection</span>
                <span className="text-xs font-black text-slate-800">• {activeInspectionNode.title}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md ${
                  isPrereqBlocked 
                    ? 'bg-rose-100 text-rose-800 border border-rose-200' 
                    : (activeInspectionNode.mastery_percentage || 0) < 50
                    ? 'bg-amber-100 text-amber-800 border border-amber-200'
                    : 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                }`}>
                  {isPrereqBlocked 
                    ? 'LOCKED BY PREREQUISITE' 
                    : (activeInspectionNode.mastery_percentage || 0) < 50 
                    ? 'REVISION RECOMMENDED' 
                    : 'ACCESSIBLE ✓'}
                </span>
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs mb-3">
              <div className="bg-white p-2.5 rounded-xl border border-slate-100">
                <span className="text-[10px] text-slate-400 uppercase font-bold block mb-0.5">Current Mastery</span>
                <span className="text-sm font-extrabold text-indigo-700">{Math.round(activeInspectionNode.mastery_percentage || 0)}%</span>
              </div>

              <div className="bg-white p-2.5 rounded-xl border border-slate-100">
                <span className="text-[10px] text-slate-400 uppercase font-bold block mb-0.5">Study Availability</span>
                <span className="text-xs font-extrabold text-emerald-700 flex items-center gap-1">
                  <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
                  <span>Available</span>
                </span>
              </div>

              <div className="bg-white p-2.5 rounded-xl border border-slate-100">
                <span className="text-[10px] text-slate-400 uppercase font-bold block mb-0.5">Practice Availability</span>
                <span className="text-xs font-extrabold block truncate">
                  {!hasPracticeQuestions ? (
                    <span className="text-slate-500 font-semibold">No questions loaded</span>
                  ) : isPrereqBlocked ? (
                    <span className="text-rose-700">Locked by Prereq</span>
                  ) : (
                    <span className="text-emerald-700">Available ({activeInspectionNode.question_count || 8} Qs)</span>
                  )}
                </span>
              </div>

              <div className="bg-white p-2.5 rounded-xl border border-slate-100">
                <span className="text-[10px] text-slate-400 uppercase font-bold block mb-0.5">Goal Alignment</span>
                <span className="text-xs font-bold text-slate-800 block truncate">
                  {isGoalTopic ? `Target: ${Math.round(activeGoal.target_mastery * 100)}%` : 'General Track'}
                </span>
              </div>
            </div>

            {/* Prerequisite status explanation */}
            {isPrereqBlocked && prereqFailures.length > 0 && (
              <div className="p-3 mb-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-900">
                <div className="font-bold flex items-center gap-1.5 mb-1">
                  <Lock className="w-3.5 h-3.5 text-rose-600" />
                  <span>Prerequisite Requirement Not Met:</span>
                </div>
                {prereqFailures.map((pf, idx) => (
                  <p key={idx} className="text-[11px] text-rose-800">
                    • <strong>{pf.parent_title}</strong>: Required mastery is <strong>{pf.required_mastery}%</strong> (Your current mastery is <strong>{pf.parent_mastery}%</strong>).
                  </p>
                ))}
                <p className="text-[10px] text-rose-700 mt-1">
                  You can study the material below to prepare, or practice the prerequisite topic first.
                </p>
              </div>
            )}

            {/* Notice for Foundational concepts without practice (e.g. Algorithmic Thinking) */}
            {!hasPracticeQuestions && (
              <div className="p-3 mb-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-amber-600 shrink-0" />
                <span>
                  <strong>Foundational Curriculum Topic:</strong> Practice questions for this topic are not currently available. Please use the comprehensive Study Material.
                </span>
              </div>
            )}

            <div className="flex items-center justify-between pt-2 border-t border-slate-200/60">
              <span className="text-[11px] text-slate-500">
                Study Material is always available for all curriculum concepts.
              </span>
              
              <div className="flex items-center gap-2">
                {/* Study Material Button (Always Accessible) */}
                <button
                  onClick={() => onOpenStudy?.(activeInspectionNode)}
                  className="px-3.5 py-1.5 bg-white hover:bg-slate-100 text-indigo-700 border border-indigo-200 font-bold text-xs rounded-xl shadow-2xs transition-colors flex items-center gap-1.5"
                >
                  <BookOpen className="w-3.5 h-3.5" />
                  <span>Study Material</span>
                </button>

                {/* Practice Button (Only when questions exist and unlocked) */}
                {hasPracticeQuestions && (
                  <button
                    onClick={() => onSelectConcept(activeInspectionNode)}
                    disabled={isPracticeDisabled}
                    className="px-4 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow-sm transition-colors flex items-center gap-1 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Play className="w-3.5 h-3.5 fill-current" />
                    <span>Practice {activeInspectionNode.code}</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
