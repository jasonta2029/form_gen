/**
 * @file vite.config.js
 * @description Vite build configuration for the FormFlow React client.
 *
 * - Uses the official React plugin (fast-refresh + JSX transform).
 * - Dev server runs on port 3000.
 * - All /api requests are proxied to the Express backend on port 5000.
 */

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],

  server: {
    port: 3000,
    open: true, // Auto-open browser on dev start
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      },
    },
  },

  build: {
    outDir: 'dist',
    sourcemap: true,
  },

  resolve: {
    alias: {
      '@': '/src', // Allow absolute imports like @/components/...
    },
  },
});
