from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()

# Database configuration optimized for Supabase PostgreSQL
engine_kwargs = {
    "pool_pre_ping": True,      # Verify connections before using
    "pool_recycle": 3600,       # Recycle connections after 1 hour
    "pool_size": 5,             # Smaller pool for serverless
    "max_overflow": 10,         # Max overflow connections
    "echo": settings.debug,     # Log SQL queries in debug mode
}

# SSL configuration for Supabase (required in production)
if settings.environment == "production":
    engine_kwargs["connect_args"] = {
        "sslmode": "require",
        "connect_timeout": 10,
    }

engine = create_engine(settings.database_url, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for getting database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
