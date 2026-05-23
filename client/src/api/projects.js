/**
 * @file projects.js
 * @description API functions for Project CRUD operations.
 *
 * A "Project" is the top-level entity in FormFlow — it owns a set of dancers,
 * formations, and settings (stage dimensions, music file, etc.).
 *
 * Endpoints (relative to apiClient.baseURL):
 *   GET    /projects            — list all projects
 *   GET    /projects/:id        — single project with populated formations
 *   POST   /projects            — create new project
 *   PUT    /projects/:id        — update project metadata / settings
 *   DELETE /projects/:id        — delete project and all children
 */

import apiClient from './client';

/**
 * Fetch all projects for the current user.
 * @returns {Promise<Array<Object>>} Array of project summary objects.
 */
export async function getProjects() {
  return apiClient.get('/projects');
}

/**
 * Fetch a single project by ID, including its formations and dancers.
 * @param {string} id — Project ID.
 * @returns {Promise<Object>} Full project document.
 */
export async function getProject(id) {
  return apiClient.get(`/projects/${id}`);
}

/**
 * Create a new project.
 * @param {Object} data — Initial project data.
 * @param {string} data.name          — Project name.
 * @param {number} [data.stageWidth]  — Stage width in grid units (default 20).
 * @param {number} [data.stageHeight] — Stage height in grid units (default 12).
 * @param {number} [data.dancerCount] — Number of dancers to generate.
 * @returns {Promise<Object>} The created project.
 */
export async function createProject(data) {
  return apiClient.post('/projects', data);
}

/**
 * Update an existing project.
 * @param {string} id   — Project ID.
 * @param {Object} data — Fields to update (name, stage dimensions, etc.).
 * @returns {Promise<Object>} The updated project.
 */
export async function updateProject(id, data) {
  return apiClient.put(`/projects/${id}`, data);
}

/**
 * Delete a project and all associated formations / dancer data.
 * @param {string} id — Project ID.
 * @returns {Promise<void>}
 */
export async function deleteProject(id) {
  return apiClient.delete(`/projects/${id}`);
}
