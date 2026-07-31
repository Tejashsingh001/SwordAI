from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.knowledge import Knowledge
from app.schemas.knowledge import KnowledgeCreate


def create_knowledge(knowledge: KnowledgeCreate, db: Session) -> Knowledge:
    db_knowledge = Knowledge(
        title=knowledge.title,
        content=knowledge.content,
        category=knowledge.category,
        importance=knowledge.importance,
        project_id=knowledge.project_id,
    )

    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)

    return db_knowledge


def get_knowledge(db: Session) -> list[Knowledge]:
    return db.query(Knowledge).all()


def update_knowledge(
    knowledge_id: int, knowledge: KnowledgeCreate, db: Session
) -> Knowledge:
    db_knowledge = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()

    if db_knowledge is None:
        raise HTTPException(
            status_code=404,
            detail="Knowledge not found",
        )

    db_knowledge.title = knowledge.title
    db_knowledge.content = knowledge.content
    db_knowledge.category = knowledge.category
    db_knowledge.importance = knowledge.importance
    db_knowledge.project_id = knowledge.project_id

    db.commit()
    db.refresh(db_knowledge)

    return db_knowledge


def delete_knowledge(knowledge_id: int, db: Session) -> dict[str, str]:
    db_knowledge = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()

    if db_knowledge is None:
        raise HTTPException(
            status_code=404,
            detail="Knowledge not found",
        )

    db.delete(db_knowledge)
    db.commit()

    return {"message": "Knowledge deleted successfully"}
