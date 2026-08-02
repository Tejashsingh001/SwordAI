from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    importance = Column(Integer, default=1)

    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="decisions")
