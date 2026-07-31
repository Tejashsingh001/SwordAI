from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.research import ResearchCreate, ResearchResponse
from app.services import research_service

router = APIRouter(
    prefix="/research",
    tags=["Research"]
)


@router.post("/", response_model=ResearchResponse)
def create_research(
    research: ResearchCreate,
    db: Session = Depends(get_db)
):
    return research_service.create_research(research, db)


@router.get("/", response_model=list[ResearchResponse])
def get_research(
    db: Session = Depends(get_db)
):
    return research_service.get_research(db)


@router.put("/{research_id}", response_model=ResearchResponse)
def update_research(
    research_id: int,
    research: ResearchCreate,
    db: Session = Depends(get_db)
):
    return research_service.update_research(research_id, research, db)


@router.delete("/{research_id}")
def delete_research(
    research_id: int,
    db: Session = Depends(get_db)
):
    return research_service.delete_research(research_id, db)
