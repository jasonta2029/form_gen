/**
 * @file client.js
 * @description Shared Axios instance for the FormFlow API.
 *
 * Features:
 *   - Base URL pulled from VITE_API_URL environment variable.
 *   - Request interceptor: attaches auth token (when implemented), logs requests.
 *   - Response interceptor: unwraps `data` envelope, normalises errors.
 *
 * Usage:
 *   import apiClient from '@/api/client';
 *   const res = await apiClient.get('/projects');
 */

import axios from 'axios';

/** Base URL defaults to /api so the Vite proxy handles it in dev. */
const BASE_URL = import.meta.env.VITE_API_URL || '/api';

/**
 * Pre-configured Axios instance used by all API modules.
 */
const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 15_000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/* ---------------------------------------------------------------------------
 * Request Interceptor
 * -------------------------------------------------------------------------*/
apiClient.interceptors.request.use(
  (config) => {
    // TODO: If authentication is added later, attach the token here.
    // const token = localStorage.getItem('auth_token');
    // if (token) config.headers.Authorization = `Bearer ${token}`;

    if (import.meta.env.DEV) {
      console.debug(`[API] ${config.method?.toUpperCase()} ${config.url}`, config.params ?? '');
    }

    return config;
  },
  (error) => Promise.reject(error),
);

/* ---------------------------------------------------------------------------
 * Response Interceptor
 * -------------------------------------------------------------------------*/
apiClient.interceptors.response.use(
  (response) => {
    // Unwrap the response body — API is expected to return { data, meta? }.
    return response.data;
  },
  (error) => {
    // Normalise the error payload for consumers.
    const normalised = {
      status: error.response?.status ?? 0,
      message:
        error.response?.data?.message ??
        error.message ??
        'An unexpected network error occurred.',
      details: error.response?.data?.errors ?? null,
    };

    if (import.meta.env.DEV) {
      console.error('[API Error]', normalised);
    }

    return Promise.reject(normalised);
  },
);

export default apiClient;
