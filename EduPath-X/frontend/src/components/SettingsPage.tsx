import React, { useState, useEffect } from 'react';
import { 
  Settings, 
  User, 
  Brain, 
  Sliders, 
  Radio, 
  Save, 
  CheckCircle2, 
  RefreshCw, 
  Code2, 
  ShieldCheck, 
  Sparkles 
} from 'lucide-react';
import { getStoredLearnerId } from '../services/api';

export function SettingsPage() {
  const learnerId = getStoredLearnerId();
  const [userName, setUserName] = useState('Aarav Sharma');
  const [userRole, setUserRole] = useState('B.Tech CSE • Semester 5');
  const [targetMastery, setTargetMastery] = useState(0.85);
  const [autoAdvance, setAutoAdvance] = useState(true);
  const [wsEnabled, setWsEnabled] = useState(true);
  const [aiPedagogyLevel, setAiPedagogyLevel] = useState<'socratic' | 'direct' | 'hint-only'>('socratic');
  const [codeRunnerTimeout, setCodeRunnerTimeout] = useState(5);
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        const u = JSON.parse(storedUser);
        if (u.name) setUserName(u.name);
      } catch {
        // use default
      }
    }
    const savedConfig = localStorage.getItem('edupath_settings');
    if (savedConfig) {
      try {
        const c = JSON.parse(savedConfig);
        if (c.targetMastery !== undefined) setTargetMastery(c.targetMastery);
        if (c.autoAdvance !== undefined) setAutoAdvance(c.autoAdvance);
        if (c.wsEnabled !== undefined) setWsEnabled(c.wsEnabled);
        if (c.aiPedagogyLevel) setAiPedagogyLevel(c.aiPedagogyLevel);
        if (c.codeRunnerTimeout) setCodeRunnerTimeout(c.codeRunnerTimeout);
      } catch {
        // use defaults
      }
    }
  }, []);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    const config = {
      targetMastery,
      autoAdvance,
      wsEnabled,
      aiPedagogyLevel,
      codeRunnerTimeout,
    };
    localStorage.setItem('edupath_settings', JSON.stringify(config));
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 3000);
  };

  const handleResetDefaults = () => {
    setTargetMastery(0.85);
    setAutoAdvance(true);
    setWsEnabled(true);
    setAiPedagogyLevel('socratic');
    setCodeRunnerTimeout(5);
    localStorage.removeItem('edupath_settings');
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 3000);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto pb-12">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-black text-slate-800 tracking-tight flex items-center gap-2.5">
            <Settings className="w-6 h-6 text-indigo-600" /> Platform Settings
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            Configure adaptive cognitive thresholds, live WebSocket updates, AI pedagogical mode, and platform preferences.
          </p>
        </div>
        <button
          type="button"
          onClick={handleResetDefaults}
          className="flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-semibold text-slate-600 hover:text-slate-800 bg-slate-100 hover:bg-slate-200 rounded-lg transition"
        >
          <RefreshCw className="w-3.5 h-3.5" /> Reset Defaults
        </button>
      </div>

      {savedSuccess && (
        <div className="flex items-center gap-2 p-3.5 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-sm font-medium animate-fadeIn">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
          Settings saved successfully to active browser session!
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-6">
        {/* Profile Card */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
            <User className="w-5 h-5 text-indigo-600" />
            <h3 className="font-bold text-slate-800">Learner Identity & Profile</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">Full Name</label>
              <input
                type="text"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                className="w-full px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">Academic Context</label>
              <input
                type="text"
                value={userRole}
                onChange={(e) => setUserRole(e.target.value)}
                className="w-full px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">Active Learner ID</label>
              <div className="px-3.5 py-2 text-sm bg-slate-100 border border-slate-200 rounded-xl text-slate-700 font-mono">
                Learner #{learnerId}
              </div>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">Authentication Mode</label>
              <div className="flex items-center gap-2 px-3.5 py-2 text-sm bg-indigo-50 border border-indigo-100 rounded-xl text-indigo-700 font-medium">
                <ShieldCheck className="w-4 h-4 text-indigo-600" /> Dynamic Bearer JWT / Demo
              </div>
            </div>
          </div>
        </div>

        {/* Cognitive Engine (BKT) Settings */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
            <Brain className="w-5 h-5 text-indigo-600" />
            <h3 className="font-bold text-slate-800">BKT & Adaptive Engine Thresholds</h3>
          </div>
          <div className="space-y-4">
            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-xs font-semibold text-slate-600">
                  Concept Mastery Target Threshold: <span className="text-indigo-600 font-bold">{Math.round(targetMastery * 100)}%</span>
                </label>
                <span className="text-xs text-slate-400">Default: 85%</span>
              </div>
              <input
                type="range"
                min="0.60"
                max="0.95"
                step="0.05"
                value={targetMastery}
                onChange={(e) => setTargetMastery(parseFloat(e.target.value))}
                className="w-full accent-indigo-600 cursor-pointer"
              />
              <p className="text-xs text-slate-500 mt-1">
                When Bayesian Knowledge Tracing posterior probability $P(L_t)$ crosses this threshold, the concept is automatically marked as Mastered.
              </p>
            </div>

            <div className="flex items-center justify-between p-3.5 bg-slate-50 rounded-xl border border-slate-100">
              <div>
                <p className="text-sm font-semibold text-slate-800">Auto-Advance Concept on Mastery</p>
                <p className="text-xs text-slate-500">Automatically switch recommendation to next unblocked prerequisite topic.</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={autoAdvance}
                  onChange={(e) => setAutoAdvance(e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-slate-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
              </label>
            </div>
          </div>
        </div>

        {/* Real-Time WebSocket & Sandbox */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
            <Radio className="w-5 h-5 text-indigo-600" />
            <h3 className="font-bold text-slate-800">Real-Time Networking & Python Sandbox</h3>
          </div>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3.5 bg-slate-50 rounded-xl border border-slate-100">
              <div>
                <p className="text-sm font-semibold text-slate-800">Live WebSocket Push Stream</p>
                <p className="text-xs text-slate-500">Receive live zero-refresh updates for BKT score updates and recommendations.</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={wsEnabled}
                  onChange={(e) => setWsEnabled(e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-slate-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
              </label>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-xs font-semibold text-slate-600 flex items-center gap-1.5">
                  <Code2 className="w-4 h-4 text-slate-500" /> Code Execution Sandbox Timeout: <span className="text-indigo-600 font-bold">{codeRunnerTimeout} seconds</span>
                </label>
              </div>
              <input
                type="range"
                min="2"
                max="15"
                step="1"
                value={codeRunnerTimeout}
                onChange={(e) => setCodeRunnerTimeout(parseInt(e.target.value, 10))}
                className="w-full accent-indigo-600 cursor-pointer"
              />
              <p className="text-xs text-slate-500 mt-1">
                Hard execution limit for sandboxed user Python DSA solutions before raising a TimeoutException.
              </p>
            </div>
          </div>
        </div>

        {/* AI Pedagogical Style */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
            <Sparkles className="w-5 h-5 text-indigo-600" />
            <h3 className="font-bold text-slate-800">AI Assistant Pedagogical Style</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {[
              { id: 'socratic', title: 'Socratic Method', desc: 'Asks guiding questions to help you derive solutions independently.' },
              { id: 'direct', title: 'Direct Explanation', desc: 'Gives explicit conceptual explanations and direct code patterns.' },
              { id: 'hint-only', title: 'Minimalist Hints', desc: 'Provides concise hints without revealing full logic or test solutions.' },
            ].map((mode) => (
              <div
                key={mode.id}
                onClick={() => setAiPedagogyLevel(mode.id as any)}
                className={`p-4 rounded-xl border-2 cursor-pointer transition ${
                  aiPedagogyLevel === mode.id
                    ? 'border-indigo-600 bg-indigo-50/40 shadow-sm'
                    : 'border-slate-100 bg-slate-50 hover:border-slate-200'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <h4 className="text-sm font-bold text-slate-800">{mode.title}</h4>
                  <input
                    type="radio"
                    name="pedagogy"
                    checked={aiPedagogyLevel === mode.id}
                    onChange={() => setAiPedagogyLevel(mode.id as any)}
                    className="accent-indigo-600"
                  />
                </div>
                <p className="text-xs text-slate-500 leading-relaxed">{mode.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Save CTA */}
        <div className="flex items-center justify-end gap-3 pt-2">
          <button
            type="submit"
            className="flex items-center gap-2 px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl shadow-md shadow-indigo-200 transition"
          >
            <Save className="w-4 h-4" /> Save Settings
          </button>
        </div>
      </form>
    </div>
  );
}
