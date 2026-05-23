/**
 * GenerationParams.jsx — Renders options inputs for geometry modifiers (spacing, spacing ratios, symmetry checks).
 */
import React from 'react';

export const GenerationParams = ({ params, onChange }) => {
  const setParam = (key, val) => {
    if (onChange) {
      onChange({ ...params, [key]: val });
    }
  };

  return (
    <div className="bg-[#212130] p-3 rounded-lg border border-[#29293a] space-y-3.5 text-left text-xs">
      {/* Density Slider */}
      <div>
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-[#b3b3cb] text-[10px] uppercase font-semibold">Dancer Spacing</span>
          <span className="font-bold text-[#ff2a7f]">{(params.density * 4).toFixed(1)}m</span>
        </div>
        <input
          type="range"
          min="0.1"
          max="1.0"
          step="0.05"
          value={params.density}
          onChange={(e) => setParam('density', parseFloat(e.target.value))}
          className="w-full h-1 bg-[#171721] rounded-lg appearance-none cursor-pointer accent-[#ff2a7f]"
        />
      </div>

      {/* Symmetry checkbox */}
      <div className="flex items-center justify-between pt-1">
        <span className="text-[#b3b3cb] text-[10px] uppercase font-semibold">Enforce Symmetry</span>
        <label className="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={params.symmetry}
            onChange={(e) => setParam('symmetry', e.target.checked)}
            className="sr-only peer"
          />
          <div className="w-9 h-5 bg-[#171721] peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-[#b3b3cb] after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#ff2a7f] peer-checked:after:bg-white" />
        </label>
      </div>

      {/* Geometric Style Selector */}
      <div>
        <span className="text-[#b3b3cb] text-[10px] uppercase font-semibold block mb-1.5">Alignment Style</span>
        <div className="grid grid-cols-2 gap-2">
          {['balanced', 'scattered'].map((styleOpt) => (
            <button
              key={styleOpt}
              type="button"
              onClick={() => setParam('style', styleOpt)}
              className={`py-1 rounded text-[10px] font-bold uppercase transition-colors ${
                params.style === styleOpt
                  ? 'bg-[#ff2a7f] text-white'
                  : 'bg-[#171721] text-[#8c8cb0] hover:bg-[#1f1f2e]'
              }`}
            >
              {styleOpt}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default GenerationParams;
//
