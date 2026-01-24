import axios from 'axios';
import type { UploadResponse } from '../types';

// Base API URL - update this to match your backend URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

// Debug: Log the API URL being used
console.log('🔗 API Base URL:', API_BASE_URL);
console.log('🔗 VITE_API_URL env var:', import.meta.env.VITE_API_URL);

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Upload resume, job description, and additional context to generate interview questions
 */
export const uploadResumeAndJobDescription = async (
  resumeFile: File,
  jobDescFile: File,
  additionalContext: string
): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('resume_file', resumeFile);
  formData.append('job_desc_file', jobDescFile);
  formData.append('additional_context', additionalContext);

  const response = await api.post<UploadResponse>('/api/v1/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

/**
 * Health check endpoint
 */
export const healthCheck = async (): Promise<{ status: string }> => {
  const response = await api.get('/health');
  return response.data;
};

export default api;

// New Voice Interview API

import type { InterviewSession } from '../types';

export const createSession = async (
  resumeFile: File,
  jobDescFile: File
): Promise<InterviewSession> => {
  const formData = new FormData();
  formData.append('resume_file', resumeFile);
  formData.append('job_desc_file', jobDescFile);

  const response = await api.post<InterviewSession>('/api/v1/sessions', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getSession = async (sessionId: number): Promise<InterviewSession> => {
  const response = await api.get<InterviewSession>(`/api/v1/sessions/${sessionId}`);
  return response.data;
};

export const recordAnswer = async (
  sessionId: number,
  questionId: number,
  audioBlob: Blob
): Promise<{ audio_url: string; transcript: string; question_id: number }> => {
  const formData = new FormData();
  formData.append('audio_file', audioBlob, 'recording.webm');

  const response = await api.post(
    `/api/v1/sessions/${sessionId}/questions/${questionId}/record`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );
  return response.data;
};

export const evaluateSession = async (sessionId: number): Promise<{
  success: boolean;
  average_score: number;
  results: any[];
}> => {
  const response = await api.post(`/api/v1/sessions/${sessionId}/evaluate`);
  return response.data;
};
