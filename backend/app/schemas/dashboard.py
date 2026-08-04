"""Response schemas for Conversation and Project dashboard statistics."""

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.conversation import ConversationResponse
from app.schemas.tag import TagResponse


class ConversationStatsResponse(BaseModel):
    """Message and state statistics for one conversation."""

    total_messages: int = Field(description="Total messages in the conversation.")
    user_messages: int = Field(description="Messages authored by the user.")
    assistant_messages: int = Field(description="Messages authored by the assistant.")
    created_at: datetime
    updated_at: datetime
    is_pinned: bool
    is_archived: bool
    tags: list[TagResponse]


class ProjectDashboardResponse(BaseModel):
    """Aggregate project statistics for the dashboard."""

    total_conversations: int
    total_messages: int
    total_memories: int
    total_decisions: int
    total_knowledge: int
    total_research: int
    total_tasks: int
    recent_conversations: list[ConversationResponse]
    pinned_conversations: list[ConversationResponse]
