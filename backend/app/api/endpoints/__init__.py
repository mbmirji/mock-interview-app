from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
import io
import pdfplumber
from docx import Document
from app.database import get_db
from app.database import get_db
from app.models import Interview, InterviewSession, InterviewQuestion, AudioResponse, SessionStatus, QuestionType
from app.schemas import InterviewResponse, InterviewQuestionsResponse, InterviewSessionSchema
from app.services import get_llm_service, LLMService
from app.services.storage import StorageService
from datetime import datetime
import json

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


def get_storage_service():
    return StorageService()


@router.post("/sessions", response_model=InterviewSessionSchema)
async def create_session(
    resume_file: UploadFile = File(...),
    job_desc_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    llm_service: LLMService = Depends(get_llm_service),
):
    """
    Create a new interview session.
    1. Uploads and extracts text from resume/JD
    2. Generates interview questions
    3. Creates session and questions in DB (generic user)
    """
    # Validate files
    validate_file_type(resume_file.filename)
    
    # Extract text
    resume_bytes = await resume_file.read()
    resume_content = extract_text_from_file(resume_bytes, resume_file.filename)
    
    job_desc_bytes = await job_desc_file.read()
    job_desc_content = extract_text_from_file(job_desc_bytes, job_desc_file.filename)
    
    # Generate questions
    questions_data = llm_service.generate_interview_questions(resume_content, job_desc_content)
    
    # Create Session (User ID 1 = anonymous)
    session = InterviewSession(
        user_id=1,
        resume_filename=resume_file.filename,
        resume_text=resume_content,
        jd_filename=job_desc_file.filename,
        jd_text=job_desc_content,
        total_questions=len(questions_data),
        status=SessionStatus.IN_PROGRESS
    )
    db.add(session)
    db.flush()  # Get ID
    
    # Create Questions
    for idx, q_data in enumerate(questions_data, 1):
        question = InterviewQuestion(
            session_id=session.id,
            question_number=idx,
            question_text=q_data.get("question", ""),
            expected_answer=q_data.get("answer", ""),
            question_type=QuestionType.BEHAVIORAL  # Default, or infer from LLM
        )
        db.add(question)
    
    db.commit()
    db.refresh(session)
    return session


@router.get("/sessions/{session_id}", response_model=InterviewSessionSchema)
def get_session(session_id: int, db: Session = Depends(get_db)):
    """Get session details including questions and audio responses"""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/sessions/{session_id}/questions/{question_id}/record")
async def record_answer(
    session_id: int,
    question_id: int,
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    storage_service: StorageService = Depends(get_storage_service),
    llm_service: LLMService = Depends(get_llm_service),
):
    """
    Upload audio answer, transcribe it, and save to DB.
    """
    # Verify ownership/existence
    question = db.query(InterviewQuestion).filter(
        InterviewQuestion.id == question_id,
        InterviewQuestion.session_id == session_id
    ).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    # Read audio
    audio_bytes = await audio_file.read()
    
    # Upload to Supabase
    try:
        audio_url = storage_service.upload_audio(
            audio_bytes, 
            audio_file.filename or "recording.webm",
            audio_file.content_type or "audio/webm"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
        
    # Transcribe
    transcript = llm_service.transcribe_audio(
        audio_bytes, 
        audio_file.content_type or "audio/webm"
    )
    
    # Update/Create AudioResponse
    if question.audio_response:
        audio_resp = question.audio_response
        audio_resp.audio_url = audio_url
        audio_resp.transcript = transcript
        audio_resp.transcription_status = "completed" if transcript else "failed"
        audio_resp.transcribed_at = datetime.now()
    else:
        audio_resp = AudioResponse(
            question_id=question.id,
            audio_url=audio_url,
            transcript=transcript,
            transcription_status="completed" if transcript else "failed",
            transcribed_at=datetime.now(),
            mime_type=audio_file.content_type
        )
        db.add(audio_resp)
        
    # Update Question
    question.user_answer = transcript
    question.answered_at = datetime.now()
    
    # Update Session progress
    session = question.session
    session.answered_questions = db.query(InterviewQuestion).filter(
        InterviewQuestion.session_id == session_id,
        InterviewQuestion.user_answer.isnot(None)
    ).count() + 1 # +1 as we just answered current one (if not counted yet)
    
    # Better count logic:
    # Actually counting is safer
    db.commit() # Commit first to save user_answer
    
    count = db.query(InterviewQuestion).filter(
        InterviewQuestion.session_id == session_id,
        InterviewQuestion.user_answer != None
    ).count()
    session.answered_questions = count
    
    db.commit()
    db.refresh(question)
    
    return {
        "audio_url": audio_url,
        "transcript": transcript,
        "question_id": question.id
    }


@router.post("/sessions/{session_id}/evaluate")
def evaluate_session(
    session_id: int, 
    db: Session = Depends(get_db),
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Batch evaluate all answers in the session.
    """
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    # Prepare data for batch scoring
    questions_to_score = []
    for q in session.questions:
        if q.user_answer:
            questions_to_score.append({
                "question_id": q.id,
                "question": q.question_text,
                "expected": q.expected_answer,
                "user_answer": q.user_answer
            })
            
    if not questions_to_score:
        return {"message": "No answers to evaluate"}
        
    # Call LLM
    results = llm_service.batch_score_answers(questions_to_score)
    
    # Update DB
    total_score = 0
    scored_count = 0
    
    for res in results:
        q_id = res.get("question_id")
        score = res.get("score")
        feedback = res.get("feedback")
        
        question = next((q for q in session.questions if q.id == q_id), None)
        if question:
            question.score = score
            question.feedback = feedback
            if score is not None:
                total_score += score
                scored_count += 1
                
    if scored_count > 0:
        session.average_score = total_score / scored_count
        
    session.evaluation_status = "completed"
    session.evaluated_at = datetime.now()
    session.status = SessionStatus.COMPLETED
    
    db.commit()
    
    return {
        "success": True,
        "average_score": session.average_score,
        "results": results
    }
