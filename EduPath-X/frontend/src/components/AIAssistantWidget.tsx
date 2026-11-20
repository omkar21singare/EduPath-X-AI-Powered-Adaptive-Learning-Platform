import React, { useState } from 'react';
import { Bot, Send, Sparkles, X } from 'lucide-react';
import { askAssistant } from '../services/api';
import type { AssistantResponse } from '../types';

interface AIAssistantWidgetProps {
  onOpenAssistantTab: () => void;
}

export const AIAssistantWidget: React.FC<AIAssistantWidgetProps> = ({ onOpenAssistantTab }) => {
  const [isOpenChat, setIsOpenChat] = useState(false);
  const [inputMsg, setInputMsg] = useState('');
  const [messages, setMessages] = useState<Array<{ sender: 'user' | 'bot'; text: string; sources?: string[] }>>([
    {
      sender: 'bot',
      text: 'Hello Aarav! I am your AI Learning Assistant. You are doing great! Focus a bit more on Graphs and Trees. How can I help your learning today?',
      sources: ['Bayesian Knowledge Tracing Model', 'Learner Profile']
    }
  ]);
  const [isSending, setIsSending] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMsg.trim()) return;

    const userText = inputMsg;
    setInputMsg('');
    setMessages(prev => [...prev, { sender: 'user', text: userText }]);
    setIsSending(true);

    try {
      const res: AssistantResponse = await askAssistant(userText);
      setMessages(prev => [...prev, { sender: 'bot', text: res.reply, sources: res.data_sources_used }]);
    } catch {
      setMessages(prev => [...prev, { sender: 'bot', text: "I'm having trouble querying learner states right now. Please try again." }]);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <>
      <div className="bg-gradient-to-r from-indigo-50 to-violet-50 p-5 rounded-2xl border border-indigo-100/80 shadow-sm flex items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-indigo-600 text-white flex items-center justify-center shadow-md shadow-indigo-200 shrink-0">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h4 className="font-heading text-sm font-bold text-slate-800 flex items-center gap-1.5">
              AI Learning Assistant
              <span className="bg-indigo-100 text-indigo-700 text-[10px] font-bold px-2 py-0.5 rounded-full">ACTIVE</span>
            </h4>
            <p className="text-xs text-slate-600 mt-0.5 max-w-md">
              You are doing great! Focus a bit more on Graphs and Tree Traversal. I have prepared a personalized learning path for you.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={() => setIsOpenChat(true)}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-xl shadow-md shadow-indigo-200 transition-colors flex items-center gap-1.5"
          >
            <Sparkles className="w-3.5 h-3.5" />
            Chat with AI
          </button>
          <button
            onClick={onOpenAssistantTab}
            className="px-4 py-2 bg-white hover:bg-slate-50 text-slate-700 text-xs font-bold rounded-xl border border-slate-200 transition-colors"
          >
            View Detailed Plan
          </button>
        </div>
      </div>

      {/* Chat Modal Overlay */}
      {isOpenChat && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-lg w-full h-[520px] flex flex-col shadow-2xl border border-slate-100 overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            {/* Header */}
            <div className="p-4 bg-indigo-600 text-white flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Bot className="w-5 h-5" />
                <h3 className="font-heading font-bold text-sm">EduPath-X AI Learning Assistant</h3>
              </div>
              <button onClick={() => setIsOpenChat(false)} className="text-white/80 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Messages body */}
            <div className="flex-1 p-4 overflow-y-auto space-y-3 bg-slate-50">
              {messages.map((m, idx) => (
                <div key={idx} className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}>
                  <div
                    className={`max-w-[85%] p-3 rounded-2xl text-xs font-medium ${
                      m.sender === 'user'
                        ? 'bg-indigo-600 text-white rounded-br-xs'
                        : 'bg-white text-slate-800 border border-slate-200 shadow-sm rounded-bl-xs'
                    }`}
                  >
                    <p className="whitespace-pre-line">{m.text}</p>
                    {m.sources && m.sources.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-slate-100 text-[10px] text-slate-400">
                        <span className="font-semibold text-slate-500">Data Sources:</span> {m.sources.join(', ')}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {isSending && (
                <div className="text-xs text-slate-400 italic">AI is checking learner states...</div>
              )}
            </div>

            {/* Form */}
            <form onSubmit={handleSend} className="p-3 bg-white border-t border-slate-100 flex items-center gap-2">
              <input
                type="text"
                placeholder="Ask: What should I study today? or Why DFS?"
                value={inputMsg}
                onChange={(e) => setInputMsg(e.target.value)}
                className="flex-1 px-3 py-2 text-xs border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <button
                type="submit"
                disabled={isSending}
                className="p-2 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 disabled:opacity-50"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </div>
      )}
    </>
  );
};
