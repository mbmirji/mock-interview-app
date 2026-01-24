import React from 'react';
import type { InterviewQuestion } from '../types';
import VoiceRecorder from './VoiceRecorder';

interface SingleQuestionViewProps {
    question: InterviewQuestion;
    onAnswerRecorded: (blob: Blob) => void;
    isUploading: boolean;
}

const SingleQuestionView: React.FC<SingleQuestionViewProps> = ({
    question,
    onAnswerRecorded,
    isUploading
}) => {
    return (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 max-w-2xl mx-auto">
            <div className="mb-6">
                <span className="inline-block px-3 py-1 text-xs font-semibold tracking-wider text-blue-100 uppercase bg-blue-600 rounded-full mb-2">
                    Question {question.question_number}
                </span>
                <h3 className="text-xl md:text-2xl font-bold text-gray-900 dark:text-white leading-relaxed">
                    {question.question_text}
                </h3>
            </div>

            <div className="mb-8 p-4 bg-gray-50 dark:bg-gray-900/50 rounded-lg border border-dashed border-gray-300 dark:border-gray-700">
                <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
                    Your Answer
                </h4>

                {question.user_answer ? (
                    <div className="prose dark:prose-invert">
                        <p className="text-gray-700 dark:text-gray-300">
                            {question.user_answer}
                        </p>
                        <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 text-center">
                            <p className="text-green-600 dark:text-green-400 font-medium text-sm flex items-center justify-center gap-2">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                                Answer Recorded
                            </p>
                            <button
                                onClick={() => {
                                    // logic to re-record? For now, simpler component, maybe just show recorder again?
                                    // Plan didn't specify re-record but it's good UX.
                                    // We'll hide recorder if answered to keep it simple as per "Displays transcript (after recording)"
                                }}
                                className="text-xs text-blue-500 hover:underline mt-2"
                            >
                                (Re-recording not implemented yet in prototype)
                            </button>
                        </div>
                    </div>
                ) : (
                    <VoiceRecorder
                        onRecordingComplete={onAnswerRecorded}
                        isUploading={isUploading}
                    />
                )}
            </div>
        </div>
    );
};

export default SingleQuestionView;
