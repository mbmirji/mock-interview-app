from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
import io
import pdfplumber
from docx import Document
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


def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extract text from PDF, DOC, DOCX, or TXT file"""
    file_ext = filename.lower().rsplit(".", 1)[-1]

    if file_ext == "pdf":
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
    elif file_ext in ["doc", "docx"]:
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join([para.text for para in doc.paragraphs])
    elif file_ext == "txt":
        return file_bytes.decode("utf-8")
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: .{file_ext}")


@router.post("/upload")
async def upload_documents(
    resume_file: UploadFile = File(...),
    job_desc_file: UploadFile = File(...),
    additional_context: str = Form(""),
    llm_service: LLMService = Depends(get_llm_service),
):
    """
    Upload resume file, job description file, and optional context to generate interview questions.
    NO DATABASE STORAGE - directly returns generated questions.

    Args:
        resume_file: Resume file (PDF, DOC, DOCX)
        job_desc_file: Job description file (PDF, DOC, DOCX, TXT)
        additional_context: Optional additional background information

    Returns:
        JSON object with questions and answers
    """
    try:
        # Validate resume file type
        validate_file_type(resume_file.filename)

        # Validate job description file type (also allow .txt)
        job_desc_ext = job_desc_file.filename.lower().rsplit(".", 1)[-1] if "." in job_desc_file.filename else ""
        allowed_job_desc_exts = {".pdf", ".doc", ".docx", ".txt"}
        if f".{job_desc_ext}" not in allowed_job_desc_exts:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid job description file type. Allowed: PDF, DOC, DOCX, TXT. Got: .{job_desc_ext}"
            )

        # Read and extract text from resume
        resume_bytes = await resume_file.read()
        resume_content = extract_text_from_file(resume_bytes, resume_file.filename)

        if not resume_content or resume_content.strip() == "":
            raise HTTPException(status_code=400, detail="Could not extract text from resume file")

        # Read and extract text from job description
        job_desc_bytes = await job_desc_file.read()
        job_desc_content = extract_text_from_file(job_desc_bytes, job_desc_file.filename)

        if not job_desc_content or job_desc_content.strip() == "":
            raise HTTPException(status_code=400, detail="Could not extract text from job description file")

        # Combine job description with additional context if provided
        full_context = job_desc_content
        if additional_context and additional_context.strip():
            full_context += f"\n\nADDITIONAL CONTEXT:\n{additional_context.strip()}"

        # Generate questions using LLM (no database storage)
        questions_answers = llm_service.generate_interview_questions(
            resume_content, full_context
        )

        # Return the questions directly
        return {
            "success": True,
            "message": "Interview questions generated successfully",
            "resume_filename": resume_file.filename,
            "job_desc_filename": job_desc_file.filename,
            "questions_count": len(questions_answers),
            "questions": questions_answers
        }

    except HTTPException:
        raise
    except Exception as e:
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
