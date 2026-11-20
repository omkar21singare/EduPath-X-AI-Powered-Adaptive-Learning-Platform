import os

pages = {
    "MyLearning.tsx": '''import React from 'react';
import { KnowledgeMap } from './KnowledgeMap';
import { RecommendationsCard } from './RecommendationsCard';

export function MyLearning({ dashboardData, handleSelectConcept, handleStartRecommendation }: any) {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-slate-800">My Learning</h2>
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-7">
          <KnowledgeMap nodes={dashboardData.knowledge_map} onSelectConcept={handleSelectConcept} />
        </div>
        <div className="lg:col-span-5">
          <RecommendationsCard recommendations={dashboardData.recommendations} onStartActivity={handleStartRecommendation} />
        </div>
      </div>
    </div>
  );
}
''',
    "PracticePage.tsx": '''import React, { useState } from 'react';
import { QuizModal } from './QuizModal';
import { Target } from 'lucide-react';

export function PracticePage({ dashboardData, onSelectConcept, onStartRecommendation }: any) {
  const rec = dashboardData?.recommendations?.[0];

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
        <Target className="w-5 h-5 text-indigo-600" /> Practice Area
      </h2>
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 flex flex-col items-center justify-center text-center space-y-4">
        {rec ? (
          <>
            <div className="w-16 h-16 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center">
              <Target className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold text-slate-800">Recommended Practice: {rec.concept_title}</h3>
            <p className="text-sm text-slate-500 max-w-md">
              Based on your current learning state, we recommend {rec.action_type} for {rec.concept_title}.
            </p>
            <button
              onClick={() => onStartRecommendation(rec)}
              className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl"
            >
              Start Practice Session
            </button>
          </>
        ) : (
          <p className="text-slate-500">No active recommendations. Please study the material first.</p>
        )}
      </div>
    </div>
  );
}
''',
    "PerformancePage.tsx": '''import React from 'react';
import { PerformanceRadar } from './PerformanceRadar';
import { RecentActivity } from './RecentActivity';

export function PerformancePage({ dashboardData }: any) {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-slate-800">Performance</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PerformanceRadar performance={dashboardData.performance_overview} />
        <RecentActivity activities={dashboardData.recent_activity} />
      </div>
    </div>
  );
}
''',
    "ProgressReportsPage.tsx": '''import React from 'react';
import { BKTTrajectory } from './BKTTrajectory';
import { RecentActivity } from './RecentActivity';

export function ProgressReportsPage({ dashboardData }: any) {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-slate-800">Progress Reports</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <BKTTrajectory recentActivity={dashboardData.recent_activity} />
        <RecentActivity activities={dashboardData.recent_activity} />
      </div>
    </div>
  );
}
''',
    "AIAssistantPage.tsx": '''import React from 'react';
import { Bot, AlertTriangle } from 'lucide-react';

export function AIAssistantPage() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
        <Bot className="w-5 h-5 text-indigo-600" /> AI Assistant
      </h2>
      <div className="bg-amber-50 p-8 rounded-2xl shadow-sm border border-amber-200 flex flex-col items-center justify-center text-center space-y-4">
        <AlertTriangle className="w-12 h-12 text-amber-500" />
        <h3 className="text-lg font-bold text-amber-800">AI Assistant — Integration Pending</h3>
        <p className="text-sm text-amber-700 max-w-md">
          The conversational AI assistant integration is currently pending. 
          The backend API for chat capabilities is not yet fully linked to this UI.
        </p>
      </div>
    </div>
  );
}
''',
    "SettingsPage.tsx": '''import React from 'react';
import { Settings, Info } from 'lucide-react';

export function SettingsPage() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
        <Settings className="w-5 h-5 text-indigo-600" /> Settings
      </h2>
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 flex flex-col items-center justify-center text-center space-y-4">
        <Info className="w-12 h-12 text-slate-400" />
        <h3 className="text-lg font-bold text-slate-800">Settings — Coming Later</h3>
        <p className="text-sm text-slate-500 max-w-md">
          Platform settings are not currently available.
        </p>
      </div>
    </div>
  );
}
'''
}

for name, content in pages.items():
    with open(f"frontend/src/components/{name}", "w", encoding="utf-8") as f:
        f.write(content)

print("Pages created")
