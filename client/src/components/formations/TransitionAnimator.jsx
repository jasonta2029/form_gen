/**
 * TransitionAnimator.jsx — Handles timeline interpolation calculations
 * to preview path movement animations.
 */
import React, { useEffect, useState } from 'react';

export const TransitionAnimator = ({
  fromFormation = null,
  toFormation = null,
  duration = 3.0,
  isPlaying = false,
  onComplete
}) => {
  const [progress, setProgress] = useState(0.0);

  useEffect(() => {
    if (!isPlaying) {
      setProgress(0.0);
      return;
    }

    let start = null;
    let animId = null;

    const step = (timestamp) => {
      if (!start) start = timestamp;
      const elapsed = (timestamp - start) / 1000.0;
      const nextProgress = Math.min(1.0, elapsed / duration);
      
      setProgress(nextProgress);
      
      if (nextProgress < 1.0) {
        animId = requestAnimationFrame(step);
      } else {
        if (onComplete) onComplete();
      }
    };

    animId = requestAnimationFrame(step);

    return () => {
      if (animId) cancelAnimationFrame(animId);
    };
  }, [isPlaying, duration, onComplete]);

  return (
    <div className="bg-[#212130] p-3.5 rounded-lg border border-[#29293a] text-xs text-left">
      <div className="flex items-center justify-between mb-2">
        <span className="text-[#b3b3cb] font-semibold">Transition Progress</span>
        <span className="font-bold text-[#ff2a7f]">{(progress * 100).toFixed(0)}%</span>
      </div>

      <div className="w-full h-1.5 bg-[#171721] rounded-full overflow-hidden">
        <div 
          className="h-full bg-[#ff2a7f] transition-all duration-75"
          style={{ width: `${progress * 100}%` }}
        />
      </div>
    </div>
  );
};

export default TransitionAnimator;
