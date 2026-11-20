import React from 'react';
import type { PerformanceOverview } from '../types';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';

interface PerformanceRadarProps {
  performance: PerformanceOverview;
}

export const PerformanceRadar: React.FC<PerformanceRadarProps> = ({ performance }) => {
  const data = [
    { subject: 'Concept Understanding', A: performance.concept_understanding, fullMark: 100 },
    { subject: 'Problem Solving', A: performance.problem_solving, fullMark: 100 },
    { subject: 'Speed', A: performance.speed, fullMark: 100 },
    { subject: 'Accuracy', A: performance.accuracy, fullMark: 100 },
    { subject: 'Consistency', A: performance.consistency, fullMark: 100 },
  ];

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col justify-between h-full">
      <div className="flex items-center justify-between mb-2">
        <div>
          <h3 className="font-heading text-lg font-bold text-slate-800">Performance Overview</h3>
          <p className="text-xs text-slate-500">Multidimensional metric profile</p>
        </div>
        <select className="bg-slate-50 text-slate-600 text-xs font-semibold px-2.5 py-1 rounded-lg border border-slate-200">
          <option>This Week</option>
          <option>This Month</option>
        </select>
      </div>

      <div className="w-full h-[260px] flex items-center justify-center">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="75%" data={data}>
            <PolarGrid stroke="#e2e8f0" />
            <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 10, fontWeight: 500 }} />
            <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 9 }} />
            <Tooltip 
              contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              itemStyle={{ color: '#4f46e5', fontWeight: 'bold' }}
            />
            <Radar
              name="Learner Profile"
              dataKey="A"
              stroke="#4f46e5"
              strokeWidth={2}
              fill="#818cf8"
              fillOpacity={0.5}
              isAnimationActive={true}
              animationDuration={1500}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-2 text-center text-xs text-slate-500 font-medium">
        Overall Knowledge Competency: <span className="font-bold text-indigo-600">{performance.concept_understanding}%</span>
      </div>
    </div>
  );
};
