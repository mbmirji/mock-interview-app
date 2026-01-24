import React, { useState, useRef, useEffect } from 'react';

interface VoiceRecorderProps {
    onRecordingComplete: (audioBlob: Blob) => void;
    isUploading: boolean;
}

const VoiceRecorder: React.FC<VoiceRecorderProps> = ({ onRecordingComplete, isUploading }) => {
    const [isRecording, setIsRecording] = useState(false);
    const [recordingTime, setRecordingTime] = useState(0);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const chunksRef = useRef<Blob[]>([]);
    const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

    useEffect(() => {
        return () => {
            if (timerRef.current) clearInterval(timerRef.current);
        };
    }, []);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            chunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (e) => {
                if (e.data.size > 0) {
                    chunksRef.current.push(e.data);
                }
            };

            mediaRecorderRef.current.onstop = () => {
                const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
                onRecordingComplete(blob);
                stream.getTracks().forEach(track => track.stop());
            };

            mediaRecorderRef.current.start();
            setIsRecording(true);
            setRecordingTime(0);

            timerRef.current = setInterval(() => {
                setRecordingTime(prev => prev + 1);
            }, 1000);

        } catch (err) {
            console.error("Error accessing microphone:", err);
            alert("Could not access microphone. Please allow permissions.");
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
            if (timerRef.current) {
                clearInterval(timerRef.current);
                timerRef.current = null;
            }
        }
    };

    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    return (
        <div className="flex flex-col items-center gap-4 p-4 border rounded-lg bg-gray-50 dark:bg-gray-800">
            <div className="text-xl font-mono font-bold text-gray-700 dark:text-gray-300">
                {isRecording ? formatTime(recordingTime) : "Ready to Record"}
            </div>

            {isUploading ? (
                <div className="text-blue-500 animate-pulse">Uploading and Transcribing...</div>
            ) : (
                <div className="flex gap-4">
                    {!isRecording ? (
                        <button
                            onClick={startRecording}
                            className="px-6 py-3 bg-red-500 hover:bg-red-600 text-white rounded-full font-semibold shadow-lg transition-all flex items-center gap-2"
                        >
                            <div className="w-3 h-3 bg-white rounded-full"></div>
                            Start (Mic)
                        </button>
                    ) : (
                        <button
                            onClick={stopRecording}
                            className="px-6 py-3 bg-gray-700 hover:bg-gray-800 text-white rounded-full font-semibold shadow-lg transition-all flex items-center gap-2"
                        >
                            <div className="w-3 h-3 bg-red-500 rounded-sm"></div>
                            Stop
                        </button>
                    )}
                </div>
            )}

            <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                {isRecording ? "Listening..." : "Click Start to record your answer"}
            </p>
        </div>
    );
};

export default VoiceRecorder;
