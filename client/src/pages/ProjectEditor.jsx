/**
 * ProjectEditor.jsx — The ultimate choreography sandbox workspace.
 */
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Users, Sparkles, Scale, FileDown, FolderOpen } from 'lucide-react';
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
import aiApi from '../api/ai';

const TABS = [
  { id: 'dancers', label: 'Roster',  Icon: Users },
  { id: 'ai',      label: 'AI',      Icon: Sparkles },
  { id: 'balance', label: 'Balance', Icon: Scale },
  { id: 'export',  label: 'Export',  Icon: FileDown },
];

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
    deleteFormation,
    duplicateFormation,
    updateDancerPositions
  } = useProject();

  const { stats, rebalance, refreshStats } = useCenterTime(id);
  const [activeTab, setActiveTab] = useState('dancers');
  const [selectedDancerId, setSelectedDancerId] = useState(null);

  useEffect(() => {
    if (id) loadProject(id);
  }, [id]);

  const handleDancerMove = (dancerId, newX, newY) => {
    if (!selectedFormation) return;
    const updatedPos = (selectedFormation.positions || []).map((p) =>
      p.dancer_id === dancerId ? { ...p, x: newX, y: newY } : p
    );
    updateDancerPositions(selectedFormation.id, updatedPos);
    setTimeout(refreshStats, 300);
  };

  const handleAddNewSnap = () => {
    const initialPos = dancers.map((d, i) => ({
      dancer_id: d.id,
      x: (i - (dancers.length - 1) / 2) * 2.0,
      y: 0.0,
    }));
    createFormation({
      name: `Snap ${formations.length + 1}`,
      timestamp_start: formations.length * 4.5,
      timestamp_end: (formations.length + 1) * 4.5,
      positions: initialPos,
    });
  };

  const handleApplyGeometricTemplate = async (templateName, params) => {
    if (!selectedFormation) return;
    try {
      // Backend returns a flat list of {dancer_id, x, y} indexed 1..N.
      // Remap onto the formation's actual dancer IDs (by position order).
      const templatePositions = await aiApi.generateFromTemplate(id, templateName, params);
      const existing = selectedFormation.positions || [];
      const remapped = templatePositions.map((tp, idx) => {
        const orig = existing[idx];
        return orig ? { ...orig, x: tp.x, y: tp.y } : tp;
      });
      updateDancerPositions(selectedFormation.id, remapped);
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
          className="flex items-center gap-2 text-xs bg-[#2b2b3a] hover:bg-[#34344d] px-3.5 py-1.5 rounded-lg border border-[#3e3e56] cursor-pointer transition-colors"
        >
          <FolderOpen size={13} />
          Back to Projects
        </button>
      </header>

      {/* Main workspace */}
      <main className="flex-1 grid grid-cols-12 p-6 gap-6 h-[calc(100vh-72px)] overflow-hidden">

        {/* Left panel — tabs */}
        <section className="col-span-4 flex flex-col space-y-4 overflow-hidden h-full">
          {/* Tab bar */}
          <div className="flex bg-[#171721] p-1 rounded-xl border border-[#23232f] select-none gap-1">
            {TABS.map(({ id: tabId, label, Icon }) => (
              <button
                key={tabId}
                onClick={() => setActiveTab(tabId)}
                className={`flex-1 flex flex-col items-center gap-1 py-2.5 rounded-lg text-[10px] font-bold uppercase tracking-wide transition-all cursor-pointer ${
                  activeTab === tabId
                    ? 'bg-[#ff2a7f] text-white shadow'
                    : 'bg-transparent text-[#6b6b8a] hover:text-[#b3b3cb] hover:bg-[#1e1e2c]'
                }`}
              >
                <Icon size={14} />
                {label}
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
                onExportPDF={async (inc) => {
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

        {/* Right — stage + timeline */}
        <section className="col-span-8 flex flex-col space-y-4 overflow-y-auto h-full pr-1">
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

          <MusicTimeline
            audioSrc={currentProject.audio_file_path}
            duration={60.0}
            currentTime={selectedFormation ? (selectedFormation.timestamp_start ?? 0) : 0.0}
          />

          <FormationTimeline
            formations={formations}
            selectedId={selectedFormationId}
            onSelect={setSelectedFormationId}
            onCreateNew={handleAddNewSnap}
            onDuplicate={duplicateFormation}
            onDelete={deleteFormation}
          />
        </section>

      </main>
    </div>
  );
};

export default ProjectEditor;
