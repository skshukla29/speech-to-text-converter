import React, { useState } from 'react';
import './AudioUpload.css';

const AudioUpload = ({ setRawTranscript: setParentRaw, setCorrectedTranscript: setParentCorrected, setDetectedLanguage: setParentLanguage, setTranslatedText: setParentTranslation }) => {
  const [file, setFile] = useState(null);
  const [transcript, setTranscript] = useState('');
  const [detectedLanguage, setDetectedLanguage] = useState('');
  const [languageName, setLanguageName] = useState('');
  const [confidence, setConfidence] = useState(0);
  const [selectedLanguage, setSelectedLanguage] = useState('auto');
  const [segments, setSegments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Supported languages
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

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError('');
      setTranscript('');
      setDetectedLanguage('');
      setSegments([]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select an audio file');
      return;
    }

    setLoading(true);
    setError('');
    setTranscript('');
    setDetectedLanguage('');
    setSegments([]);

    const formData = new FormData();
    formData.append('audio', file);
    
    // Add language preference if not auto-detect
    if (selectedLanguage !== 'auto') {
      formData.append('force_language', selectedLanguage);
    }

    try {
      const response = await fetch('http://localhost:5000/api/transcribe', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.success) {
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
        setError(data.error || 'Failed to transcribe audio');
      }
    } catch (err) {
      setError('Failed to connect to the server. Make sure the backend is running on port 5000.');
      console.error('Upload error:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="audio-upload">
      <h2>📤 Upload Audio File</h2>
      
      <div className="upload-section">
        <div className="language-selector">
          <label htmlFor="language-select">Force Language (Optional):</label>
          <select
            id="language-select"
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="language-dropdown"
            disabled={loading}
          >
            {languages.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>

        <input
          type="file"
          accept="audio/*,.mp3,.wav,.webm,.ogg,.m4a,.flac,.aac,.wma"
          onChange={handleFileChange}
          className="file-input"
          id="audio-file"
        />
        <label htmlFor="audio-file" className="file-label">
          {file ? file.name : 'Choose Audio File'}
        </label>
        
        <button
          onClick={handleUpload}
          disabled={!file || loading}
          className="upload-button"
        >
          {loading ? 'Processing...' : 'Upload & Transcribe'}
        </button>
      </div>

      {loading && (
        <div className="loading-message">
          <p>🔄 Processing your audio... This may take a minute.</p>
        </div>
      )}

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

export default AudioUpload;
