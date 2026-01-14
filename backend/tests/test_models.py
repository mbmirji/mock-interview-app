"""
Test database models
"""
import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from app.models import User, InterviewSession, InterviewQuestion, SessionStatus


class TestUserModel:
    """Test User model"""

    def test_create_user(self, db_session):
        """Test creating a user"""
        user = User(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            hashed_password="hashed_password",
            is_active=True
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_user_unique_email(self, db_session, sample_user):
        """Test that email must be unique"""
        duplicate_user = User(
            email=sample_user.email,  # Same email
            username="different_username",
            hashed_password="password"
        )

        db_session.add(duplicate_user)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_user_unique_username(self, db_session, sample_user):
        """Test that username must be unique"""
        duplicate_user = User(
            email="different@example.com",
            username=sample_user.username,  # Same username
            hashed_password="password"
        )

        db_session.add(duplicate_user)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_user_relationships(self, db_session, sample_user):
        """Test user-session relationship"""
        from app.models import InterviewSession

        # Create sessions for the user
        for i in range(3):
            session = InterviewSession(
                user_id=sample_user.id,
                job_description=f"Job {i}",
                status="created"
            )
            db_session.add(session)

        db_session.commit()
        db_session.refresh(sample_user)

        assert len(sample_user.interview_sessions) == 3


class TestInterviewSessionModel:
    """Test InterviewSession model"""

    def test_create_session(self, db_session, sample_user):
        """Test creating an interview session"""
        session = InterviewSession(
            user_id=sample_user.id,
            resume_filename="resume.pdf",
            resume_content="Resume content here",
            job_description="Job description here",
            status=SessionStatus.CREATED
        )

        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        assert session.id is not None
        assert session.user_id == sample_user.id
        assert session.status == SessionStatus.CREATED
        assert session.total_questions == 0
        assert session.answered_questions == 0

    def test_session_status_enum(self, db_session, sample_session):
        """Test session status transitions"""
        assert sample_session.status == SessionStatus.CREATED

        sample_session.status = SessionStatus.IN_PROGRESS
        db_session.commit()
        db_session.refresh(sample_session)

        assert sample_session.status == SessionStatus.IN_PROGRESS

    def test_session_relationships(self, db_session, sample_session):
        """Test session-question relationship"""
        from app.models import InterviewQuestion

        # Create questions for the session
        for i in range(5):
            question = InterviewQuestion(
                session_id=sample_session.id,
                question_text=f"Question {i}?",
                reference_answer=f"Answer {i}",
                question_order=i + 1
            )
            db_session.add(question)

        db_session.commit()
        db_session.refresh(sample_session)

        assert len(sample_session.questions) == 5

    def test_session_cascade_delete(self, db_session, sample_user):
        """Test that deleting a user cascades to sessions"""
        from app.models import InterviewSession

        session = InterviewSession(
            user_id=sample_user.id,
            job_description="Test job",
            status="created"
        )
        db_session.add(session)
        db_session.commit()

        session_id = session.id

        # Delete user
        db_session.delete(sample_user)
        db_session.commit()

        # Session should be deleted
        deleted_session = db_session.query(InterviewSession).filter_by(id=session_id).first()
        assert deleted_session is None


class TestInterviewQuestionModel:
    """Test InterviewQuestion model"""

    def test_create_question(self, db_session, sample_session):
        """Test creating a question"""
        question = InterviewQuestion(
            session_id=sample_session.id,
            question_text="What is FastAPI?",
            reference_answer="FastAPI is a modern web framework.",
            question_order=1,
            is_answered=False
        )

        db_session.add(question)
        db_session.commit()
        db_session.refresh(question)

        assert question.id is not None
        assert question.session_id == sample_session.id
        assert question.is_answered is False
        assert question.score is None

    def test_answer_question(self, db_session, sample_questions):
        """Test answering a question"""
        question = sample_questions[0]

        question.user_answer = "My answer to the question"
        question.is_answered = True
        question.score = 8.5
        question.feedback = "Good answer!"

        db_session.commit()
        db_session.refresh(question)

        assert question.is_answered is True
        assert question.score == 8.5
        assert question.user_answer == "My answer to the question"

    def test_question_ordering(self, db_session, sample_session):
        """Test question ordering"""
        from app.models import InterviewQuestion

        # Create questions with specific order
        orders = [3, 1, 5, 2, 4]
        for order in orders:
            question = InterviewQuestion(
                session_id=sample_session.id,
                question_text=f"Question {order}",
                reference_answer=f"Answer {order}",
                question_order=order
            )
            db_session.add(question)

        db_session.commit()

        # Query with ordering
        questions = (
            db_session.query(InterviewQuestion)
            .filter_by(session_id=sample_session.id)
            .order_by(InterviewQuestion.question_order)
            .all()
        )

        assert len(questions) == 5
        assert [q.question_order for q in questions] == [1, 2, 3, 4, 5]

    def test_question_cascade_delete(self, db_session, sample_session, sample_questions):
        """Test that deleting a session cascades to questions"""
        from app.models import InterviewQuestion

        session_id = sample_session.id
        question_ids = [q.id for q in sample_questions]

        # Delete session
        db_session.delete(sample_session)
        db_session.commit()

        # Questions should be deleted
        for question_id in question_ids:
            deleted_question = db_session.query(InterviewQuestion).filter_by(id=question_id).first()
            assert deleted_question is None
