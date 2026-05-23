/**
 * centerTime.js — API client for dancer center-stage residency metrics and balancing.
 */
import client from './client';

export const centerTimeApi = {
  /**
   * Retrieves overall center-time exposure metrics for all dancers in a project
   * @param {string|number} projectId 
   */
  getCenterTimeStats: async (projectId) => {
    const response = await client.get(`/projects/${projectId}/center-time`);
    return response.data;
  },

  /**
   * Retrieves a single dancer's detailed residency breakdown across snapshots
   * @param {string|number} projectId 
   * @param {string|number} dancerId 
   */
  getCenterTimeForDancer: async (projectId, dancerId) => {
    const response = await client.get(`/projects/${projectId}/center-time/${dancerId}`);
    return response.data;
  },

  /**
   * Posts weights to rebalance placements and reduce deviations automatically
   * @param {string|number} projectId 
   * @param {object} targetWeights — { [dancerId]: float_weight }
   * @param {string} strategy — 'equal' | 'weighted'
   */
  rebalanceCenterTime: async (projectId, targetWeights, strategy = 'equal') => {
    const response = await client.post(`/projects/${projectId}/center-time/rebalance`, {
      target_weights: targetWeights,
      strategy,
    });
    return response.data;
  }
};

export default centerTimeApi;
