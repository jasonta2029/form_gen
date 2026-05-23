/**
 * CenterTimeBar.jsx — Visual indicator bar showing dancer center percentage residency.
 */
import React from 'react';

export const CenterTimeBar = ({
  name,
  percentage,
  isFlagged = false,
  deviation = 0
}) => {
  // Color code depending on deviation flags
  const barColor = isFlagged 
    ? 'bg-[#ff4747] shadow-[0_0_8px_rgba(255,71,71,0.3)]' 
    : 'bg-[#10b981] shadow-[0_0_8px_rgba(16,185,129,0.3)]';

  return (
    <div className="space-y-1.5 text-left text-xs select-none">
      <div className="flex items-center justify-between font-semibold text-[11px]">
        <span className="text-white">{name}</span>
        <div className="flex items-center space-x-1.5">
          <span className={isFlagged ? 'text-[#ff4747] font-bold' : 'text-[#b3b3cb]'}>
            {percentage.toFixed(0)}%
          </span>
          {isFlagged && (
            <span className="text-[9px] text-[#ff4747] uppercase tracking-wider bg-[#5a1818]/60 px-1 py-0.5 rounded border border-[#ff4747]/20 font-bold">
              {deviation > 0 ? 'Over' : 'Under'}
            </span>
          )}
        </div>
      </div>
      
      {/* Visual meter bar background outline */}
      <div className="w-full h-2 bg-[#171721] rounded-full overflow-hidden border border-[#23232f]">
        <div 
          className={`h-full rounded-full transition-all duration-500 ${barColor}`} 
          style={{ width: `${Math.min(100, percentage)}%` }} 
        />
      </div>
    </div>
  );
};

export default CenterTimeBar;
