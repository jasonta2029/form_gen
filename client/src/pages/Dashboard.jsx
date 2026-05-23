/**
 * Dashboard.jsx — Main Landing dashboard displaying all stored choreography projects.
 * Supports creating new project instances.
 */
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import projectsApi from '../api/projects';
import LoadingSpinner from '../components/common/LoadingSpinner';

export const Dashboard = () => {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Modal toggle settings options state
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

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleCreateProject = async (e) => {
    e.preventDefault();
    if (!projectName.trim()) return;

    try {
      const response = await projectsApi.createProject({
        name: projectName.trim(),
        description: projectDesc.trim(),
        num_dancers: parseInt(numDancers)
      });
      // Direct routing redirect to Studio editor
      navigate(`/project/${response.id}`);
    } catch (err) {
      console.error("Failed to construct project instance:", err);
      alert("Failed to build project. Please check network.");
    }
  };

  return (
    <div className="min-h-screen bg-[#121214] text-white p-8 font-sans">
      <div className="max-w-6xl mx-auto space-y-8 select-none">
        
        {/* Header Branding section banner */}
        <div className="flex items-center justify-between border-b border-[#23232f] pb-6">
          <div>
            <h1 className="text-3xl font-black tracking-tight text-white flex items-center">
              Form<span className="text-[#ff2a7f]">Flow</span>
            </h1>
            <p className="text-xs text-[#b3b3cb] uppercase tracking-wider font-semibold mt-1">
              AI-Powered Choreography formation planner
            </p>
          </div>

          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-[#ff2a7f] hover:bg-[#e0206f] text-white font-extrabold px-5 py-2.5 rounded-lg text-sm transition-all shadow-[0_0_12px_rgba(255,42,127,0.3)] hover:scale-105"
          >
            + Create Studio
          </button>
        </div>

        {/* Listings grids */}
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
            <p className="text-sm text-[#b3b3cb]">No dance choreography shows registered yet.</p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="bg-[#ff2a7f]/10 border border-[#ff2a7f] text-[#ff2a7f] hover:bg-[#ff2a7f]/20 font-bold px-4 py-2 rounded-lg text-xs"
            >
              Start Your First Project
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {projects.map((proj) => (
              <div
                key={proj.id}
                onClick={() => navigate(`/project/${proj.id}`)}
                className="bg-[#1a1a24] border border-[#23232f] hover:border-[#ff2a7f] p-5 rounded-2xl cursor-pointer transition-all hover:scale-[1.02] flex flex-col justify-between h-44 text-left"
              >
                <div>
                  <h3 className="font-extrabold text-lg truncate text-white">{proj.name}</h3>
                  <p className="text-xs text-[#b3b3cb] line-clamp-2 mt-1.5">{proj.description || 'No description.'}</p>
                </div>

                <div className="flex items-center justify-between border-t border-[#272739] pt-3.5">
                  <span className="text-xs font-bold text-[#b3b3cb]">👤 {proj.num_dancers} Dancers</span>
                  <span className="text-[10px] text-gray-500">Edit Studio ➜</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Modal additions prompts Overlay */}
        {showCreateModal && (
          <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-[#1a1a24] border border-[#2d2d3d] p-6 rounded-2xl w-full max-w-md text-left space-y-4">
              <div className="flex items-center justify-between border-b border-[#2d2d3d] pb-3">
                <h3 className="font-extrabold text-lg">Create New Show</h3>
                <button onClick={() => setShowCreateModal(false)} className="text-gray-500 hover:text-white">✕</button>
              </div>

              <form onSubmit={handleCreateProject} className="space-y-4 text-xs">
                <div>
                  <label className="block text-[10px] uppercase font-bold text-[#b3b3cb] tracking-wider mb-1.5">Show Title</label>
                  <input
                    type="text"
                    value={projectName}
                    onChange={(e) => setProjectName(e.target.value)}
                    placeholder="e.g. She's Confident Tour"
                    className="w-full bg-[#121214] border border-[#2d2d3d] text-white px-3.5 py-2.5 rounded-lg focus:outline-none focus:border-[#ff2a7f]"
                    required
                  />
                </div>

                <div>
                  <label className="block text-[10px] uppercase font-bold text-[#b3b3cb] tracking-wider mb-1.5">Description</label>
                  <textarea
                    value={projectDesc}
                    onChange={(e) => setProjectDesc(e.target.value)}
                    placeholder="Brief notes..."
                    className="w-full bg-[#121214] border border-[#2d2d3d] text-white px-3.5 py-2.5 rounded-lg focus:outline-none focus:border-[#ff2a7f] h-20"
                  />
                </div>

                <div>
                  <label className="block text-[10px] uppercase font-bold text-[#b3b3cb] tracking-wider mb-1.5">Roster Size (Dancers)</label>
                  <input
                    type="number"
                    min="1"
                    max="50"
                    value={numDancers}
                    onChange={(e) => setNumDancers(parseInt(e.target.value))}
                    className="w-full bg-[#121214] border border-[#2d2d3d] text-white px-3.5 py-2.5 rounded-lg focus:outline-none focus:border-[#ff2a7f]"
                    required
                  />
                </div>

                <div className="flex space-x-3 pt-2">
                  <button
                    type="button"
                    onClick={() => setShowCreateModal(false)}
                    className="flex-1 bg-[#272739] hover:bg-[#34344d] text-white py-2.5 rounded-lg font-bold"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 bg-[#ff2a7f] hover:bg-[#e0206f] text-white py-2.5 rounded-lg font-bold"
                  >
                    Build Show
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
