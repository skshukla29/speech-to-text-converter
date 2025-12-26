# Speech-to-Text Converter - Complete Setup Guide

A full-stack web application that converts audio files and live recordings into text using OpenAI's Whisper model.

## Features

- 🎤 **Live Recording**: Record audio directly from your microphone
- 📁 **File Upload**: Upload audio files in various formats (MP3, WAV, M4A, FLAC, etc.)
- 🌍 **Language Detection**: Automatically detects the language being spoken
- ⏱️ **Timestamped Segments**: View transcription with precise timestamps
- 🎨 **Dark/Light Theme**: Toggle between dark and light modes
- 🚀 **Fast Processing**: Uses Whisper base model for quick transcription

## Tech Stack

### Backend
- Python 3.8+
- Flask - Web framework
- OpenAI Whisper - Speech recognition
- FFmpeg-Python - Audio preprocessing
- Flask-CORS - Cross-origin resource sharing

### Frontend
- React 18
- Context API for theme management
- Modern CSS with CSS variables
- Responsive design

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 14+** and npm - [Download Node.js](https://nodejs.org/)
- **FFmpeg** - Required for audio processing
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `choco install ffmpeg`
  - Mac: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`

## Installation & Setup

### 1. Backend Setup

#### Navigate to Backend Directory

```bash
cd backend
```

#### Create Virtual Environment

```bash
python -m venv venv
```

#### Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

#### Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note:** The first time you run the app, Whisper will download the model (~140MB for base model). This is a one-time download.

### 2. Frontend Setup

Open a new terminal window and navigate to the frontend directory:

```bash
cd frontend
npm install
```

## Running the Application

### Start the Backend Server

In the backend directory with the virtual environment activated:

```bash
cd backend
.\venv\Scripts\Activate.ps1  # Windows PowerShell
python app.py
```

The backend server will start on `http://localhost:5000`

You should see:
```
Loading Whisper model...
Whisper model 'base' loaded successfully
 * Running on http://0.0.0.0:5000
```

### Start the Frontend Development Server

In a new terminal, navigate to the frontend directory:

```bash
cd frontend
npm start
```

The frontend will open automatically in your browser at `http://localhost:3000`

## Usage

### 1. Upload Audio File
- Click on "Upload Audio" in the sidebar
- Choose an audio file from your computer (MP3, WAV, M4A, FLAC, etc.)
- Click "Upload & Transcribe"
- Wait for the transcription to complete (may take 30-60 seconds)
- View the full transcript, detected language, and timestamped segments

### 2. Live Recording
- Click on "Live Recording" in the sidebar
- Click "Start Recording" and allow microphone access when prompted
- Speak into your microphone
- Click "Stop Recording" when finished
- The audio will be automatically transcribed

### 3. Theme Toggle
- Click the sun/moon icon in the sidebar to switch between light and dark themes

## Project Structure

```
Speech-to-Text-Converter/
├── backend/
│   ├── app.py                    # Flask API server with endpoints
│   ├── preprocess_audio.py       # Audio preprocessing with FFmpeg
│   ├── transcribe_whisper.py     # Whisper transcription module
│   ├── requirements.txt          # Python dependencies
│   ├── venv/                     # Virtual environment (created by you)
│   └── output/                   # Temporary audio files (auto-created)
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── manifest.json
│   ├── src/
│   │   ├── App.js               # Main app component
│   │   ├── App.css
│   │   ├── index.js
│   │   ├── components/
│   │   │   ├── AudioUpload.js   # File upload component
│   │   │   ├── AudioUpload.css
│   │   │   ├── LiveRecording.js # Live recording component
│   │   │   ├── LiveRecording.css
│   │   │   ├── Sidebar.js       # Navigation sidebar
│   │   │   └── Sidebar.css
│   │   └── context/
│   │       └── ThemeContext.js  # Theme management
│   ├── package.json
│   └── node_modules/            # Node dependencies (created by npm)
└── README.md
```

## API Endpoints

### `POST /api/upload`
Upload and transcribe an audio file.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `audio` file

**Response:**
```json
{
  "success": true,
  "transcript": "Transcribed text...",
  "language": "en",
  "segments": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "Hello world"
    }
  ]
}
```

### `POST /api/live-record`
Transcribe a live recording.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `audio` blob (WebM format)

**Response:** Same as `/api/upload`

### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "Speech-to-Text API is running"
}
```

## Configuration

### Change Whisper Model Size

Edit `backend/app.py` line 18:

```python
transcriber = WhisperTranscriber(model_size="base")  # Change to tiny, small, medium, or large
```

Available models (accuracy vs speed):
- `tiny` - Fastest, least accurate (~39M params)
- `base` - Good balance, recommended (default) (~74M params)
- `small` - Better accuracy (~244M params)
- `medium` - High accuracy (~769M params)
- `large` - Best accuracy, slowest (~1550M params)

### Change Max Upload Size

Edit `backend/app.py` line 16:

```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Change to desired size in bytes
```

### Supported Audio Formats

The app supports: MP3, WAV, WEBM, OGG, M4A, FLAC, AAC, WMA

To add more formats, edit `backend/app.py` line 14:

```python
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'webm', 'ogg', 'm4a', 'flac', 'aac', 'wma', 'your_format'}
```

## Troubleshooting

### Backend Issues

#### Error: "Import 'flask' could not be resolved"
**Solution:**
- Make sure you've activated the virtual environment
- Run `pip install -r requirements.txt` again
- Check if you're in the correct directory

#### Error: "FFmpeg not found" or "ffmpeg.Error"
**Solution:**
- Install FFmpeg and ensure it's in your system PATH
- Verify installation: Run `ffmpeg -version` in terminal
- Restart your terminal after installation
- On Windows, you may need to restart VS Code

#### Error: "Module 'whisper' not found"
**Solution:**
```bash
pip install openai-whisper
```

#### Slow transcription on first run
**Explanation:**
- Whisper downloads the model on first use (~140MB)
- Subsequent runs will be much faster
- Consider using `tiny` or `base` model for faster processing

#### Out of memory errors
**Solution:**
- Use a smaller Whisper model (`tiny` or `base`)
- Reduce audio file size
- Close other applications

### Frontend Issues

#### Error: "Failed to connect to the server"
**Solution:**
- Ensure the backend is running on `http://localhost:5000`
- Check terminal for backend errors
- Verify CORS is properly configured in `app.py`

#### Error: "npm: command not found"
**Solution:**
- Install Node.js from [nodejs.org](https://nodejs.org/)
- Restart your terminal
- Verify: `node --version` and `npm --version`

#### Microphone not working
**Solution:**
- Grant microphone permissions in your browser
- Check browser console for errors (F12)
- Try a different browser (Chrome/Firefox recommended)
- HTTPS is required for microphone access in production

#### "Loading" stuck or infinite loading
**Solution:**
- Check backend terminal for errors
- Verify file size is within limits
- Check network tab in browser DevTools (F12)

### General Issues

#### Port already in use
**Backend (Port 5000):**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

**Frontend (Port 3000):**
- React will automatically suggest port 3001
- Press 'Y' to use alternate port

## Performance Tips

1. **Use smaller Whisper models** (`tiny` or `base`) for faster processing
2. **Limit audio file size** (< 10MB recommended)
3. **Split long audio** into smaller chunks for better performance
4. **Use GPU** for faster transcription (requires CUDA-enabled PyTorch)
5. **Close unnecessary applications** to free up memory

## Production Deployment

### Build Frontend

```bash
cd frontend
npm run build
```

### Serve with Production Server

Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables

For production, set:
- `FLASK_ENV=production`
- Configure proper CORS origins
- Use environment-specific configuration

## Common Commands

### Backend
```bash
# Activate virtual environment (Windows)
cd backend
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py

# Deactivate virtual environment
deactivate
```

### Frontend
```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## License

MIT License - feel free to use this project for learning and development.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition model
- [Flask](https://flask.palletsprojects.com/) - Backend framework
- [React](https://react.dev/) - Frontend library
- [FFmpeg](https://ffmpeg.org/) - Audio processing

## Support

For issues and questions:
1. Check this troubleshooting guide
2. Review backend terminal output
3. Check browser console (F12)
4. Open an issue on GitHub with error details

---

**Happy transcribing! 🎤→📝**
