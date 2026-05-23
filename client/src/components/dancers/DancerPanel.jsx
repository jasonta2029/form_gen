/**
 * DancerPanel.jsx — Sidebar subpanel managing dancer rosters, roster details editing,
 * and binding color codes.
 */
import React, { useState } from 'react';
import AddDancerForm from './AddDancerForm';
import DancerCard from './DancerCard';

export const DancerPanel = ({
  dancers = [],
  centerTimeStats = [],
  onAddDancer,
  onRemoveDancer,
  selectedDancerId,
  onSelectDancer
}) => {
  const [showAddForm, setShowAddForm] = useState(false);

  return (
    <div className="flex flex-col h-full bg-[#1a1a24] text-white p-4 rounded-xl border border-[#23232f]">
      <div className="flex items-center justify-between border-b border-[#2d2d3d] pb-3 mb-4">
        <h3 className="font-bold text-md tracking-wide">Dancer Roster ({dancers.length})</h3>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="bg-[#ff2a7f] hover:bg-[#e0206f] text-xs font-bold text-white px-3 py-1.5 rounded-lg transition-colors"
        >
          {showAddForm ? 'Close' : '+ Add'}
        </button>
      </div>

      {showAddForm && (
        <div className="mb-4 bg-[#212130] p-3 rounded-lg border border-[#34344c]">
          <AddDancerForm
            onSubmit={(data) => {
              onAddDancer(data);
              setShowAddForm(false);
            }}
          />
        </div>
      )}

      {/* Roster scrollable lists */}
      <div className="flex-1 overflow-y-auto space-y-2 pr-1 custom-scrollbar">
        {dancers.length === 0 ? (
          <div className="text-center text-xs text-[#b3b3cb] py-8">
            No dancers registered. Click "+ Add" above to start the roster.
          </div>
        ) : (
          dancers.map((dancer) => {
            const stats = centerTimeStats.find((s) => s.dancer_id === dancer.id);
            return (
              <DancerCard
                key={dancer.id}
                dancer={dancer}
                centerTimePercentage={stats ? stats.percentage : 0}
                isFlagged={stats ? stats.is_flagged : false}
                isSelected={selectedDancerId === dancer.id}
                onClick={onSelectDancer}
                onDelete={onRemoveDancer}
              />
            );
          })
        )}
      </div>
    </div>
  );
};

export default DancerPanel;
