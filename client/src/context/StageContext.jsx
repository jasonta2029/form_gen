/**
 * StageContext.jsx — Governs view state details of the grid.
 * Houses pan settings, scaling ratios, dancer selections, and alignment guides.
 */
import React, { createContext, useContext, useState } from 'react';

const StageContext = createContext(null);

export const StageProvider = ({ children }) => {
  const [zoom, setZoom] = useState(1.0);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [selectedDancerId, setSelectedDancerId] = useState(null);
  const [showGridLines, setShowGridLines] = useState(true);
  const [snapToGrid, setSnapToGrid] = useState(false);
  const [focalRadius, setFocalRadius] = useState(2.5); // normalized stage units around center (0,0)

  const resetViewport = () => {
    setZoom(1.0);
    setPan({ x: 0, y: 0 });
    setSelectedDancerId(null);
  };

  return (
    <StageContext.Provider value={{
      zoom,
      setZoom,
      pan,
      setPan,
      selectedDancerId,
      setSelectedDancerId,
      showGridLines,
      setShowGridLines,
      snapToGrid,
      setSnapToGrid,
      focalRadius,
      setFocalRadius,
      resetViewport,
    }}>
      {children}
    </StageContext.Provider>
  );
};

export const useStageContext = () => {
  const context = useContext(StageContext);
  if (!context) {
    throw new Error("useStageContext must be used inside a StageProvider");
  }
  return context;
};

export default StageContext;
