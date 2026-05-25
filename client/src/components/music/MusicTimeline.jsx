/**
 * MusicTimeline.jsx — Waveform style controller bar displaying track durations,
 * marker flags, and playback triggers.
 */
import React from 'react';

export const MusicTimeline = ({
  audioSrc = '',
  markers = [],
  currentTime = 0,
  duration = 0,
  onSeek,
  onTogglePlay,
  isPlaying = false,
  onAddMarker
}) => {
  const progressPercent = duration > 0 ? (currentTime / duration) * 100 : 0;

  const handleTimelineClick = (e) => {
    if (duration === 0) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const seekTime = (clickX / rect.width) * duration;
    if (onSeek) onSeek(seekTime);
  };

  const handleAddMarkerPrompt = () => {
    const markerName = prompt("Enter bookmark description:", `Marker @ ${(currentTime ?? 0).toFixed(1)}s`);
    if (markerName && onAddMarker) {
      onAddMarker({ name: markerName, timestamp: currentTime });
    }
  };

  return (
    <div className="bg-[#1a1a24] p-4 rounded-xl border border-[#23232f] text-white flex flex-col space-y-3 select-none">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3.5">
          {/* Play state trigger buttons */}
          <button
            onClick={onTogglePlay}
            disabled={!audioSrc}
            className={`w-9 h-9 rounded-full flex items-center justify-center font-bold text-white transition-colors ${
              isPlaying ? 'bg-[#ff2a7f] hover:bg-[#e0206f]' : 'bg-[#10b981] hover:bg-[#0ea271]'
            } disabled:opacity-50`}
          >
            {isPlaying ? '⏸' : '▶'}
          </button>

          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-[#b3b3cb]">Music Track Player</h4>
            <span className="text-xs font-semibold text-white">
              {(currentTime ?? 0).toFixed(1)}s / {duration > 0 ? duration.toFixed(1) : '0.0'}s
            </span>
          </div>
        </div>

        <button
          onClick={handleAddMarkerPrompt}
          disabled={duration === 0}
          className="bg-[#272739] hover:bg-[#34344d] border border-[#3e3e56] text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors text-[#b3b3cb] disabled:opacity-40"
        >
          ⏱ Drop Annotation
        </button>
      </div>

      {/* Waveform timeline track container */}
      <div className="relative pt-3 pb-1">
        <div
          onClick={handleTimelineClick}
          className="h-10 w-full bg-[#161622] rounded-lg border border-[#232331] cursor-pointer relative overflow-visible flex items-center"
        >
          {/* Mock simulated visual sound waves bars */}
          <div className="absolute inset-0 flex items-center justify-around px-2 opacity-20 pointer-events-none">
            {Array.from({ length: 48 }).map((_, i) => {
              const h = Math.sin(i * 0.45) * 16 + 20;
              return <div key={i} className="w-0.5 bg-[#ff2a7f] rounded-full" style={{ height: `${h}px` }} />;
            })}
          </div>

          {/* Played progress fill overlays */}
          <div
            className="h-full bg-[#ff2a7f]/10 border-r-2 border-[#ff2a7f] absolute top-0 left-0 pointer-events-none transition-all duration-75"
            style={{ width: `${progressPercent}%` }}
          />

          {/* Bookmark Annotations pins overlays */}
          {markers.map((marker) => {
            const pct = duration > 0 ? (marker.timestamp / duration) * 100 : 0;
            return (
              <div
                key={marker.id}
                className="absolute bottom-full mb-1 flex flex-col items-center group pointer-events-auto cursor-help"
                style={{ left: `${pct}%`, transform: 'translateX(-50%)' }}
              >
                {/* Visual anchor flag */}
                <div className="w-2.5 h-2.5 bg-[#10b981] border border-[#171721] rounded-full filter drop-shadow" />
                <div className="w-0.5 h-4 bg-[#10b981]/60 absolute top-2" />
                
                {/* Popover helper text metadata annotation */}
                <span className="absolute bottom-full mb-1 bg-[#1e1e29] border border-[#34344a] text-[9px] font-bold text-white px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-50">
                  {marker.name} ({marker.timestamp.toFixed(1)}s)
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default MusicTimeline;
