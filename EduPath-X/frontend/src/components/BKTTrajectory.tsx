import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

interface Props {
  recentActivity?: any[];
}

export function BKTTrajectory({ recentActivity }: Props) {
  // Try to parse historical BKT data if available.
  // We need to map it by interaction index.
  const hasData = recentActivity && recentActivity.length > 0 && recentActivity.some(a => a.bkt_posterior !== undefined);
  
  let chartData: any[] = [];
  if (hasData) {
    // Reverse because recentActivity is descending by timestamp usually
    const ascending = [...recentActivity].reverse();
    chartData = ascending.map((act, i) => ({
      interaction: i + 1,
      concept: act.concept_code || 'Concept',
      mastery: act.bkt_posterior ? act.bkt_posterior * 100 : 0
    }));
  }

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 h-full flex flex-col">
      <h3 className="text-lg font-bold text-slate-800 mb-6">BKT Mastery Trajectory</h3>
      
      {hasData ? (
        <div className="flex-1 min-h-[250px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
              <XAxis dataKey="interaction" tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
              <YAxis domain={[0, 100]} tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
              <Tooltip 
                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                labelStyle={{ fontWeight: 'bold', color: '#1e293b' }}
              />
              <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
              <Line type="monotone" dataKey="mastery" stroke="#4f46e5" strokeWidth={3} dot={{ r: 4, strokeWidth: 2 }} activeDot={{ r: 6 }} name="Mastery (%)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center text-sm text-slate-400 italic">
          Mastery history will appear after the learner completes interactions.
        </div>
      )}
    </div>
  );
}
