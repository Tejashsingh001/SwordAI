from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.task import TaskCreate, TaskResponse
from app.services import task_service

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    return task_service.create_task(task, db)


@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db)
):
    return task_service.get_tasks(db)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    return task_service.update_task(task_id, task, db)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    return task_service.delete_task(task_id, db)
