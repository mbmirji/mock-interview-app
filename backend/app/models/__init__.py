from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class SessionStatus(str, enum.Enum):
    """Status of an interview session"""
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class QuestionType(str, enum.Enum):
    """Type of interview question"""
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    SITUATIONAL = "situational"
    EXPERIENCE = "experience"


class User(Base):
    """User model for authentication and profile management"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    sessions = relationship("InterviewSession", back_populates="user", cascade="all, delete-orphan")


class InterviewSession(Base):
    """Interview session model - represents a single mock interview attempt"""
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Session metadata
    title = Column(String(255), nullable=True)
    status = Column(Enum(SessionStatus), default=SessionStatus.CREATED, nullable=False, index=True)

    # Resume information
    resume_filename = Column(String(255), nullable=False)
    resume_path = Column(String(500), nullable=True)  # Path to stored file
    resume_text = Column(Text, nullable=False)  # Extracted text content

    # Job description information
    jd_filename = Column(String(255), nullable=False)
    jd_path = Column(String(500), nullable=True)  # Path to stored file
    jd_text = Column(Text, nullable=False)  # Extracted text content

    # Session statistics
    total_questions = Column(Integer, default=0, nullable=False)
    answered_questions = Column(Integer, default=0, nullable=False)
    average_score = Column(Float, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="sessions")
    questions = relationship("InterviewQuestion", back_populates="session", cascade="all, delete-orphan")


class InterviewQuestion(Base):
    """Individual interview question and answer within a session"""
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False, index=True)

    # Question details
    question_number = Column(Integer, nullable=False)  # Order within the session
    question_text = Column(Text, nullable=False)
    question_type = Column(Enum(QuestionType), nullable=True, index=True)

    # Answer details
    expected_answer = Column(Text, nullable=True)  # LLM-generated expected answer
    user_answer = Column(Text, nullable=True)  # User's actual answer

    # Evaluation
    feedback = Column(Text, nullable=True)  # LLM-generated feedback
    score = Column(Float, nullable=True)  # Score out of 10

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    answered_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    session = relationship("InterviewSession", back_populates="questions")


# Legacy model - kept for backward compatibility, consider migrating to new schema
class Interview(Base):
    """
    DEPRECATED: Legacy interview model. Use InterviewSession instead.
    Kept for backward compatibility with existing data.
    """
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    resume_filename = Column(String, nullable=False)
    resume_content = Column(Text, nullable=False)
    job_description_filename = Column(String, nullable=False)
    job_description_content = Column(Text, nullable=False)
    questions_answers = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
