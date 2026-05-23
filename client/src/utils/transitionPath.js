/**
 * transitionPath.js — Computes interpolation frames for animating movements between consecutive snapshots.
 */

/**
 * Linearly interpolates between two coordinate positions
 */
export function interpolatePoints(start, end, progress) {
  return {
    x: start.x + (end.x - start.x) * progress,
    y: start.y + (end.y - start.y) * progress,
  };
}

/**
 * Calculates a slightly curved path to visual elements (to reduce overlapping path appearances)
 */
export function getCurvedWaypoint(start, end, progress, curveOffset = 3.0) {
  // Linear mid point calculation
  const midX = (start.x + end.x) / 2;
  const midY = (start.y + end.y) / 2;
  
  // Normal direction vector
  const dx = end.x - start.x;
  const dy = end.y - start.y;
  const len = Math.sqrt(dx * dx + dy * dy);
  
  if (len === 0) return start;
  
  const nx = -dy / len;
  const ny = dx / len;
  
  // Bezier coordinate control point
  const cpX = midX + nx * curveOffset;
  const cpY = midY + ny * curveOffset;
  
  // Quadratic bezier interpolation formula
  const t = progress;
  const x = (1 - t) * (1 - t) * start.x + 2 * (1 - t) * t * cpX + t * t * end.x;
  const y = (1 - t) * (1 - t) * start.y + 2 * (1 - t) * t * cpY + t * t * end.y;
  
  return { x, y };
}

export default {
  interpolatePoints,
  getCurvedWaypoint,
};
