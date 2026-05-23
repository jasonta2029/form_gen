/**
 * ExportView.jsx — Fullscreen preview of printable sheets and download catalog.
 */
import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';

export const ExportView = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[#121214] text-white p-8 text-left select-none">
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="flex items-center justify-between border-b border-[#23232f] pb-4">
          <h2 className="text-2xl font-bold">Printable Sheets Booklet</h2>
          <button 
            onClick={() => navigate(`/project/${id}`)}
            className="text-xs bg-[#2b2b3a] hover:bg-[#34344d] px-3.5 py-1.5 rounded-lg border border-[#3e3e56]"
          >
            ➜ Return to Studio
          </button>
        </div>

        <div className="bg-[#1a1a24] border border-[#23232f] p-8 rounded-2xl flex flex-col items-center justify-center space-y-4 min-h-[300px]">
          <span className="text-lg font-bold">Show Formation Catalog Ready</span>
          <p className="text-xs text-[#b3b3cb]">
            All snapshots generated and cached. Select format settings options inside active Studio export tab to download.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ExportView;
