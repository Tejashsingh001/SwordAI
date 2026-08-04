"""Application services for conversation and project dashboard statistics."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.conversation_repository import ConversationRepository
from app.repositories.dashboard_repository import DashboardRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.dashboard import ConversationStatsResponse, ProjectDashboardResponse


def get_conversation_stats(
    conversation_id: int,
    db: Session,
) -> ConversationStatsResponse:
    """Return message totals and metadata for one conversation."""
    conversation = ConversationRepository(db).get_by_id(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    repository = MessageRepository(db)
    return ConversationStatsResponse(
        total_messages=repository.count_by_conversation_id(conversation_id),
        user_messages=repository.count_by_conversation_and_role(
            conversation_id,
            "user",
        ),
        assistant_messages=repository.count_by_conversation_and_role(
            conversation_id,
            "assistant",
        ),
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        is_pinned=conversation.is_pinned,
        is_archived=conversation.is_archived,
        tags=list(conversation.tags),
    )


def get_project_dashboard(
    project_id: int,
    db: Session,
) -> ProjectDashboardResponse:
    """Return aggregate project activity and useful conversation lists."""
    repository = DashboardRepository(db)
    if repository.get_project(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

    memory_counts = repository.memory_counts(project_id)
    return ProjectDashboardResponse(
        total_conversations=repository.count_project_conversations(project_id),
        total_messages=repository.count_project_messages(project_id),
        total_memories=sum(memory_counts.values()),
        total_decisions=memory_counts["decisions"],
        total_knowledge=memory_counts["knowledge"],
        total_research=memory_counts["research"],
        total_tasks=memory_counts["tasks"],
        recent_conversations=repository.get_recent_conversations(project_id),
        pinned_conversations=repository.get_pinned_conversations(project_id),
    )
