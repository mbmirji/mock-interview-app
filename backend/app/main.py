from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.database import engine, Base
from app.config import get_settings

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="API for Mock Interview Application",
    version="1.0.0",
)

# Configure CORS - Temporarily allow all origins for debugging
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TEMPORARY: Allow all origins for testing
    allow_credentials=False,  # Must be False when using wildcard
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1", tags=["interviews"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Mock Interview API", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
