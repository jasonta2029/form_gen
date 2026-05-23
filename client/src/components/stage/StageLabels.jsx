/**
 * StageLabels.jsx — Renders AUDIENCE and BACKSTAGE stage indicators.
 */
import React from 'react';

export const StageLabels = ({ width, height }) => {
  return (
    <g className="stage-labels select-none pointer-events-none font-sans font-bold tracking-widest opacity-80">
      {/* BACKSTAGE label at top */}
      <text
        x={width / 2}
        y="30"
        fill="#b3b3cb"
        fontSize="14"
        textAnchor="middle"
      >
        BACKSTAGE
      </text>

      {/* AUDIENCE label at bottom */}
      <text
        x={width / 2}
        y={height - 20}
        fill="#b3b3cb"
        fontSize="14"
        textAnchor="middle"
      >
        AUDIENCE
      </text>
    </g>
  );
};

export default StageLabels;
