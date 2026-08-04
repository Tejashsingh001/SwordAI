from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete"
    )
    decisions = relationship(
        "Decision",
        back_populates="project",
        cascade="all, delete"
    )
    research = relationship(
        "Research",
        back_populates="project",
        cascade="all, delete"
    )
    timeline = relationship(
        "Timeline",
        back_populates="project",
        cascade="all, delete"
    )
    knowledge = relationship(
        "Knowledge",
        back_populates="project",
        cascade="all, delete"
    )
    conversations = relationship(
        "Conversation",
        back_populates="project",
        cascade="all, delete"
    )
