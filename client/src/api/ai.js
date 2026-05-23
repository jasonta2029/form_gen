/**
 * ai.js — API client for AI formation and transition suggestions.
 */
import client from './client';

export const aiApi = {
  /**
   * Generates a new formation based on parameters (style, symmetry, etc.)
   * @param {string|number} projectId 
   * @param {object} params — { style, density, symmetry, focal_point }
   */
  generateFormation: async (projectId, params) => {
    const response = await client.post(`/projects/${projectId}/ai/generate`, params);
    return response.data;
  },

  /**
   * Generates transitions path routing between formations to minimize crossings
   * @param {string|number} projectId 
   * @param {object} params — { from_formation_id, to_formation_id }
   */
  suggestTransitions: async (projectId, params) => {
    const response = await client.post(`/projects/${projectId}/ai/suggest-transitions`, params);
    return response.data;
  },

  /**
   * Generates coordinate offsets based on standard geometric formation templates
   * @param {string|number} projectId 
   * @param {string} templateName — V_SHAPE, ARC, CLUSTER, SPLIT, DIAGONAL, LINE, CIRCLE, DIAMOND, SCATTER
   * @param {object} params — additional geometry custom parameters
   */
  generateFromTemplate: async (projectId, templateName, params = {}) => {
    const response = await client.post(`/projects/${projectId}/ai/template`, {
      template_name: templateName,
      params,
    });
    return response.data;
  }
};

export default aiApi;
