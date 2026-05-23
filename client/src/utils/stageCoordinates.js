/**
 * stageCoordinates.js — Normalized Stage Grid System conversions and calculations.
 * Coordinate Limits:
 * - X Axis: Stage Left [-25.0] to Stage Right [+25.0]
 * - Y Axis: Audience Down [-15.0] to Backstage Up [+15.0]
 * - Focal Origin Point: Center stage (0,0)
 */

export const STAGE_GRID_WIDTH = 50.0;
export const STAGE_GRID_HEIGHT = 30.0;

/**
 * Translates relative grid coordinates [-25 to +25, -15 to +15] to browser viewport pixels
 */
export function gridToPixel(gridX, gridY, canvasWidth, canvasHeight) {
  const pixelX = ((gridX + 25.0) / STAGE_GRID_WIDTH) * canvasWidth;
  // Browser Y axis is inverted (0 is top)
  const pixelY = ((15.0 - gridY) / STAGE_GRID_HEIGHT) * canvasHeight;
  return { x: pixelX, y: pixelY };
}

/**
 * Translates browser click pixels back to relative grid coordinates
 */
export function pixelToGrid(pixelX, pixelY, canvasWidth, canvasHeight) {
  const gridX = (pixelX / canvasWidth) * STAGE_GRID_WIDTH - 25.0;
  const gridY = 15.0 - (pixelY / canvasHeight) * STAGE_GRID_HEIGHT;
  return { x: gridX, y: gridY };
}

/**
 * Restricts values to legal limits of the stage area
 */
export function clampToStage(gridX, gridY) {
  return {
    x: Math.max(-25.0, Math.min(gridX, 25.0)),
    y: Math.max(-15.0, Math.min(gridY, 15.0)),
  };
}

/**
 * Simple Pythagorean theorem calculator
 */
export function calculateDistance(x1, y1, x2, y2) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  return Math.sqrt(dx * dx + dy * dy);
}

export default {
  STAGE_GRID_WIDTH,
  STAGE_GRID_HEIGHT,
  gridToPixel,
  pixelToGrid,
  clampToStage,
  calculateDistance,
};
