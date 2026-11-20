import { useState, useEffect, useRef } from 'react';
import { Bot, Send, Sparkles, User, HelpCircle } from 'lucide-react';
import { askAssistant, getDashboard } from '../services/api';
import type { AssistantResponse, DashboardResponse } from '../types';

export function AIAssistantPage() {
  const [inputMsg, setInputMsg] = useState('');
  const [messages, setMessages] = useState<Array<{ sender: 'user' | 'bot'; text: string; sources?: string[] }>>([
    {
      sender: 'bot',
      text: "Hello! I am your AI Learning Assistant powered by your real-time Bayesian Knowledge Tracing state. I analyze your quiz responses, prerequisite gaps, and weak concepts to guide your preparation. What would you like help with today?",
      sources: ['Bayesian Knowledge Tracing Engine', 'Real-time Analytics']
    }
  ]);
  const [isSending, setIsSending] = useState(false);
  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getDashboard()
      .then((data: DashboardResponse) => setDashboard(data))
      .catch((err: unknown) => console.error("Could not fetch dashboard context for AI Assistant", err));
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isSending]);

  const handleSend = async (textToSend?: string) => {
    const text = (textToSend || inputMsg).trim();
    if (!text || isSending) return;

    setInputMsg('');
    setMessages(prev => [...prev, { sender: 'user', text }]);
    setIsSending(true);

    try {
      const res: AssistantResponse = await askAssistant(text);
      setMessages(prev => [
        ...prev,
        {
          sender: 'bot',
          text: res.reply,
          sources: res.data_sources_used
        }
      ]);
    } catch {
      setMessages(prev => [
        ...prev,
        {
          sender: 'bot',
          text: "I couldn't reach the AI assistant engine right now. Please check that the backend is running at http://localhost:8000.",
          sources: ['System Diagnostic']
        }
      ]);
    } finally {
      setIsSending(false);
    }
  };

  const quickPrompts = [
    "What are my weakest concepts right now?",
    "Why is this topic recommended for me?",
    "Give me a DSA practice strategy based on my recent errors",
    "Explain the time complexity of Breadth-First Search"
  ];

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-indigo-600 via-indigo-700 to-violet-700 rounded-3xl p-6 text-white shadow-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-2xl bg-white/10 backdrop-blur-md flex items-center justify-center border border-white/20 shadow-inner">
            <Bot className="w-8 h-8 text-indigo-100" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold font-heading">AI Pedagogical Assistant</h2>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-200 border border-emerald-400/30 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                Live Context Active
              </span>
            </div>
            <p className="text-indigo-100 text-xs mt-1 max-w-xl">
              Connected directly to your Bayesian Knowledge Tracing (BKT) probability models, prerequisite mastery DAG, and live misconception records.
            </p>
          </div>
        </div>

        {/* Real-time Learner Context Snapshot Pill */}
        {dashboard && (
          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-3 border border-white/15 text-xs text-indigo-50 min-w-[200px]">
            <div className="font-semibold text-white flex items-center justify-between">
              <span>Overall Progress</span>
              <span className="text-emerald-300 font-bold">{Math.round((dashboard.kpis?.overall_progress || 0))}%</span>
            </div>
            <div className="mt-1 text-[11px] text-indigo-200 truncate">
              Mastered: <span className="font-medium text-emerald-200">{dashboard.kpis?.concepts_mastered || 0} / {dashboard.kpis?.total_concepts || 0} Concepts</span>
            </div>
          </div>
        )}
      </div>

      {/* Main Chat Container */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden flex flex-col h-[600px]">
        {/* Messages Scroll Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex gap-3 max-w-[85%] ${
                msg.sender === 'user' ? 'ml-auto flex-row-reverse' : 'mr-auto'
              }`}
            >
              <div
                className={`w-9 h-9 rounded-2xl flex items-center justify-center shrink-0 shadow-sm ${
                  msg.sender === 'user'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-indigo-50 border border-indigo-100 text-indigo-600'
                }`}
              >
                {msg.sender === 'user' ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
              </div>

              <div className="space-y-1.5">
                <div
                  className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed whitespace-pre-line shadow-sm ${
                    msg.sender === 'user'
                      ? 'bg-indigo-600 text-white rounded-tr-none'
                      : 'bg-slate-50 border border-slate-200/80 text-slate-800 rounded-tl-none'
                  }`}
                >
                  {msg.text}
                </div>

                {/* Sources Used Badge */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="flex flex-wrap items-center gap-1.5 pt-0.5 px-1">
                    <span className="text-[10px] text-slate-400 font-medium">Telemetry Sources:</span>
                    {msg.sources.map((src, sIdx) => (
                      <span
                        key={sIdx}
                        className="text-[10px] bg-indigo-50 text-indigo-700 border border-indigo-100 px-2 py-0.5 rounded-full font-medium"
                      >
                        {src}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {isSending && (
            <div className="flex gap-3 mr-auto max-w-[80%] items-center animate-pulse">
              <div className="w-9 h-9 rounded-2xl bg-indigo-50 border border-indigo-100 text-indigo-600 flex items-center justify-center">
                <Sparkles className="w-5 h-5 animate-spin text-indigo-500" />
              </div>
              <div className="bg-slate-50 border border-slate-200 px-4 py-3 rounded-2xl text-xs text-slate-500 flex items-center gap-2">
                <span>Analyzing knowledge state & synthesizing pedagogical guidance...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Quick Suggestion Chips */}
        <div className="px-6 py-2 bg-slate-50 border-t border-slate-100 flex items-center gap-2 overflow-x-auto no-scrollbar">
          <span className="text-[11px] font-semibold text-slate-400 flex items-center gap-1 shrink-0">
            <HelpCircle className="w-3.5 h-3.5" /> Suggestions:
          </span>
          {quickPrompts.map((prompt, pIdx) => (
            <button
              key={pIdx}
              onClick={() => handleSend(prompt)}
              disabled={isSending}
              className="text-[11px] bg-white border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50/50 text-slate-700 px-3 py-1 rounded-full whitespace-nowrap transition-all shadow-2xs shrink-0 cursor-pointer disabled:opacity-50"
            >
              {prompt}
            </button>
          ))}
        </div>

        {/* Input Form */}
        <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="p-4 bg-white border-t border-slate-200 flex items-center gap-3">
          <input
            type="text"
            value={inputMsg}
            onChange={(e) => setInputMsg(e.target.value)}
            placeholder="Ask about your knowledge gaps, algorithm explanations, or study plan..."
            disabled={isSending}
            className="flex-1 bg-slate-50 border border-slate-200 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all placeholder:text-slate-400"
          />
          <button
            type="submit"
            disabled={!inputMsg.trim() || isSending}
            className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-40 text-white p-3.5 rounded-2xl shadow-md shadow-indigo-200 transition-all shrink-0 cursor-pointer disabled:cursor-not-allowed"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
