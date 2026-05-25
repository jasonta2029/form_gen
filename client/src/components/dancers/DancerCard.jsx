import React from 'react';
import { X, AlertTriangle } from 'lucide-react';

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
        <div
          className="w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs border-2 text-white flex-shrink-0"
          style={{ backgroundColor: dancer.color, borderColor: 'rgba(255,255,255,0.15)' }}
        >
          {dancer.number}
        </div>
        <div>
          <h4 className="font-semibold text-sm leading-tight">{dancer.name}</h4>
          <span className="text-[10px] text-[#b3b3cb] uppercase tracking-wider">
            {dancer.group || 'ensemble'}
          </span>
        </div>
      </div>

      <div className="flex items-center space-x-2">
        <div className="text-right">
          <div className={`text-xs font-bold flex items-center gap-1 justify-end ${isFlagged ? 'text-red-400' : 'text-emerald-400'}`}>
            {isFlagged && <AlertTriangle size={11} />}
            {centerTimePercentage.toFixed(0)}% center
          </div>
          {isFlagged && (
            <span className="text-[9px] bg-red-900/30 border border-red-500/30 px-1.5 py-0.5 rounded text-red-400 font-semibold animate-pulse block mt-0.5">
              Over-represented
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
            className="text-[#6b6b8a] hover:text-red-400 p-1 rounded transition-colors cursor-pointer"
            aria-label={`Remove ${dancer.name}`}
          >
            <X size={13} />
          </button>
        )}
      </div>
    </div>
  );
};

export default DancerCard;
