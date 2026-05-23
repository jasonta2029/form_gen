/**
 * colorPalette.js — Dancer circular icon colors selection.
 * Color codes match the style choices shown in the reference graphics (dance pic 1 & 2).
 */

export const DANCER_COLORS = [
  '#3b82f6', // Bright Blue
  '#10b981', // Emerald Teal Green
  '#ec4899', // Confident Pink / Magenta
  '#8b5cf6', // Indigo Purple
  '#f59e0b', // Amber Orange
  '#6b7280', // Neutral Slate Grey
  '#06b6d4', // Cyan Blue
  '#f43f5e', // Rose Red
  '#14b8a6', // Teal
  '#a855f7', // Light Purple
];

/**
 * Deterministically binds a hex color code to a dancer ID/index
 */
export function getDancerColor(index) {
  return DANCER_COLORS[index % DANCER_COLORS.length];
}

export default {
  DANCER_COLORS,
  getDancerColor,
};
