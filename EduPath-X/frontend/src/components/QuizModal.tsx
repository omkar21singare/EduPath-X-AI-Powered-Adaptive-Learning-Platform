import React, { useState } from 'react';
import type { Question, QuestionAttemptResult, LearningMaterial } from '../types';
import { submitQuestion } from '../services/api';
import { CheckCircle2, XCircle, BookOpen, Loader2 } from 'lucide-react';
import { AnimatedNumber } from './AnimatedNumber';

interface QuizModalProps {
  conceptTitle: string;
  material?: LearningMaterial;
  questions: Question[];
  onClose: () => void;
  onRefreshDashboard: () => void;
}

export const QuizModal: React.FC<QuizModalProps> = ({
  conceptTitle,
  material,
  questions,
  onClose,
  onRefreshDashboard
}) => {
  const [activeTab, setActiveTab] = useState<'study' | 'quiz'>('study');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [attemptResult, setAttemptResult] = useState<QuestionAttemptResult | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const currentQ = questions[currentIndex];

  const handleSubmit = async () => {
    if (!currentQ || !selectedOption || isSubmitting) return;

    setIsSubmitting(true);
    try {
      const result = await submitQuestion(currentQ.id, selectedOption, 15.0, 1);
      setAttemptResult(result);
      onRefreshDashboard();
    } catch (err) {
      console.error("Failed to submit attempt", err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNext = () => {
    setAttemptResult(null);
    setSelectedOption(null);
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
    } else {
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-slate-100 overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="p-5 bg-gradient-to-r from-indigo-600 to-violet-600 text-white flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">
              <span className="bg-white/20 text-white text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">
                Adaptive Learning Session
              </span>
              <span className="text-xs text-indigo-100 font-medium">• {conceptTitle}</span>
            </div>
            <h3 className="font-heading text-lg font-bold text-white mt-0.5">{conceptTitle} Practice & Mastery</h3>
          </div>

          <div className="flex items-center gap-2">
            <div className="flex bg-indigo-700/60 p-1 rounded-xl">
              <button
                onClick={() => setActiveTab('study')}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-colors ${activeTab === 'study' ? 'bg-white text-indigo-700' : 'text-indigo-100'}`}
              >
                Study Material
              </button>
              <button
                onClick={() => setActiveTab('quiz')}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-colors ${activeTab === 'quiz' ? 'bg-white text-indigo-700' : 'text-indigo-100'}`}
              >
                Quiz ({questions.length})
              </button>
            </div>

            <button onClick={onClose} className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center font-bold text-white">
              ✕
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="flex-1 p-6 overflow-y-auto">
          {activeTab === 'study' ? (
            <div className="space-y-4 text-xs text-slate-700">
              {material ? (
                <>
                  <div className="bg-indigo-50/70 p-4 rounded-2xl border border-indigo-100">
                    <h4 className="font-bold text-indigo-900 text-sm mb-2 flex items-center gap-2">
                      <BookOpen className="w-4 h-4 text-indigo-600" /> Learning Objectives
                    </h4>
                    <ul className="list-disc list-inside space-y-1 text-slate-700">
                      {material.learning_objectives.map((obj, i) => (
                        <li key={i}>{obj}</li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h4 className="font-bold text-slate-800 text-sm mb-1">Concept Explanation</h4>
                    <p className="leading-relaxed bg-slate-50 p-4 rounded-2xl border border-slate-100">
                      {material.explanation}
                    </p>
                  </div>

                  {material.code_example && (
                    <div>
                      <h4 className="font-bold text-slate-800 text-sm mb-1">Code Example</h4>
                      <pre className="bg-slate-900 text-slate-100 p-4 rounded-2xl font-mono text-[11px] overflow-x-auto">
                        {material.code_example}
                      </pre>
                    </div>
                  )}

                  {material.source && (
                    <div className="pt-3 border-t border-slate-100 text-[11px] text-slate-400 flex items-center justify-between">
                      <span>Source: <strong className="text-slate-600">{material.source.source_name}</strong></span>
                      <a href={material.source.official_url} target="_blank" rel="noreferrer" className="text-indigo-600 hover:underline">
                        View Verified Source ↗
                      </a>
                    </div>
                  )}
                </>
              ) : (
                <p className="text-slate-500">Loading verified source material...</p>
              )}
            </div>
          ) : (
            <div>
              {currentQ ? (
                <div className="space-y-4">
                  <div className="flex items-center justify-between text-xs text-slate-500">
                    <span className="font-bold text-indigo-600">Question {currentIndex + 1} of {questions.length}</span>
                    <span className="bg-slate-100 text-slate-600 font-semibold px-2.5 py-0.5 rounded-full">{currentQ.difficulty} • {currentQ.question_type}</span>
                  </div>

                  <h4 className="font-heading text-base font-bold text-slate-800">
                    {currentQ.question_text}
                  </h4>

                  <div className="space-y-2 mt-4">
                    {currentQ.options.map((opt, i) => (
                      <button
                        key={i}
                        onClick={() => !attemptResult && setSelectedOption(opt)}
                        disabled={!!attemptResult}
                        className={`w-full p-3.5 rounded-xl border text-left text-xs font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-1 ${
                          selectedOption === opt
                            ? 'bg-indigo-50 border-indigo-500 text-indigo-900 shadow-md ring-1 ring-indigo-500'
                            : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50 hover:border-slate-300 hover:-translate-y-0.5 hover:shadow-sm'
                        } ${!!attemptResult ? 'opacity-80 cursor-default hover:translate-y-0 hover:shadow-none' : 'cursor-pointer'}`}
                      >
                        {opt}
                      </button>
                    ))}
                  </div>

                  {/* Immediate Feedback Card after submit (PART 5 & 6) */}
                  {attemptResult && (
                    <div className={`p-4 rounded-2xl border ${attemptResult.is_correct ? 'bg-emerald-50 border-emerald-200' : 'bg-rose-50 border-rose-200'} space-y-3 animate-in fade-in duration-200`}>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          {attemptResult.is_correct ? (
                            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                          ) : (
                            <XCircle className="w-5 h-5 text-rose-600" />
                          )}
                          <span className={`font-bold text-sm ${attemptResult.is_correct ? 'text-emerald-900' : 'text-rose-900'}`}>
                            {attemptResult.is_correct ? 'Correct Answer! ✓' : 'Incorrect ✗'}
                          </span>
                        </div>
                        <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-white/80 border border-slate-200 text-slate-600">
                          BKT Update
                        </span>
                      </div>

                      <p className="text-xs text-slate-700 bg-white/70 p-2.5 rounded-xl border border-slate-100 animate-in slide-in-from-top-2 fade-in duration-300">
                        {attemptResult.explanation}
                      </p>

                      {/* BKT State Transition (PART 5 & 6) */}
                      <div className="bg-white p-3 rounded-xl border border-slate-100 grid grid-cols-3 gap-2 text-center text-xs">
                        <div>
                          <span className="text-[10px] text-slate-400 block uppercase font-bold">Prior P(K)</span>
                          <span className="font-extrabold text-slate-700">{(attemptResult.bkt_prior * 100).toFixed(1)}%</span>
                        </div>
                        <div>
                          <span className="text-[10px] text-slate-400 block uppercase font-bold">Posterior P(K)</span>
                          <span className={`font-extrabold ${attemptResult.is_correct ? 'text-emerald-700' : 'text-rose-700'}`}>
                            <AnimatedNumber value={attemptResult.bkt_posterior * 100} fractionDigits={1} />%
                          </span>
                        </div>
                        <div>
                          <span className="text-[10px] text-slate-400 block uppercase font-bold">Delta Change</span>
                          <span className={`font-extrabold ${attemptResult.mastery_change >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                            {attemptResult.mastery_change >= 0 ? '+' : ''}{(attemptResult.mastery_change * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>

                      {/* Next Recommendation */}
                      {attemptResult.next_recommendation && (
                        <div className="pt-2 border-t border-slate-200/60 text-xs">
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Next Action Recommendation</span>
                            <span className="text-[10px] font-bold text-indigo-700 bg-indigo-50 border border-indigo-200 px-2 py-0.5 rounded">
                              {attemptResult.next_recommendation.target_difficulty || 'Medium'} Difficulty
                            </span>
                          </div>
                          <div className="font-bold text-slate-800">
                            {attemptResult.next_recommendation.concept_title} — {attemptResult.next_recommendation.action_type}
                          </div>
                          {attemptResult.next_recommendation.reason_text && (
                            <p className="text-[11px] text-slate-500 italic mt-0.5">
                              "{attemptResult.next_recommendation.reason_text}"
                            </p>
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-12 space-y-2">
                  <p className="text-slate-700 font-semibold text-sm">No practice questions are currently available for your recommended topic.</p>
                  <p className="text-slate-400 text-xs">Please explore the verified study material in the Study tab or choose another topic.</p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="p-4 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
          {activeTab === 'study' ? (
            <button
              onClick={() => setActiveTab('quiz')}
              className="ml-auto px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow-md transition-colors"
            >
              Start Practice Questions →
            </button>
          ) : (
            <>
              {questions.length === 0 ? (
                <button
                  onClick={onClose}
                  className="ml-auto px-5 py-2.5 bg-slate-600 hover:bg-slate-700 text-white font-bold text-xs rounded-xl shadow-md transition-colors"
                >
                  Close Session
                </button>
              ) : !attemptResult ? (
                <button
                  onClick={handleSubmit}
                  disabled={!selectedOption || isSubmitting}
                  className="ml-auto flex items-center gap-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow-md transition-all hover:-translate-y-0.5 disabled:opacity-50 disabled:hover:translate-y-0 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >
                  {isSubmitting && <Loader2 className="w-4 h-4 animate-spin" />}
                  {isSubmitting ? 'Evaluating BKT...' : 'Submit Answer'}
                </button>
              ) : (
                <button
                  onClick={handleNext}
                  className="ml-auto px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow-md transition-colors"
                >
                  {currentIndex < questions.length - 1 ? 'Next Question →' : 'Complete Session ✓'}
                </button>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};
