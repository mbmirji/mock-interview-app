import React from 'react';
import type { InterviewSession } from '../types';

interface ResultsViewProps {
    session: InterviewSession;
}

const ResultsView: React.FC<ResultsViewProps> = ({ session }) => {
    const getScoreColor = (score: number | null | undefined) => {
        if (score == null) return 'text-gray-500';
        if (score >= 8) return 'text-green-600';
        if (score >= 6) return 'text-yellow-600';
        return 'text-red-600';
    };

    const getScoreBg = (score: number | null | undefined) => {
        if (score == null) return 'bg-gray-100';
        if (score >= 8) return 'bg-green-100';
        if (score >= 6) return 'bg-yellow-100';
        return 'bg-red-100';
    };

    return (
        <div className="max-w-4xl mx-auto p-4">
            <div className="text-center mb-10">
                <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                    Interview Results
                </h2>
                <div className="inline-flex flex-col items-center justify-center p-6 bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700">
                    <span className="text-sm text-gray-500 uppercase tracking-widest font-semibold mb-2">Overall Score</span>
                    <span className={`text-6xl font-extrabold ${getScoreColor(session.average_score)}`}>
                        {session.average_score?.toFixed(1) || 'N/A'}
                    </span>
                    <span className="text-sm text-gray-400 mt-2 font-medium">out of 10</span>
                </div>
            </div>

            <div className="grid gap-6">
                {session.questions.map((q) => (
                    <div key={q.id} className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden border border-gray-100 dark:border-gray-700 transition-all hover:shadow-lg">
                        <div className="p-6">
                            <div className="flex justify-between items-start gap-4 mb-4">
                                <div className="flex-1">
                                    <span className="text-xs font-bold text-gray-400 uppercase tracking-wide">Question {q.question_number}</span>
                                    <p className="text-lg font-semibold text-gray-800 dark:text-white mt-1">
                                        {q.question_text}
                                    </p>
                                </div>
                                <div className={`flex flex-col items-center justify-center w-16 h-16 rounded-xl ${getScoreBg(q.score)} flex-shrink-0`}>
                                    <span className={`text-xl font-bold ${getScoreColor(q.score)}`}>
                                        {q.score?.toFixed(1) || '-'}
                                    </span>
                                </div>
                            </div>

                            <div className="space-y-4">
                                <div className="bg-gray-50 dark:bg-gray-900/50 p-4 rounded-lg">
                                    <p className="text-xs font-bold text-gray-500 uppercase mb-1">Your Answer</p>
                                    <p className="text-gray-700 dark:text-gray-300 text-sm italic">
                                        "{q.user_answer || 'No answer recorded'}"
                                    </p>
                                </div>

                                {q.feedback && (
                                    <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-100 dark:border-blue-900/30">
                                        <p className="text-xs font-bold text-blue-600 dark:text-blue-400 uppercase mb-1 flex items-center gap-2">
                                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                            Feedback
                                        </p>
                                        <p className="text-gray-800 dark:text-gray-200 text-sm leading-relaxed">
                                            {q.feedback}
                                        </p>
                                    </div>
                                )}

                                <details className="group">
                                    <summary className="cursor-pointer text-xs font-semibold text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors flex items-center gap-2">
                                        <span className="group-open:rotate-90 transition-transform">▸</span>
                                        Show Expected Answer
                                    </summary>
                                    <div className="mt-2 pl-4 text-sm text-gray-500 border-l-2 border-gray-200">
                                        {q.expected_answer}
                                    </div>
                                </details>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ResultsView;
