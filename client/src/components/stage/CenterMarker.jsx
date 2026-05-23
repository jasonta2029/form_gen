/**
 * CenterMarker.jsx — SVG group drawing the signature Red X focal point.
 */
import React from 'react';

export const CenterMarker = ({ x, y, size = 20 }) => {
  const half = size / 2;
  return (
    <g className="center-marker" transform={`translate(${x}, ${y})`}>
      {/* Red cross lines */}
      <line 
        x1={-half} 
        y1={-half} 
        x2={half} 
        y2={half} 
        stroke="#ff2a7f" 
        strokeWidth="3.5"
        strokeLinecap="round"
      />
      <line 
        x1={half} 
        y1={-half} 
        x2={-half} 
        y2={half} 
        stroke="#ff2a7f" 
        strokeWidth="3.5"
        strokeLinecap="round"
      />
      {/* Outer subtle glow */}
      <circle 
        cx="0" 
        cy="0" 
        r={size * 0.8} 
        fill="none" 
        stroke="#ff2a7f" 
        strokeWidth="1" 
        strokeDasharray="2,2" 
        opacity="0.6"
      />
    </g>
  );
};

export default CenterMarker;
