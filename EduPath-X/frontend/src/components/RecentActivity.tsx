import React from 'react';
import type { RecentActivity as RecentActivityType } from '../types';
import { CheckCircle2, BookOpen, Award, XCircle } from 'lucide-react';

interface RecentActivityProps {
  activities: RecentActivityType[];
}

export const RecentActivity: React.FC<RecentActivityProps> = ({ activities }) => {
  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col justify-between h-full">
      <div>
        <h3 className="font-heading text-lg font-bold text-slate-800 mb-4">Recent Activity</h3>

        <div className="space-y-3">
          {activities.map((act) => (
            <div key={act.id} className="flex items-start gap-3 p-3 rounded-xl bg-slate-50/60 border border-slate-100">
              <div className="mt-0.5 shrink-0">
                {act.type === 'QUIZ' ? (
                  act.is_correct ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                  ) : (
                    <XCircle className="w-5 h-5 text-rose-500" />
                  )
                ) : act.type === 'TEST' ? (
                  <Award className="w-5 h-5 text-amber-500" />
                ) : (
                  <BookOpen className="w-5 h-5 text-blue-500" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <h4 className="text-xs font-bold text-slate-800 truncate">{act.title}</h4>
                <p className="text-[11px] text-slate-400 mt-0.5">{act.timestamp}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-4 pt-3 border-t border-slate-100 text-center">
        <button className="text-xs text-indigo-600 font-semibold hover:underline">
          View Complete Activity Log →
        </button>
      </div>
    </div>
  );
};
