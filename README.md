# Mock Interview Application

A monorepo application that helps students prepare for interviews by uploading their resume and job description to generate relevant interview questions using AI.

## Project Structure

```
mock-interview-app/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── config.py
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
└── frontend/         # Frontend (to be implemented)
```

## Backend Setup

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- OpenAI API key

### Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your configuration:
- Update `DATABASE_URL` with your PostgreSQL credentials
- Add your `OPENAI_API_KEY`

5. Create the PostgreSQL database:
```bash
createdb mock_interview_db
```

### Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /api/v1/upload
Upload resume and job description documents

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body:
  - `resume`: File (text file)
  - `job_description`: File (text file)

**Response:**
```json
{
  "id": 1,
  "resume_filename": "resume.txt",
  "job_description_filename": "jd.txt",
  "questions_answers": [
    {
      "question": "What experience do you have with Python?",
      "answer": "Reference answer based on resume..."
    }
  ],
  "created_at": "2024-01-08T10:00:00Z",
  "updated_at": "2024-01-08T10:00:00Z"
}
```

### GET /api/v1/interviews
Get all interviews

### GET /api/v1/interviews/{interview_id}
Get a specific interview by ID

### GET /api/v1/interviews/{interview_id}/questions
Get only the questions and answers for a specific interview

## Database Schema

### Interview Table
- `id`: Primary key
- `resume_filename`: Name of uploaded resume file
- `resume_content`: Content of the resume
- `job_description_filename`: Name of uploaded job description file
- `job_description_content`: Content of the job description
- `questions_answers`: JSON array of generated questions and answers
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

## Features

- Upload resume and job description documents
- Store documents in PostgreSQL database
- Generate 10-15 relevant interview questions using OpenAI GPT-4
- Retrieve interview questions and answers
- RESTful API with full documentation

## Technology Stack

### Backend
- FastAPI - Modern web framework for building APIs
- SQLAlchemy - SQL toolkit and ORM
- PostgreSQL - Database
- OpenAI API - LLM for question generation
- Pydantic - Data validation

## Future Enhancements

- Frontend application for file upload and question display
- User authentication and authorization
- Support for PDF and DOCX file formats
- Question difficulty levels
- Practice interview session with timer
- Answer evaluation using AI
