/**
 * DancerCard.jsx — Individual list element inside the Dancer Panel side scroll list.
 */
import React from 'react';

export const DancerCard = ({
  dancer,
  centerTimePercentage = 0,
  isFlagged = false,
  isSelected = false,
  onClick,
  onDelete
}) => {
  return (
    <div
      onClick={() => onClick && onClick(dancer.id)}
      className={`flex items-center justify-between p-3 rounded-lg cursor-pointer transition-all border ${
        isSelected
          ? 'bg-[#291e2b] border-[#ff2a7f]'
          : 'bg-[#212130] border-[#29293a] hover:border-[#383852]'
      }`}
    >
      <div className="flex items-center space-x-3">
        {/* Dancer color circle */}
        <div
          className="w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs border text-white"
          style={{ backgroundColor: dancer.color, borderColor: '#171721' }}
        >
          {dancer.number}
        </div>
        <div>
          <h4 className="font-semibold text-sm">{dancer.name}</h4>
          <span className="text-[10px] text-[#b3b3cb] uppercase tracking-wider">
            {dancer.group || 'ensemble'}
          </span>
        </div>
      </div>

      <div className="flex items-center space-x-2">
        {/* Exposure indicators */}
        <div className="text-right">
          <div className={`text-xs font-bold ${isFlagged ? 'text-[#ff4747]' : 'text-[#10b981]'}`}>
            {centerTimePercentage.toFixed(0)}% center
          </div>
          {isFlagged && (
            <span className="text-[9px] bg-[#5a1818]/60 border border-[#ff4747]/40 px-1 py-0.5 rounded text-[#ff4747] font-semibold animate-pulse">
              Flagged
            </span>
          )}
        </div>

        {onDelete && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              if (confirm(`Remove ${dancer.name} from choreography?`)) {
                onDelete(dancer.id);
              }
            }}
            className="text-gray-500 hover:text-red-500 p-1 transition-colors text-xs"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  );
};

export default DancerCard;
