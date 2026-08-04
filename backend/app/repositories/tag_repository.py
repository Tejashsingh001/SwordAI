"""SQLAlchemy repository for reusable conversation tag persistence."""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.tag import Tag


class TagRepository:
    """Provide database access methods for reusable Tag records only."""

    def __init__(self, db: Session) -> None:
        """Initialize the repository with an injected SQLAlchemy session."""
        self.db = db

    def create(self, name: str) -> Tag:
        """Create, commit, and return a reusable tag."""
        tag = Tag(name=name)
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)

        return tag

    def get_all(self) -> list[Tag]:
        """Return every reusable tag."""
        return self.db.query(Tag).all()

    def get_by_id(self, tag_id: int) -> Tag | None:
        """Return one tag by ID when it exists."""
        return self.db.query(Tag).filter(Tag.id == tag_id).first()

    def get_by_name(self, name: str) -> Tag | None:
        """Return a tag using a case-insensitive exact name match."""
        return self.db.query(Tag).filter(
            func.lower(Tag.name) == name.casefold()
        ).first()

    def update(self, tag: Tag, name: str) -> Tag:
        """Rename, commit, and return an existing tag."""
        tag.name = name
        self.db.commit()
        self.db.refresh(tag)

        return tag

    def delete(self, tag: Tag) -> None:
        """Delete and commit a reusable tag."""
        self.db.delete(tag)
        self.db.commit()
