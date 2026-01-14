import axios from 'axios';
import type { UploadResponse } from '../types';

// Base API URL - update this to match your backend URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

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
