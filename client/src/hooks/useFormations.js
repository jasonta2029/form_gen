/**
 * useFormations.js — Custom controller hook executing snapshots additions, updates, reorderings, and AI templates mappings.
 */
import { useCallback } from 'react';
import { useProject } from '../context/ProjectContext';
import formationsApi from '../api/formations';
import aiApi from '../api/ai';

export const useFormations = () => {
  const {
    currentProject,
    formations,
    setFormations,
    selectedFormationId,
    setSelectedFormationId,
    loadProject
  } = useProject();

  const handleDuplicateFormation = useCallback(async (formationId) => {
    if (!currentProject) return;
    const target = formations.find(f => f.id === formationId);
    if (!target) return;

    try {
      const duplicated = await formationsApi.createFormation(currentProject.id, {
        name: `${target.name} (Copy)`,
        order_index: formations.length,
        timestamp_start: target.timestamp_start,
        timestamp_end: target.timestamp_end,
        positions: target.positions || []
      });
      loadProject(currentProject.id);
      return duplicated;
    } catch (err) {
      console.error("Failed to duplicate formation:", err);
      throw err;
    }
  }, [currentProject, formations, loadProject]);

  const handleApplyAITemplate = useCallback(async (templateName, params = {}) => {
    if (!currentProject || !selectedFormationId) return;
    try {
      const result = await aiApi.generateFromTemplate(currentProject.id, templateName, params);
      
      // Update local state with positions
      setFormations(prev => prev.map(f => {
        if (f.id === selectedFormationId) {
          return { ...f, positions: result.formation.positions };
        }
        return f;
      }));
      
      return result;
    } catch (err) {
      console.error("Failed to apply AI geometric template:", err);
      throw err;
    }
  }, [currentProject, selectedFormationId, setFormations]);

  return {
    formations,
    selectedFormationId,
    setSelectedFormationId,
    duplicateFormation: handleDuplicateFormation,
    applyAITemplate: handleApplyAITemplate,
  };
};

export default useFormations;
