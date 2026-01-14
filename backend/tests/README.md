# Testing Guide

This directory contains comprehensive tests for the Mock Interview API.

## Test Structure

```
tests/
├── __init__.py              # Package marker
├── conftest.py              # Pytest fixtures and configuration
├── mock_data.py             # Mock data for testing
├── test_api.py              # API endpoint tests
├── test_models.py           # Database model tests
└── README.md                # This file
```

## Running Tests

### Install Test Dependencies

First, install pytest and required testing packages:

```bash
pip install pytest pytest-cov pytest-asyncio httpx
```

### Run All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run specific test class
pytest tests/test_api.py::TestFileUpload

# Run specific test
pytest tests/test_api.py::TestFileUpload::test_upload_pdf_file
```

## Test Categories

### 1. API Endpoint Tests (`test_api.py`)

Tests all API endpoints with mocked data:

- **Health Check**: `/health` endpoint
- **File Upload**: File validation and upload processing
- **Interview Sessions**: CRUD operations for sessions
- **Interview Questions**: Question retrieval and answer submission
- **LLM Service**: Mocked LLM integration
- **File Validation**: File type and extension validation

### 2. Database Model Tests (`test_models.py`)

Tests database models and relationships:

- **User Model**: User creation, uniqueness constraints, relationships
- **InterviewSession Model**: Session creation, status transitions, cascade deletes
- **InterviewQuestion Model**: Question creation, answering, ordering

## Mock Data

### Available Mock Data (`mock_data.py`)

- `MOCK_RESUME_CONTENT`: Sample resume text
- `MOCK_JOB_DESCRIPTION_BACKEND`: Backend engineer job description
- `MOCK_JOB_DESCRIPTION_FULLSTACK`: Full-stack developer job description
- `MOCK_INTERVIEW_QUESTIONS`: List of 15 sample Q&A pairs
- `MOCK_PDF_CONTENT`: Valid PDF file bytes
- `MOCK_USERS`: Sample user data
- `MOCK_SESSION_DATA`: Sample session data
- `MOCK_USER_ANSWERS`: Sample answer submissions

## Fixtures

### Database Fixtures

- `db_session`: Fresh in-memory SQLite database for each test
- `client`: FastAPI TestClient with database override
- `sample_user`: Pre-created test user
- `sample_session`: Pre-created test interview session
- `sample_questions`: Pre-created test questions with answers

### Usage Example

```python
def test_example(client, sample_user, sample_session):
    """Test using fixtures"""
    response = client.get(f"/api/v1/sessions/{sample_session.id}")
    assert response.status_code == 200
```

## Mocking External Services

### LLM Service Mocking

The tests mock the Google Gemini API to avoid real API calls:

```python
from unittest.mock import Mock, patch

@patch("app.services.get_llm_service")
def test_generate_questions(mock_llm):
    mock_service = Mock()
    mock_service.generate_interview_questions.return_value = MOCK_INTERVIEW_QUESTIONS
    mock_llm.return_value = mock_service

    # Your test code here
```

### File Upload Mocking

```python
import io

def test_upload():
    pdf_file = io.BytesIO(MOCK_PDF_CONTENT)
    response = client.post(
        "/api/v1/upload",
        files={"file": ("resume.pdf", pdf_file, "application/pdf")},
        data={"job_description": "Test job"}
    )
```

## Test Database

Tests use an **in-memory SQLite database** that is:
- Created fresh for each test
- Automatically cleaned up after each test
- Fast and doesn't require external database

This is different from your production Supabase PostgreSQL database.

## Writing New Tests

### Example Test Structure

```python
class TestMyFeature:
    """Test my new feature"""

    def test_basic_functionality(self, client):
        """Test basic functionality"""
        response = client.get("/api/v1/myendpoint")
        assert response.status_code == 200
        assert "expected_key" in response.json()

    def test_error_handling(self, client):
        """Test error handling"""
        response = client.post("/api/v1/myendpoint", json={})
        assert response.status_code == 400

    def test_with_mock_data(self, client, sample_user):
        """Test with fixtures"""
        response = client.get(f"/api/v1/users/{sample_user.id}")
        assert response.status_code == 200
```

## Coverage Report

After running tests with coverage:

```bash
pytest --cov=app --cov-report=html
```

Open `htmlcov/index.html` in your browser to see detailed coverage report.

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.12
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest --cov=app
```

## Best Practices

1. **Isolate Tests**: Each test should be independent
2. **Use Fixtures**: Reuse common setup with fixtures
3. **Mock External Services**: Don't make real API calls in tests
4. **Test Edge Cases**: Test error conditions, not just happy paths
5. **Keep Tests Fast**: Use in-memory database, mock external services
6. **Clear Test Names**: Use descriptive test names that explain what's being tested
7. **Assert Clearly**: Use specific assertions with helpful messages

## Common Issues

### Issue: Tests fail with "Table already exists"

**Solution**: Make sure you're using the `db_session` fixture, which handles cleanup.

### Issue: Tests fail with "API key not found"

**Solution**: Tests should mock the LLM service. Don't use real API keys in tests.

### Issue: File upload tests fail

**Solution**: Ensure you're creating valid file objects with `io.BytesIO()`.

## Running Tests Before Deployment

Always run tests before deploying:

```bash
# Run tests
pytest -v

# If all pass, deploy
./deploy.sh
```

## Need Help?

- Check the test examples in `test_api.py` and `test_models.py`
- Review pytest documentation: https://docs.pytest.org/
- Check FastAPI testing docs: https://fastapi.tiangolo.com/tutorial/testing/
