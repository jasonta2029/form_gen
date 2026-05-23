/**
 * TemplateSelector.jsx — Grid options listing for V_SHAPE, ARC, CLUSTER, SPLIT, CIRCLE.
 */
import React from 'react';

const TEMPLATES = [
  { id: 'V_SHAPE', label: 'V-Shape', symbol: '∨' },
  { id: 'ARC', label: 'Arc Line', symbol: '⌒' },
  { id: 'SPLIT', label: 'Split Group', symbol: '¦' },
  { id: 'CIRCLE', label: 'Circle Ring', symbol: '◯' },
  { id: 'DIAGONAL', label: 'Diagonal', symbol: '╱' },
  { id: 'CLUSTER', label: 'Cluster Box', symbol: '⛶' }
];

export const TemplateSelector = ({ selected, onSelect }) => {
  return (
    <div className="grid grid-cols-3 gap-2">
      {TEMPLATES.map((tmpl) => {
        const isSelected = selected === tmpl.id;
        return (
          <div
            key={tmpl.id}
            onClick={() => onSelect && onSelect(tmpl.id)}
            className={`p-2.5 rounded-lg border text-center cursor-pointer transition-all ${
              isSelected
                ? 'bg-[#291e2b] border-[#ff2a7f] text-white'
                : 'bg-[#212130] border-[#29293a] text-[#b3b3cb] hover:border-[#383852]'
            }`}
          >
            <div className="text-xl font-bold mb-1 leading-none">{tmpl.symbol}</div>
            <div className="text-[10px] font-semibold truncate">{tmpl.label}</div>
          </div>
        );
      })}
    </div>
  );
};

export default TemplateSelector;
