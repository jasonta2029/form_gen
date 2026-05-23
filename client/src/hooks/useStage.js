/**
 * useStage.js — Hook managing active viewport drag manipulations and dimension computations.
 */
import { useCallback } from 'react';
import { useStageContext } from '../context/StageContext';
import { gridToPixel, pixelToGrid } from '../utils/stageCoordinates';

export const useStage = (canvasWidth = 800, canvasHeight = 480) => {
  const {
    zoom,
    setZoom,
    pan,
    setPan,
    selectedDancerId,
    setSelectedDancerId,
    snapToGrid,
    setSnapToGrid,
  } = useStageContext();

  const handleZoomIn = useCallback(() => {
    setZoom(prev => Math.min(prev + 0.1, 2.5));
  }, [setZoom]);

  const handleZoomOut = useCallback(() => {
    setZoom(prev => Math.max(prev - 0.1, 0.5));
  }, [setZoom]);

  const handlePan = useCallback((dx, dy) => {
    setPan(prev => ({ x: prev.x + dx, y: prev.y + dy }));
  }, [setPan]);

  const getCoordinates = useCallback((gridX, gridY) => {
    const rawCoords = gridToPixel(gridX, gridY, canvasWidth, canvasHeight);
    // Apply zoom and panning translations
    return {
      x: rawCoords.x * zoom + pan.x,
      y: rawCoords.y * zoom + pan.y
    };
  }, [zoom, pan, canvasWidth, canvasHeight]);

  return {
    zoom,
    pan,
    selectedDancerId,
    setSelectedDancerId,
    snapToGrid,
    setSnapToGrid,
    handleZoomIn,
    handleZoomOut,
    handlePan,
    getCoordinates,
  };
};

export default useStage;
