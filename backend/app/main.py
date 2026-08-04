from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.routes import (
    ai,
    conversation,
    knowledge,
    message,
    project,
    research,
    task,
    tag,
    timeline,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SwordAI API",
    version="1.0.0",
    description="Backend API for SwordAI"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project.router)
app.include_router(task.router)
app.include_router(research.router)
app.include_router(timeline.router)
app.include_router(knowledge.router)
app.include_router(ai.router)
app.include_router(conversation.router)
app.include_router(message.router)
app.include_router(tag.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to SwordAI 🚀"}


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "service": "SwordAI Backend"
    }
