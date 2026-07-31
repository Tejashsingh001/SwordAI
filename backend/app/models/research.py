from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Research(Base):
    __tablename__ = "research"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    source = Column(String, nullable=True)

    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="research")
