from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.research import Research
from app.schemas.research import ResearchCreate


def create_research(research: ResearchCreate, db: Session) -> Research:
    db_research = Research(
        title=research.title,
        content=research.content,
        source=research.source,
        project_id=research.project_id,
    )

    db.add(db_research)
    db.commit()
    db.refresh(db_research)

    return db_research


def get_research(db: Session) -> list[Research]:
    return db.query(Research).all()


def update_research(
    research_id: int, research: ResearchCreate, db: Session
) -> Research:
    db_research = db.query(Research).filter(Research.id == research_id).first()

    if db_research is None:
        raise HTTPException(
            status_code=404,
            detail="Research not found",
        )

    db_research.title = research.title
    db_research.content = research.content
    db_research.source = research.source
    db_research.project_id = research.project_id

    db.commit()
    db.refresh(db_research)

    return db_research


def delete_research(research_id: int, db: Session) -> dict[str, str]:
    db_research = db.query(Research).filter(Research.id == research_id).first()

    if db_research is None:
        raise HTTPException(
            status_code=404,
            detail="Research not found",
        )

    db.delete(db_research)
    db.commit()

    return {"message": "Research deleted successfully"}
