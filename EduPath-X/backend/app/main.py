from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.session import engine, SessionLocal
from app.database.base import Base
from app.database.seed_data import seed_database

from app.api.auth import router as auth_router
from app.api.concepts import router as concepts_router
from app.api.materials import router as materials_router
from app.api.questions import router as questions_router
from app.api.attempts import router as attempts_router
from app.api.sessions import router as sessions_router
from app.api.knowledge import router as knowledge_router
from app.api.recommendations import router as recommendations_router
from app.api.dashboard import router as dashboard_router
from app.api.progress import router as progress_router
from app.api.simulation import router as simulation_router
from app.api.evaluation import router as evaluation_router
from app.api.assistant import router as assistant_router
from app.api.goals import router as goals_router

app = FastAPI(
    title="EduPath-X API",
    description="AI-Powered Adaptive Learning Platform Backend",
    version="1.0.0"
)

# CORS Policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup Event to initialize database & seed data
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

# Include Routers
app.include_router(auth_router)
app.include_router(concepts_router)
app.include_router(materials_router)
app.include_router(questions_router)
app.include_router(attempts_router)
app.include_router(sessions_router)
app.include_router(knowledge_router)
app.include_router(recommendations_router)
app.include_router(dashboard_router)
app.include_router(progress_router)
app.include_router(simulation_router)
app.include_router(evaluation_router)
app.include_router(assistant_router)
app.include_router(goals_router)

@app.get("/")
def root():
    return {
        "status": "ONLINE",
        "app": "EduPath-X AI-Powered Adaptive Learning Platform",
        "docs": "/docs"
    }
