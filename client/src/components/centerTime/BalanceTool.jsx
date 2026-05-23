/**
 * BalanceTool.jsx — Visual sliders list targeting center time weights.
 */
import React from 'react';

export const BalanceTool = ({
  dancers = [],
  weights = {},
  onWeightChange,
  onSubmit
}) => {
  return (
    <div className="space-y-4 text-left text-xs">
      <div className="bg-[#212130] p-3 rounded-lg border border-[#29293a] space-y-3.5 max-h-[220px] overflow-y-auto pr-1 custom-scrollbar">
        <span className="text-[10px] text-[#b3b3cb] uppercase font-bold tracking-wider block mb-2 border-b border-[#2d2d3d] pb-1">
          Adjust Dancer Priority Weights
        </span>

        {dancers.map((dancer) => {
          const val = weights[dancer.id] !== undefined ? weights[dancer.id] : 1.0;
          return (
            <div key={dancer.id} className="space-y-1">
              <div className="flex items-center justify-between text-[11px]">
                <span className="font-semibold text-white">{dancer.name}</span>
                <span className="font-bold text-[#ff2a7f]">{val.toFixed(1)}x</span>
              </div>
              <input
                type="range"
                min="0.0"
                max="3.0"
                step="0.1"
                value={val}
                onChange={(e) => onWeightChange && onWeightChange(dancer.id, parseFloat(e.target.value))}
                className="w-full h-1 bg-[#171721] rounded-lg appearance-none cursor-pointer accent-[#ff2a7f]"
              />
            </div>
          );
        })}
      </div>

      <button
        onClick={onSubmit}
        className="w-full bg-[#ff2a7f] hover:bg-[#e0206f] text-white font-bold py-2 rounded-lg transition-colors text-xs flex items-center justify-center space-x-1"
      >
        <span>⚖ Auto-Balance Placements</span>
      </button>
    </div>
  );
};

export default BalanceTool;
