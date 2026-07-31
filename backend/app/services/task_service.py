from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate


def create_task(task: TaskCreate, db: Session) -> Task:
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        project_id=task.project_id,
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def get_tasks(db: Session) -> list[Task]:
    return db.query(Task).all()


def update_task(task_id: int, task: TaskCreate, db: Session) -> Task:
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    db_task.title = task.title
    db_task.description = task.description
    db_task.status = task.status
    db_task.project_id = task.project_id

    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(task_id: int, db: Session) -> dict[str, str]:
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    db.delete(db_task)
    db.commit()

    return {"message": "Task deleted successfully"}
