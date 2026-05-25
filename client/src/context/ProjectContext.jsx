/**
 * ProjectContext.jsx — Core context managing active project data.
 * Governs active project state, list of dancers, list of formations, active selection,
 * timeline markers, and triggers updates to coordinate state seamlessly.
 */
import React, { createContext, useContext, useState, useEffect } from 'react';
import projectsApi from '../api/projects';
import dancersApi from '../api/dancers';
import formationsApi from '../api/formations';
import { useToast } from './ToastContext';

const ProjectContext = createContext(null);

export const ProjectProvider = ({ children }) => {
  const { showToast } = useToast();
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
      showToast(`${newDancer.name} added to roster`, 'success');
      return newDancer;
    } catch (err) {
      showToast('Failed to add dancer', 'error');
      throw err;
    }
  };

  // Remove Dancer
  const removeDancer = async (dancerId) => {
    if (!currentProject) return;
    const dancer = dancers.find(d => d.id === dancerId);
    try {
      await dancersApi.removeDancer(currentProject.id, dancerId);
      setDancers(prev => prev.filter(d => d.id !== dancerId));
      showToast(`${dancer?.name || 'Dancer'} removed`, 'info');
    } catch (err) {
      showToast('Failed to remove dancer', 'error');
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
      showToast(`"${newFormation.name}" snap created`, 'success');
      return newFormation;
    } catch (err) {
      showToast('Failed to create formation snap', 'error');
      throw err;
    }
  };

  // Delete Formation
  const deleteFormation = async (formationId) => {
    if (!currentProject) return;
    const formation = formations.find(f => f.id === formationId);
    try {
      await formationsApi.deleteFormation(currentProject.id, formationId);
      setFormations(prev => {
        const filtered = prev.filter(f => f.id !== formationId);
        if (selectedFormationId === formationId && filtered.length > 0) {
          setSelectedFormationId(filtered[0].id);
        }
        return filtered;
      });
      showToast(`"${formation?.name || 'Snap'}" deleted`, 'info');
    } catch (err) {
      showToast('Failed to delete formation', 'error');
      throw err;
    }
  };

  // Duplicate Formation
  const duplicateFormation = async (formationId) => {
    if (!currentProject) return;
    try {
      const duplicate = await formationsApi.duplicateFormation(currentProject.id, formationId);
      setFormations(prev => [...prev, duplicate]);
      setSelectedFormationId(duplicate.id);
      showToast(`"${duplicate.name}" created`, 'success');
      return duplicate;
    } catch (err) {
      showToast('Failed to duplicate formation', 'error');
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
      await formationsApi.updateFormation(currentProject.id, formationId, {
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
      setFormations,
      selectedFormationId,
      selectedFormation: getSelectedFormation(),
      setSelectedFormationId,
      isLoading,
      error,
      loadProject,
      addDancer,
      removeDancer,
      createFormation,
      deleteFormation,
      duplicateFormation,
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
