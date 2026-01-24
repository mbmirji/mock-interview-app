import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app
from app.services import LLMService, StorageService, get_llm_service
from app.api.endpoints import get_storage_service

# Mock Services
mock_llm_service = MagicMock(spec=LLMService)
mock_storage_service = MagicMock(spec=StorageService)

# Setup overrides
app.dependency_overrides[get_llm_service] = lambda: mock_llm_service
app.dependency_overrides[get_storage_service] = lambda: mock_storage_service

client = TestClient(app)

@pytest.fixture
def mock_upload_file():
    return {"file": ("resume.pdf", b"dummy content", "application/pdf")}

@patch("app.api.endpoints.pdfplumber.open")
def test_voice_interview_flow(mock_pdf_open):
    # Mock PDF extraction
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Resume Content"
    mock_pdf = MagicMock()
    mock_pdf.pages = [mock_page]
    mock_pdf.__enter__.return_value = mock_pdf # Context manager
    mock_pdf_open.return_value = mock_pdf

    # 1. Setup Mocks
    mock_llm_service.generate_interview_questions.return_value = [
        {"question": "Q1", "answer": "A1"},
        {"question": "Q2", "answer": "A2"}
    ]
    mock_storage_service.upload_audio.return_value = "http://supabase/audio.webm"
    mock_llm_service.transcribe_audio.return_value = "My answer transcript"
    mock_llm_service.batch_score_answers.return_value = [
        {"question_id": 1, "score": 8.5, "feedback": "Good job"},
        {"question_id": 2, "score": 0.0, "feedback": "No answer"}
    ]

    # 2. Create Session
    files = [
        ('resume_file', ('resume.pdf', b"Resume content", 'application/pdf')),
        ('job_desc_file', ('jd.txt', b"JD content", 'text/plain'))
    ]
    response = client.post("/api/v1/sessions", files=files)
    assert response.status_code == 200
    session_data = response.json()
    assert session_data["status"] == "in_progress"
    assert len(session_data["questions"]) == 2
    session_id = session_data["id"]
    question_id = session_data["questions"][0]["id"]
    
    # 3. Record Answer
    audio_files = {'audio_file': ('recording.webm', b"audio data", 'audio/webm')}
    response = client.post(
        f"/api/v1/sessions/{session_id}/questions/{question_id}/record",
        files=audio_files
    )
    assert response.status_code == 200
    record_data = response.json()
    assert record_data["transcript"] == "My answer transcript"
    assert record_data["audio_url"] == "http://supabase/audio.webm"
    
    # 4. Evaluate Session
    # Fix: batch_score_answers mock should return IDs matching the actual DB IDs
    # Since we don't know DB IDs in advance easily in validation without real DB, 
    # but here we use TestClient with the actual DB (SQLite/Postgres).
    # Wait, TestClient uses the app's DB. We didn't mock the DB, only services.
    # So the DB IDs will be real.
    # We need to update the mock return value to use the real Question IDs if possible,
    # OR the service implementation matches mainly by order? No, by ID.
    # The `batch_score_answers` takes input with IDs and returns IDs.
    # So we should mock `batch_score_answers` to dynamically return results based on input?
    
    def side_effect_batch_score(answers):
        results = []
        for ans in answers:
            results.append({
                "question_id": ans["question_id"],
                "score": 9.0,
                "feedback": "Great answer"
            })
        return results
        
    mock_llm_service.batch_score_answers.side_effect = side_effect_batch_score

    response = client.post(f"/api/v1/sessions/{session_id}/evaluate")
    assert response.status_code == 200
    eval_data = response.json()
    assert eval_data["success"] is True
    assert eval_data["average_score"] == 9.0
    
    # 5. Get Session Results
    response = client.get(f"/api/v1/sessions/{session_id}")
    assert response.status_code == 200
    final_session = response.json()
    assert final_session["status"] == "completed"
    assert final_session["average_score"] == 9.0
    assert final_session["questions"][0]["user_answer"] == "My answer transcript"
    assert final_session["questions"][0]["score"] == 9.0

