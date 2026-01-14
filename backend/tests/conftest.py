"""
Test configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import User, InterviewSession, InterviewQuestion

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override"""
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing"""
    user = User(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        hashed_password="$2b$12$KIXqH9ZxJ8yKZ8YZ8Z8Z8Z",  # Mock hashed password
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_session(db_session, sample_user):
    """Create a sample interview session for testing"""
    session = InterviewSession(
        user_id=sample_user.id,
        resume_filename="test_resume.pdf",
        resume_content="Software Engineer with 5 years of experience in Python, FastAPI, and React.",
        job_description="Looking for a Senior Backend Engineer with Python and FastAPI experience.",
        status="created",
        total_questions=0,
        answered_questions=0
    )
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    return session


@pytest.fixture
def sample_questions(db_session, sample_session):
    """Create sample interview questions for testing"""
    questions = [
        InterviewQuestion(
            session_id=sample_session.id,
            question_text="Tell me about your experience with FastAPI?",
            reference_answer="FastAPI is a modern, fast web framework for building APIs with Python 3.7+.",
            question_order=1,
            is_answered=False
        ),
        InterviewQuestion(
            session_id=sample_session.id,
            question_text="How do you handle database connections in FastAPI?",
            reference_answer="Use dependency injection with SQLAlchemy sessions.",
            question_order=2,
            is_answered=False
        ),
        InterviewQuestion(
            session_id=sample_session.id,
            question_text="Describe your experience with React.",
            reference_answer="React is a JavaScript library for building user interfaces.",
            question_order=3,
            is_answered=True,
            user_answer="I have 3 years of experience building SPAs with React.",
            score=8.5,
            feedback="Good answer, demonstrates practical experience."
        )
    ]

    for question in questions:
        db_session.add(question)

    db_session.commit()

    # Refresh all questions
    for question in questions:
        db_session.refresh(question)

    return questions
