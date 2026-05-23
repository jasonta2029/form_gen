/**
 * StageGrid.jsx — Main Interactive SVG Stage grid.
 * Governs grid lines drawing, pink rounded borders, audience directions, Red X centers,
 * and tracks coordinates translations during mouse dragging.
 */
import React, { useRef, useEffect, useState } from 'react';
import GridLines from './GridLines';
import StageBorder from './StageBorder';
import StageLabels from './StageLabels';
import CenterMarker from './CenterMarker';
import DancerIcon from './DancerIcon';
import { useStage } from '../../hooks/useStage';
import { useDragDancer } from '../../hooks/useDragDancer';
import { getDancerColor } from '../../utils/colorPalette';

export const StageGrid = ({
  project,
  dancers = [],
  formation = null,
  onDancerMove,
  selectedDancerId,
  onSelectDancer,
  snap = false,
  width = 800,
  height = 480
}) => {
  const svgRef = useRef(null);
  const { getCoordinates } = useStage(width, height);

  // Hook managing active dancer relocations coordinate updates
  const { isDragging, activeDancerId, startDrag, handleDrag, stopDrag } = useDragDancer(
    width,
    height,
    (dancerId, newGridX, newGridY) => {
      if (onDancerMove) {
        onDancerMove(dancerId, newGridX, newGridY);
      }
    },
    snap
  );

  const handleMouseMove = (e) => {
    if (!isDragging || !svgRef.current) return;
    const rect = svgRef.current.getBoundingClientRect();
    handleDrag(e.clientX, e.clientY, rect);
  };

  const handleMouseUpOrLeave = () => {
    if (isDragging) stopDrag();
  };

  // Translate positions mapping for circles
  const positionsMap = formation?.positions || [];

  return (
    <div className="relative select-none flex justify-center items-center p-4 bg-[#121214] rounded-xl border border-[#23232f]">
      {/* Formation title card overlay */}
      {formation && (
        <div className="absolute top-6 left-8 bg-[#1e1e29]/90 backdrop-blur border border-[#34344a] px-5 py-2 rounded-lg">
          <span className="text-xs uppercase tracking-wider text-[#b3b3cb] font-semibold">Formation Snap</span>
          <h3 className="text-lg font-bold text-white border-b-2 border-[#ff2a7f] pb-0.5">{formation.name}</h3>
        </div>
      )}

      {/* SVG Canvas Drawing */}
      <svg
        ref={svgRef}
        width={width}
        height={height}
        className="bg-[#171721] rounded-2xl cursor-default overflow-visible"
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUpOrLeave}
        onMouseLeave={handleMouseUpOrLeave}
      >
        {/* Background Grid */}
        <GridLines width={width} height={height} />

        {/* Central Red X Focal Marker */}
        {(() => {
          const centerCoords = getCoordinates(0, 0);
          return <CenterMarker x={centerCoords.x} y={centerCoords.y} size={22} />;
        })()}

        {/* Backdrop Side Direction Titles (BACKSTAGE / AUDIENCE) */}
        <StageLabels width={width} height={height} />

        {/* Dancers Placements Coordinates Nodes */}
        {dancers.map((dancer, index) => {
          const pos = positionsMap.find((p) => p.dancer_id === dancer.id);
          if (!pos) return null;

          const coords = getCoordinates(pos.x, pos.y);
          const color = dancer.color || getDancerColor(index);
          const isSelected = selectedDancerId === dancer.id;
          const isDancerDragging = isDragging && activeDancerId === dancer.id;

          return (
            <DancerIcon
              key={dancer.id}
              dancer={dancer}
              x={coords.x}
              y={coords.y}
              color={color}
              isSelected={isSelected}
              isDragging={isDancerDragging}
              onMouseDown={() => startDrag(dancer.id)}
              onClick={onSelectDancer}
            />
          );
        })}

        {/* Gorgeous Pink rounded bounding boundary ring */}
        <StageBorder width={width} height={height} />
      </svg>
    </div>
  );
};

export default StageGrid;
