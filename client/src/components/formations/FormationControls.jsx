/**
 * FormationControls.jsx — Overlay toolbar matching timing and naming settings options.
 */
import React from 'react';

export const FormationControls = ({
  onDuplicate,
  onDelete,
  onRename,
  formation = null
}) => {
  const handleRenamePrompt = () => {
    if (!formation) return;
    const newName = prompt("Enter new formation title:", formation.name);
    if (newName && newName.trim() && onRename) {
      onRename(formation.id, newName.trim());
    }
  };

  return (
    <div className="bg-[#212130] p-3 rounded-lg border border-[#29293a] flex items-center justify-between text-xs text-white">
      <div>
        <span className="text-[10px] text-[#b3b3cb] uppercase font-bold block">Current Active Snap</span>
        <h4 className="font-extrabold text-sm text-[#ff2a7f] mt-0.5">{formation ? formation.name : 'None Selected'}</h4>
      </div>

      <div className="flex space-x-2">
        <button
          onClick={handleRenamePrompt}
          disabled={!formation}
          className="bg-[#2b2b3a] hover:bg-[#3b3b52] px-3 py-1.5 rounded font-bold transition-colors disabled:opacity-40"
        >
          ✏ Rename
        </button>
        <button
          onClick={() => onDuplicate && onDuplicate(formation?.id)}
          disabled={!formation}
          className="bg-[#2b2b3a] hover:bg-[#3b3b52] px-3 py-1.5 rounded font-bold transition-colors disabled:opacity-40"
        >
          ❏ Duplicate
        </button>
        <button
          onClick={() => onDelete && onDelete(formation?.id)}
          disabled={!formation}
          className="bg-red-900/60 hover:bg-red-800 border border-red-700 px-3 py-1.5 rounded font-bold text-red-300 transition-colors disabled:opacity-40"
        >
          ✕ Delete
        </button>
      </div>
    </div>
  );
};

export default FormationControls;
