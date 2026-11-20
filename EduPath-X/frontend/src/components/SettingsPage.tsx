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
