from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Timeline(Base):
    __tablename__ = "timeline"

    id = Column(Integer, primary_key=True, index=True)
    event = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="timeline")
