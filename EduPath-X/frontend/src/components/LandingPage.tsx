import React from 'react';
import { 
  Sparkles, 
  ArrowRight, 
  Brain, 
  Network, 
  Target, 
  ShieldCheck, 
  Activity, 
  Cpu, 
  Compass, 
  BookOpen, 
  Code2
} from 'lucide-react';
import { StructureFlowCollection } from '../effects/structure-flow/StructureFlowCollection';
import '../effects/structure-flow/styles.css';

interface LandingPageProps {
  onEnterPlatform: () => void;
  onOpenAuth: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({
  onEnterPlatform,
  onOpenAuth,
}) => {
  return (
    <div className="relative min-h-screen w-full bg-[#050508] text-white overflow-x-hidden font-sans select-none flex flex-col justify-between">
      {/* Three.js Structure Flow Background (Topology Field) */}
      <div className="absolute inset-0 z-0 pointer-events-none">
        <div className="shader-frame w-full h-full">
          <StructureFlowCollection
            variant="topology-field"
            hue={0}
            saturation={1.0}
            brightness={1.0}
          />
        </div>
      </div>

      {/* Atmospheric Top Gradient */}
      <div className="absolute top-0 inset-x-0 h-40 bg-gradient-to-b from-[#050508]/80 via-transparent to-transparent pointer-events-none z-10" />

      {/* Navigation Header */}
      <header className="relative z-20 max-w-7xl mx-auto w-full px-6 py-6 flex items-center justify-between">
        {/* Project Branding */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-violet-400 p-[1px] shadow-lg shadow-indigo-500/20 flex items-center justify-center">
            <div className="w-full h-full bg-[#0d0f1a] rounded-2xl flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-indigo-400 animate-pulse" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-heading text-xl font-black tracking-tight text-white">EduPath-X</span>
              <span className="px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 rounded-full">
                v2.0 Active
              </span>
            </div>
            <p className="text-[10px] font-medium tracking-widest uppercase text-slate-400">
              AI Adaptive Platform
            </p>
          </div>
        </div>

        {/* Header Action CTAs */}
        <div className="flex items-center gap-3">
          <button
            onClick={onOpenAuth}
            className="px-4 py-2 text-xs font-semibold text-slate-300 hover:text-white bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl backdrop-blur-md transition-all duration-200"
          >
            Sign In / Demo
          </button>
          <button
            onClick={onEnterPlatform}
            className="group flex items-center gap-2 px-5 py-2 text-xs font-bold text-white bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 rounded-xl shadow-lg shadow-indigo-600/30 hover:shadow-indigo-500/50 hover:scale-[1.02] active:scale-[0.98] transition-all duration-200"
          >
            <span>Launch Platform</span>
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
          </button>
        </div>
      </header>

      {/* Hero Body Content */}
      <main className="relative z-20 max-w-7xl mx-auto w-full px-6 py-12 lg:py-20 flex-1 flex flex-col justify-center">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* Left Column: Headlines & Callouts */}
          <div className="lg:col-span-7 space-y-6">
            
            {/* Pill Tag */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-950/60 border border-indigo-500/30 text-indigo-300 text-xs font-medium backdrop-blur-md shadow-sm">
              <Brain className="w-3.5 h-3.5 text-indigo-400" />
              <span>Bayesian Knowledge Tracing & Graph Mastery</span>
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
            </div>

            {/* Title */}
            <h1 className="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight leading-[1.05] text-white">
              Adaptive Mastery.<br />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-violet-300 to-purple-400">
                Cognitive Topology.
              </span>
            </h1>

            {/* Subtitle */}
            <p className="text-base sm:text-lg text-slate-300 max-w-xl font-normal leading-relaxed">
              EduPath-X models your real cognitive state across Data Structures & Algorithms using dynamic Bayesian parameters, real-time WebSocket mastery push, and sandboxed execution.
            </p>

            {/* Actions */}
            <div className="flex flex-wrap items-center gap-4 pt-2">
              <button
                onClick={onEnterPlatform}
                className="group flex items-center gap-3 px-7 py-3.5 text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-500 rounded-2xl shadow-xl shadow-indigo-600/40 hover:shadow-indigo-500/60 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200"
              >
                <span>Enter Workspace</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>

              <button
                onClick={onOpenAuth}
                className="flex items-center gap-2 px-6 py-3.5 text-sm font-semibold text-slate-200 hover:text-white bg-white/5 hover:bg-white/10 border border-white/15 rounded-2xl backdrop-blur-md transition-all duration-200"
              >
                <ShieldCheck className="w-4 h-4 text-indigo-400" />
                <span>Switch Learner / Demo</span>
              </button>
            </div>

            {/* Micro Metrics Highlights */}
            <div className="grid grid-cols-3 gap-4 pt-6 border-t border-white/10 max-w-lg">
              <div>
                <p className="text-2xl font-black text-white">120+</p>
                <p className="text-xs text-slate-400 mt-0.5">Topology Nodes</p>
              </div>
              <div>
                <p className="text-2xl font-black text-indigo-400">0ms</p>
                <p className="text-xs text-slate-400 mt-0.5">Live WebSocket</p>
              </div>
              <div>
                <p className="text-2xl font-black text-emerald-400">92.4%</p>
                <p className="text-xs text-slate-400 mt-0.5">Mastery Precision</p>
              </div>
            </div>
          </div>

          {/* Right Column: Floating Telemetry Cards over the 3D Sphere */}
          <div className="lg:col-span-5 relative flex flex-col gap-4">
            
            {/* Card 1: Live Knowledge Tracing Status */}
            <div className="p-5 rounded-2xl bg-[#0e111d]/75 border border-indigo-500/20 backdrop-blur-xl shadow-2xl shadow-black/80 space-y-3 transform lg:translate-x-2 hover:scale-[1.02] transition-all duration-300">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="p-2 rounded-xl bg-indigo-500/10 text-indigo-400">
                    <Activity className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-white">Bayesian Knowledge State</h4>
                    <p className="text-[11px] text-slate-400">Real-time Posterior Calculation</p>
                  </div>
                </div>
                <span className="flex items-center gap-1.5 px-2.5 py-1 text-[10px] font-semibold bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 rounded-full">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" /> Live Stream
                </span>
              </div>
              
              <div className="space-y-1.5">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Concept: Binary Search Trees</span>
                  <span className="text-indigo-300 font-mono font-semibold">P(L) = 0.88</span>
                </div>
                <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 rounded-full w-[88%]" />
                </div>
              </div>
            </div>

            {/* Card 2: DSA Code Sandbox Runner */}
            <div className="p-5 rounded-2xl bg-[#0e111d]/75 border border-white/10 backdrop-blur-xl shadow-2xl shadow-black/80 space-y-3 transform lg:-translate-x-4 hover:scale-[1.02] transition-all duration-300">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="p-2 rounded-xl bg-violet-500/10 text-violet-400">
                    <Code2 className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-white">Sandboxed Python AST Runner</h4>
                    <p className="text-[11px] text-slate-400">Safe multi-test validation</p>
                  </div>
                </div>
                <span className="text-[11px] font-mono text-slate-400">5.0s Timeout</span>
              </div>
              <p className="text-xs text-slate-300 font-mono bg-black/40 p-2.5 rounded-xl border border-white/5">
                <span className="text-indigo-400">def</span> <span className="text-yellow-300">max_depth</span>(root): ...
                <span className="block text-emerald-400 mt-1">✓ 10/10 Test cases verified</span>
              </p>
            </div>

            {/* Card 3: AI Socratic Pedagogical Engine */}
            <div className="p-5 rounded-2xl bg-[#0e111d]/75 border border-indigo-500/20 backdrop-blur-xl shadow-2xl shadow-black/80 flex items-center justify-between hover:scale-[1.02] transition-all duration-300">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-xl bg-indigo-500/10 text-indigo-400">
                  <Brain className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-white">AI Assistant Pedagogy</h4>
                  <p className="text-xs text-slate-400">Socratic mode • Real Gemini API</p>
                </div>
              </div>
              <button 
                onClick={onEnterPlatform}
                className="px-3 py-1.5 text-xs font-semibold text-indigo-300 hover:text-white bg-indigo-500/20 hover:bg-indigo-500/30 rounded-lg transition"
              >
                Inspect
              </button>
            </div>

          </div>

        </div>
      </main>

      {/* Footer System Telemetry */}
      <footer className="relative z-20 max-w-7xl mx-auto w-full px-6 py-6 flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-white/5 text-xs text-slate-500">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400" /> System Operational
          </span>
          <span>•</span>
          <span>Topology Field r128-r160</span>
          <span>•</span>
          <span>EduPath-X Adaptive Network</span>
        </div>
        <div className="flex items-center gap-6">
          <button onClick={onEnterPlatform} className="hover:text-slate-300 transition">
            Platform Dashboard
          </button>
          <button onClick={onOpenAuth} className="hover:text-slate-300 transition">
            Authentication
          </button>
        </div>
      </footer>
    </div>
  );
};
