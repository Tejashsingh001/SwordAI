from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.knowledge import KnowledgeCreate, KnowledgeResponse
from app.services import knowledge_service

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge"]
)


@router.post("/", response_model=KnowledgeResponse)
def create_knowledge(
    knowledge: KnowledgeCreate,
    db: Session = Depends(get_db)
):
    return knowledge_service.create_knowledge(knowledge, db)


@router.get("/", response_model=list[KnowledgeResponse])
def get_knowledge(
    db: Session = Depends(get_db)
):
    return knowledge_service.get_knowledge(db)


@router.put("/{knowledge_id}", response_model=KnowledgeResponse)
def update_knowledge(
    knowledge_id: int,
    knowledge: KnowledgeCreate,
    db: Session = Depends(get_db)
):
    return knowledge_service.update_knowledge(knowledge_id, knowledge, db)


@router.delete("/{knowledge_id}")
def delete_knowledge(
    knowledge_id: int,
    db: Session = Depends(get_db)
):
    return knowledge_service.delete_knowledge(knowledge_id, db)
