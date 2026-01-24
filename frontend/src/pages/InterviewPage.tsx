import React, { useState } from 'react';
import { createSession, recordAnswer, evaluateSession } from '../services/api';
import type { InterviewSession } from '../types';
import SingleQuestionView from '../components/SingleQuestionView';
import QuestionNavigator from '../components/QuestionNavigator';
import ResultsView from '../components/ResultsView';

const InterviewPage: React.FC = () => {
    // State
    const [step, setStep] = useState<'upload' | 'interview' | 'evaluating' | 'results'>('upload');
    const [session, setSession] = useState<InterviewSession | null>(null);
    const [currentQIndex, setCurrentQIndex] = useState(0);
    const [isUploading, setIsUploading] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false); // For session creation / evaluation

    // Upload Form State
    const [resumeFile, setResumeFile] = useState<File | null>(null);
    const [jdFile, setJdFile] = useState<File | null>(null);

    const handleStartInterview = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!resumeFile || !jdFile) return;

        setIsProcessing(true);
        try {
            const newSession = await createSession(resumeFile, jdFile);
            setSession(newSession);
            setStep('interview');
        } catch (err) {
            console.error(err);
            alert("Failed to start session");
        } finally {
            setIsProcessing(false);
        }
    };

    const handleAnswerRecorded = async (audioBlob: Blob) => {
        if (!session) return;

        setIsUploading(true);
        const question = session.questions[currentQIndex];

        try {
            const result = await recordAnswer(session.id, question.id, audioBlob);

            // Update session state locally
            const updatedQuestions = [...session.questions];
            updatedQuestions[currentQIndex] = {
                ...question,
                user_answer: result.transcript,
                audio_response: {
                    id: 0, // Placeholder or from result if returned
                    audio_url: result.audio_url,
                    transcript: result.transcript,
                    transcription_status: 'completed'
                }
            };

            setSession({
                ...session,
                questions: updatedQuestions,
                answered_questions: session.answered_questions + 1
            });

        } catch (err) {
            console.error(err);
            alert("Failed to upload/transcribe answer");
        } finally {
            setIsUploading(false);
        }
    };

    const handleSubmitAll = async () => {
        if (!session) return;

        if (confirm("Are you sure you want to finish and get your evaluation?")) {
            setStep('evaluating');
            try {
                const result = await evaluateSession(session.id);

                // Merge results into session
                const updatedQuestions = session.questions.map(q => {
                    const res = result.results.find((r: any) => r.question_id === q.id);
                    if (res) {
                        return { ...q, score: res.score, feedback: res.feedback };
                    }
                    return q;
                });

                setSession({
                    ...session,
                    questions: updatedQuestions,
                    average_score: result.average_score,
                    status: 'completed'
                });
                setStep('results');
            } catch (err) {
                console.error(err);
                alert("Evaluation failed");
                setStep('interview'); // Go back
            }
        }
    };

    if (step === 'upload') {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
                <div className="bg-white p-8 rounded-xl shadow-xl max-w-md w-full">
                    <h1 className="text-2xl font-bold mb-6 text-center text-blue-900">Start Mock Interview</h1>
                    <form onSubmit={handleStartInterview} className="space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Resume (PDF/DOC)</label>
                            <input
                                type="file"
                                onChange={e => setResumeFile(e.target.files?.[0] || null)}
                                className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Job Description (PDF/DOC/TXT)</label>
                            <input
                                type="file"
                                onChange={e => setJdFile(e.target.files?.[0] || null)}
                                className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                                required
                            />
                        </div>
                        <button
                            type="submit"
                            disabled={isProcessing}
                            className="w-full py-3 px-4 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                        >
                            {isProcessing ? 'Generating Session...' : 'Start Interview'}
                        </button>
                    </form>
                </div>
            </div>
        );
    }

    if (step === 'evaluating') {
        return (
            <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
                <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mb-4"></div>
                <h2 className="text-xl font-semibold text-gray-800">Analyzing your answers...</h2>
                <p className="text-gray-500">This may take a moment.</p>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pb-12">
            <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                    <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                        Mock Interview Session
                    </h1>
                    {step === 'interview' && (
                        <span className="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full">
                            In Progress
                        </span>
                    )}
                </div>
            </header>

            <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {step === 'results' && session ? (
                    <ResultsView session={session} />
                ) : session ? (
                    <>
                        <QuestionNavigator
                            currentQuestionIndex={currentQIndex}
                            totalQuestions={session.questions.length}
                            answeredCount={session.questions.filter(q => q.user_answer).length}
                            onNavigate={setCurrentQIndex}
                            canNavigateNext={!!session.questions[currentQIndex]?.user_answer}
                        />

                        <SingleQuestionView
                            question={session.questions[currentQIndex]}
                            onAnswerRecorded={handleAnswerRecorded}
                            isUploading={isUploading}
                        />

                        <div className="mt-8 flex justify-center">
                            {session.questions.filter(q => q.user_answer).length === session.questions.length && (
                                <button
                                    onClick={handleSubmitAll}
                                    className="px-8 py-4 bg-green-600 hover:bg-green-700 text-white rounded-xl font-bold shadow-lg transform hover:scale-105 transition-all flex items-center gap-2"
                                >
                                    ✅ Submit All & Get Results
                                </button>
                            )}
                        </div>
                    </>
                ) : null}
            </main>
        </div>
    );
};

export default InterviewPage;
