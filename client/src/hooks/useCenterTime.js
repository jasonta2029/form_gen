/**
 * useCenterTime.js — Custom hook coordinating center-stage exposure scores, flags, and weight updates.
 */
import { useState, useEffect, useCallback } from 'react';
import centerTimeApi from '../api/centerTime';

export const useCenterTime = (projectId) => {
  const [stats, setStats] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [thresholdRadius, setThresholdRadius] = useState(2.5);

  const loadStats = useCallback(async () => {
    if (!projectId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await centerTimeApi.getCenterTimeStats(projectId);
      setStats(data.stats || []);
      setThresholdRadius(data.threshold_radius || 2.5);
    } catch (err) {
      console.error("Failed to load center-time metrics:", err);
      setError("Failed to fetch center balancing data.");
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  const triggerRebalance = useCallback(async (targetWeights, strategy = 'equal') => {
    if (!projectId) return;
    setLoading(true);
    try {
      const response = await centerTimeApi.rebalanceCenterTime(projectId, targetWeights, strategy);
      // Reload stats after adjustments
      await loadStats();
      return response.suggested_changes;
    } catch (err) {
      console.error("Failed to execute balance algorithm:", err);
      setError("Failed to adjust dancer mappings.");
      throw err;
    } finally {
      setLoading(false);
    }
  }, [projectId, loadStats]);

  useEffect(() => {
    loadStats();
  }, [loadStats]);

  return {
    stats,
    loading,
    error,
    thresholdRadius,
    refreshStats: loadStats,
    rebalance: triggerRebalance,
  };
};

export default useCenterTime;
