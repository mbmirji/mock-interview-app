from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Interview
from app.schemas import InterviewResponse, InterviewQuestionsResponse
from app.services import get_llm_service, LLMService

router = APIRouter()


def validate_file_type(filename: str) -> None:
    """
    Validate that the uploaded file is a Word document or PDF.
    Allowed extensions: .pdf, .doc, .docx
    """
    if not filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    allowed_extensions = {".pdf", ".doc", ".docx"}
    file_ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""

    if f".{file_ext}" not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Only PDF and Word documents (.pdf, .doc, .docx) are allowed. Got: .{file_ext}"
        )


@router.post("/upload", response_model=InterviewResponse)
async def upload_documents(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...),
    db: Session = Depends(get_db),
    llm_service: LLMService = Depends(get_llm_service),
):
    """
    Upload resume and job description, store in database, and generate interview questions.
    Only accepts PDF and Word documents (.pdf, .doc, .docx).
    """
    try:
        # Validate file types
        validate_file_type(resume.filename)
        validate_file_type(job_description.filename)

        # Read file contents
        resume_content = (await resume.read()).decode("utf-8")
        jd_content = (await job_description.read()).decode("utf-8")

        # Create database entry
        interview = Interview(
            resume_filename=resume.filename,
            resume_content=resume_content,
            job_description_filename=job_description.filename,
            job_description_content=jd_content,
        )

        db.add(interview)
        db.commit()
        db.refresh(interview)

        # Generate questions using LLM
        questions_answers = llm_service.generate_interview_questions(
            resume_content, jd_content
        )

        # Update the interview with generated questions
        interview.questions_answers = questions_answers
        db.commit()
        db.refresh(interview)

        return interview

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing documents: {str(e)}")


@router.get("/interviews", response_model=List[InterviewResponse])
def get_all_interviews(db: Session = Depends(get_db)):
    """
    Get all interviews from the database
    """
    interviews = db.query(Interview).all()
    return interviews


@router.get("/interviews/{interview_id}", response_model=InterviewResponse)
def get_interview(interview_id: int, db: Session = Depends(get_db)):
    """
    Get a specific interview by ID
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview


@router.get("/interviews/{interview_id}/questions", response_model=InterviewQuestionsResponse)
def get_interview_questions(interview_id: int, db: Session = Depends(get_db)):
    """
    Get only the questions and answers for a specific interview
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    return InterviewQuestionsResponse(
        id=interview.id, questions_answers=interview.questions_answers or []
    )
