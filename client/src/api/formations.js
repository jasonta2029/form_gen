/**
 * @file formations.js
 * @description API functions for Formation CRUD and reorder operations.
 *
 * A "Formation" is a single snapshot of dancer positions on the stage.
 * Formations belong to a Project and are ordered sequentially.
 *
 * Endpoints:
 *   GET    /projects/:pid/formations                — list formations
 *   POST   /projects/:pid/formations                — create formation
 *   PUT    /projects/:pid/formations/:fid            — update formation
 *   DELETE /projects/:pid/formations/:fid            — delete formation
 *   PUT    /projects/:pid/formations/reorder          — reorder formations
 */

import apiClient from './client';

/**
 * Fetch all formations for a project, ordered by sequence.
 * @param {string} projectId
 * @returns {Promise<Array<Object>>}
 */
export async function getFormations(projectId) {
  return apiClient.get(`/projects/${projectId}/formations`);
}

/**
 * Create a new formation.
 * @param {string} projectId
 * @param {Object} data
 * @param {string}  data.name      — Display name (e.g. "Chorus – V Shape").
 * @param {number}  [data.order]   — Insert position; appended if omitted.
 * @param {Array}   data.positions — Array of { dancerId, x, y }.
 * @returns {Promise<Object>} Created formation.
 */
export async function createFormation(projectId, data) {
  return apiClient.post(`/projects/${projectId}/formations`, data);
}

/**
 * Update an existing formation (positions, name, etc.).
 * @param {string} projectId
 * @param {string} formationId
 * @param {Object} data — Partial update payload.
 * @returns {Promise<Object>} Updated formation.
 */
export async function updateFormation(projectId, formationId, data) {
  return apiClient.put(`/projects/${projectId}/formations/${formationId}`, data);
}

/**
 * Delete a formation.
 * @param {string} projectId
 * @param {string} formationId
 * @returns {Promise<void>}
 */
export async function deleteFormation(projectId, formationId) {
  return apiClient.delete(`/projects/${projectId}/formations/${formationId}`);
}

/**
 * Reorder formations within a project.
 * @param {string}   projectId
 * @param {string[]} formationIds — Formation IDs in desired order.
 * @returns {Promise<void>}
 */
export async function reorderFormations(projectId, formationIds) {
  return apiClient.put(`/projects/${projectId}/formations/reorder`, {
    formation_ids: formationIds,
  });
}
