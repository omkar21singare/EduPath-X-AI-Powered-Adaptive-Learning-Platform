import React from 'react';
import { 
  LayoutDashboard, 
  BookOpen, 
  Network, 
  Sparkles, 
  Target, 
  BarChart3, 
  FileText, 
  Bot, 
  Settings, 
  PlayCircle,
  FlaskConical,
  UserCheck
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  userName: string;
  className: string;
  semester: string;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  userName,
  className: learnerClass,
  semester
}) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'mylearning', label: 'My Learning', icon: BookOpen },
    { id: 'knowledgemap', label: 'Knowledge Map', icon: Network },
    { id: 'recommendations', label: 'Recommendations', icon: Sparkles },
    { id: 'practice', label: 'Practice', icon: Target },
    { id: 'performance', label: 'Performance', icon: BarChart3 },
    { id: 'progress', label: 'Progress Reports', icon: FileText },
    { id: 'assistant', label: 'AI Assistant', icon: Bot },
    { id: 'guided_demo', label: 'Guided Demo', icon: PlayCircle },
    { id: 'evaluation', label: 'Adaptive vs Fixed', icon: FlaskConical },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-white border-r border-slate-100 flex flex-col justify-between h-screen sticky top-0 z-20">
      <div>
        {/* Logo */}
        <div className="p-6 flex items-center gap-3 border-b border-slate-50">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-md shadow-indigo-200">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="font-heading text-xl font-bold text-slate-800 tracking-tight leading-none">EduPath-X</h1>
            <span className="text-[10px] font-medium text-indigo-600 uppercase tracking-wider">AI Adaptive Platform</span>
          </div>
        </div>

        {/* Navigation */}
        <nav className="p-4 space-y-1 overflow-y-auto max-h-[calc(100vh-180px)]">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 ${
                  isActive
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200 font-semibold'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900 hover:-translate-y-0.5'
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* User Profile Footer */}
      <div className="p-4 m-4 bg-slate-50 rounded-2xl border border-slate-100 flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center text-white font-bold text-sm shadow-sm">
          {userName.split(' ').map(n => n[0]).join('')}
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-semibold text-slate-800 truncate">{userName}</h4>
          <p className="text-xs text-slate-500 truncate">{learnerClass} • {semester}</p>
        </div>
        <UserCheck className="w-4 h-4 text-emerald-500 shrink-0" />
      </div>
    </aside>
  );
};
