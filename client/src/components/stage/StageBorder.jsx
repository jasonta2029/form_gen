/**
 * StageBorder.jsx — Renders a gorgeous pink/magenta bounding ring matching the visual references.
 */
import React from 'react';

export const StageBorder = ({ width, height, borderColor = '#ff2a7f' }) => {
  return (
    <rect
      x="4"
      y="4"
      width={width - 8}
      height={height - 8}
      rx="24"
      ry="24"
      fill="none"
      stroke={borderColor}
      strokeWidth="4"
      className="filter drop-shadow-[0_0_8px_rgba(255,42,127,0.3)]"
    />
  );
};

export default StageBorder;
