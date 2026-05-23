/**
 * LoadingSpinner.jsx — Renders a beautiful pink/magenta visual load animation overlay.
 */
import React from 'react';

export const LoadingSpinner = ({ size = 'medium', message = 'Loading...' }) => {
  const sizes = {
    small: 'w-6 h-6 border-2',
    medium: 'w-10 h-10 border-3',
    large: 'w-14 h-14 border-4'
  };

  return (
    <div className="flex flex-col items-center justify-center space-y-3 p-6 text-xs text-[#b3b3cb] font-semibold select-none">
      <div 
        className={`animate-spin rounded-full border-t-[#ff2a7f] border-[#272739] ${sizes[size] || sizes.medium}`}
      />
      {message && <span className="animate-pulse tracking-wide uppercase">{message}</span>}
    </div>
  );
};

export default LoadingSpinner;
