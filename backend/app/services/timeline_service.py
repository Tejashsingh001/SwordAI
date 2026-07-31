from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.timeline import Timeline
from app.schemas.timeline import TimelineCreate


def create_timeline(timeline: TimelineCreate, db: Session) -> Timeline:
    db_timeline = Timeline(
        event=timeline.event,
        description=timeline.description,
        project_id=timeline.project_id,
    )

    db.add(db_timeline)
    db.commit()
    db.refresh(db_timeline)

    return db_timeline


def get_timeline(db: Session) -> list[Timeline]:
    return db.query(Timeline).all()


def update_timeline(
    timeline_id: int, timeline: TimelineCreate, db: Session
) -> Timeline:
    db_timeline = db.query(Timeline).filter(Timeline.id == timeline_id).first()

    if db_timeline is None:
        raise HTTPException(
            status_code=404,
            detail="Timeline event not found",
        )

    db_timeline.event = timeline.event
    db_timeline.description = timeline.description
    db_timeline.project_id = timeline.project_id

    db.commit()
    db.refresh(db_timeline)

    return db_timeline


def delete_timeline(timeline_id: int, db: Session) -> dict[str, str]:
    db_timeline = db.query(Timeline).filter(Timeline.id == timeline_id).first()

    if db_timeline is None:
        raise HTTPException(
            status_code=404,
            detail="Timeline event not found",
        )

    db.delete(db_timeline)
    db.commit()

    return {"message": "Timeline event deleted successfully"}
