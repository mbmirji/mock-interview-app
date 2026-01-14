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

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server (default)
        "http://localhost:5174",  # Vite dev server (alternate port)
        "http://localhost:3000",  # Alternative frontend port
        "https://mock-interview-app-git-main-mbmirjis-projects.vercel.app",  # Vercel deployment
        "https://*.vercel.app",  # All Vercel preview deployments
        "https://mock-interview-app.vercel.app",  # Production Vercel domain (if different)
    ],
    allow_credentials=True,
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
