import React, { createContext, useContext, useState, useCallback } from 'react';
import { CheckCircle, XCircle, AlertCircle, X } from 'lucide-react';

const ToastContext = createContext(null);

const ICONS = {
  success: <CheckCircle size={16} className="text-emerald-400 flex-shrink-0" />,
  error:   <XCircle    size={16} className="text-red-400    flex-shrink-0" />,
  info:    <AlertCircle size={16} className="text-blue-400  flex-shrink-0" />,
};

const BORDERS = {
  success: 'border-emerald-500/30',
  error:   'border-red-500/30',
  info:    'border-blue-500/30',
};

function Toast({ id, message, type, onDismiss }) {
  return (
    <div
      className={`flex items-center gap-3 bg-[#1e1e2a] border ${BORDERS[type]} px-4 py-3 rounded-xl shadow-xl text-sm text-white max-w-sm w-full animate-slide-in`}
      role="alert"
      aria-live="polite"
    >
      {ICONS[type]}
      <span className="flex-1 leading-snug">{message}</span>
      <button
        onClick={() => onDismiss(id)}
        className="text-[#6b6b8a] hover:text-white transition-colors cursor-pointer flex-shrink-0"
        aria-label="Dismiss"
      >
        <X size={14} />
      </button>
    </div>
  );
}

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const showToast = useCallback((message, type = 'info', duration = 3500) => {
    const id = Date.now() + Math.random();
    setToasts(prev => [...prev, { id, message, type }]);
    setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), duration);
  }, []);

  const dismiss = useCallback((id) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <div className="fixed bottom-6 right-6 z-[9999] flex flex-col gap-2 items-end pointer-events-none">
        {toasts.map(t => (
          <div key={t.id} className="pointer-events-auto">
            <Toast {...t} onDismiss={dismiss} />
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export const useToast = () => {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error('useToast must be inside ToastProvider');
  return ctx;
};
