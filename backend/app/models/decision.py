from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database.database import Base


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="decisions")
