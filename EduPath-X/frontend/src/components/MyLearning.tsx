import { KnowledgeMap } from './KnowledgeMap';
import { RecommendationsCard } from './RecommendationsCard';

export function MyLearning({ dashboardData, handleSelectConcept, handleStartRecommendation, handleOpenStudy }: any) {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-slate-800">My Learning</h2>
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-7">
          <KnowledgeMap 
            nodes={dashboardData.knowledge_map} 
            onSelectConcept={handleSelectConcept} 
            onOpenStudy={handleOpenStudy || handleSelectConcept}
            activeGoal={dashboardData.goal}
          />
        </div>
        <div className="lg:col-span-5">
          <RecommendationsCard recommendations={dashboardData.recommendations} onStartActivity={handleStartRecommendation} />
        </div>
      </div>
    </div>
  );
}
