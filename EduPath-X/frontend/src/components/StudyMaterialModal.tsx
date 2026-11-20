import { useState } from 'react';
import { 
  X, 
  BookOpen, 
  CheckCircle, 
  AlertCircle, 
  ChevronRight, 
  ChevronLeft, 
  ExternalLink, 
  HelpCircle, 
  Code2, 
  Target, 
  TrendingUp, 
  Sparkles,
  Play
} from 'lucide-react';
import type { ConceptNode } from '../types';
import { getConceptContent } from '../data/learningContent';

interface StudyMaterialModalProps {
  concept: ConceptNode;
  activeGoal?: any;
  onClose: () => void;
  onStartPractice?: (concept: ConceptNode) => void;
}

export function StudyMaterialModal({ 
  concept, 
  activeGoal, 
  onClose, 
  onStartPractice 
}: StudyMaterialModalProps) {
  const content = getConceptContent(concept.code);

  const [activeModuleIndex, setActiveModuleIndex] = useState(0);
  const [activeLessonIndex, setActiveLessonIndex] = useState(0);
  
  // Quick Check state: { [lessonId]: { selectedIndex: number, isSubmitted: boolean } }
  const [quickCheckStates, setQuickCheckStates] = useState<Record<string, { selectedIndex: number | null; isSubmitted: boolean }>>({});

  const isGoalTopic = activeGoal && activeGoal.concept_id === concept.id;
  const currentModule = content?.modules[activeModuleIndex];
  const currentLesson = currentModule?.lessons[activeLessonIndex];

  const currentQcState = currentLesson?.quick_check 
    ? quickCheckStates[currentLesson.id] || { selectedIndex: null, isSubmitted: false }
    : null;

  const handleSelectOption = (lessonId: string, index: number) => {
    setQuickCheckStates(prev => ({
      ...prev,
      [lessonId]: { ...(prev[lessonId] || {}), selectedIndex: index, isSubmitted: false }
    }));
  };

  const handleSubmitQuickCheck = (lessonId: string) => {
    setQuickCheckStates(prev => ({
      ...prev,
      [lessonId]: { ...(prev[lessonId] || { selectedIndex: null }), isSubmitted: true }
    }));
  };

  const handleNextLesson = () => {
    if (!content) return;
    if (currentModule && activeLessonIndex < currentModule.lessons.length - 1) {
      setActiveLessonIndex(prev => prev + 1);
    } else if (activeModuleIndex < content.modules.length - 1) {
      setActiveModuleIndex(prev => prev + 1);
      setActiveLessonIndex(0);
    }
  };

  const handlePrevLesson = () => {
    if (!content) return;
    if (activeLessonIndex > 0) {
      setActiveLessonIndex(prev => prev - 1);
    } else if (activeModuleIndex > 0) {
      setActiveModuleIndex(prev => prev - 1);
      const prevModule = content.modules[activeModuleIndex - 1];
      setActiveLessonIndex(prevModule.lessons.length - 1);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white w-full max-w-6xl h-[92vh] rounded-3xl shadow-2xl flex flex-col overflow-hidden border border-slate-100">
        
        {/* Top Header */}
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/70">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-indigo-600 text-white flex items-center justify-center shadow-sm">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-lg font-extrabold text-slate-800">{concept.title}</h2>
                <span className="text-[10px] font-black tracking-wider uppercase px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-700">
                  {concept.code}
                </span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-200 text-slate-700">
                  Verified Study Material
                </span>
              </div>
              <p className="text-xs text-slate-500 truncate max-w-xl">
                Structured pedagogical modules, code walkthroughs, Big-O analysis, and verified references
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* Live BKT Mastery Badge */}
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white border border-slate-200/80 shadow-xs">
              <span className="text-[10px] font-bold text-slate-400 uppercase">BKT Mastery:</span>
              <span className="text-xs font-black text-indigo-600">
                {Math.round(concept.mastery_percentage || 0)}%
              </span>
            </div>

            {/* Active Goal Badge */}
            {isGoalTopic && (
              <div className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-purple-50 border border-purple-200 text-purple-700 text-xs font-bold shadow-xs">
                <Target className="w-3.5 h-3.5 text-purple-600" />
                <span>Goal: {Math.round(activeGoal.target_mastery * 100)}%</span>
              </div>
            )}

            <button
              onClick={onClose}
              className="p-2 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content Body Layout */}
        <div className="flex-1 flex overflow-hidden">
          
          {/* Left Navigation Sidebar */}
          <div className="w-72 sm:w-80 border-r border-slate-100 bg-slate-50/50 flex flex-col justify-between overflow-y-auto p-4 shrink-0">
            <div className="space-y-4">
              <div>
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-2 px-1">
                  Learning Modules
                </span>
                
                {content ? (
                  <div className="space-y-3">
                    {content.modules.map((mod, modIdx) => (
                      <div key={mod.id} className="bg-white rounded-2xl border border-slate-200/70 p-2 shadow-2xs">
                        <div className="px-2 py-1 text-xs font-bold text-slate-700 flex items-center justify-between">
                          <span className="truncate">{mod.title}</span>
                          <span className="text-[10px] font-semibold text-slate-400">
                            {mod.lessons.length} {mod.lessons.length === 1 ? 'lesson' : 'lessons'}
                          </span>
                        </div>
                        <div className="mt-1 space-y-1">
                          {mod.lessons.map((lesson, lesIdx) => {
                            const isActive = activeModuleIndex === modIdx && activeLessonIndex === lesIdx;
                            return (
                              <button
                                key={lesson.id}
                                onClick={() => {
                                  setActiveModuleIndex(modIdx);
                                  setActiveLessonIndex(lesIdx);
                                }}
                                className={`w-full text-left px-2.5 py-1.5 rounded-xl text-xs font-medium transition-all flex items-center justify-between ${
                                  isActive
                                    ? 'bg-indigo-600 text-white font-bold shadow-xs'
                                    : 'text-slate-600 hover:bg-slate-100'
                                }`}
                              >
                                <span className="truncate pr-2">{lesson.title}</span>
                                {isActive && <ChevronRight className="w-3.5 h-3.5 shrink-0" />}
                              </button>
                            );
                          })}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="p-4 bg-white rounded-2xl border border-slate-200 text-xs text-slate-500">
                    Content is being loaded for {concept.title}...
                  </div>
                )}
              </div>
            </div>

            {/* Practice Availability Status Card */}
            <div className="mt-4 pt-4 border-t border-slate-200/80">
              <div className="bg-white p-3.5 rounded-2xl border border-slate-200/80 shadow-2xs">
                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                  Practice Pathway
                </span>
                
                {content?.has_practice ? (
                  concept.is_unlocked !== false ? (
                    <div>
                      <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-700 mb-2">
                        <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
                        <span>Live Practice Questions Ready</span>
                      </div>
                      <p className="text-[11px] text-slate-500 mb-3">
                        Reinforce these lessons with real backend questions and advance your BKT knowledge state.
                      </p>
                      {onStartPractice && (
                        <button
                          onClick={() => {
                            onClose();
                            onStartPractice(concept);
                          }}
                          className="w-full py-2 px-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold shadow-sm transition-colors flex items-center justify-center gap-1.5"
                        >
                          <Play className="w-3.5 h-3.5 fill-current" />
                          <span>Start Practice Session</span>
                        </button>
                      )}
                    </div>
                  ) : (
                    <div>
                      <div className="flex items-center gap-1.5 text-xs font-bold text-rose-700 mb-1">
                        <AlertCircle className="w-3.5 h-3.5 text-rose-600" />
                        <span>Prerequisite Required</span>
                      </div>
                      <p className="text-[11px] text-slate-500">
                        {concept.prerequisite_details && concept.prerequisite_details.length > 0
                          ? `Requires ${concept.prerequisite_details[0].required_mastery}% on ${concept.prerequisite_details[0].parent_title} (Current: ${concept.prerequisite_details[0].parent_mastery}%).`
                          : 'Complete prerequisite topics to unlock practice.'}
                      </p>
                    </div>
                  )
                ) : (
                  <div>
                    <div className="flex items-center gap-1.5 text-xs font-bold text-amber-700 mb-1">
                      <Sparkles className="w-3.5 h-3.5 text-amber-600" />
                      <span>Foundational Study Topic</span>
                    </div>
                    <p className="text-[11px] text-slate-500">
                      Practice questions for this topic are not currently available. Please focus on conceptual mastery.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right Main Lesson Pane */}
          <div className="flex-1 overflow-y-auto p-6 sm:p-8 space-y-6">
            {currentLesson ? (
              <>
                {/* Lesson Header & Learning Objectives */}
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-[11px] font-bold text-indigo-600 uppercase tracking-wider">
                      {currentModule?.title}
                    </span>
                    <span className="text-slate-300">•</span>
                    <span className="text-[11px] font-bold text-slate-400">
                      Lesson {activeLessonIndex + 1} of {currentModule?.lessons.length}
                    </span>
                  </div>
                  <h1 className="text-2xl font-black text-slate-900 tracking-tight mb-4">
                    {currentLesson.title}
                  </h1>

                  {/* Learning Objectives Checklist */}
                  {currentLesson.learning_objectives.length > 0 && (
                    <div className="p-4 rounded-2xl bg-indigo-50/50 border border-indigo-100 mb-6">
                      <h4 className="text-xs font-bold text-indigo-900 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                        <CheckCircle className="w-4 h-4 text-indigo-600" />
                        <span>Learning Objectives</span>
                      </h4>
                      <ul className="space-y-1.5">
                        {currentLesson.learning_objectives.map((obj, i) => (
                          <li key={i} className="text-xs text-indigo-950/80 flex items-start gap-2">
                            <span className="text-indigo-500 font-bold">•</span>
                            <span>{obj}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {/* Core Conceptual Explanation */}
                <div className="prose prose-slate max-w-none text-slate-700 leading-relaxed text-sm space-y-4">
                  {currentLesson.explanation.split('\n\n').map((paragraph, idx) => (
                    <p key={idx} className="whitespace-pre-line">
                      {paragraph}
                    </p>
                  ))}
                </div>

                {/* Code Example Box */}
                {currentLesson.code_example && (
                  <div className="rounded-2xl border border-slate-800 bg-slate-900 text-slate-100 overflow-hidden shadow-sm">
                    <div className="px-4 py-2 bg-slate-950/80 border-b border-slate-800 flex items-center justify-between text-xs text-slate-400">
                      <div className="flex items-center gap-2">
                        <Code2 className="w-4 h-4 text-indigo-400" />
                        <span className="font-mono font-bold uppercase">{currentLesson.code_example.language} Example</span>
                      </div>
                      <span className="text-[10px] text-slate-500">Verified Executable Logic</span>
                    </div>
                    <div className="p-4 overflow-x-auto font-mono text-xs leading-relaxed text-emerald-400/90 bg-slate-900">
                      <pre>{currentLesson.code_example.code}</pre>
                    </div>
                    <div className="px-4 py-3 bg-slate-950/60 border-t border-slate-800/80 text-xs text-slate-300">
                      <p><strong className="text-indigo-300">Code Analysis:</strong> {currentLesson.code_example.explanation}</p>
                      {currentLesson.code_example.output && (
                        <p className="mt-1 font-mono text-[11px] text-slate-400">
                          <strong className="text-slate-500">Output:</strong> {currentLesson.code_example.output}
                        </p>
                      )}
                    </div>
                  </div>
                )}

                {/* Complexity Analysis Card */}
                {currentLesson.complexity && (
                  <div className="p-4 rounded-2xl bg-amber-50/60 border border-amber-200/80">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <TrendingUp className="w-4 h-4 text-amber-700" />
                        <span className="text-xs font-bold uppercase tracking-wider text-amber-900">
                          Complexity Breakdown
                        </span>
                      </div>
                      <div className="flex items-center gap-2 text-xs font-extrabold">
                        <span className="px-2 py-0.5 rounded-md bg-amber-200/80 text-amber-900">
                          Time: {currentLesson.complexity.time}
                        </span>
                        <span className="px-2 py-0.5 rounded-md bg-amber-200/80 text-amber-900">
                          Space: {currentLesson.complexity.space}
                        </span>
                      </div>
                    </div>
                    <p className="text-xs text-amber-950/80 leading-relaxed">
                      <strong className="text-amber-900">Why this complexity?</strong> {currentLesson.complexity.rationale}
                    </p>
                  </div>
                )}

                {/* Common Mistakes & Pitfalls */}
                {currentLesson.common_mistakes.length > 0 && (
                  <div className="p-4 rounded-2xl bg-rose-50/50 border border-rose-100">
                    <h4 className="text-xs font-bold text-rose-900 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                      <AlertCircle className="w-4 h-4 text-rose-600" />
                      <span>Common Mistakes & Traps to Avoid</span>
                    </h4>
                    <ul className="space-y-1.5">
                      {currentLesson.common_mistakes.map((mistake, i) => (
                        <li key={i} className="text-xs text-rose-950/80 flex items-start gap-2">
                          <span className="text-rose-500 font-bold">✕</span>
                          <span>{mistake}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Key Takeaways */}
                {currentLesson.key_takeaways.length > 0 && (
                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80">
                    <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">
                      Key Takeaways
                    </h4>
                    <ul className="space-y-1.5">
                      {currentLesson.key_takeaways.map((takeaway, i) => (
                        <li key={i} className="text-xs text-slate-600 flex items-start gap-2">
                          <span className="text-indigo-600 font-bold">✓</span>
                          <span>{takeaway}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Interactive Quick Check Section */}
                {currentLesson.quick_check && currentQcState && (
                  <div className="p-5 rounded-2xl bg-white border-2 border-indigo-100 shadow-xs">
                    <div className="flex items-center gap-2 mb-3">
                      <HelpCircle className="w-4 h-4 text-indigo-600" />
                      <span className="text-xs font-bold uppercase tracking-wider text-indigo-900">
                        Concept Quick Check
                      </span>
                    </div>

                    <p className="text-sm font-bold text-slate-800 mb-3">
                      {currentLesson.quick_check.question}
                    </p>

                    <div className="space-y-2 mb-4">
                      {currentLesson.quick_check.options.map((opt, optIdx) => {
                        const isSelected = currentQcState.selectedIndex === optIdx;
                        const isCorrectOption = optIdx === currentLesson.quick_check?.correct_index;
                        const showResult = currentQcState.isSubmitted;

                        let optionStyle = 'border-slate-200 hover:border-indigo-300 bg-slate-50/50';
                        if (isSelected && !showResult) {
                          optionStyle = 'border-indigo-600 bg-indigo-50/50 font-bold text-indigo-900';
                        } else if (showResult) {
                          if (isCorrectOption) {
                            optionStyle = 'border-emerald-500 bg-emerald-50 text-emerald-900 font-bold';
                          } else if (isSelected && !isCorrectOption) {
                            optionStyle = 'border-rose-400 bg-rose-50 text-rose-900 font-bold';
                          }
                        }

                        return (
                          <button
                            key={optIdx}
                            onClick={() => handleSelectOption(currentLesson.id, optIdx)}
                            disabled={currentQcState.isSubmitted}
                            className={`w-full text-left p-3 rounded-xl border text-xs transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-1 hover:-translate-y-0.5 flex items-center justify-between ${optionStyle} ${currentQcState.isSubmitted ? 'hover:translate-y-0' : 'cursor-pointer hover:shadow-sm'}`}
                          >
                            <span>{opt}</span>
                            {showResult && isCorrectOption && (
                              <CheckCircle className="w-4 h-4 text-emerald-600 shrink-0" />
                            )}
                            {showResult && isSelected && !isCorrectOption && (
                              <X className="w-4 h-4 text-rose-600 shrink-0" />
                            )}
                          </button>
                        );
                      })}
                    </div>

                    {!currentQcState.isSubmitted ? (
                      <button
                        onClick={() => handleSubmitQuickCheck(currentLesson.id)}
                        disabled={currentQcState.selectedIndex === null}
                        className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white text-xs font-bold rounded-xl transition-all focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 hover:-translate-y-0.5 disabled:hover:translate-y-0"
                      >
                        Verify Answer
                      </button>
                    ) : (
                      <div className="p-3.5 rounded-xl bg-slate-100 text-xs text-slate-700 animate-in slide-in-from-top-2 fade-in duration-300">
                        <strong className="block mb-1 text-slate-900">Explanation:</strong>
                        {currentLesson.quick_check.explanation}
                      </div>
                    )}
                  </div>
                )}

                {/* Verified External References */}
                {currentLesson.external_references.length > 0 && (
                  <div className="pt-4 border-t border-slate-200/60">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-2">
                      Verified External Educational Resources
                    </span>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      {currentLesson.external_references.map((ref, idx) => (
                        <a
                          key={idx}
                          href={ref.url}
                          target="_blank"
                          rel="noreferrer"
                          className="p-3 rounded-xl border border-slate-200/80 hover:border-indigo-300 hover:bg-indigo-50/20 bg-white transition-all flex flex-col justify-between group"
                        >
                          <div>
                            <div className="flex items-center justify-between text-xs font-bold text-slate-800 mb-1">
                              <span>{ref.name}</span>
                              <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-indigo-600" />
                            </div>
                            <span className="text-[10px] font-semibold text-indigo-600 block mb-1">
                              {ref.source_type}
                            </span>
                            <p className="text-[11px] text-slate-500 leading-snug">
                              {ref.description}
                            </p>
                          </div>
                        </a>
                      ))}
                    </div>
                  </div>
                )}

                {/* Lesson Pagination Footer */}
                <div className="flex items-center justify-between pt-6 border-t border-slate-200">
                  <button
                    onClick={handlePrevLesson}
                    disabled={activeModuleIndex === 0 && activeLessonIndex === 0}
                    className="px-4 py-2 border border-slate-200 hover:bg-slate-50 disabled:opacity-40 text-slate-700 text-xs font-bold rounded-xl transition-colors flex items-center gap-1.5"
                  >
                    <ChevronLeft className="w-4 h-4" />
                    <span>Previous Lesson</span>
                  </button>

                  <div className="flex items-center gap-3">
                    {content?.has_practice && concept.is_unlocked !== false && onStartPractice && (
                      <button
                        onClick={() => {
                          onClose();
                          onStartPractice(concept);
                        }}
                        className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl transition-colors flex items-center gap-1.5 shadow-sm"
                      >
                        <Play className="w-3.5 h-3.5 fill-current" />
                        <span>Practice This Concept</span>
                      </button>
                    )}

                    <button
                      onClick={handleNextLesson}
                      className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-xl transition-colors flex items-center gap-1.5 shadow-sm"
                    >
                      <span>Next Lesson</span>
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <div className="text-center py-20 text-slate-400 text-sm">
                Select a lesson from the sidebar to begin studying.
              </div>
            )}
          </div>

        </div>

      </div>
    </div>
  );
}
