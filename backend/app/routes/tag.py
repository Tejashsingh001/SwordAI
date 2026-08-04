"""HTTP endpoints for reusable conversation tag CRUD operations."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.tag import TagCreate, TagResponse
from app.services import tag_service

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=TagResponse)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)) -> TagResponse:
    """Create a reusable conversation tag."""
    return tag_service.create_tag(tag, db)


@router.get("/", response_model=list[TagResponse])
def get_tags(db: Session = Depends(get_db)) -> list[TagResponse]:
    """Return all reusable conversation tags."""
    return tag_service.get_tags(db)


@router.get("/{tag_id}", response_model=TagResponse)
def get_tag(tag_id: int, db: Session = Depends(get_db)) -> TagResponse:
    """Return one reusable tag."""
    return tag_service.get_tag(tag_id, db)


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_id: int,
    tag: TagCreate,
    db: Session = Depends(get_db),
) -> TagResponse:
    """Rename one reusable tag."""
    return tag_service.update_tag(tag_id, tag, db)


@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    """Delete one reusable tag."""
    return tag_service.delete_tag(tag_id, db)
