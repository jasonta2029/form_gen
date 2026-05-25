/**
 * @file App.jsx
 * @description Root application component.
 *
 * Responsibilities:
 *   1. Define top-level routes (Dashboard, ProjectEditor, ExportView).
 *   2. Wrap all pages in a persistent <Layout /> shell (Header + Sidebar + content).
 *   3. Provide global context providers (ProjectContext, StageContext).
 *
 * Route map:
 *   /                        → Dashboard   — project listing & creation
 *   /project/:id             → ProjectEditor — main stage editor
 *   /project/:id/export      → ExportView  — export preview & download
 */

import React from 'react';
import { Routes, Route } from 'react-router-dom';

// Layout
import Layout from './components/layout/Layout';

// Pages
import Dashboard from './pages/Dashboard';
import ProjectEditor from './pages/ProjectEditor';
import ExportView from './pages/ExportView';

// Context providers
import { ProjectProvider } from './context/ProjectContext';
import { StageProvider } from './context/StageContext';
import { ToastProvider } from './context/ToastContext';

/**
 * App — root component rendered by main.jsx.
 * Wraps pages in context providers and layout shell.
 */
export default function App() {
  return (
    <ToastProvider>
    <ProjectProvider>
      <StageProvider>
        <Layout>
          <Routes>
            {/* Home / project list */}
            <Route path="/" element={<Dashboard />} />

            {/* Main editor — stage view, formations, AI tools */}
            <Route path="/project/:id" element={<ProjectEditor />} />

            {/* Export preview & download */}
            <Route path="/project/:id/export" element={<ExportView />} />
          </Routes>
        </Layout>
      </StageProvider>
    </ProjectProvider>
    </ToastProvider>
  );
}
