import React, { useState } from 'react';
import { FileUpload } from '../components/FileUpload';
import { QuestionList } from '../components/QuestionList';
import { uploadResumeAndJobDescription } from '../services/api';
import type { Question } from '../types';

export const UploadPage: React.FC = () => {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jobDescFile, setJobDescFile] = useState<File | null>(null);
  const [additionalContext, setAdditionalContext] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [questions, setQuestions] = useState<Question[]>([]);

  const handleResumeSelect = (selectedFile: File) => {
    setResumeFile(selectedFile);
    setError('');
  };

  const handleJobDescSelect = (selectedFile: File) => {
    setJobDescFile(selectedFile);
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!resumeFile) {
      setError('Please select a resume file');
      return;
    }

    if (!jobDescFile) {
      setError('Please select a job description file');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await uploadResumeAndJobDescription(resumeFile, jobDescFile, additionalContext);
      setQuestions(response.questions);
    } catch (err: any) {
      console.error('Upload error:', err);
      setError(
        err.response?.data?.detail ||
        'Failed to upload. Please check your backend server is running and try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResumeFile(null);
    setJobDescFile(null);
    setAdditionalContext('');
    setQuestions([]);
    setError('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl mb-6 shadow-lg">
            <svg
              className="w-9 h-9 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
          </div>
          <h1 className="text-5xl font-extrabold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent mb-4">
            AI-Powered Interview Prep
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Upload your resume and job description to generate personalized interview questions
            tailored to your experience and target role
          </p>
        </div>

        {/* Upload Form */}
        {questions.length === 0 ? (
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
            {/* Progress Steps */}
            <div className="mb-8">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold shadow-md">
                    1
                  </div>
                  <span className="text-gray-700 font-medium">Upload Files</span>
                </div>
                <div className="flex-1 h-1 bg-gray-200 mx-4"></div>
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gray-200 text-gray-500 rounded-full flex items-center justify-center font-semibold">
                    2
                  </div>
                  <span className="text-gray-400 font-medium">Add Context</span>
                </div>
                <div className="flex-1 h-1 bg-gray-200 mx-4"></div>
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gray-200 text-gray-500 rounded-full flex items-center justify-center font-semibold">
                    3
                  </div>
                  <span className="text-gray-400 font-medium">Get Questions</span>
                </div>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-8">
              {/* Resume Upload */}
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border-2 border-blue-100">
                <div className="flex items-center mb-4">
                  <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center mr-3">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <label className="text-lg font-semibold text-gray-800">
                    Resume Upload <span className="text-red-500">*</span>
                  </label>
                </div>
                <FileUpload
                  onFileSelect={handleResumeSelect}
                  accept=".pdf,.doc,.docx"
                  maxSizeMB={10}
                />
                {resumeFile && (
                  <div className="mt-4 flex items-center space-x-2 bg-white rounded-lg px-4 py-3 border border-green-200">
                    <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span className="text-sm font-medium text-green-700">{resumeFile.name}</span>
                    <span className="text-xs text-green-600 ml-auto">
                      {(resumeFile.size / 1024 / 1024).toFixed(2)} MB
                    </span>
                  </div>
                )}
              </div>

              {/* Job Description Upload */}
              <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-6 border-2 border-purple-100">
                <div className="flex items-center mb-4">
                  <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center mr-3">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <label className="text-lg font-semibold text-gray-800">
                    Job Description Upload <span className="text-red-500">*</span>
                  </label>
                </div>
                <FileUpload
                  onFileSelect={handleJobDescSelect}
                  accept=".pdf,.doc,.docx,.txt"
                  maxSizeMB={10}
                />
                {jobDescFile && (
                  <div className="mt-4 flex items-center space-x-2 bg-white rounded-lg px-4 py-3 border border-green-200">
                    <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span className="text-sm font-medium text-green-700">{jobDescFile.name}</span>
                    <span className="text-xs text-green-600 ml-auto">
                      {(jobDescFile.size / 1024 / 1024).toFixed(2)} MB
                    </span>
                  </div>
                )}
                <p className="mt-3 text-sm text-gray-600 flex items-center">
                  <svg className="w-4 h-4 mr-2 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                  </svg>
                  Accepts PDF, Word documents, or text files
                </p>
              </div>

              {/* Additional Context */}
              <div className="bg-gradient-to-r from-green-50 to-teal-50 rounded-xl p-6 border-2 border-green-100">
                <div className="flex items-center mb-4">
                  <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center mr-3">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                    </svg>
                  </div>
                  <label htmlFor="additional-context" className="text-lg font-semibold text-gray-800">
                    Additional Background & Context
                    <span className="text-sm font-normal text-gray-500 ml-2">(Optional)</span>
                  </label>
                </div>
                <textarea
                  id="additional-context"
                  value={additionalContext}
                  onChange={(e) => setAdditionalContext(e.target.value)}
                  placeholder="E.g., 'I have 2 years of experience with microservices', 'Focus on system design questions', 'I'm particularly interested in cloud architecture roles'"
                  rows={5}
                  className="w-full px-4 py-3 border-2 border-green-200 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none placeholder-gray-400"
                />
                <div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-2">
                  <button
                    type="button"
                    onClick={() => setAdditionalContext("I have 2 years of experience with microservices")}
                    className="text-xs bg-white border border-green-200 text-green-700 px-3 py-2 rounded-lg hover:bg-green-50 transition-colors"
                  >
                    💡 Add Microservices Experience
                  </button>
                  <button
                    type="button"
                    onClick={() => setAdditionalContext("Focus on system design questions")}
                    className="text-xs bg-white border border-green-200 text-green-700 px-3 py-2 rounded-lg hover:bg-green-50 transition-colors"
                  >
                    💡 Focus on System Design
                  </button>
                  <button
                    type="button"
                    onClick={() => setAdditionalContext("I'm interested in cloud architecture roles")}
                    className="text-xs bg-white border border-green-200 text-green-700 px-3 py-2 rounded-lg hover:bg-green-50 transition-colors"
                  >
                    💡 Cloud Architecture Focus
                  </button>
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4">
                  <div className="flex items-start gap-3">
                    <div className="w-6 h-6 bg-red-600 rounded-full flex items-center justify-center flex-shrink-0">
                      <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <p className="text-sm font-medium text-red-800">{error}</p>
                  </div>
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading || !resumeFile || !jobDescFile}
                className={`
                  w-full py-4 px-6 rounded-xl font-bold text-lg text-white
                  transition-all duration-200 shadow-lg
                  ${
                    loading || !resumeFile || !jobDescFile
                      ? 'bg-gray-300 cursor-not-allowed'
                      : 'bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-700 hover:via-indigo-700 hover:to-purple-700 transform hover:scale-105'
                  }
                `}
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-3">
                    <svg
                      className="animate-spin h-6 w-6 text-white"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      ></circle>
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      ></path>
                    </svg>
                    Generating Your Personalized Questions...
                  </span>
                ) : (
                  <span className="flex items-center justify-center gap-2">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    Generate Interview Questions
                  </span>
                )}
              </button>

              <p className="text-center text-sm text-gray-500">
                ⏱️ This usually takes 10-30 seconds • Powered by AI
              </p>
            </form>
          </div>
        ) : (
          /* Questions Display */
          <div className="space-y-6">
            {/* Success Banner */}
            <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-200 rounded-2xl p-6 shadow-lg">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 bg-green-600 rounded-xl flex items-center justify-center flex-shrink-0 shadow-md">
                  <svg className="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="flex-grow">
                  <h3 className="text-xl font-bold text-green-900 mb-1">
                    🎉 Success! Your Questions Are Ready
                  </h3>
                  <p className="text-green-700">
                    We've generated <span className="font-bold">{questions.length} personalized interview questions</span> based on your resume and job description.
                  </p>
                </div>
              </div>
            </div>

            {/* Question List */}
            <QuestionList questions={questions} />

            {/* Reset Button */}
            <div className="flex justify-center pt-6">
              <button
                onClick={handleReset}
                className="px-8 py-4 bg-gradient-to-r from-gray-700 to-gray-900 hover:from-gray-800 hover:to-black text-white font-bold rounded-xl transition-all duration-200 shadow-lg transform hover:scale-105 flex items-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Start New Interview Prep Session
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
