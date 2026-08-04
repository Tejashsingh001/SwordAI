"""SQLAlchemy repository for Conversation persistence operations."""

from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.tag import Tag


class ConversationRepository:
    """Provide database access methods for Conversation records only."""

    def __init__(self, db: Session) -> None:
        """Initialize the repository with an injected SQLAlchemy session."""
        self.db = db

    def create(
        self,
        project_id: int,
        title: str,
        summary: str,
        summary_is_manual: bool,
        is_pinned: bool,
        is_archived: bool,
    ) -> Conversation:
        """Create, commit, and return a conversation record."""
        conversation = Conversation(
            project_id=project_id,
            title=title,
            summary=summary,
            summary_is_manual=summary_is_manual,
            is_pinned=is_pinned,
            is_archived=is_archived,
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def get_all(self) -> list[Conversation]:
        """Return every conversation record."""
        return self.db.query(Conversation).all()

    def get_by_project_id(self, project_id: int) -> list[Conversation]:
        """Return every conversation associated with one project."""
        return self.db.query(Conversation).filter(
            Conversation.project_id == project_id
        ).all()

    def get_by_id(self, conversation_id: int) -> Conversation | None:
        """Return a conversation by ID when it exists."""
        return self.db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

    def update(
        self,
        conversation: Conversation,
        project_id: int,
        title: str,
        summary: str,
        summary_is_manual: bool,
        is_pinned: bool,
        is_archived: bool,
    ) -> Conversation:
        """Update, commit, and return an existing conversation."""
        conversation.project_id = project_id
        conversation.title = title
        conversation.summary = summary
        conversation.summary_is_manual = summary_is_manual
        conversation.is_pinned = is_pinned
        conversation.is_archived = is_archived
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def set_pinned(
        self,
        conversation: Conversation,
        is_pinned: bool,
    ) -> Conversation:
        """Persist and return the conversation's pinned state."""
        conversation.is_pinned = is_pinned
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def set_archived(
        self,
        conversation: Conversation,
        is_archived: bool,
    ) -> Conversation:
        """Persist and return the conversation's archive state."""
        conversation.is_archived = is_archived
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def add_tag(self, conversation: Conversation, tag: Tag) -> Conversation:
        """Attach a tag to a conversation when it is not already assigned."""
        if tag not in conversation.tags:
            conversation.tags.append(tag)
            self.db.commit()
            self.db.refresh(conversation)

        return conversation

    def remove_tag(self, conversation: Conversation, tag: Tag) -> Conversation:
        """Detach a tag from a conversation when it is assigned."""
        if tag in conversation.tags:
            conversation.tags.remove(tag)
            self.db.commit()
            self.db.refresh(conversation)

        return conversation

    def update_summary(
        self,
        conversation: Conversation,
        summary: str,
    ) -> Conversation:
        """Persist an automatically generated conversation summary."""
        conversation.summary = summary
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def delete(self, conversation: Conversation) -> None:
        """Delete and commit an existing conversation."""
        self.db.delete(conversation)
        self.db.commit()
