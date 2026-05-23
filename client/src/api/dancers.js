/**
 * @file dancers.js
 * @description API functions for Dancer management within a project.
 *
 * Each dancer has an id, name, display number, and assigned colour index.
 * Dancers belong to a Project; their per-formation positions live in Formation.positions[].
 *
 * Endpoints:
 *   GET    /projects/:pid/dancers            — list all dancers
 *   POST   /projects/:pid/dancers            — add a dancer
 *   PUT    /projects/:pid/dancers/:did        — update dancer info
 *   DELETE /projects/:pid/dancers/:did        — remove dancer
 */

import apiClient from './client';

/**
 * Fetch all dancers belonging to a project.
 * @param {string} projectId
 * @returns {Promise<Array<Object>>} Array of dancer objects.
 */
export async function getDancers(projectId) {
  return apiClient.get(`/projects/${projectId}/dancers`);
}

/**
 * Add a new dancer to the project.
 * @param {string} projectId
 * @param {Object} data
 * @param {string}  data.name       — Display name.
 * @param {number}  [data.number]   — Display number (auto-assigned if omitted).
 * @param {number}  [data.colorIdx] — Colour palette index.
 * @returns {Promise<Object>} The created dancer.
 */
export async function addDancer(projectId, data) {
  return apiClient.post(`/projects/${projectId}/dancers`, data);
}

/**
 * Update a dancer's information (name, number, colour, etc.).
 * @param {string} projectId
 * @param {string} dancerId
 * @param {Object} data — Fields to update.
 * @returns {Promise<Object>} Updated dancer.
 */
export async function updateDancer(projectId, dancerId, data) {
  return apiClient.put(`/projects/${projectId}/dancers/${dancerId}`, data);
}

/**
 * Remove a dancer from the project and all formations.
 * @param {string} projectId
 * @param {string} dancerId
 * @returns {Promise<void>}
 */
export async function removeDancer(projectId, dancerId) {
  return apiClient.delete(`/projects/${projectId}/dancers/${dancerId}`);
}
