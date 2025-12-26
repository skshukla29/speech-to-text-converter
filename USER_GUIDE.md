# 🎙️ Speech-to-Text Converter - User Guide

Complete guide for using the Speech-to-Text Converter web application.

## 📋 Table of Contents
1. [Features](#features)
2. [Quick Start](#quick-start)
3. [How to Use](#how-to-use)
4. [API Documentation](#api-documentation)
5. [Troubleshooting](#troubleshooting)

---

## ✨ Features

### Language Detection & Transcription
- **Automatic Language Detection**: Detects spoken language from audio
- **Native Language Transcription**: Transcribes in detected language (no forced English)
- **100+ Languages**: English, Spanish, French, German, Arabic, Hindi, Urdu, Chinese, Japanese, Korean, and more
- **Confidence Scores**: Shows transcription quality percentage
- **Timestamped Segments**: Displays when each phrase was spoken

### Audio Input Methods
- **File Upload**: MP3, WAV, WEBM, OGG, M4A, FLAC, AAC, WMA (max 50MB)
- **Live Recording**: Record directly from microphone
- **Separate Displays**: Upload and live recording shown separately

### Translation Feature
- **One-Click Translation**: Dropdown menu to select target language
- **10+ Languages**: English, Spanish, French, German, Chinese, Japanese, Korean, Arabic, Hindi, Russian
- **Original Preserved**: Original transcript remains visible
- **Free Service**: Uses Google Translate (no API key needed)

---

## 🚀 Quick Start

### Prerequisites
```bash
# Required:
- Python 3.8+
- Node.js 14+
- FFmpeg
```

### Installation

**1. Backend Setup**
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**2. Frontend Setup**
```bash
cd frontend
npm install
```

### Running

**Terminal 1 - Backend:**
```bash
cd backend
.\venv\Scripts\Activate.ps1
python app.py
```
✅ Backend: http://localhost:5000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```
✅ Frontend: http://localhost:3000

---

## 💡 How to Use

### Method 1: Upload Audio File

1. **Select "Upload Audio File"** from sidebar
2. **(Optional)** Choose expected language from dropdown
   - Select "Auto-detect" for automatic detection
   - Or force a specific language
3. **Click "Choose Audio File"**
   - Supported: MP3, WAV, WEBM, OGG, M4A, FLAC, AAC, WMA
   - Max size: 50MB
4. **Click "Upload & Transcribe"**
5. **Wait for processing** (1-2 min per 10 min of audio)
6. **View Results:**
   - Detected language
   - Confidence score
   - Full transcript
   - Timestamped segments

### Method 2: Live Recording

1. **Select "Live Recording"** from sidebar
2. **(Optional)** Choose expected language
3. **Click "Start Recording"**
   - Allow microphone access when prompted
4. **Speak clearly** into your microphone
5. **Click "Stop Recording"** when done
6. **Wait for processing**
7. **View Results:**
   - Same as file upload
   - Separate from uploaded files

### Method 3: Translate Transcript

1. **After transcription completes:**
   - Scroll to "Translate Transcript" section
   - Original transcript is shown at top
2. **Select target language** from dropdown
   - Choose from 10 available languages
3. **Wait for translation** (< 1 second)
4. **View translated version** below original
5. **Original remains visible** for comparison

---

## 🌐 API Documentation

### POST /api/transcribe
Transcribe uploaded audio file with language detection.

**Request:**
```http
POST http://localhost:5000/api/transcribe
Content-Type: multipart/form-data

FormData:
  audio: <file>
  force_language: "en" (optional)
```

**Response:**
```json
{
  "success": true,
  "language": "en",
  "language_name": "English",
  "text": "Full transcript text...",
  "confidence": 0.92,
  "segments": [
    {
      "start": 0.0,
      "end": 5.2,
      "text": "Segment text..."
    }
  ]
}
```

### POST /api/live
Transcribe live microphone recording.

**Request:**
```http
POST http://localhost:5000/api/live
Content-Type: multipart/form-data

FormData:
  audio: <webm_blob>
  force_language: "es" (optional)
```

**Response:** Same structure as /api/transcribe

### POST /api/translate
Translate text to target language.

**Request:**
```http
POST http://localhost:5000/api/translate
Content-Type: application/json

{
  "text": "Hello world",
  "source_lang": "auto",
  "target_lang": "es"
}
```

**Response:**
```json
{
  "success": true,
  "original_text": "Hello world",
  "translated_text": "Hola mundo",
  "source_lang": "en",
  "target_lang": "es"
}
```

---

## 🔧 Troubleshooting

### Backend Won't Start

**Error: "Module not found"**
```bash
# Solution: Activate venv and reinstall
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Error: "FFmpeg not found"**
```bash
# Solution: Install FFmpeg
# Windows (Chocolatey):
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
# Add to PATH environment variable
```

**Error: "Port 5000 already in use"**
```bash
# Solution: Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Frontend Won't Start

**Error: "Port 3000 already in use"**
```bash
# Solution: Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Error: "npm: command not found"**
```bash
# Solution: Install Node.js
# Download from: https://nodejs.org/
```

### Transcription Issues

**Low Confidence Score (<60%)**
- Use higher quality audio
- Reduce background noise
- Speak clearly and slowly
- Try larger Whisper model (edit app.py)

**Wrong Language Detected**
- Use "Force Language" dropdown
- Ensure audio is primarily in one language
- Check for background music/noise

**Translation Failed**
- Check internet connection (required for translation)
- Try different target language
- Check if source text is valid

### Microphone Not Working

**"Permission Denied"**
- Allow microphone access in browser
- Check Windows microphone permissions
- Try different browser (Chrome recommended)

**No Audio Recorded**
- Check microphone is plugged in
- Test microphone in Windows Sound settings
- Ensure correct microphone is selected

---

## 📊 Output Files

Transcripts are auto-saved in `backend/output/`:

**Filename Format:**
```
transcript_<language>_<timestamp>.txt
transcript_<language>_<timestamp>.json
```

**Example:**
```
transcript_en_20251226_143052.txt
transcript_en_20251226_143052.json
```

**Text File Content:**
```
Language: English (en)
Confidence: 0.92
Timestamp: 2025-12-26 14:30:52
------------------------------------------------------------

Full transcript text appears here with proper formatting
and line breaks for readability.

------------------------------------------------------------

Segments:

[0.00s - 5.20s] First segment of speech
[5.20s - 10.45s] Second segment of speech
[10.45s - 15.80s] Third segment of speech
```

**JSON File Content:**
```json
{
  "language": "en",
  "language_name": "English",
  "text": "Full transcript...",
  "confidence": 0.92,
  "segments": [
    {
      "start": 0.0,
      "end": 5.2,
      "text": "First segment of speech"
    }
  ]
}
```

---

## 🎯 Best Practices

### For Best Transcription Quality:
1. Use high-quality audio (WAV > MP3)
2. Minimize background noise
3. Speak clearly at moderate pace
4. Use microphone close to speaker
5. One speaker at a time works best

### For Accurate Language Detection:
1. Audio should be primarily in one language
2. Longer audio = better detection
3. Clear speech improves detection
4. If known, force the language manually

### For Better Translations:
1. Shorter sentences translate better
2. Avoid idioms and slang
3. Technical terms may not translate well
4. Review translations for accuracy

---

## 🌍 Supported Languages

### Transcription (100+ languages via Whisper)
English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Chinese (Simplified & Traditional), Korean, Arabic, Hindi, Urdu, Bengali, Turkish, Polish, Dutch, Swedish, Danish, Norwegian, Finnish, Ukrainian, Greek, Czech, Romanian, Hungarian, Bulgarian, Serbian, Croatian, Slovak, Slovenian, Lithuanian, Latvian, Estonian, Vietnamese, Thai, Indonesian, Malay, Tagalog, Hebrew, Persian, Swahili, Tamil, Telugu, Kannada, Malayalam, Marathi, Punjabi, Gujarati, and many more!

### Translation (10 quick-access languages)
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Chinese Simplified (zh-CN)
- Japanese (ja)
- Korean (ko)
- Arabic (ar)
- Hindi (hi)
- Russian (ru)

---

## ⚙️ Configuration Options

### Change Whisper Model Size

Edit `backend/app.py` or `backend/multilingual_transcribe.py`:

```python
# Options:
transcriber = MultilingualTranscriber(model_size="tiny")    # Fastest, least accurate
transcriber = MultilingualTranscriber(model_size="base")    # Balanced (default)
transcriber = MultilingualTranscriber(model_size="small")   # Better accuracy
transcriber = MultilingualTranscriber(model_size="medium")  # Best accuracy, slowest
transcriber = MultilingualTranscriber(model_size="large")   # Maximum accuracy, very slow
```

### Add More Translation Languages

Edit `frontend/src/App.js`:

```javascript
const translationLanguages = [
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Spanish' },
  { code: 'pt', name: 'Portuguese' },  // Add new
  { code: 'it', name: 'Italian' },     // Add new
  // ... add more
];
```

---

## 📞 Support

### Common Questions

**Q: How long does transcription take?**  
A: ~1-2 minutes per 10 minutes of audio (base model).

**Q: Is my data private?**  
A: Yes! All processing is local. Translation uses public Google API but data isn't stored.

**Q: Can I use this offline?**  
A: Transcription works offline after initial model download. Translation requires internet.

**Q: What's the file size limit?**  
A: 50MB per file. For larger files, split them first.

**Q: Can I process multiple files at once?**  
A: No, but you can upload files sequentially. Each saves separately.

---

## ✅ Quick Reference

```bash
# Start Everything
cd backend
.\venv\Scripts\Activate.ps1
python app.py

# New terminal
cd frontend
npm start

# Access
http://localhost:3000

# Check Output
cd backend/output
dir  # or ls on Linux/Mac
```

---

**Happy Transcribing! 🎉**
