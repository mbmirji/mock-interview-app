from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime


class QuestionAnswer(BaseModel):
    question: str
    answer: str


class InterviewCreate(BaseModel):
    resume_filename: str
    resume_content: str
    job_description_filename: str
    job_description_content: str


class InterviewResponse(BaseModel):
    id: int
    resume_filename: str
    job_description_filename: str
    questions_answers: Optional[List[Dict[str, str]]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class InterviewQuestionsResponse(BaseModel):
    id: int
    questions_answers: List[Dict[str, str]]


class AudioResponseSchema(BaseModel):
    id: int
    audio_url: str
    transcript: Optional[str] = None
    transcription_status: str

    class Config:
        from_attributes = True


class InterviewQuestionSchema(BaseModel):
    id: int
    question_number: int
    question_text: str
    expected_answer: Optional[str] = None
    user_answer: Optional[str] = None
    score: Optional[float] = None
    feedback: Optional[str] = None
    audio_response: Optional[AudioResponseSchema] = None

    class Config:
        from_attributes = True


class InterviewSessionSchema(BaseModel):
    id: int
    status: str
    total_questions: int
    answered_questions: int
    average_score: Optional[float] = None
    questions: List[InterviewQuestionSchema] = []
    
    class Config:
        from_attributes = True

