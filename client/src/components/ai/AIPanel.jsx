/**
 * AIPanel.jsx — Sidebar subpanel providing AI generators, preset shapes selection,
 * density metrics, and symmetry toggles.
 */
import React, { useState } from 'react';
import TemplateSelector from './TemplateSelector';
import GenerationParams from './GenerationParams';

export const AIPanel = ({
  onApplyTemplate,
  onGenerateAI,
  onSuggestTransitions,
  dancersCount = 0
}) => {
  const [selectedTemplate, setSelectedTemplate] = useState('V_SHAPE');
  const [params, setParams] = useState({
    density: 0.5,
    symmetry: true,
    style: 'balanced'
  });

  return (
    <div className="flex flex-col bg-[#1a1a24] text-white p-4 rounded-xl border border-[#23232f] space-y-4">
      <div className="border-b border-[#2d2d3d] pb-2.5">
        <h3 className="font-bold text-md tracking-wide">AI Placements Studio</h3>
        <p className="text-[10px] text-[#b3b3cb] mt-1">
          Choreograph complex structures dynamically using geometric equations and LLMs.
        </p>
      </div>

      {/* Preset Geometry Templates */}
      <div>
        <label className="block text-[10px] uppercase text-[#b3b3cb] tracking-wider mb-2 font-semibold">
          Select Structural Template
        </label>
        <TemplateSelector
          selected={selectedTemplate}
          onSelect={setSelectedTemplate}
        />
      </div>

      {/* Constraints parameters inputs */}
      <div>
        <label className="block text-[10px] uppercase text-[#b3b3cb] tracking-wider mb-2 font-semibold">
          Constraint Tuning
        </label>
        <GenerationParams
          params={params}
          onChange={setParams}
        />
      </div>

      <div className="pt-2 space-y-2">
        <button
          onClick={() => onApplyTemplate && onApplyTemplate(selectedTemplate, params)}
          className="w-full bg-[#ff2a7f] hover:bg-[#e0206f] text-white font-bold py-2.5 rounded-lg text-xs transition-colors flex items-center justify-center space-x-1.5"
        >
          <span>✨ Apply Layout Preset</span>
        </button>

        <button
          onClick={() => onSuggestTransitions && onSuggestTransitions()}
          className="w-full bg-[#272739] hover:bg-[#34344d] border border-[#3e3e56] text-xs py-2 rounded-lg transition-colors text-white font-medium"
        >
          Detect Path Crossing Routes
        </button>
      </div>
    </div>
  );
};

export default AIPanel;
