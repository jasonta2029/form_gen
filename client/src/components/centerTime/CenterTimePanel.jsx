/**
 * CenterTimePanel.jsx — Sidebar subpanel checking center time residency stats,
 * showcasing flags warnings, and providing rebalancing target slides.
 */
import React, { useState } from 'react';
import CenterTimeBar from './CenterTimeBar';
import BalanceTool from './BalanceTool';

export const CenterTimePanel = ({
  stats = [],
  onRebalance,
  dancers = []
}) => {
  const [showSliders, setShowSliders] = useState(false);
  const [weights, setWeights] = useState({});

  // Initialize weights if not set
  const handleWeightChange = (dancerId, value) => {
    setWeights((prev) => ({ ...prev, [dancerId]: value }));
  };

  const handleTriggerBalance = () => {
    if (onRebalance) {
      onRebalance(weights);
    }
    setShowSliders(false);
  };

  return (
    <div className="flex flex-col bg-[#1a1a24] text-white p-4 rounded-xl border border-[#23232f] space-y-4">
      <div className="border-b border-[#2d2d3d] pb-2.5 flex items-center justify-between">
        <div>
          <h3 className="font-bold text-md tracking-wide">Center Balancer</h3>
          <p className="text-[10px] text-[#b3b3cb] mt-0.5">
            Dancer residency times at center stage (Focal Point X).
          </p>
        </div>
        <button
          onClick={() => setShowSliders(!showSliders)}
          className="text-xs bg-[#2b2b3a] hover:bg-[#3b3b50] border border-[#3e3e56] px-2.5 py-1.5 rounded-lg text-white"
        >
          {showSliders ? 'Stats' : 'Targets'}
        </button>
      </div>

      {showSliders ? (
        /* Weights targets editing sliders */
        <BalanceTool
          dancers={dancers}
          weights={weights}
          onWeightChange={handleWeightChange}
          onSubmit={handleTriggerBalance}
        />
      ) : (
        /* Exposure Stats list indicators bar charts */
        <div className="space-y-3 max-h-[300px] overflow-y-auto pr-1 custom-scrollbar">
          {stats.length === 0 ? (
            <div className="text-center text-xs text-[#b3b3cb] py-8">
              No stats available. Move dancers onto the Central Red X to calculate metrics.
            </div>
          ) : (
            stats.map((stat) => (
              <CenterTimeBar
                key={stat.dancer_id}
                name={stat.dancer_name}
                percentage={stat.percentage}
                isFlagged={stat.is_flagged}
                deviation={stat.deviation}
              />
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default CenterTimePanel;
