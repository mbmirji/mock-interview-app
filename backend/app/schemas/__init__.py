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
