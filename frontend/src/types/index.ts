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

export interface AudioResponse {
  id: number;
  audio_url: string;
  transcript: string | null;
  transcription_status: 'pending' | 'completed' | 'failed';
}

export interface InterviewQuestion {
  id: number;
  question_number: number;
  question_text: string;
  expected_answer: string;
  user_answer?: string | null;
  audio_response?: AudioResponse | null;
  score?: number | null;
  feedback?: string | null;
}

export interface InterviewSession {
  id: number;
  status: 'created' | 'in_progress' | 'completed';
  total_questions: number;
  answered_questions: number;
  average_score?: number | null;
  questions: InterviewQuestion[];
}
