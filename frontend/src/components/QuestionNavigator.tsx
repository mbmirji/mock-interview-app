import React from 'react';

interface QuestionNavigatorProps {
    currentQuestionIndex: number;
    totalQuestions: number;
    answeredCount: number;
    onNavigate: (index: number) => void;
    canNavigateNext: boolean; // e.g. only if answered
}

const QuestionNavigator: React.FC<QuestionNavigatorProps> = ({
    currentQuestionIndex,
    totalQuestions,
    answeredCount,
    onNavigate,
    canNavigateNext
}) => {
    const progress = Math.round((answeredCount / totalQuestions) * 100);

    return (
        <div className="w-full mb-6">
            <div className="flex justify-between items-center mb-2">
                <h2 className="text-lg font-semibold text-gray-800 dark:text-white">
                    Question {currentQuestionIndex + 1} of {totalQuestions}
                </h2>
                <span className="text-sm font-medium text-blue-600 dark:text-blue-400">
                    {progress}% Completed
                </span>
            </div>

            <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700 mb-6">
                <div
                    className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                ></div>
            </div>

            <div className="flex justify-between">
                <button
                    onClick={() => onNavigate(currentQuestionIndex - 1)}
                    disabled={currentQuestionIndex === 0}
                    className={`px-4 py-2 rounded-md ${currentQuestionIndex === 0
                            ? 'bg-gray-300 cursor-not-allowed text-gray-500'
                            : 'bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 shadow-sm'
                        }`}
                >
                    &larr; Previous
                </button>

                <button
                    onClick={() => onNavigate(currentQuestionIndex + 1)}
                    disabled={currentQuestionIndex === totalQuestions - 1} // Let them navigate next even if not answered? Requirements say "One Question at a Time".
                    // Usually strict mode prevents next. 
                    // Plan says: "Disabled Next until current question is recorded"
                    className={`px-4 py-2 rounded-md ${currentQuestionIndex === totalQuestions - 1
                            ? 'invisible'
                            : (!canNavigateNext
                                ? 'bg-gray-300 cursor-not-allowed text-gray-500'
                                : 'bg-blue-600 hover:bg-blue-700 text-white shadow-sm'
                            )
                        }`}
                >
                    Next &rarr;
                </button>
            </div>
        </div>
    );
};

export default QuestionNavigator;
