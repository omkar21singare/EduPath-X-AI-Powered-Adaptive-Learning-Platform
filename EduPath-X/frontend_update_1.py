import os
import re

# 1. Update App.tsx Header
app_path = "frontend/src/App.tsx"
with open(app_path, "r") as f:
    app_code = f.read()

# Replace Header
old_header = '''        <header className="px-8 py-5 bg-white border-b border-slate-100 flex items-center justify-between gap-4 sticky top-12 z-20 shadow-xs">
          <div>
            <h2 className="font-heading text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
              Welcome back, {dashboardData?.user_name || 'Aarav'}! 👋
            </h2>
            <p className="text-xs text-slate-500 font-medium mt-0.5">
              Your personalized adaptive learning journey continues...
            </p>
          </div>'''

new_header = '''        <header className="px-8 py-6 bg-white border-b border-slate-100 flex items-center justify-between gap-4 sticky top-12 z-20 shadow-xs">
          <div>
            <h1 className="font-heading text-2xl font-extrabold text-indigo-900 tracking-tight flex items-center gap-2">
              EduPath-X
            </h1>
            <p className="text-sm text-indigo-600 font-semibold mt-0.5">
              AI-Powered Adaptive Learning
            </p>
            <div className="flex items-center gap-2 mt-2">
              <span className="flex h-2.5 w-2.5 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
              <span className="text-xs font-medium text-slate-600">Status: Live backend connected</span>
            </div>
          </div>

          <div className="text-right">
            {isLoading ? (
              <p className="text-sm text-slate-500 font-medium italic">Waiting for learner data...</p>
            ) : (
              <>
                <h2 className="font-heading text-lg font-bold text-slate-800">
                  Welcome, {dashboardData?.user_name || 'Student'}
                </h2>
                <p className="text-xs text-slate-500 font-medium mt-0.5">
                  Session Active • {dashboardData?.class_name || 'Course'}
                </p>
              </>
            )}
          </div>'''

app_code = app_code.replace(old_header, new_header)

# Import new components
imports_to_add = '''import { AdaptiveVisualizer } from './components/AdaptiveVisualizer';
import { BKTTrajectory } from './components/BKTTrajectory';
'''
app_code = app_code.replace("import { ObservabilityPanel } from './components/ObservabilityPanel';", 
                            "import { ObservabilityPanel } from './components/ObservabilityPanel';\n" + imports_to_add)

# Inject BKT Trajectory and Adaptive Visualizer
injection_point = '''              <ObservabilityPanel 
                dashboardData={dashboardData} 
                recentActivity={dashboardData.recent_activity} 
              />'''

new_injection = '''              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
                <AdaptiveVisualizer recommendations={dashboardData.recommendations} />
                <BKTTrajectory recentActivity={dashboardData.recent_activity} />
              </div>

              <ObservabilityPanel 
                dashboardData={dashboardData} 
                recentActivity={dashboardData.recent_activity} 
              />
'''
app_code = app_code.replace(injection_point, new_injection)

with open(app_path, "w") as f:
    f.write(app_code)

# 2. Update KnowledgeMap.tsx
map_path = "frontend/src/components/KnowledgeMap.tsx"
with open(map_path, "r") as f:
    map_code = f.read()

# Make it more prominent and map backend logic
new_map_code = '''import React from 'react';
import type { ConceptNode } from '../types';
import { BookOpen, CheckCircle, Lock, TrendingUp, AlertTriangle } from 'lucide-react';

interface KnowledgeMapProps {
  nodes: ConceptNode[];
  onSelectConcept: (concept: ConceptNode) => void;
}

export function KnowledgeMap({ nodes, onSelectConcept }: KnowledgeMapProps) {
  const getStatusDetails = (mastery: number) => {
    if (mastery < 50) return { label: 'REVISION', color: 'bg-rose-100 text-rose-700 border-rose-200', icon: <AlertTriangle className="w-4 h-4" /> };
    if (mastery < 80) return { label: 'PRACTICE', color: 'bg-amber-100 text-amber-700 border-amber-200', icon: <TrendingUp className="w-4 h-4" /> };
    if (mastery <= 90) return { label: 'CHALLENGE', color: 'bg-indigo-100 text-indigo-700 border-indigo-200', icon: <BookOpen className="w-4 h-4" /> };
    return { label: 'ADVANCE', color: 'bg-emerald-100 text-emerald-700 border-emerald-200', icon: <CheckCircle className="w-4 h-4" /> };
  };

  const CORE_CONCEPTS = ['ARRAYS', 'LINKED_LIST', 'STACKS', 'TREES', 'GRAPHS'];

  // Filter out any concepts not physically present in backend seeds
  const visibleNodes = nodes.filter(n => CORE_CONCEPTS.includes(n.code));

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 h-full">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-bold text-slate-800">Concept Mastery Map</h3>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {visibleNodes.map((node) => {
          const { label, color, icon } = getStatusDetails(node.mastery_percentage || 0);
          
          return (
            <button
              key={node.id}
              onClick={() => node.is_unlocked && onSelectConcept(node)}
              className={p-4 rounded-xl border-2 text-left transition-all }
            >
              <div className="flex items-center justify-between mb-3">
                <div className={p-2 rounded-lg }>
                  {node.is_unlocked ? icon : <Lock className="w-4 h-4 text-slate-400" />}
                </div>
                <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">{node.code}</div>
              </div>
              
              <h4 className="font-bold text-slate-800 mb-1">{node.title}</h4>
              
              <div className="mt-3">
                <div className="flex justify-between text-xs mb-1">
                  <span className="font-semibold text-slate-600">Mastery</span>
                  <span className="font-bold text-indigo-600">{Math.round(node.mastery_percentage || 0)}%</span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-1.5">
                  <div 
                    className="bg-indigo-600 h-1.5 rounded-full" 
                    style={{ width: ${Math.max(5, node.mastery_percentage || 0)}% }}
                  ></div>
                </div>
              </div>

              <div className="mt-4 inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider bg-white border border-slate-200 text-slate-600">
                Action: {label}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
'''
with open(map_path, "w") as f:
    f.write(new_map_code)

print("Updated App.tsx and KnowledgeMap.tsx")
