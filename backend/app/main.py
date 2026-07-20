from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.routes import project, task

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


@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to SwordAI 🚀"}


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "service": "SwordAI Backend"
    }