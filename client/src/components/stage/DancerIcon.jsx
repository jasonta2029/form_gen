/**
 * DancerIcon.jsx — Rendered dancer dot on the SVG stage area.
 * Displays colored indicator ring, dancer index number, and name below.
 */
import React from 'react';

export const DancerIcon = ({
  dancer,
  x,
  y,
  color = '#3b82f6',
  isSelected = false,
  isDragging = false,
  onMouseDown,
  onClick
}) => {
  return (
    <g
      className={`dancer-icon-group select-none cursor-grab ${isDragging ? 'cursor-grabbing opacity-80' : ''}`}
      transform={`translate(${x}, ${y})`}
      onMouseDown={(e) => {
        e.stopPropagation();
        if (onMouseDown) onMouseDown(e);
      }}
      onClick={(e) => {
        e.stopPropagation();
        if (onClick) onClick(dancer.id);
      }}
    >
      {/* Outer focus glow ring when selected */}
      {isSelected && (
        <circle
          cx="0"
          cy="0"
          r="22"
          fill="none"
          stroke="#ff2a7f"
          strokeWidth="3.5"
          className="animate-pulse"
        />
      )}

      {/* Main dancer dot circle */}
      <circle
        cx="0"
        cy="0"
        r="15"
        fill={color}
        stroke="#1a1a24"
        strokeWidth="2"
        className="transition-transform duration-100 hover:scale-110"
      />

      {/* Dancer Number Label */}
      <text
        x="0"
        y="5"
        fill="#ffffff"
        fontSize="12"
        fontWeight="bold"
        textAnchor="middle"
        pointerEvents="none"
      >
        {dancer.number}
      </text>

      {/* Dancer Name beneath */}
      <text
        x="0"
        y="30"
        fill={isSelected ? '#ff2a7f' : '#b3b3cb'}
        fontSize="11"
        fontWeight="500"
        textAnchor="middle"
        pointerEvents="none"
        className="font-sans filter drop-shadow-md"
      >
        {dancer.name}
      </text>
    </g>
  );
};

export default DancerIcon;
