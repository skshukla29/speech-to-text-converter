# Speech-to-Text Converter

A full-stack application for converting speech to text using React and Flask.

## Features

- 🎤 **Live Microphone Recording**: Record audio directly from your microphone
- 📁 **Audio File Upload**: Upload pre-recorded audio files for transcription
- 🌓 **Dark/Light Theme**: Toggle between dark and light modes
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🎨 **Modern UI**: Clean interface with sidebar navigation

## Project Structure

```
Speech-to-Text Converter/
├── frontend/                 # React application
│   ├── public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── manifest.json
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.js
│   │   │   ├── AudioUpload.js
│   │   │   └── LiveRecording.js
│   │   ├── context/
│   │   │   └── ThemeContext.js
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── backend/                  # Flask API
│   ├── app.py
│   └── requirements.txt
└── README.md
```

## Setup Instructions

### Backend Setup (Flask)

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup (React)

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## Integrating Speech-to-Text

The current implementation includes a placeholder for speech-to-text functionality. To add actual transcription, choose one of these options:

### Option 1: OpenAI Whisper API (Recommended)

1. Install the package:
```bash
pip install openai
```

2. Update `backend/app.py` `transcribe_audio()` function:
```python
import openai

def transcribe_audio(audio_path):
    openai.api_key = "your-api-key-here"
    with open(audio_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]
```

### Option 2: Local Whisper Model

1. Install the package:
```bash
pip install openai-whisper torch
```

2. Update the transcription function:
```python
import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]
```

### Option 3: Google Cloud Speech-to-Text

1. Install the package:
```bash
pip install google-cloud-speech
```

2. Set up Google Cloud credentials and update the function accordingly.

### Option 4: AssemblyAI

1. Install the package:
```bash
pip install assemblyai
```

2. Use AssemblyAI's API for transcription.

## Usage

1. Start both the backend and frontend servers
2. Open your browser to `http://localhost:3000`
3. Choose between:
   - **Upload Audio**: Select an audio file from your computer
   - **Live Recording**: Record audio directly from your microphone
4. Click the appropriate button to transcribe
5. View the transcription results on the page

## API Endpoints

- `POST /api/upload` - Upload audio file for transcription
- `POST /api/live-record` - Process live recording
- `GET /api/health` - Health check endpoint

## Technologies Used

### Frontend
- React 18
- Context API for state management
- CSS3 with CSS variables for theming
- Web Audio API for recording

### Backend
- Flask 3.0
- Flask-CORS for cross-origin requests
- Werkzeug for secure file handling

## Customization

### Changing Theme Colors

Edit the CSS variables in `frontend/src/App.css`:
```css
:root {
  --bg-color: #ffffff;
  --text-color: #333333;
  --button-bg: #007bff;
  /* ... more variables */
}
```

### Adding More Features

- Add user authentication
- Store transcription history
- Support multiple languages
- Export transcriptions to different formats
- Real-time streaming transcription

## Troubleshooting

**CORS Issues**: Make sure Flask-CORS is installed and configured properly

**Microphone Access**: Ensure your browser has permission to access the microphone

**File Size Limit**: The default limit is 16MB. Adjust in `backend/app.py` if needed

**Backend Not Running**: Make sure you activated the virtual environment and installed all dependencies

## License

MIT

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
