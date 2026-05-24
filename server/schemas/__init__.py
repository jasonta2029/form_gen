"""
schemas — Pydantic schemas (request/response models) for the FormFlow API.
"""

from schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectDetailResponse, ProjectListResponse
from schemas.dancer import DancerCreate, DancerUpdate, DancerResponse
from schemas.formation import (
    FormationCreate, FormationUpdate, FormationResponse,
    FormationWithPositions, ReorderRequest,
)
from schemas.position import PositionCreate, PositionUpdate, PositionResponse
from schemas.music_marker import MarkerCreate, MarkerUpdate, MarkerResponse
from schemas.ai import (
    GenerationRequest, GenerationResponse,
    TransitionRequest, TransitionResponse,
    TemplateRequest,
)
from schemas.center_time import CenterTimeStats, DancerCenterTime, RebalanceRequest, RebalanceResponse
from schemas.export import ExportImageRequest, ExportPDFRequest, ExportResponse

__all__ = [
    # project
    "ProjectCreate", "ProjectUpdate", "ProjectResponse", "ProjectDetailResponse", "ProjectListResponse",
    # dancer
    "DancerCreate", "DancerUpdate", "DancerResponse",
    # formation
    "FormationCreate", "FormationUpdate", "FormationResponse",
    "FormationWithPositions", "ReorderRequest",
    # position
    "PositionCreate", "PositionUpdate", "PositionResponse",
    # music marker
    "MarkerCreate", "MarkerUpdate", "MarkerResponse",
    # ai
    "GenerationRequest", "GenerationResponse",
    "TransitionRequest", "TransitionResponse", "TemplateRequest",
    # center time
    "CenterTimeStats", "DancerCenterTime", "RebalanceRequest", "RebalanceResponse",
    # export
    "ExportImageRequest", "ExportPDFRequest", "ExportResponse",
]
