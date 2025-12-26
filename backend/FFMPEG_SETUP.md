# FFmpeg Setup Guide for Windows 11

## Understanding the Error

When you see:
```
Error preprocessing audio: [WinError 2] The system cannot find the file specified
```

This error occurs because:
1. **FFmpeg is not installed** - The ffmpeg-python library needs the actual FFmpeg executable
2. **FFmpeg is not in PATH** - Windows can't find the FFmpeg executable
3. **Input audio file doesn't exist** - The audio file path is incorrect

## Step 1: Check if FFmpeg is Already Installed

Open PowerShell and run:
```powershell
ffmpeg -version
```

If you see version information, FFmpeg is installed. If you see an error, continue with installation.

## Step 2: Install FFmpeg on Windows 11

### Option A: Using Chocolatey (Recommended - Easiest)

1. **Install Chocolatey** (if not already installed):
   - Open PowerShell as Administrator
   - Run:
     ```powershell
     Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
     ```

2. **Install FFmpeg**:
   ```powershell
   choco install ffmpeg
   ```

3. **Verify Installation**:
   ```powershell
   ffmpeg -version
   ```

### Option B: Manual Installation

1. **Download FFmpeg**:
   - Go to: https://www.gyan.dev/ffmpeg/builds/
   - Download: **ffmpeg-release-essentials.zip** (or latest release)
   - Alternative link: https://github.com/BtbN/FFmpeg-Builds/releases

2. **Extract Files**:
   - Extract the ZIP file
   - You'll see a folder like `ffmpeg-7.0-essentials_build`
   - Move or rename this folder to: `C:\ffmpeg`

3. **Add FFmpeg to System PATH**:
   
   **Method 1: Using PowerShell (Quick)**
   ```powershell
   # Open PowerShell as Administrator
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\ffmpeg\bin", "Machine")
   ```

   **Method 2: Using GUI**
   - Press `Win + X` and select "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New"
   - Add: `C:\ffmpeg\bin`
   - Click "OK" on all windows

4. **Restart Terminal**:
   - Close all PowerShell/CMD/VS Code terminals
   - Open a new terminal

5. **Verify Installation**:
   ```powershell
   ffmpeg -version
   ```

   You should see output like:
   ```
   ffmpeg version 7.0-essentials_build-www.gyan.dev Copyright (c) 2000-2024 the FFmpeg developers
   built with gcc 13.2.0 (Rev5, Built by MSYS2 project)
   ```

## Step 3: Verify FFmpeg in Your Project

In your VS Code terminal, navigate to your backend directory:

```powershell
cd "d:\Speech-to-Text Converter\backend"
.\venv\Scripts\Activate.ps1
```

Test FFmpeg detection:
```powershell
python -c "import shutil; print('FFmpeg found!' if shutil.which('ffmpeg') else 'FFmpeg NOT found')"
```

## Step 4: Create a Sample Audio File for Testing

### Option A: Download a Sample Audio File

1. Download any audio file (MP3, WAV, M4A) from the internet
2. Place it in: `d:\Speech-to-Text Converter\backend\samples\`
3. Rename it to: `test.mp3`

### Option B: Create a Test Directory

```powershell
cd "d:\Speech-to-Text Converter\backend"
mkdir samples
# Then manually copy an audio file to this folder
```

## Step 5: Test Your preprocess_audio.py Script

```powershell
cd "d:\Speech-to-Text Converter\backend"
.\venv\Scripts\Activate.ps1
python preprocess_audio.py
```

### Test with a Specific Audio File

```powershell
# Test with Python command
python -c "from preprocess_audio import preprocess_audio; preprocess_audio('samples/test.mp3')"
```

Or create a quick test script:

```powershell
# Create test_conversion.py
@"
from preprocess_audio import preprocess_audio

# Replace with your audio file path
audio_file = "samples/test.mp3"

try:
    result = preprocess_audio(audio_file)
    print(f"Success! Output: {result}")
except Exception as e:
    print(f"Error: {e}")
"@ | Out-File -Encoding utf8 test_conversion.py

# Run it
python test_conversion.py
```

## Step 6: Expected Output

When successful, you should see:
```
Processing audio file: D:\Speech-to-Text Converter\backend\samples\test.mp3
Output will be saved to: D:\Speech-to-Text Converter\backend\output\clean.wav
Output directory ready: D:\Speech-to-Text Converter\backend\output
Running FFmpeg conversion...
✓ Audio preprocessed successfully: D:\Speech-to-Text Converter\backend\output\clean.wav
```

## Troubleshooting

### Issue: "FFmpeg is not recognized"

**Solution**: FFmpeg is not in PATH
- Verify PATH: `echo $env:Path`
- Check if `C:\ffmpeg\bin` is listed
- Restart your terminal
- If using VS Code, restart VS Code entirely

### Issue: "Input audio file not found"

**Solution**: Check your file path
```powershell
# Check if file exists
Test-Path "samples/test.mp3"  # Should return True

# Use absolute path
python -c "from preprocess_audio import preprocess_audio; preprocess_audio('D:/Speech-to-Text Converter/backend/samples/test.mp3')"
```

### Issue: "Permission denied"

**Solution**: Run as Administrator or check file permissions
```powershell
# Check file permissions
Get-Acl "samples/test.mp3"
```

### Issue: FFmpeg works in CMD but not in Python

**Solution**: Restart VS Code to refresh environment variables
1. Close VS Code completely
2. Open new VS Code
3. Open new terminal
4. Activate venv and try again

## Quick Verification Script

Save this as `check_setup.py`:

```python
import os
import sys
import shutil

print("=" * 60)
print("Speech-to-Text Setup Checker")
print("=" * 60)

# Check 1: FFmpeg
print("\n1. Checking FFmpeg...")
if shutil.which("ffmpeg"):
    print("   ✓ FFmpeg is installed and in PATH")
    os.system("ffmpeg -version 2>&1 | Select-Object -First 1")
else:
    print("   ❌ FFmpeg NOT found in PATH")
    print("   Please install FFmpeg and add to PATH")

# Check 2: Python packages
print("\n2. Checking Python packages...")
try:
    import ffmpeg
    print("   ✓ ffmpeg-python is installed")
except ImportError:
    print("   ❌ ffmpeg-python not installed")
    print("   Run: pip install ffmpeg-python")

try:
    import whisper
    print("   ✓ openai-whisper is installed")
except ImportError:
    print("   ❌ openai-whisper not installed")
    print("   Run: pip install openai-whisper")

# Check 3: Sample audio files
print("\n3. Checking for sample audio files...")
sample_dirs = ["samples", ".", "../samples"]
found_audio = False
for dir_path in sample_dirs:
    if os.path.exists(dir_path):
        audio_files = [f for f in os.listdir(dir_path) if f.endswith(('.mp3', '.wav', '.m4a', '.flac'))]
        if audio_files:
            print(f"   ✓ Found audio files in {dir_path}: {audio_files}")
            found_audio = True
if not found_audio:
    print("   ⚠ No audio files found for testing")

print("\n" + "=" * 60)
```

Run it:
```powershell
python check_setup.py
```

## Summary - Quick Commands

```powershell
# 1. Install FFmpeg (Chocolatey)
choco install ffmpeg

# 2. Verify FFmpeg
ffmpeg -version

# 3. Test in Python
cd "d:\Speech-to-Text Converter\backend"
.\venv\Scripts\Activate.ps1
python preprocess_audio.py

# 4. Test with specific file
python -c "from preprocess_audio import preprocess_audio; preprocess_audio('your_audio.mp3')"
```

## Need More Help?

1. Check FFmpeg installation: `ffmpeg -version`
2. Check PATH: `echo $env:Path`
3. Restart terminal/VS Code
4. Check file exists: `Test-Path "path/to/audio.mp3"`
5. Use absolute paths when testing

---

**Note**: After adding FFmpeg to PATH, you MUST restart your terminal (and VS Code) for changes to take effect.
