from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.timeline import TimelineCreate, TimelineResponse
from app.services import timeline_service

router = APIRouter(
    prefix="/timeline",
    tags=["Timeline"]
)


@router.post("/", response_model=TimelineResponse)
def create_timeline(
    timeline: TimelineCreate,
    db: Session = Depends(get_db)
):
    return timeline_service.create_timeline(timeline, db)


@router.get("/", response_model=list[TimelineResponse])
def get_timeline(
    db: Session = Depends(get_db)
):
    return timeline_service.get_timeline(db)


@router.put("/{timeline_id}", response_model=TimelineResponse)
def update_timeline(
    timeline_id: int,
    timeline: TimelineCreate,
    db: Session = Depends(get_db)
):
    return timeline_service.update_timeline(timeline_id, timeline, db)


@router.delete("/{timeline_id}")
def delete_timeline(
    timeline_id: int,
    db: Session = Depends(get_db)
):
    return timeline_service.delete_timeline(timeline_id, db)
