import React, { useState } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import Sidebar from './components/Sidebar';
import AudioUpload from './components/AudioUpload';
import LiveRecording from './components/LiveRecording';
import './App.css';

function App() {
  const [activeView, setActiveView] = useState('upload');
  const [rawTranscript, setRawTranscript] = useState('');
  const [correctedTranscript, setCorrectedTranscript] = useState('');
  const [detectedLanguage, setDetectedLanguage] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [isTranslating, setIsTranslating] = useState(false);
  const [showRaw, setShowRaw] = useState(false); // Toggle between raw and corrected

  // Translation languages
  const translationLanguages = [
    { code: 'en', name: 'English' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'zh-CN', name: 'Chinese' },
    { code: 'ja', name: 'Japanese' },
    { code: 'ko', name: 'Korean' },
    { code: 'ar', name: 'Arabic' },
    { code: 'hi', name: 'Hindi' },
    { code: 'ru', name: 'Russian' }
  ];

  // Handle translation
  const handleTranslate = async (targetLang) => {
    const textToTranslate = showRaw ? rawTranscript : correctedTranscript;
    if (!textToTranslate) return;

    setIsTranslating(true);
    try {
      const response = await fetch('http://localhost:5000/api/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: textToTranslate,
          source_lang: detectedLanguage || 'auto',
          target_lang: targetLang,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setTranslatedText(data.translated_text);
      } else {
        alert('Translation failed: ' + (data.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('Translation error:', error);
      alert('Failed to translate. Please check your connection.');
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <ThemeProvider>
      <div className="app">
        <Sidebar activeView={activeView} setActiveView={setActiveView} />
        <main className="main-content">
          <div className="container">
            <h1>🎙️ Speech-to-Text Converter</h1>
            <p className="subtitle">Multilingual transcription with automatic language detection</p>
            
            {activeView === 'upload' && (
              <AudioUpload 
                setRawTranscript={setRawTranscript}
                setCorrectedTranscript={setCorrectedTranscript}
                setDetectedLanguage={setDetectedLanguage}
                setTranslatedText={setTranslatedText}
              />
            )}
            
            {activeView === 'live' && (
              <LiveRecording 
                setRawTranscript={setRawTranscript}
                setCorrectedTranscript={setCorrectedTranscript}
                setDetectedLanguage={setDetectedLanguage}
                setTranslatedText={setTranslatedText}
              />
            )}

            {/* Transcript Display with Raw/Corrected Toggle */}
            {(rawTranscript || correctedTranscript) && (
              <div className="translation-panel">
                <div className="transcript-header">
                  <h3>📝 Transcript</h3>
                  <div className="toggle-container">
                    <label className="toggle-switch">
                      <input 
                        type="checkbox" 
                        checked={showRaw} 
                        onChange={() => setShowRaw(!showRaw)}
                      />
                      <span className="toggle-slider"></span>
                    </label>
                    <span className="toggle-label">
                      {showRaw ? 'Raw (Whisper Output)' : 'Corrected (NLP Enhanced)'}
                    </span>
                  </div>
                </div>
                
                <div className="language-info">
                  Detected Language: <strong>{detectedLanguage.toUpperCase()}</strong>
                </div>
                
                <div className="transcript-box">
                  <p>{showRaw ? rawTranscript : correctedTranscript}</p>
                </div>

                {!showRaw && rawTranscript !== correctedTranscript && (
                  <div className="correction-note">
                    ✨ This text has been enhanced with grammar correction and filler word removal
                  </div>
                )}

                <div className="translation-controls">
                  <h4>🌍 Translate Transcript</h4>
                  <div className="translation-selector">
                    <label htmlFor="target-lang">Choose target language:</label>
                    <select 
                      id="target-lang" 
                      className="language-dropdown"
                      onChange={(e) => {
                        if (e.target.value) {
                          handleTranslate(e.target.value);
                        }
                      }}
                      disabled={isTranslating}
                      defaultValue=""
                    >
                      <option value="">-- Select Language --</option>
                      {translationLanguages.map((lang) => (
                        <option key={lang.code} value={lang.code}>
                          {lang.name}
                        </option>
                      ))}
                    </select>
                    {isTranslating && <span className="translating-indicator">Translating...</span>}
                  </div>
                </div>

                {translatedText && (
                  <div className="translated-result">
                    <h4>✨ Translated Version</h4>
                    <div className="translated-box">
                      <p>{translatedText}</p>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </main>
      </div>
    </ThemeProvider>
  );
}

export default App;
