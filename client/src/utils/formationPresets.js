/**
 * formationPresets.js — Local geometric generator equations for instant formations creation.
 * Standard boundaries:
 * - width [-25.0, 25.0]
 * - height [-15.0, 15.0]
 */

export const PRESETS = {
  V_SHAPE: 'V_SHAPE',
  ARC: 'ARC',
  CLUSTER: 'CLUSTER',
  SPLIT: 'SPLIT',
  DIAGONAL: 'DIAGONAL',
  LINE: 'LINE',
  CIRCLE: 'CIRCLE',
  DIAMOND: 'DIAMOND',
  SCATTER: 'SCATTER'
};

/**
 * Distributes 'n' dancers symmetrically in a V-Shape structure
 */
export function generateVShape(numDancers, spacing = 2.0, focalX = 0, focalY = 0) {
  const positions = [];
  const half = Math.floor(numDancers / 2);
  
  for (let i = 0; i < numDancers; i++) {
    let x, y;
    if (i === 0) {
      // Peak point (focal bottom of the V)
      x = focalX;
      y = focalY - 4;
    } else if (i % 2 === 1) {
      // Left Wing
      const step = Math.floor(i / 2) + 1;
      x = focalX - step * spacing;
      y = focalY - 4 + step * (spacing * 0.7);
    } else {
      // Right Wing
      const step = Math.floor(i / 2);
      x = focalX + step * spacing;
      y = focalY - 4 + step * (spacing * 0.7);
    }
    positions.push({ x, y });
  }
  return positions;
}

/**
 * Distributes 'n' dancers along a horizontal arc shape
 */
export function generateArc(numDancers, radius = 15.0, focalX = 0, focalY = 0) {
  const positions = [];
  const startAngle = Math.PI * 0.2; // 36 degrees
  const endAngle = Math.PI * 0.8;   // 144 degrees
  const angleStep = (endAngle - startAngle) / Math.max(1, numDancers - 1);

  for (let i = 0; i < numDancers; i++) {
    const angle = startAngle + i * angleStep;
    const x = focalX + radius * Math.cos(angle);
    const y = focalY + radius * Math.sin(angle) - 5; // offset downwards
    positions.push({ x, y });
  }
  return positions;
}

/**
 * Distributes 'n' dancers in a split ensemble (Left vs Right teams)
 */
export function generateSplit(numDancers, separation = 12.0) {
  const positions = [];
  const half = Math.ceil(numDancers / 2);
  
  for (let i = 0; i < numDancers; i++) {
    const isLeft = i < half;
    const teamIndex = isLeft ? i : i - half;
    const teamSize = isLeft ? half : numDancers - half;
    
    const x = isLeft ? -separation / 2 : separation / 2;
    const yStep = 2.5;
    const startY = -((teamSize - 1) * yStep) / 2;
    const y = startY + teamIndex * yStep;
    
    positions.push({ x, y });
  }
  return positions;
}

export function generatePreset(presetName, numDancers) {
  switch (presetName) {
    case PRESETS.V_SHAPE:
      return generateVShape(numDancers);
    case PRESETS.ARC:
      return generateArc(numDancers);
    case PRESETS.SPLIT:
      return generateSplit(numDancers);
    case PRESETS.CIRCLE:
      return Array.from({ length: numDancers }, (_, i) => {
        const angle = (2 * Math.PI * i) / numDancers;
        return { x: 8 * Math.cos(angle), y: 8 * Math.sin(angle) };
      });
    default:
      // Default scattered random placements
      return Array.from({ length: numDancers }, (_, i) => ({
        x: (Math.random() - 0.5) * 40,
        y: (Math.random() - 0.5) * 20,
      }));
  }
}

export default {
  PRESETS,
  generateVShape,
  generateArc,
  generateSplit,
  generatePreset,
};
