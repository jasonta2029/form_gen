/**
 * ExportPanel.jsx — Sidebar subpanel triggering PDF books generation,
 * image snapshots packages, and custom layouts dimensions settings.
 */
import React, { useState } from 'react';

export const ExportPanel = ({
  onExportPDF,
  onExportZip,
  onExportSingle,
  activeFormationId = null
}) => {
  const [includeTransitions, setIncludeTransitions] = useState(true);
  const [pageSize, setPageSize] = useState('letter');

  return (
    <div className="flex flex-col bg-[#1a1a24] text-white p-4 rounded-xl border border-[#23232f] space-y-4">
      <div className="border-b border-[#2d2d3d] pb-2.5">
        <h3 className="font-bold text-md tracking-wide">Export Sheets Manager</h3>
        <p className="text-[10px] text-[#b3b3cb] mt-1">
          Compile formations sequence into print-ready PDF sheets booklets or PNG zip bundles.
        </p>
      </div>

      <div className="bg-[#212130] p-3 rounded-lg border border-[#29293a] space-y-3 text-xs text-left">
        {/* Transition flags */}
        <div className="flex items-center justify-between">
          <span className="text-[#b3b3cb] text-[10px] uppercase font-semibold">Include Path Routes</span>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={includeTransitions}
              onChange={(e) => setIncludeTransitions(e.target.checked)}
              className="sr-only peer"
            />
            <div className="w-9 h-5 bg-[#171721] rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-[#b3b3cb] after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#ff2a7f]" />
          </label>
        </div>

        {/* Page size settings options selection */}
        <div>
          <span className="text-[#b3b3cb] text-[10px] uppercase font-semibold block mb-1">Page Format</span>
          <select
            value={pageSize}
            onChange={(e) => setPageSize(e.target.value)}
            className="w-full bg-[#171721] border border-[#2d2d3d] text-white px-2.5 py-1.5 rounded text-xs focus:outline-none focus:border-[#ff2a7f]"
          >
            <option value="letter">US Letter (Landscape)</option>
            <option value="a4">A4 Standard (Landscape)</option>
          </select>
        </div>
      </div>

      <div className="space-y-2 pt-1.5">
        <button
          onClick={() => onExportPDF && onExportPDF(includeTransitions, pageSize)}
          className="w-full bg-[#ff2a7f] hover:bg-[#e0206f] text-white font-bold py-2.5 rounded-lg text-xs transition-colors flex items-center justify-center space-x-1"
        >
          <span>📄 Generate PDF Booklet</span>
        </button>

        <button
          onClick={() => onExportZip && onExportZip()}
          className="w-full bg-[#272739] hover:bg-[#34344d] border border-[#3e3e56] text-xs py-2 rounded-lg transition-colors text-[#b3b3cb] font-semibold"
        >
          Download PNG Snapshots Bundle (.zip)
        </button>
      </div>
    </div>
  );
};

export default ExportPanel;
