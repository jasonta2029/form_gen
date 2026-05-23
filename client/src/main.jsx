/**
 * @file main.jsx
 * @description Application entry point.
 *
 * Mounts the root <App /> component inside:
 *   - React.StrictMode  — highlights potential problems during development
 *   - BrowserRouter     — enables client-side routing via react-router-dom
 *
 * Global CSS is imported here so it applies to the entire app tree.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
);
