import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, ArrowRight, Plus, X, Loader2 } from 'lucide-react';
import projectsApi from '../api/projects';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { useToast } from '../context/ToastContext';

export const Dashboard = () => {
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState(null);

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [projectName, setProjectName] = useState('');
  const [projectDesc, setProjectDesc] = useState('');
  const [numDancers, setNumDancers] = useState(12);

  const fetchProjects = async () => {
    setLoading(true);
    try {
      const data = await projectsApi.getProjects();
      setProjects(data.projects || []);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch project listings.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchProjects(); }, []);

  const handleCreateProject = async (e) => {
    e.preventDefault();
    if (!projectName.trim()) return;
    setCreating(true);
    try {
      const response = await projectsApi.createProject({
        name: projectName.trim(),
        description: projectDesc.trim(),
        num_dancers: parseInt(numDancers),
      });
      showToast(`"${response.name}" created!`, 'success');
      navigate(`/project/${response.id}`);
    } catch (err) {
      console.error(err);
      showToast('Failed to create project', 'error');
    } finally {
      setCreating(false);
    }
  };

  const closeModal = () => {
    setShowCreateModal(false);
    setProjectName('');
    setProjectDesc('');
    setNumDancers(12);
  };

  return (
    <div className="min-h-screen bg-[#121214] text-white p-8 font-sans">
      <div className="max-w-6xl mx-auto space-y-8 select-none">

        {/* Header */}
        <div className="flex items-center justify-between border-b border-[#23232f] pb-6">
          <div>
            <h1 className="text-3xl font-black tracking-tight text-white">
              Form<span className="text-[#ff2a7f]">Flow</span>
            </h1>
            <p className="text-xs text-[#b3b3cb] uppercase tracking-wider font-semibold mt-1">
              AI-Powered Choreography Formation Planner
            </p>
          </div>

          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center gap-2 bg-[#ff2a7f] hover:bg-[#e0206f] text-white font-bold px-5 py-2.5 rounded-lg text-sm transition-all shadow-[0_0_12px_rgba(255,42,127,0.3)] hover:shadow-[0_0_20px_rgba(255,42,127,0.4)] hover:scale-[1.02] cursor-pointer"
          >
            <Plus size={15} />
            Create Studio
          </button>
        </div>

        {/* Project grid */}
        {loading ? (
          <div className="py-24">
            <LoadingSpinner message="Fetching show listings..." />
          </div>
        ) : error ? (
          <div className="text-center py-16 border border-red-500/20 bg-red-500/5 rounded-xl text-red-400">
            <span className="text-sm font-semibold">{error}</span>
          </div>
        ) : projects.length === 0 ? (
          <div className="text-center py-20 bg-[#1a1a24] rounded-2xl border border-[#23232f] space-y-4">
            <p className="text-sm text-[#b3b3cb]">No choreography shows yet.</p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="inline-flex items-center gap-2 bg-[#ff2a7f]/10 border border-[#ff2a7f] text-[#ff2a7f] hover:bg-[#ff2a7f]/20 font-bold px-4 py-2 rounded-lg text-xs transition-colors cursor-pointer"
            >
              <Plus size={13} />
              Start Your First Project
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {projects.map((proj) => (
              <div
                key={proj.id}
                onClick={() => navigate(`/project/${proj.id}`)}
                className="bg-[#1a1a24] border border-[#23232f] hover:border-[#ff2a7f]/60 p-5 rounded-2xl cursor-pointer transition-all hover:scale-[1.02] hover:shadow-[0_0_20px_rgba(255,42,127,0.1)] flex flex-col justify-between h-44 text-left group"
              >
                <div>
                  <h3 className="font-extrabold text-lg truncate text-white">{proj.name}</h3>
                  <p className="text-xs text-[#b3b3cb] line-clamp-2 mt-1.5">{proj.description || 'No description.'}</p>
                </div>

                <div className="flex items-center justify-between border-t border-[#272739] pt-3.5">
                  <span className="flex items-center gap-1.5 text-xs font-bold text-[#b3b3cb]">
                    <Users size={12} />
                    {proj.num_dancers} Dancers
                  </span>
                  <span className="flex items-center gap-1 text-[10px] text-[#6b6b8a] group-hover:text-[#ff2a7f] transition-colors">
                    Edit Studio
                    <ArrowRight size={11} />
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Create modal */}
        {showCreateModal && (
          <div
            className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4"
            onClick={(e) => e.target === e.currentTarget && closeModal()}
          >
            <div className="bg-[#1a1a24] border border-[#2d2d3d] p-6 rounded-2xl w-full max-w-md text-left space-y-4 animate-scale-in">
              <div className="flex items-center justify-between border-b border-[#2d2d3d] pb-3">
                <h3 className="font-extrabold text-lg">Create New Show</h3>
                <button
                  onClick={closeModal}
                  className="text-[#6b6b8a] hover:text-white transition-colors cursor-pointer p-1 rounded"
                  aria-label="Close"
                >
                  <X size={16} />
                </button>
              </div>

              <form onSubmit={handleCreateProject} className="space-y-4 text-xs">
                <div>
                  <label className="block text-[10px] uppercase font-bold text-[#b3b3cb] tracking-wider mb-1.5">
                    Show Title <span className="text-[#ff2a7f]">*</span>
                  </label>
                  <input
                    type="text"
                    value={projectName}
                    onChange={(e) => setProjectName(e.target.value)}
                    placeholder="e.g. She's Confident Tour"
                    className="w-full bg-[#121214] border border-[#2d2d3d] text-white px-3.5 py-2.5 rounded-lg focus:outline-none focus:border-[#ff2a7f] transition-colors"
                    required
                    autoFocus
                  />
                </div>

                <div>
                  <label className="block text-[10px] uppercase font-bold text-[#b3b3cb] tracking-wider mb-1.5">
                    Description
                  </label>
                  <textarea
                    value={projectDesc}
                    onChange={(e) => setProjectDesc(e.target.value)}
                    placeholder="Brief notes..."
                    className="w-full bg-[#121214] border border-[#2d2d3d] text-white px-3.5 py-2.5 rounded-lg focus:outline-none focus:border-[#ff2a7f] h-20 resize-none transition-colors"
                  />
                </div>

                <div>
                  <label className="block text-[10px] uppercase font-bold text-[#b3b3cb] tracking-wider mb-1.5">
                    Roster Size <span className="text-[#ff2a7f]">*</span>
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="50"
                    value={numDancers}
                    onChange={(e) => setNumDancers(parseInt(e.target.value))}
                    className="w-full bg-[#121214] border border-[#2d2d3d] text-white px-3.5 py-2.5 rounded-lg focus:outline-none focus:border-[#ff2a7f] transition-colors"
                    required
                  />
                </div>

                <div className="flex space-x-3 pt-2">
                  <button
                    type="button"
                    onClick={closeModal}
                    className="flex-1 bg-[#272739] hover:bg-[#34344d] text-white py-2.5 rounded-lg font-bold transition-colors cursor-pointer"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={creating || !projectName.trim()}
                    className="flex-1 flex items-center justify-center gap-2 bg-[#ff2a7f] hover:bg-[#e0206f] disabled:opacity-50 disabled:cursor-not-allowed text-white py-2.5 rounded-lg font-bold transition-colors cursor-pointer"
                  >
                    {creating ? <><Loader2 size={14} className="animate-spin" /> Building…</> : 'Build Show'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

      </div>
    </div>
  );
};

export default Dashboard;
