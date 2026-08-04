from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.project import ProjectCreate, ProjectResponse
from app.schemas.dashboard import ProjectDashboardResponse
from app.services import dashboard_service, project_service

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    return project_service.create_project(project, db)


@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db)
):
    return project_service.get_projects(db)


@router.get("/{project_id}/dashboard", response_model=ProjectDashboardResponse)
def get_project_dashboard(
    project_id: int,
    db: Session = Depends(get_db),
) -> ProjectDashboardResponse:
    """Return aggregate statistics and activity for one project."""
    return dashboard_service.get_project_dashboard(project_id, db)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    return project_service.update_project(project_id, project, db)


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    return project_service.delete_project(project_id, db)
