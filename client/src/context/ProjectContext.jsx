/**
 * ProjectContext.jsx — Core context managing active project data.
 * Governs active project state, list of dancers, list of formations, active selection,
 * timeline markers, and triggers updates to coordinate state seamlessly.
 */
import React, { createContext, useContext, useState, useEffect } from 'react';
import projectsApi from '../api/projects';
import dancersApi from '../api/dancers';
import formationsApi from '../api/formations';

const ProjectContext = createContext(null);

export const ProjectProvider = ({ children }) => {
  const [currentProject, setCurrentProject] = useState(null);
  const [dancers, setDancers] = useState([]);
  const [formations, setFormations] = useState([]);
  const [selectedFormationId, setSelectedFormationId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load project details
  const loadProject = async (projectId) => {
    setIsLoading(true);
    setError(null);
    try {
      const project = await projectsApi.getProject(projectId);
      setCurrentProject(project);
      setDancers(project.dancers || []);
      
      const sortedFormations = (project.formations || []).sort(
        (a, b) => a.order_index - b.order_index
      );
      setFormations(sortedFormations);
      
      if (sortedFormations.length > 0) {
        setSelectedFormationId(sortedFormations[0].id);
      }
    } catch (err) {
      console.error("Failed to load project details:", err);
      setError("Failed to fetch project details. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const getSelectedFormation = () => {
    return formations.find(f => f.id === selectedFormationId) || null;
  };

  // Add Dancer
  const addDancer = async (dancerData) => {
    if (!currentProject) return;
    try {
      const newDancer = await dancersApi.addDancer(currentProject.id, dancerData);
      setDancers(prev => [...prev, newDancer]);
      return newDancer;
    } catch (err) {
      setError("Failed to add dancer.");
      throw err;
    }
  };

  // Remove Dancer
  const removeDancer = async (dancerId) => {
    if (!currentProject) return;
    try {
      await dancersApi.removeDancer(currentProject.id, dancerId);
      setDancers(prev => prev.filter(d => d.id !== dancerId));
    } catch (err) {
      setError("Failed to remove dancer.");
      throw err;
    }
  };

  // Create Formation
  const createFormation = async (formationData) => {
    if (!currentProject) return;
    try {
      const newFormation = await formationsApi.createFormation(currentProject.id, {
        ...formationData,
        order_index: formations.length,
      });
      setFormations(prev => [...prev, newFormation]);
      setSelectedFormationId(newFormation.id);
      return newFormation;
    } catch (err) {
      setError("Failed to create formation snapshot.");
      throw err;
    }
  };

  // Update dancer positions within current selected formation
  const updateDancerPositions = async (formationId, updatedPositions) => {
    if (!currentProject) return;
    
    // Optimistic UI update
    setFormations(prev => prev.map(f => {
      if (f.id === formationId) {
        return { ...f, positions: updatedPositions };
      }
      return f;
    }));

    try {
      await client.put(`/projects/${currentProject.id}/formations/${formationId}/positions`, {
        positions: updatedPositions
      });
    } catch (err) {
      console.error("Failed to save dancer coordinates:", err);
      setError("Failed to persist stage alignments.");
    }
  };

  return (
    <ProjectContext.Provider value={{
      currentProject,
      dancers,
      formations,
      selectedFormationId,
      selectedFormation: getSelectedFormation(),
      setSelectedFormationId,
      isLoading,
      error,
      loadProject,
      addDancer,
      removeDancer,
      createFormation,
      updateDancerPositions,
      setError,
    }}>
      {children}
    </ProjectContext.Provider>
  );
};

export const useProject = () => {
  const context = useContext(ProjectContext);
  if (!context) {
    throw new Error("useProject must be used inside a ProjectProvider");
  }
  return context;
};

export default ProjectContext;
