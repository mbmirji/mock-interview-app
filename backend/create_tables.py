"""
Database initialization script
Creates all tables defined in the models
"""
from app.database import engine, Base
from app.models import User, InterviewSession, InterviewQuestion, Interview


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ All tables created successfully!")
    print("\nCreated tables:")
    print("  - users")
    print("  - interview_sessions")
    print("  - interview_questions")
    print("  - interviews (legacy)")


if __name__ == "__main__":
    create_tables()
