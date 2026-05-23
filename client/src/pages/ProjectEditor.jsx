/**
 * ProjectEditor.jsx — The ultimate choreography sandbox workspace.
 * Ties StageGrid canvases, timeline controllers, dancer roster sheets, AI presets,
 * and audio markers sync tools together.
 */
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useProject } from '../context/ProjectContext';
import { useCenterTime } from '../hooks/useCenterTime';
import StageGrid from '../components/stage/StageGrid';
import DancerPanel from '../components/dancers/DancerPanel';
import FormationTimeline from '../components/formations/FormationTimeline';
import AIPanel from '../components/ai/AIPanel';
import CenterTimePanel from '../components/centerTime/CenterTimePanel';
import MusicTimeline from '../components/music/MusicTimeline';
import ExportPanel from '../components/export/ExportPanel';
import LoadingSpinner from '../components/common/LoadingSpinner';
import exportApi from '../api/exportApi';

export const ProjectEditor = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const {
    currentProject,
    dancers,
    formations,
    selectedFormationId,
    selectedFormation,
    setSelectedFormationId,
    isLoading,
    loadProject,
    addDancer,
    removeDancer,
    createFormation,
    updateDancerPositions
  } = useProject();

  const { stats, rebalance, refreshStats } = useCenterTime(id);
  const [activeTab, setActiveTab] = useState('dancers'); // dancers | ai | balance | export
  const [selectedDancerId, setSelectedDancerId] = useState(null);

  useEffect(() => {
    if (id) {
      loadProject(id);
    }
  }, [id]);

  const handleDancerMove = (dancerId, newX, newY) => {
    if (!selectedFormation) return;
    const updatedPos = (selectedFormation.positions || []).map((p) => {
      if (p.dancer_id === dancerId) {
        return { ...p, x: newX, y: newY };
      }
      return p;
    });
    updateDancerPositions(selectedFormation.id, updatedPos);
    // Reload residency exposure stats
    setTimeout(refreshStats, 300);
  };

  const handleAddNewSnap = () => {
    // Scaffold default locations for dancers
    const initialPos = dancers.map((d, i) => ({
      dancer_id: d.id,
      x: (i - (dancers.length - 1) / 2) * 2.0,
      y: 0.0
    }));
    createFormation({
      name: `Snap ${formations.length + 1}`,
      timestamp_start: formations.length * 4.5,
      timestamp_end: (formations.length + 1) * 4.5,
      positions: initialPos
    });
  };

  const handleApplyGeometricTemplate = async (templateName, params) => {
    if (!selectedFormation) return;
    try {
      const response = await client.post(`/projects/${id}/ai/template`, {
        template_name: templateName,
        params
      });
      updateDancerPositions(selectedFormation.id, response.formation.positions);
      setTimeout(refreshStats, 300);
    } catch (err) {
      console.error(err);
      alert("Failed to apply AI preset coordinates.");
    }
  };

  if (isLoading || !currentProject) {
    return (
      <div className="min-h-screen bg-[#121214] flex items-center justify-center">
        <LoadingSpinner message="Entering Studio Sandbox..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#121214] text-white flex flex-col font-sans">
      
      {/* Top Navbar */}
      <header className="bg-[#1a1a24] border-b border-[#23232f] px-6 py-4 flex items-center justify-between select-none">
        <div className="flex items-center space-x-5">
          <h1 
            onClick={() => navigate('/')} 
            className="text-xl font-black cursor-pointer tracking-tight"
          >
            Form<span className="text-[#ff2a7f]">Flow</span>
          </h1>
          <div className="w-px h-5 bg-[#34344a]" />
          <div>
            <h2 className="font-bold text-sm text-white">{currentProject.name}</h2>
            <span className="text-[10px] text-[#b3b3cb] uppercase tracking-wider font-medium">
              Choreography Studio Workspace
            </span>
          </div>
        </div>

        <button 
          onClick={() => navigate('/')} 
          className="text-xs bg-[#2b2b3a] hover:bg-[#34344d] px-3.5 py-1.5 rounded-lg border border-[#3e3e56]"
        >
          🗂 Back to Projects
        </button>
      </header>

      {/* Main Sandbox Grids split layouts */}
      <main className="flex-1 grid grid-cols-12 p-6 gap-6 h-[calc(100vh-72px)] overflow-hidden">
        
        {/* Left Side column tool controls tabs panels (4 columns) */}
        <section className="col-span-4 flex flex-col space-y-4 overflow-hidden h-full">
          {/* Tab selector buttons */}
          <div className="grid grid-cols-4 gap-1.5 bg-[#171721] p-1 rounded-xl border border-[#23232f] select-none">
            {[
              { id: 'dancers', label: '👤 Roster' },
              { id: 'ai', label: '✨ AI Preset' },
              { id: 'balance', label: '⚖ Balance' },
              { id: 'export', label: '📄 Export' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 rounded-lg text-[10px] font-bold uppercase transition-all ${
                  activeTab === tab.id
                    ? 'bg-[#ff2a7f] text-white'
                    : 'bg-transparent text-[#b3b3cb] hover:bg-[#1a1a24]'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <div className="flex-1 overflow-y-auto">
            {activeTab === 'dancers' && (
              <DancerPanel
                dancers={dancers}
                centerTimeStats={stats}
                onAddDancer={addDancer}
                onRemoveDancer={removeDancer}
                selectedDancerId={selectedDancerId}
                onSelectDancer={setSelectedDancerId}
              />
            )}

            {activeTab === 'ai' && (
              <AIPanel
                dancersCount={dancers.length}
                onApplyTemplate={handleApplyGeometricTemplate}
              />
            )}

            {activeTab === 'balance' && (
              <CenterTimePanel
                stats={stats}
                dancers={dancers}
                onRebalance={async (w) => {
                  await rebalance(w);
                  loadProject(id);
                }}
              />
            )}

            {activeTab === 'export' && (
              <ExportPanel
                activeFormationId={selectedFormationId}
                onExportPDF={async (inc, sz) => {
                  try {
                    const blob = await exportApi.exportAsPDF(id, inc);
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `formflow-${currentProject.name}.pdf`;
                    a.click();
                  } catch (err) {
                    alert("Failed to build PDF catalog.");
                  }
                }}
              />
            )}
          </div>
        </section>

        {/* Center stage workspace and timeline sequencing (8 columns) */}
        <section className="col-span-8 flex flex-col space-y-4 overflow-y-auto h-full pr-1">
          {/* Main Visual Stage canvas grid */}
          <div className="flex-1 min-h-[480px]">
            <StageGrid
              project={currentProject}
              dancers={dancers}
              formation={selectedFormation}
              selectedDancerId={selectedDancerId}
              onSelectDancer={setSelectedDancerId}
              onDancerMove={handleDancerMove}
              width={800}
              height={480}
            />
          </div>

          {/* Audio stream wave indicators markers syncing */}
          <MusicTimeline
            audioSrc={currentProject.audio_file_path}
            duration={60.0}
            currentTime={selectedFormation ? selectedFormation.timestamp_start : 0.0}
          />

          {/* Timelines Snapshots row */}
          <FormationTimeline
            formations={formations}
            selectedId={selectedFormationId}
            onSelect={setSelectedFormationId}
            onCreateNew={handleAddNewSnap}
          />
        </section>

      </main>
    </div>
  );
};

export default ProjectEditor;
//
