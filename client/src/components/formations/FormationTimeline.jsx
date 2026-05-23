/**
 * FormationTimeline.jsx — Bottom sequencer bar detailing all transition snapshots,
 * timeline order, and timestamps.
 */
import React from 'react';
import FormationCard from './FormationCard';

export const FormationTimeline = ({
  formations = [],
  selectedId = null,
  onSelect,
  onCreateNew,
  onDuplicate,
  onDelete
}) => {
  return (
    <div className="bg-[#1a1a24] p-4 rounded-xl border border-[#23232f] text-white">
      <div className="flex items-center justify-between border-b border-[#2d2d3d] pb-2.5 mb-4">
        <div className="flex items-center space-x-3">
          <h3 className="font-bold text-sm tracking-wide">Timeline Sequence</h3>
          <span className="text-xs bg-[#2b2b3a] px-2 py-0.5 rounded text-[#b3b3cb]">
            {formations.length} Snaps
          </span>
        </div>

        <button
          onClick={onCreateNew}
          className="bg-[#ff2a7f] hover:bg-[#e0206f] text-xs font-bold px-3 py-1.5 rounded-lg transition-colors"
        >
          + Add Snap
        </button>
      </div>

      {/* Horizontal timeline snapshots */}
      <div className="flex items-center space-x-4 overflow-x-auto pb-2 pr-1 custom-scrollbar">
        {formations.length === 0 ? (
          <div className="w-full text-center text-xs text-[#b3b3cb] py-6">
            No formations created. Click "+ Add Snap" above to start planning formations.
          </div>
        ) : (
          formations.map((form, index) => (
            <div key={form.id} className="relative group flex-shrink-0">
              <FormationCard
                formation={form}
                index={index}
                isSelected={selectedId === form.id}
                onClick={onSelect}
              />
              
              {/* Duplication & Deletion context tools overlay */}
              <div className="absolute -top-2 right-1 flex space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  onClick={() => onDuplicate && onDuplicate(form.id)}
                  className="bg-[#2d2d3d] border border-[#444] hover:bg-[#ff2a7f] p-1 rounded text-[10px]"
                  title="Duplicate Snap"
                >
                  ❏
                </button>
                {formations.length > 1 && (
                  <button
                    onClick={() => onDelete && onDelete(form.id)}
                    className="bg-[#2d2d3d] border border-[#444] hover:bg-red-500 p-1 rounded text-[10px]"
                    title="Delete Snap"
                  >
                    ✕
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default FormationTimeline;
