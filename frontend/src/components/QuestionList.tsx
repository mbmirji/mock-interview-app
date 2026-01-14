import React from 'react';
import type { Question } from '../types';

interface QuestionListProps {
  questions: Question[];
}

export const QuestionList: React.FC<QuestionListProps> = ({ questions }) => {
  if (questions.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No questions available</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-6 shadow-lg">
        <h2 className="text-3xl font-bold text-white flex items-center gap-3">
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Your Interview Questions
          <span className="ml-auto bg-white text-blue-600 px-4 py-1 rounded-full text-base font-bold">
            {questions.length}
          </span>
        </h2>
      </div>

      <div className="space-y-5">
        {questions.map((question, index) => (
          <div
            key={index}
            className="bg-white border-2 border-gray-100 rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-200 hover:border-blue-200"
          >
            <div className="flex items-start gap-5">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 text-white rounded-xl flex items-center justify-center font-bold text-lg shadow-md">
                  {index + 1}
                </div>
              </div>

              <div className="flex-grow">
                <h3 className="text-xl font-bold text-gray-900 mb-4 leading-relaxed">
                  {question.question}
                </h3>

                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-100 rounded-xl p-5">
                  <div className="flex items-center gap-2 mb-3">
                    <svg className="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                    </svg>
                    <p className="text-sm font-bold text-blue-900 uppercase tracking-wide">
                      Reference Answer
                    </p>
                  </div>
                  <p className="text-base text-gray-700 leading-relaxed">
                    {question.answer}
                  </p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
