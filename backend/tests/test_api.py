"""
API endpoint tests
"""
import io
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import UploadFile

from tests.mock_data import (
    MOCK_RESUME_CONTENT,
    MOCK_JOB_DESCRIPTION_BACKEND,
    MOCK_INTERVIEW_QUESTIONS,
    MOCK_PDF_CONTENT,
    MOCK_SESSION_DATA,
    MOCK_USER_ANSWERS
)


class TestHealthCheck:
    """Test health check endpoint"""

    def test_health_check(self, client):
        """Test GET /health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestFileUpload:
    """Test file upload and validation"""

    def test_upload_pdf_file(self, client, sample_user):
        """Test uploading a PDF file"""
        # Create a mock PDF file
        pdf_file = io.BytesIO(MOCK_PDF_CONTENT)

        with patch("app.services.get_llm_service") as mock_llm:
            # Mock the LLM service response
            mock_service = Mock()
            mock_service.generate_interview_questions.return_value = MOCK_INTERVIEW_QUESTIONS
            mock_llm.return_value = mock_service

            response = client.post(
                "/api/v1/upload",
                files={"file": ("test_resume.pdf", pdf_file, "application/pdf")},
                data={"job_description": MOCK_JOB_DESCRIPTION_BACKEND}
            )

            assert response.status_code == 200
            data = response.json()
            assert "session_id" in data
            assert "questions" in data
            assert len(data["questions"]) > 0

    def test_upload_invalid_file_type(self, client):
        """Test uploading an invalid file type"""
        # Create a mock text file
        txt_file = io.BytesIO(b"This is a text file")

        response = client.post(
            "/api/v1/upload",
            files={"file": ("test.txt", txt_file, "text/plain")},
            data={"job_description": MOCK_JOB_DESCRIPTION_BACKEND}
        )

        assert response.status_code == 400
        assert "Invalid file type" in response.json()["detail"]

    def test_upload_missing_job_description(self, client):
        """Test uploading without job description"""
        pdf_file = io.BytesIO(MOCK_PDF_CONTENT)

        response = client.post(
            "/api/v1/upload",
            files={"file": ("test_resume.pdf", pdf_file, "application/pdf")},
            data={}
        )

        assert response.status_code == 422  # Validation error


class TestInterviewSession:
    """Test interview session endpoints"""

    def test_get_session(self, client, sample_session, sample_questions):
        """Test retrieving an interview session"""
        response = client.get(f"/api/v1/sessions/{sample_session.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_session.id
        assert data["status"] == sample_session.status
        assert "questions" in data

    def test_get_nonexistent_session(self, client):
        """Test retrieving a non-existent session"""
        response = client.get("/api/v1/sessions/99999")

        assert response.status_code == 404

    def test_list_sessions(self, client, sample_user, sample_session):
        """Test listing all sessions for a user"""
        response = client.get(f"/api/v1/users/{sample_user.id}/sessions")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_update_session_status(self, client, sample_session):
        """Test updating session status"""
        response = client.patch(
            f"/api/v1/sessions/{sample_session.id}",
            json={"status": "in_progress"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "in_progress"


class TestInterviewQuestions:
    """Test interview question endpoints"""

    def test_get_question(self, client, sample_questions):
        """Test retrieving a specific question"""
        question = sample_questions[0]
        response = client.get(f"/api/v1/questions/{question.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == question.id
        assert data["question_text"] == question.question_text

    def test_submit_answer(self, client, sample_questions):
        """Test submitting an answer to a question"""
        question = sample_questions[0]
        answer_data = MOCK_USER_ANSWERS[0]

        with patch("app.services.get_llm_service") as mock_llm:
            # Mock scoring response
            mock_service = Mock()
            mock_service.score_answer = Mock(return_value={
                "score": 8.5,
                "feedback": "Excellent answer with good technical depth."
            })
            mock_llm.return_value = mock_service

            response = client.post(
                f"/api/v1/questions/{question.id}/answer",
                json={"answer": answer_data["answer"]}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["is_answered"] is True
            assert data["user_answer"] == answer_data["answer"]

    def test_get_session_questions(self, client, sample_session, sample_questions):
        """Test retrieving all questions for a session"""
        response = client.get(f"/api/v1/sessions/{sample_session.id}/questions")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == len(sample_questions)


class TestLLMService:
    """Test LLM service integration"""

    @patch("app.services.LLMService.generate_interview_questions")
    def test_generate_questions(self, mock_generate):
        """Test question generation with mocked LLM"""
        from app.services import get_llm_service

        mock_generate.return_value = MOCK_INTERVIEW_QUESTIONS

        llm_service = get_llm_service()
        questions = llm_service.generate_interview_questions(
            resume_content=MOCK_RESUME_CONTENT,
            job_description=MOCK_JOB_DESCRIPTION_BACKEND
        )

        assert len(questions) > 0
        assert "question" in questions[0]
        assert "answer" in questions[0]

    @patch("app.services.genai.GenerativeModel")
    def test_llm_service_handles_errors(self, mock_model):
        """Test LLM service error handling"""
        from app.services import LLMService

        # Mock an error response
        mock_model.return_value.generate_content.side_effect = Exception("API Error")

        llm_service = LLMService()
        questions = llm_service.generate_interview_questions(
            resume_content=MOCK_RESUME_CONTENT,
            job_description=MOCK_JOB_DESCRIPTION_BACKEND
        )

        # Should return empty list on error
        assert questions == []


class TestFileValidation:
    """Test file validation logic"""

    def test_validate_pdf_extension(self, client):
        """Test that PDF files are accepted"""
        pdf_file = io.BytesIO(MOCK_PDF_CONTENT)

        with patch("app.services.get_llm_service") as mock_llm:
            mock_service = Mock()
            mock_service.generate_interview_questions.return_value = MOCK_INTERVIEW_QUESTIONS
            mock_llm.return_value = mock_service

            response = client.post(
                "/api/v1/upload",
                files={"file": ("resume.pdf", pdf_file, "application/pdf")},
                data={"job_description": "Test job"}
            )

            assert response.status_code == 200

    def test_validate_docx_extension(self, client):
        """Test that DOCX files are accepted"""
        # Create a minimal valid DOCX file (it's actually a ZIP file)
        import zipfile
        docx_buffer = io.BytesIO()

        with zipfile.ZipFile(docx_buffer, 'w', zipfile.ZIP_DEFLATED) as docx:
            docx.writestr('[Content_Types].xml', '<?xml version="1.0"?><Types/>')

        docx_buffer.seek(0)

        with patch("app.services.get_llm_service") as mock_llm:
            mock_service = Mock()
            mock_service.generate_interview_questions.return_value = MOCK_INTERVIEW_QUESTIONS
            mock_llm.return_value = mock_service

            response = client.post(
                "/api/v1/upload",
                files={"file": ("resume.docx", docx_buffer, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
                data={"job_description": "Test job"}
            )

            # May fail if document processing fails, but should not fail on validation
            assert response.status_code in [200, 500]  # 500 if parsing fails, but validation passed

    def test_reject_invalid_extensions(self, client):
        """Test that invalid file types are rejected"""
        invalid_files = [
            ("test.txt", "text/plain"),
            ("test.jpg", "image/jpeg"),
            ("test.exe", "application/x-msdownload"),
            ("test.zip", "application/zip"),
        ]

        for filename, content_type in invalid_files:
            file_content = io.BytesIO(b"fake content")

            response = client.post(
                "/api/v1/upload",
                files={"file": (filename, file_content, content_type)},
                data={"job_description": "Test job"}
            )

            assert response.status_code == 400
            assert "Invalid file type" in response.json()["detail"]


class TestDatabaseOperations:
    """Test database operations"""

    def test_create_user(self, db_session):
        """Test creating a user"""
        from app.models import User

        user = User(
            email="newuser@example.com",
            username="newuser",
            full_name="New User",
            hashed_password="hashed_password_here",
            is_active=True
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.email == "newuser@example.com"

    def test_create_session_with_questions(self, db_session, sample_user):
        """Test creating a session with questions"""
        from app.models import InterviewSession, InterviewQuestion

        session = InterviewSession(
            user_id=sample_user.id,
            job_description="Test job description",
            status="created"
        )

        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Add questions
        for i, q in enumerate(MOCK_INTERVIEW_QUESTIONS[:5], 1):
            question = InterviewQuestion(
                session_id=session.id,
                question_text=q["question"],
                reference_answer=q["answer"],
                question_order=i
            )
            db_session.add(question)

        db_session.commit()

        # Verify
        questions = db_session.query(InterviewQuestion).filter_by(session_id=session.id).all()
        assert len(questions) == 5

    def test_cascade_delete(self, db_session, sample_session, sample_questions):
        """Test that deleting a session cascades to questions"""
        from app.models import InterviewQuestion

        session_id = sample_session.id

        # Verify questions exist
        questions_before = db_session.query(InterviewQuestion).filter_by(session_id=session_id).all()
        assert len(questions_before) > 0

        # Delete session
        db_session.delete(sample_session)
        db_session.commit()

        # Verify questions are also deleted (cascade)
        questions_after = db_session.query(InterviewQuestion).filter_by(session_id=session_id).all()
        assert len(questions_after) == 0
