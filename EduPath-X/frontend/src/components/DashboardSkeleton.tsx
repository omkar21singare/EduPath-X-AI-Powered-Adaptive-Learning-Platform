import React from 'react';

export const DashboardSkeleton: React.FC = () => {
  return (
    <div className="space-y-6 animate-pulse">
      {/* KPI Cards Skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="bg-white rounded-2xl p-5 border border-slate-100 shadow-sm h-32">
            <div className="w-10 h-10 bg-slate-100 rounded-xl mb-4"></div>
            <div className="h-4 bg-slate-100 rounded w-1/2 mb-2"></div>
            <div className="h-6 bg-slate-100 rounded w-1/3"></div>
          </div>
        ))}
      </div>

      {/* Main Grid: Knowledge Map & Recommendations */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-7 bg-white rounded-2xl border border-slate-100 shadow-sm p-6 h-[400px]">
          <div className="flex items-center justify-between mb-6">
            <div className="h-6 bg-slate-100 rounded w-1/4"></div>
            <div className="h-4 bg-slate-100 rounded w-1/6"></div>
          </div>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-20 bg-slate-50 rounded-xl border border-slate-100"></div>
            ))}
          </div>
        </div>
        <div className="lg:col-span-5 bg-white rounded-2xl border border-slate-100 shadow-sm p-6 h-[400px]">
          <div className="h-6 bg-slate-100 rounded w-1/3 mb-6"></div>
          <div className="h-32 bg-slate-50 rounded-xl border border-slate-100 mb-4"></div>
          <div className="h-10 bg-slate-100 rounded-xl"></div>
        </div>
      </div>

      {/* Secondary Grid: Performance & Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-7 bg-white rounded-2xl border border-slate-100 shadow-sm p-6 h-[350px]">
          <div className="h-6 bg-slate-100 rounded w-1/4 mb-6"></div>
          <div className="h-full bg-slate-50 rounded-full w-64 h-64 mx-auto"></div>
        </div>
        <div className="lg:col-span-5 bg-white rounded-2xl border border-slate-100 shadow-sm p-6 h-[350px]">
          <div className="h-6 bg-slate-100 rounded w-1/3 mb-6"></div>
          <div className="space-y-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="flex gap-3 items-center">
                <div className="w-8 h-8 bg-slate-100 rounded-full"></div>
                <div className="flex-1">
                  <div className="h-3 bg-slate-100 rounded w-full mb-2"></div>
                  <div className="h-2 bg-slate-100 rounded w-1/3"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
