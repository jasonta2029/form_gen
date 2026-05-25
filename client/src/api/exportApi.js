/**
 * exportApi.js — API client for generating downloadable images and PDF timeline books.
 */
import client from './client';

export const exportApi = {
  /**
   * Triggers generation of high-res image representing a single formation snapshot
   * @param {string|number} projectId 
   * @param {string|number} formationId 
   * @param {string} format — 'png' | 'jpg'
   */
  exportAsImage: async (projectId, formationId, format = 'png') => {
    const response = await client.post(`/projects/${projectId}/export/image`, {
      formation_id: formationId,
      format,
    }, { responseType: 'blob' });
    return response;
  },

  /**
   * Requests a generated PDF document detailing the complete formation sequence
   * @param {string|number} projectId 
   * @param {boolean} includeTransitions 
   */
  exportAsPDF: async (projectId, includeTimeline = true) => {
    const response = await client.post(`/projects/${projectId}/export/pdf`, {
      include_timeline: includeTimeline,
    }, { responseType: 'blob' });
    return response;
  },

  /**
   * Request structured archive including image sheets for all formations
   * @param {string|number} projectId 
   */
  exportAllFormations: async (projectId) => {
    const response = await client.post(`/projects/${projectId}/export/all`, {}, { responseType: 'blob' });
    return response;
  }
};

export default exportApi;
