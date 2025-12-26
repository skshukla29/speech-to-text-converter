# Local Testing Instructions for VS Code

## Prerequisites
- Python 3.9 or 3.10 installed
- FFmpeg installed on your system

## Step 1: Create Virtual Environment

Open VS Code terminal in the backend folder:

```powershell
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Step 2: Install Dependencies

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install build tools first
pip install setuptools wheel Cython

# Install all requirements
pip install -r requirements.txt
```

**Note**: Installing torch and openai-whisper takes 5-10 minutes. Be patient!

## Step 3: Run Flask App

```powershell
# Run the app
python app.py
```

You should see:
```
Loading Whisper model...
 * Running on http://0.0.0.0:5000
```

## Step 4: Test Health Endpoint

Open a new terminal or browser and test:

```powershell
# Using curl (if available)
curl http://localhost:5000/api/health

# Or using PowerShell
Invoke-RestMethod -Uri http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Speech-to-Text API is running"
}
```

## Step 5: Test Transcription Endpoint

Create a test file to verify transcription works:

```powershell
# Test with a small audio file
curl -X POST -F "audio=@path/to/your/audio.mp3" http://localhost:5000/api/transcribe
```

## Troubleshooting

### Issue: Virtual environment not activating
**Solution**: Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: pip install fails with "error: Microsoft Visual C++ 14.0 is required"
**Solution**: Install Visual C++ Build Tools:
- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Install "Desktop development with C++"

### Issue: "FFmpeg not found"
**Solution**: Install FFmpeg:
```powershell
# Using Chocolatey (if installed)
choco install ffmpeg

# Or download manually from https://ffmpeg.org/download.html
# Add FFmpeg to PATH environment variable
```

### Issue: Out of memory when loading Whisper model
**Solution**: Use a smaller model in app.py:
```python
transcriber = WhisperTranscriber(model_size="tiny")  # or "base"
```

## Deactivate Virtual Environment

When done testing:
```powershell
deactivate
```

## Quick Test Script

Save this as `test_backend.py` in the backend folder:

```python
import requests

# Test health endpoint
response = requests.get('http://localhost:5000/api/health')
print(f"Health Check: {response.json()}")

# Test if server is running
if response.status_code == 200:
    print("✅ Backend is running successfully!")
else:
    print("❌ Backend is not responding")
```

Run it:
```powershell
python test_backend.py
```
