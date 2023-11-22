import React, { useState, useRef, useEffect } from 'react';

const AudioRecorder = () => {
  const [isRecording, setRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const audioRef = useRef(null);
  const mediaRecorderRef = useRef(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      const chunks = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunks.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        setAudioBlob(blob);
        const audioUrl = URL.createObjectURL(blob);
        audioRef.current.src = audioUrl;

        // Send the recorded audio to the Flask server
        uploadAudio(blob);
      };

      mediaRecorder.start();
      setRecording(true);
      mediaRecorderRef.current = mediaRecorder;
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  const uploadAudio = async (audioBlob) => {
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob);

      await fetch('http://localhost:5000/audio', {
        method: 'POST',
        body: formData,
      });

      console.log('Audio uploaded successfully');
    } catch (error) {
      console.error('Error uploading audio:', error);
    }
  };

  useEffect(() => {
    return () => {
      // Clean up when the component is unmounted
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.ondataavailable = null;
        mediaRecorderRef.current.onstop = null;
        mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  return (
    <div>
      <h1>Audio Recorder</h1>
      <button onClick={startRecording} disabled={isRecording}>
        Start Recording
      </button>
      <button onClick={stopRecording} disabled={!isRecording}>
        Stop Recording
      </button>
      <audio ref={audioRef} controls />
    </div>
  );
};

export default AudioRecorder;
