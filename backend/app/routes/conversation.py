"""HTTP endpoints for project conversation CRUD operations."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.conversation import ConversationCreate, ConversationResponse
from app.schemas.dashboard import ConversationStatsResponse
from app.schemas.tag import TagResponse
from app.services import conversation_service, dashboard_service, tag_service

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post("/", response_model=ConversationResponse)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
) -> ConversationResponse:
    """Create a conversation associated with a project."""
    return conversation_service.create_conversation(conversation, db)


@router.get("/", response_model=list[ConversationResponse])
def get_conversations(
    include_archived: bool = Query(
        default=False,
        description="Include archived conversations in the listing.",
    ),
    db: Session = Depends(get_db),
) -> list[ConversationResponse]:
    """Return conversations, with pinned records first."""
    return conversation_service.get_conversations(db, include_archived)


@router.get("/search", response_model=list[ConversationResponse])
def search_conversations(
    project_id: int = Query(
        ...,
        gt=0,
        description="Project ID used to scope the conversation search.",
    ),
    query: str = Query(
        default="",
        description="Optional title, summary, or tag text to search for.",
    ),
    tag: str | None = Query(
        default=None,
        description="Optional reusable tag name used to filter conversations.",
    ),
    include_archived: bool = Query(
        default=False,
        description="Include archived conversations in search results.",
    ),
    db: Session = Depends(get_db),
) -> list[ConversationResponse]:
    """Search conversations within one project."""
    return conversation_service.search_conversations(
        project_id,
        query,
        db,
        include_archived,
        tag,
    )


@router.post("/{conversation_id}/pin", response_model=ConversationResponse)
def pin_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
) -> ConversationResponse:
    """Pin one conversation."""
    return conversation_service.pin_conversation(conversation_id, db)


@router.post("/{conversation_id}/unpin", response_model=ConversationResponse)
def unpin_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
) -> ConversationResponse:
    """Unpin one conversation."""
    return conversation_service.unpin_conversation(conversation_id, db)


@router.post("/{conversation_id}/archive", response_model=ConversationResponse)
def archive_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
) -> ConversationResponse:
    """Archive one conversation."""
    return conversation_service.archive_conversation(conversation_id, db)


@router.post("/{conversation_id}/restore", response_model=ConversationResponse)
def restore_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
) -> ConversationResponse:
    """Restore one archived conversation."""
    return conversation_service.restore_conversation(conversation_id, db)


@router.get("/{conversation_id}/tags", response_model=list[TagResponse])
def get_conversation_tags(
    conversation_id: int,
    db: Session = Depends(get_db),
) -> list[TagResponse]:
    """Return tags assigned to one conversation."""
    return tag_service.get_conversation_tags(conversation_id, db)


@router.post("/{conversation_id}/tags/{tag_id}", response_model=TagResponse)
def add_tag_to_conversation(
    conversation_id: int,
    tag_id: int,
    db: Session = Depends(get_db),
) -> TagResponse:
    """Assign an existing reusable tag to one conversation."""
    return tag_service.add_tag_to_conversation(conversation_id, tag_id, db)


@router.delete("/{conversation_id}/tags/{tag_id}")
def remove_tag_from_conversation(
    conversation_id: int,
    tag_id: int,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Remove a tag from one conversation."""
    return tag_service.remove_tag_from_conversation(conversation_id, tag_id, db)


@router.get("/{conversation_id}/stats", response_model=ConversationStatsResponse)
def get_conversation_stats(
    conversation_id: int,
    db: Session = Depends(get_db),
) -> ConversationStatsResponse:
    """Return aggregate statistics for one conversation."""
    return dashboard_service.get_conversation_stats(conversation_id, db)


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
) -> ConversationResponse:
    """Return one conversation by ID."""
    return conversation_service.get_conversation(conversation_id, db)


@router.put("/{conversation_id}", response_model=ConversationResponse)
def update_conversation(
    conversation_id: int,
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
) -> ConversationResponse:
    """Update one conversation by ID."""
    return conversation_service.update_conversation(
        conversation_id,
        conversation,
        db,
    )


@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Delete one conversation by ID."""
    return conversation_service.delete_conversation(conversation_id, db)
