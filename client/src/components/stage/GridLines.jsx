/**
 * GridLines.jsx — Renders vertical and horizontal grid marks for dancer spacing references.
 */
import React from 'react';

export const GridLines = ({ width, height, gridSpacingX = 10, gridSpacingY = 10 }) => {
  const horizontalLines = [];
  const verticalLines = [];

  // Generate vertical lines
  for (let i = 1; i < gridSpacingX; i++) {
    const x = (i / gridSpacingX) * width;
    verticalLines.push(
      <line
        key={`v-${i}`}
        x1={x}
        y1="0"
        x2={x}
        y2={height}
        stroke="#2d2d3d"
        strokeWidth="1.2"
        strokeDasharray="2,2"
      />
    );
  }

  // Generate horizontal lines
  for (let i = 1; i < gridSpacingY; i++) {
    const y = (i / gridSpacingY) * height;
    horizontalLines.push(
      <line
        key={`h-${i}`}
        x1="0"
        y1={y}
        x2={width}
        y2={y}
        stroke="#2d2d3d"
        strokeWidth="1.2"
        strokeDasharray="2,2"
      />
    );
  }

  return (
    <g className="grid-lines" opacity="0.8">
      {/* Center axis lines */}
      <line
        x1={width / 2}
        y1="0"
        x2={width / 2}
        y2={height}
        stroke="#45455d"
        strokeWidth="1.5"
      />
      <line
        x1="0"
        y1={height / 2}
        x2={width}
        y2={height / 2}
        stroke="#45455d"
        strokeWidth="1.5"
      />
      {verticalLines}
      {horizontalLines}
    </g>
  );
};

export default GridLines;
