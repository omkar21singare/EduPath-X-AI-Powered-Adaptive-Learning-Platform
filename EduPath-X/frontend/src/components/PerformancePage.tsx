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
