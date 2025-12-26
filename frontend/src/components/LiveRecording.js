import React, { useState, useRef } from 'react';
import './LiveRecording.css';
import { startLiveRecording } from '../api';

const LiveRecording = ({ setRawTranscript: setParentRaw, setCorrectedTranscript: setParentCorrected, setDetectedLanguage: setParentLanguage, setTranslatedText: setParentTranslation }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [detectedLanguage, setDetectedLanguage] = useState('');
  const [languageName, setLanguageName] = useState('');
  const [confidence, setConfidence] = useState(0);
  const [selectedLanguage, setSelectedLanguage] = useState('auto');
  const [segments, setSegments] = useState([]);
  const [error, setError] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  // Supported languages (same as AudioUpload)
  const languages = [
    { code: 'auto', name: 'Auto-detect' },
    { code: 'en', name: 'English' },
    { code: 'es', name: 'Spanish (Español)' },
    { code: 'fr', name: 'French (Français)' },
    { code: 'de', name: 'German (Deutsch)' },
    { code: 'it', name: 'Italian (Italiano)' },
    { code: 'pt', name: 'Portuguese (Português)' },
    { code: 'ru', name: 'Russian (Русский)' },
    { code: 'ja', name: 'Japanese (日本語)' },
    { code: 'zh', name: 'Chinese (中文)' },
    { code: 'ko', name: 'Korean (한국어)' },
    { code: 'ar', name: 'Arabic (العربية)' },
    { code: 'hi', name: 'Hindi (हिन्दी)' },
    { code: 'ur', name: 'Urdu (اردو)' },
    { code: 'tr', name: 'Turkish (Türkçe)' },
    { code: 'pl', name: 'Polish (Polski)' },
    { code: 'nl', name: 'Dutch (Nederlands)' },
    { code: 'sv', name: 'Swedish (Svenska)' },
    { code: 'da', name: 'Danish (Dansk)' },
    { code: 'no', name: 'Norwegian (Norsk)' },
    { code: 'fi', name: 'Finnish (Suomi)' },
    { code: 'uk', name: 'Ukrainian (Українська)' },
    { code: 'el', name: 'Greek (Ελληνικά)' },
    { code: 'cs', name: 'Czech (Čeština)' },
    { code: 'ro', name: 'Romanian (Română)' },
    { code: 'vi', name: 'Vietnamese (Tiếng Việt)' },
    { code: 'th', name: 'Thai (ไทย)' },
    { code: 'id', name: 'Indonesian (Bahasa Indonesia)' },
    { code: 'ms', name: 'Malay (Bahasa Melayu)' },
    { code: 'he', name: 'Hebrew (עברית)' },
    { code: 'fa', name: 'Persian (فارسی)' }
  ];

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

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        await sendAudioToServer(audioBlob);
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setError('');
      setTranscript('');
      setDetectedLanguage('');
      setSegments([]);
    } catch (err) {
      setError('Failed to access microphone. Please check permissions.');
      console.error('Microphone access error:', err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const sendAudioToServer = async (audioBlob) => {
    setIsProcessing(true);
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');
    
    // Add language preference if not auto-detect
    if (selectedLanguage !== 'auto') {
      formData.append('force_language', selectedLanguage);
    }

    try {
      const data = await startLiveRecording(formData);

      if (data.success) {
        // Set transcript locally for display
        setTranscript(data.corrected_text || data.text);
        setDetectedLanguage(data.language);
        setLanguageName(data.language_name);
        setConfidence(data.confidence);
        setSegments(data.segments || []);
        
        // Update parent state with both raw and corrected
        if (setParentRaw) setParentRaw(data.raw_text || data.text);
        if (setParentCorrected) setParentCorrected(data.corrected_text || data.text);
        if (setParentLanguage) setParentLanguage(data.language);
        if (setParentTranslation) setParentTranslation('');
      } else {
        setError(data.error || 'Failed to transcribe recording');
      }
    } catch (err) {
      setError(err.error || 'Failed to connect to the server. Make sure the backend is running.');
      console.error('Upload error:', err);
    } finally {
      setIsProcessing(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="live-recording">
      <h2>🎤 Live Microphone Recording</h2>
      
      <div className="recording-section">
        <div className="language-selector">
          <label htmlFor="language-select-live">Force Language (Optional):</label>
          <select
            id="language-select-live"
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="language-dropdown"
            disabled={isRecording || isProcessing}
          >
            {languages.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={isRecording ? stopRecording : startRecording}
          className={`record-button ${isRecording ? 'recording' : ''}`}
          disabled={isProcessing}
        >
          <span className="icon">{isRecording ? '⏹️' : '🎤'}</span>
          <span>{isRecording ? 'Stop Recording' : 'Start Recording'}</span>
        </button>
        
        {isRecording && (
          <div className="recording-indicator">
            <span className="pulse"></span>
            Recording in progress...
          </div>
        )}

        {isProcessing && (
          <div className="processing-indicator">
            Processing your recording... This may take a minute.
          </div>
        )}
      </div>

      {error && <div className="error-message">❌ {error}</div>}

      {transcript && (
        <div className="transcription-result">
          <div className="result-header">
            <h3>✅ Transcription Complete</h3>
            <div className="result-info">
              {languageName && (
                <span className="language-badge">
                  Language: {languageName} ({detectedLanguage.toUpperCase()})
                </span>
              )}
              {confidence > 0 && (
                <span className="confidence-badge">
                  Confidence: {(confidence * 100).toFixed(0)}%
                </span>
              )}
            </div>
          </div>
          
          <div className="transcript-text">
            <p>{transcript}</p>
          </div>

          {segments.length > 0 && (
            <div className="segments-section">
              <h4>⏱️ Timestamped Segments:</h4>
              <div className="segments-list">
                {segments.map((segment, index) => (
                  <div key={index} className="segment-item">
                    <span className="segment-time">
                      {formatTime(segment.start)} - {formatTime(segment.end)}
                    </span>
                    <span className="segment-text">{segment.text}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default LiveRecording;
