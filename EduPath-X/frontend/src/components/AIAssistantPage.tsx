import { Bot, AlertTriangle } from 'lucide-react';

export function AIAssistantPage() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
        <Bot className="w-5 h-5 text-indigo-600" /> AI Assistant
      </h2>
      <div className="bg-amber-50 p-8 rounded-2xl shadow-sm border border-amber-200 flex flex-col items-center justify-center text-center space-y-4">
        <AlertTriangle className="w-12 h-12 text-amber-500" />
        <h3 className="text-lg font-bold text-amber-800">AI Assistant — Integration Pending</h3>
        <p className="text-sm text-amber-700 max-w-md">
          The conversational AI assistant integration is currently pending. 
          The backend API for chat capabilities is not yet fully linked to this UI.
        </p>
      </div>
    </div>
  );
}
