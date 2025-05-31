import { useState, useRef } from "react";

export default function Home() {
  const [recording, setRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // Determine API URL based on environment
  const apiUrl = typeof window !== "undefined" && process.env.NODE_ENV === "development"
    ? "http://localhost:8000"
    : "";

  const startRecording = async () => {
    setTranscript("");
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    audioChunksRef.current = [];
    mediaRecorderRef.current.ondataavailable = (e) => {
      audioChunksRef.current.push(e.data);
    };
    mediaRecorderRef.current.onstop = async () => {
      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
      const formData = new FormData();
      formData.append("file", audioBlob, "audio.webm");
      const res = await fetch(`${apiUrl}/api/speech_to_text`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setTranscript(data.transcription);
    };
    mediaRecorderRef.current.start();
    setRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setRecording(false);
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>Speech to Text Demo</h1>
      <button onClick={recording ? stopRecording : startRecording}>
        {recording ? "Stop Recording" : "Start Recording"}
      </button>
      <div style={{ marginTop: 20 }}>
        <strong>Transcription:</strong>
        <div>{transcript}</div>
      </div>
    </div>
  );
} 