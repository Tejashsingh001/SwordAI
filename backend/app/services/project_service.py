from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate


def create_project(project: ProjectCreate, db: Session) -> Project:
    db_project = Project(
        name=project.name,
        description=project.description,
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


def get_projects(db: Session) -> list[Project]:
    return db.query(Project).all()


def update_project(
    project_id: int, project: ProjectCreate, db: Session
) -> Project:
    db_project = db.query(Project).filter(Project.id == project_id).first()

    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    db_project.name = project.name
    db_project.description = project.description

    db.commit()
    db.refresh(db_project)

    return db_project


def delete_project(project_id: int, db: Session) -> dict[str, str]:
    db_project = db.query(Project).filter(Project.id == project_id).first()

    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    db.delete(db_project)
    db.commit()

    return {"message": "Project deleted successfully"}
