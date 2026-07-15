from fastapi import FastAPI

from app.database.database import Base, engine
from app.models.project import Project
from app.routes.project import router as project_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(project_router)


@app.get("/")
def root():
    return {"message": "Welcome to SwordAI 🚀"}