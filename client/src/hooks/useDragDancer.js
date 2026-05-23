/**
 * useDragDancer.js — Custom mouse drag operations mapping browser pixels directly back to normalized stage grid coordinates.
 */
import { useCallback, useState } from 'react';
import { pixelToGrid, clampToStage } from '../utils/stageCoordinates';

export const useDragDancer = (canvasWidth, canvasHeight, onMoveDancer, snap = false) => {
  const [isDragging, setIsDragging] = useState(false);
  const [activeDancerId, setActiveDancerId] = useState(null);

  const startDrag = useCallback((dancerId) => {
    setIsDragging(true);
    setActiveDancerId(dancerId);
  }, []);

  const handleDrag = useCallback((clientX, clientY, rect) => {
    if (!isDragging || activeDancerId === null) return;
    
    // Relative click calculation
    const relativeX = clientX - rect.left;
    const relativeY = clientY - rect.top;
    
    // Translate relative pixels back to normalized grid units
    let gridCoords = pixelToGrid(relativeX, relativeY, canvasWidth, canvasHeight);
    
    // Grid Snap alignment rounding
    if (snap) {
      gridCoords.x = Math.round(gridCoords.x * 2) / 2; // 0.5 unit increments
      gridCoords.y = Math.round(gridCoords.y * 2) / 2;
    }
    
    const bounded = clampToStage(gridCoords.x, gridCoords.y);
    onMoveDancer(activeDancerId, bounded.x, bounded.y);
  }, [isDragging, activeDancerId, canvasWidth, canvasHeight, onMoveDancer, snap]);

  const stopDrag = useCallback(() => {
    setIsDragging(false);
    setActiveDancerId(null);
  }, []);

  return {
    isDragging,
    activeDancerId,
    startDrag,
    handleDrag,
    stopDrag,
  };
};

export default useDragDancer;
