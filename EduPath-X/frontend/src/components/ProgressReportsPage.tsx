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
