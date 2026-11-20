import os

app_path = "frontend/src/App.tsx"
with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add imports for the new pages
imports = '''import { MyLearning } from './components/MyLearning';
import { PracticePage } from './components/PracticePage';
import { PerformancePage } from './components/PerformancePage';
import { ProgressReportsPage } from './components/ProgressReportsPage';
import { AIAssistantPage } from './components/AIAssistantPage';
import { SettingsPage } from './components/SettingsPage';
'''
# Insert after BKTTrajectory import
content = content.replace("import { BKTTrajectory } from './components/BKTTrajectory';", f"import {{ BKTTrajectory }} from './components/BKTTrajectory';\n{imports}")

# Rewrite renderMainContent
render_logic = '''
  const renderMainContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <>
            <KPICards stats={dashboardData.kpis} recommendations={dashboardData.recommendations} recentActivity={dashboardData.recent_activity} />
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              <div className="lg:col-span-7">
                <KnowledgeMap nodes={dashboardData.knowledge_map} onSelectConcept={handleSelectConcept} />
              </div>
              <div className="lg:col-span-5">
                <RecommendationsCard recommendations={dashboardData.recommendations} onStartActivity={handleStartRecommendation} />
              </div>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              <div className="lg:col-span-7">
                <PerformanceRadar performance={dashboardData.performance_overview} />
              </div>
              <div className="lg:col-span-5">
                <RecentActivity activities={dashboardData.recent_activity} />
              </div>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              <div className="lg:col-span-8">
                <AIAssistantWidget onOpenAssistantTab={() => setActiveTab('assistant')} />
              </div>
              <div className="lg:col-span-4">
                <GoalWidget goal={dashboardData.goal} />
              </div>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
              <AdaptiveVisualizer recommendations={dashboardData.recommendations} />
              <BKTTrajectory recentActivity={dashboardData.recent_activity} />
            </div>
            <ObservabilityPanel dashboardData={dashboardData} recentActivity={dashboardData.recent_activity} />
          </>
        );
      case 'mylearning':
        return <MyLearning dashboardData={dashboardData} handleSelectConcept={handleSelectConcept} handleStartRecommendation={handleStartRecommendation} />;
      case 'knowledgemap':
        return <KnowledgeMap nodes={dashboardData.knowledge_map} onSelectConcept={handleSelectConcept} />;
      case 'recommendations':
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-slate-800">Recommendations</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <RecommendationsCard recommendations={dashboardData.recommendations} onStartActivity={handleStartRecommendation} />
              <AdaptiveVisualizer recommendations={dashboardData.recommendations} />
            </div>
          </div>
        );
      case 'practice':
        return <PracticePage dashboardData={dashboardData} onSelectConcept={handleSelectConcept} onStartRecommendation={handleStartRecommendation} />;
      case 'performance':
        return <PerformancePage dashboardData={dashboardData} />;
      case 'progress':
        return <ProgressReportsPage dashboardData={dashboardData} />;
      case 'assistant':
        return <AIAssistantPage />;
      case 'guided_demo':
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-slate-800">Guided Demo</h2>
            <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 flex flex-col items-center justify-center text-center space-y-4">
              <p className="text-sm text-slate-500">The Guided Demo illustrates the Adaptive pipeline.</p>
              <button onClick={() => setIsOpenGuidedDemo(true)} className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl">
                Open Guided Demo
              </button>
            </div>
          </div>
        );
      case 'evaluation':
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-slate-800">Adaptive vs Fixed Evaluation</h2>
            <ObservabilityPanel dashboardData={dashboardData} recentActivity={dashboardData.recent_activity} />
          </div>
        );
      case 'settings':
        return <SettingsPage />;
      default:
        return <div className="text-center text-slate-500">Page not found</div>;
    }
  };
'''

# Find the main tag
main_start = content.find("<main className=\"p-8 space-y-6 flex-1\">")
main_end = content.find("</main>") + len("</main>")

new_main = f'''{render_logic}
        <main className="p-8 space-y-6 flex-1">
          {{isLoading && !dashboardData ? (
            <div className="p-12 text-center text-slate-500 font-medium">
              Loading EduPath-X Adaptive Learning Engine...
            </div>
          ) : dashboardData ? (
            renderMainContent()
          ) : (
            <div className="p-12 text-center text-slate-500 font-medium">
              No data available.
            </div>
          )}}
        </main>'''

content = content[:main_start] + new_main + content[main_end:]

with open(app_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated App.tsx")
