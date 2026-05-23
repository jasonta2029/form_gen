/**
 * FormationCard.jsx — Miniature visual layout representer displaying snapshots.
 */
import React from 'react';

export const FormationCard = ({
  formation,
  index,
  isSelected = false,
  onClick
}) => {
  return (
    <div
      onClick={() => onClick && onClick(formation.id)}
      className={`w-36 p-3 rounded-xl cursor-pointer text-left transition-all border ${
        isSelected
          ? 'bg-[#291e2b] border-[#ff2a7f] shadow-[0_0_12px_rgba(255,42,127,0.2)]'
          : 'bg-[#212130] border-[#29293a] hover:border-[#383852]'
      }`}
    >
      {/* Miniature stage frame graphic mockup */}
      <div className="w-full h-16 bg-[#161622] rounded-lg border border-[#2c2c3e] relative overflow-hidden mb-2 flex items-center justify-center">
        {/* Render a tiny V shape or grid lines depending on name */}
        <div className="absolute inset-0 flex items-center justify-center opacity-30 text-[10px] uppercase font-bold text-[#8c8cb0] tracking-wider pointer-events-none">
          {formation.name.includes("V-shape") || formation.name.includes("confident") ? "V-Shape" : "Grid"}
        </div>
        
        {/* Central micro marker */}
        <div className="w-1.5 h-1.5 rounded-full bg-[#ff2a7f]/50 absolute" />
        
        {/* Micro dots indicating dancers */}
        {(formation.positions || []).slice(0, 7).map((pos, idx) => (
          <div
            key={idx}
            className="w-1 h-1 rounded-full bg-blue-400 absolute"
            style={{
              left: `${50 + pos.x * 1.5}%`,
              top: `${50 - pos.y * 2}%`
            }}
          />
        ))}
      </div>

      <div className="flex flex-col">
        <span className="text-[9px] uppercase tracking-wider font-semibold text-[#8c8cb0]">
          SNAP {index + 1}
        </span>
        <h4 className="font-bold text-xs truncate text-white">{formation.name}</h4>
        <span className="text-[10px] text-[#b3b3cb] mt-1">
          {formation.timestamp_start.toFixed(1)}s - {formation.timestamp_end.toFixed(1)}s
        </span>
      </div>
    </div>
  );
};

export default FormationCard;
