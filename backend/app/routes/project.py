from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.project import Project

router = APIRouter()


@router.post("/projects")
def create_project(name: str, description: str):
    db: Session = SessionLocal()

    project = Project(
        name=name,
        description=description
    )

    db.add(project)
    db.commit()
    db.refresh(project)
    db.close()

    return project

@router.get("/projects")
def get_projects():
    db: Session = SessionLocal()

    projects = db.query(Project).all()

    db.close()

    return projects

@router.put("/projects/{project_id}")
def update_project(project_id: int, name: str, description: str):
    db: Session = SessionLocal()

    project = db.query(Project).filter(Project.id == project_id).first()

    if project is None:
        db.close()
        return {"message": "Project not found"}

    project.name = name
    project.description = description

    db.commit()
    db.refresh(project)
    db.close()

    return project

@router.delete("/projects/{project_id}")
def delete_project(project_id: int):
    db: Session = SessionLocal()

    project = db.query(Project).filter(Project.id == project_id).first()

    if project is None:
        db.close()
        return {"message": "Project not found"}

    db.delete(project)
    db.commit()
    db.close()

    return {"message": "Project deleted successfully"}