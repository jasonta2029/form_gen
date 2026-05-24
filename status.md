# Status

## Completed
- Fixed formation reorder mismatch (frontend/backend contract mismatch)
- Added duplicate formation endpoint (POST /api/projects/{project_id}/formations/{formation_id}/duplicate)
- Added bulk delete dancers endpoint (DELETE /api/projects/{project_id}/dancers/bulk)
- Wrote tests for:
  - Export endpoints (test_export.py)
  - Audio upload endpoints (test_audio.py)
  - Transition suggestion endpoints (test_transitions.py)
  - Formation duplicate and reorder endpoints (updated test_formations.py)

## In Progress
- None

## Blocked
- None

## Next Steps
- Review and refine any remaining frontend components
- Ensure all API contracts are documented and consistent
- Prepare for user acceptance testing