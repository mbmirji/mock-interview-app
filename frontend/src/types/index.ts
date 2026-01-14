// Type definitions for the Mock Interview Application

export interface Question {
  question: string;
  answer: string;
}

export interface UploadResponse {
  success: boolean;
  message: string;
  resume_filename: string;
  job_desc_filename: string;
  questions_count: number;
  questions: Question[];
}

export interface ApiError {
  detail: string;
}
