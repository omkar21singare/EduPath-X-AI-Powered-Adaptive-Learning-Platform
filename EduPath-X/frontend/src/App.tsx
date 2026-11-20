import { useEffect, useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { SimulationBar } from './components/SimulationBar';
import { DashboardSkeleton } from './components/DashboardSkeleton';
import { KPICards } from './components/KPICards';
import { KnowledgeMap } from './components/KnowledgeMap';
import { RecommendationsCard } from './components/RecommendationsCard';
import { PerformanceRadar } from './components/PerformanceRadar';
import { RecentActivity } from './components/RecentActivity';
import { AIAssistantWidget } from './components/AIAssistantWidget';
import { GoalWidget } from './components/GoalWidget';
import { QuizModal } from './components/QuizModal';
import { GuidedDemoModal } from './components/GuidedDemoModal';
import { EvaluationModal } from './components/EvaluationModal';
import { ObservabilityPanel } from './components/ObservabilityPanel';
import { AdaptiveVisualizer } from './components/AdaptiveVisualizer';
import { BKTTrajectory } from './components/BKTTrajectory';
import { MyLearning } from './components/MyLearning';
import { PracticePage } from './components/PracticePage';
import { PerformancePage } from './components/PerformancePage';
import { ProgressReportsPage } from './components/ProgressReportsPage';
import { AIAssistantPage } from './components/AIAssistantPage';
import { SettingsPage } from './components/SettingsPage';
import { RecommendationsPage } from './components/RecommendationsPage';
import { StudyMaterialModal } from './components/StudyMaterialModal';

import { 
  getDashboard, 
  getMaterial, 
  getQuestions, 
  simulateDays, 
  resetSimulation 
} from './services/api';
import type { DashboardResponse, ConceptNode, LearningMaterial, Question, Recommendation } from './types';
import { Calendar, Bell } from 'lucide-react';

export function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dashboardData, setDashboardData] = useState<DashboardResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Simulation state
  const [currentSimDay, setCurrentSimDay] = useState(1);
  const [selectedProfile, setSelectedProfile] = useState('Struggling with Trees');

  // Modals state
  const [selectedConcept, setSelectedConcept] = useState<ConceptNode | null>(null);
  const [material, setMaterial] = useState<LearningMaterial | undefined>(undefined);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [isOpenQuiz, setIsOpenQuiz] = useState(false);

  const [isOpenStudyModal, setIsOpenStudyModal] = useState(false);
  const [studyConcept, setStudyConcept] = useState<ConceptNode | null>(null);

  const [isOpenGuidedDemo, setIsOpenGuidedDemo] = useState(false);
  const [isOpenEvaluation, setIsOpenEvaluation] = useState(false);

  // Load Dashboard Data
  const loadDashboard = async () => {
    try {
      setIsLoading(true);
      const data = await getDashboard(1);
      setDashboardData(data);
    } catch (err) {
      console.error("Failed loading dashboard", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  // Handlers for Simulation
  const handleSimulateDays = async (days: number) => {
    try {
      setIsLoading(true);
      const res = await simulateDays(days, selectedProfile, 1);
      setCurrentSimDay(res.current_day);
      await loadDashboard();
    } catch (err) {
      console.error("Simulation error", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetSimulation = async () => {
    try {
      setIsLoading(true);
      await resetSimulation(1);
      setCurrentSimDay(1);
      await loadDashboard();
    } catch (err) {
      console.error("Reset error", err);
    } finally {
      setIsLoading(false);
    }
  };

  // Launch Learning Activity / Quiz
  const handleSelectConcept = async (conceptNode: ConceptNode) => {
    try {
      setSelectedConcept(conceptNode);
      const [matData, qData] = await Promise.all([
        getMaterial(conceptNode.id).catch(() => undefined),
        getQuestions(conceptNode.id).catch(() => [])
      ]);
      setMaterial(matData);
      setQuestions(qData);
      setIsOpenQuiz(true);
    } catch (err) {
      console.error(err);
    }
  };

  const handleStartRecommendation = async (rec: Recommendation) => {
    const conceptNode: ConceptNode = {
      id: rec.concept_id,
      code: rec.concept_code,
      title: rec.concept_title,
      category: 'Data Structures',
      mastery_percentage: rec.rationale.mastery_level || 50,
      status: 'IN_PROGRESS',
      is_unlocked: true,
      prerequisites: []
    };
    await handleSelectConcept(conceptNode);
  };

  const handleOpenStudy = (conceptNode: ConceptNode) => {
    setStudyConcept(conceptNode);
    setIsOpenStudyModal(true);
  };

  const renderMainContent = (data: DashboardResponse) => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <>
            <KPICards stats={data.kpis} recommendations={data.recommendations} recentActivity={data.recent_activity} />
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              <div className="lg:col-span-7">
                <KnowledgeMap 
                  nodes={data.knowledge_map} 
                  onSelectConcept={handleSelectConcept} 
                  onOpenStudy={handleOpenStudy}
                />
              </div>
              <div className="lg:col-span-5">
                <RecommendationsCard recommendations={data.recommendations} onStartActivity={handleStartRecommendation} />
              </div>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              <div className="lg:col-span-7">
                <PerformanceRadar performance={data.performance_overview} />
              </div>
              <div className="lg:col-span-5">
                <RecentActivity activities={data.recent_activity} />
              </div>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              <div className="lg:col-span-8">
                <AIAssistantWidget onOpenAssistantTab={() => setActiveTab('assistant')} />
              </div>
              <div className="lg:col-span-4">
                <GoalWidget
                  goal={data.goal}
                  concepts={data.knowledge_map}
                  onRefreshDashboard={loadDashboard}
                />
              </div>
            </div>
            {/* Research & Telemetry Zone */}
            <div className="mt-12 p-6 sm:p-8 bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl">
              <div className="mb-6 flex items-center gap-3 border-b border-slate-800 pb-4">
                <span className="bg-rose-500/20 text-rose-400 font-bold px-3 py-1 rounded-full text-[10px] uppercase tracking-widest border border-rose-500/30">
                  Live Adaptive Telemetry
                </span>
                <span className="text-slate-400 text-xs hidden sm:inline">Research & Diagnostic Dashboard</span>
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <AdaptiveVisualizer recommendations={data.recommendations} />
                <BKTTrajectory recentActivity={data.recent_activity} />
              </div>
              <ObservabilityPanel dashboardData={dashboardData} recentActivity={data.recent_activity} />
            </div>
          </>
        );
      case 'mylearning':
        return <MyLearning dashboardData={dashboardData} handleSelectConcept={handleSelectConcept} handleStartRecommendation={handleStartRecommendation} handleOpenStudy={handleOpenStudy} />;
      case 'knowledgemap':
        return (
          <KnowledgeMap
            nodes={data.knowledge_map}
            onSelectConcept={handleSelectConcept}
            onOpenStudy={handleOpenStudy}
            activeGoal={data.goal}
          />
        );
      case 'recommendations':
        return (
          <RecommendationsPage
            dashboardData={dashboardData}
            onStartRecommendation={handleStartRecommendation}
          />
        );
      case 'practice':
        return (
          <PracticePage 
            dashboardData={dashboardData} 
            onSelectConcept={handleSelectConcept} 
            onOpenStudy={handleOpenStudy}
            onStartRecommendation={handleStartRecommendation} 
          />
        );
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
            <ObservabilityPanel dashboardData={dashboardData} recentActivity={data.recent_activity} />
          </div>
        );
      case 'settings':
        return <SettingsPage />;
      default:
        return <div className="text-center text-slate-500">Page not found</div>;
    }
  };

  return (
    <div className="min-h-screen bg-[#f6f8fc] flex text-slate-800 font-sans antialiased">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        userName={dashboardData?.user_name || 'Aarav Sharma'}
        className={dashboardData?.class_name || 'B.Tech CSE'}
        semester={dashboardData?.semester || 'Semester 4'}
      />

      {/* Main Workspace */}
      <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        {/* Top Mode B Simulation Bar */}
        <SimulationBar
          currentDay={currentSimDay}
          selectedProfile={selectedProfile}
          setSelectedProfile={setSelectedProfile}
          onSimulateDays={handleSimulateDays}
          onResetSimulation={handleResetSimulation}
          onStartGuidedDemo={() => setIsOpenGuidedDemo(true)}
          onOpenEvaluation={() => setIsOpenEvaluation(true)}
          isLoading={isLoading}
        />

        {/* Header Bar */}
        <header className="px-8 py-5 bg-white border-b border-slate-100 flex items-center justify-between gap-4 sticky top-12 z-20 shadow-xs">
          <div>
            <h2 className="font-heading text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
              Welcome back, {dashboardData?.user_name || 'Aarav'}! 👋
            </h2>
            <p className="text-xs text-slate-500 font-medium mt-0.5">
              Your personalized adaptive learning journey continues...
            </p>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3.5 py-2 bg-slate-50 rounded-xl border border-slate-100 text-xs font-semibold text-slate-600">
              <Calendar className="w-4 h-4 text-slate-400" />
              <span>16 May 2025, Friday</span>
            </div>

            <button className="w-9 h-9 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-100 flex items-center justify-center text-slate-500 transition-colors relative">
              <Bell className="w-4 h-4" />
              <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-indigo-600"></span>
            </button>
          </div>
        </header>

        {/* Dashboard Content */}

        <main className="p-8 space-y-6 flex-1">
          {isLoading && !dashboardData ? (
            <DashboardSkeleton />
          ) : dashboardData ? (
            renderMainContent(dashboardData)
          ) : (
            <div className="p-12 text-center text-slate-500 font-medium">
              No data available.
            </div>
          )}
        </main>
      </div>

      {/* Modals */}
      {isOpenStudyModal && studyConcept && (
        <StudyMaterialModal
          concept={studyConcept}
          activeGoal={dashboardData?.goal}
          onClose={() => setIsOpenStudyModal(false)}
          onStartPractice={(c) => {
            setIsOpenStudyModal(false);
            handleSelectConcept(c);
          }}
        />
      )}

      {isOpenQuiz && selectedConcept && (
        <QuizModal
          conceptTitle={selectedConcept.title}
          material={material}
          questions={questions}
          onClose={() => setIsOpenQuiz(false)}
          onRefreshDashboard={loadDashboard}
        />
      )}

      {isOpenGuidedDemo && (
        <GuidedDemoModal
          onClose={() => setIsOpenGuidedDemo(false)}
          onRefreshDashboard={loadDashboard}
        />
      )}

      {isOpenEvaluation && (
        <EvaluationModal
          onClose={() => setIsOpenEvaluation(false)}
        />
      )}
    </div>
  );
}

export default App;
