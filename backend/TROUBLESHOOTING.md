# 🔧 Fixing the FFmpeg Error - Complete Guide

## ❌ The Error You're Seeing

```
Error preprocessing audio: [WinError 2] The system cannot find the file specified
```

---

## 📋 Why This Error Happens

### 1. **FFmpeg Not Installed**
   - The `ffmpeg-python` package is just a Python wrapper
   - It requires the actual FFmpeg executable to be installed on Windows
   - Without FFmpeg, Python can't find the `ffmpeg.exe` program

### 2. **FFmpeg Not in PATH**
   - Even if FFmpeg is installed, Windows needs to know where to find it
   - The PATH environment variable tells Windows where to look for programs
   - If FFmpeg's location isn't in PATH, it won't be found

### 3. **Input Audio File Doesn't Exist**
   - The audio file path might be incorrect
   - The file might not exist in the specified location

---

## ✅ Solution: Install FFmpeg (Choose ONE Method)

### Method 1: Using Chocolatey (EASIEST - Recommended)

#### Step 1: Install Chocolatey Package Manager

Open **PowerShell as Administrator** and run:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

#### Step 2: Install FFmpeg

```powershell
choco install ffmpeg -y
```

#### Step 3: Verify Installation

Close PowerShell and open a **new terminal**, then run:

```powershell
ffmpeg -version
```

✅ You should see FFmpeg version information!

---

### Method 2: Manual Installation

#### Step 1: Download FFmpeg

1. Go to: **https://www.gyan.dev/ffmpeg/builds/**
2. Download: **ffmpeg-release-essentials.zip** (latest version)
   - Alternative: https://github.com/BtbN/FFmpeg-Builds/releases

#### Step 2: Extract Files

1. Extract the downloaded ZIP file
2. You'll see a folder like `ffmpeg-7.0.1-essentials_build`
3. **Rename** this folder to just `ffmpeg`
4. **Move** it to `C:\ffmpeg`

Your structure should be:
```
C:\ffmpeg\
    ├── bin\
    │   ├── ffmpeg.exe
    │   ├── ffplay.exe
    │   └── ffprobe.exe
    ├── doc\
    └── presets\
```

#### Step 3: Add FFmpeg to System PATH

**Option A: Using PowerShell (Quick)**

Open **PowerShell as Administrator** and run:

```powershell
# Add FFmpeg to PATH permanently
$currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
if ($currentPath -notlike "*C:\ffmpeg\bin*") {
    [Environment]::SetEnvironmentVariable("Path", $currentPath + ";C:\ffmpeg\bin", "Machine")
    Write-Host "FFmpeg added to PATH successfully!"
}
```

**Option B: Using Windows Settings (GUI)**

1. Press `Win + X` and select **"System"**
2. Click **"Advanced system settings"** on the right
3. Click **"Environment Variables"** button
4. Under **"System variables"**, find **"Path"** and click **"Edit"**
5. Click **"New"**
6. Type: `C:\ffmpeg\bin`
7. Click **"OK"** on all windows
8. **Restart** your terminal and VS Code

#### Step 4: Verify Installation

**IMPORTANT:** Close all terminals and VS Code, then reopen.

Open a **new terminal** and run:

```powershell
ffmpeg -version
```

You should see output like:
```
ffmpeg version 7.0.1-essentials_build-www.gyan.dev Copyright (c) 2000-2024 the FFmpeg developers
```

---

## 🧪 Test Your Setup

### 1. Verify FFmpeg in Your Project

In VS Code terminal:

```powershell
cd "d:\Speech-to-Text Converter\backend"
.\venv\Scripts\Activate.ps1
python check_setup.py
```

You should see:
```
✓ FFmpeg is installed and in PATH
```

### 2. Test FFmpeg Detection

```powershell
python -c "import shutil; print('✓ FFmpeg found!' if shutil.which('ffmpeg') else '❌ FFmpeg NOT found')"
```

---

## 🎵 Prepare a Test Audio File

### Option 1: Download a Sample

1. Download any audio file (MP3, WAV, M4A) from your computer or online
2. Place it in: `d:\Speech-to-Text Converter\backend\samples\`
3. Rename it to: `test.mp3`

### Option 2: Use Existing Audio

If you have any audio file on your computer, copy it to the samples folder:

```powershell
cd "d:\Speech-to-Text Converter\backend"
# Copy your audio file
Copy-Item "C:\path\to\your\audio.mp3" -Destination "samples\test.mp3"
```

---

## 🚀 Run the Updated Script

### Test the Preprocessing Script

```powershell
cd "d:\Speech-to-Text Converter\backend"
.\venv\Scripts\Activate.ps1
python preprocess_audio.py
```

### Test with a Specific File

```powershell
python -c "from preprocess_audio import preprocess_audio; preprocess_audio('samples/test.mp3')"
```

### Expected Success Output

```
============================================================
Audio Preprocessing Test
============================================================
✓ FFmpeg is installed and ready

Found test file: samples/test.mp3
Processing audio file: D:\Speech-to-Text Converter\backend\samples\test.mp3
Output will be saved to: D:\Speech-to-Text Converter\backend\output\clean.wav
Output directory ready: D:\Speech-to-Text Converter\backend\output
Running FFmpeg conversion...
✓ Audio preprocessed successfully: D:\Speech-to-Text Converter\backend\output\clean.wav

✓ SUCCESS! Preprocessed audio saved to: D:\Speech-to-Text Converter\backend\output\clean.wav
```

---

## 📝 What the Updated Code Does

Your updated `preprocess_audio.py` now:

### ✅ 1. Checks if FFmpeg is Installed
```python
def check_ffmpeg_installed():
    return shutil.which("ffmpeg") is not None
```

### ✅ 2. Validates Input File Exists
```python
if not os.path.exists(input_path):
    raise FileNotFoundError(f"Input audio file not found: {input_path}")
```

### ✅ 3. Provides Clear Error Messages
```python
if not check_ffmpeg_installed():
    raise RuntimeError(
        "FFmpeg is not installed or not in PATH.\n"
        "Please install FFmpeg..."
    )
```

### ✅ 4. Shows Processing Progress
```python
print(f"Processing audio file: {input_path}")
print(f"Output will be saved to: {output_path}")
print("Running FFmpeg conversion...")
```

### ✅ 5. Uses Absolute Paths
```python
input_path = os.path.abspath(input_path)
output_path = os.path.abspath(output_path)
```

---

## 🔍 Troubleshooting Common Issues

### Issue 1: "FFmpeg is not recognized"

**Cause:** FFmpeg not in PATH or terminal not restarted

**Solution:**
```powershell
# Check if FFmpeg is in PATH
echo $env:Path | Select-String "ffmpeg"

# If not found, add it (as Administrator)
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\ffmpeg\bin", "Machine")

# MUST restart terminal/VS Code
```

### Issue 2: "Input audio file not found"

**Cause:** Incorrect file path

**Solution:**
```powershell
# Check if file exists
Test-Path "samples/test.mp3"

# If False, verify the path
Get-ChildItem samples

# Use absolute path
python -c "from preprocess_audio import preprocess_audio; preprocess_audio('D:/Speech-to-Text Converter/backend/samples/test.mp3')"
```

### Issue 3: FFmpeg works in CMD but not in Python

**Cause:** VS Code using old environment variables

**Solution:**
1. **Close VS Code completely** (not just the terminal)
2. **Reopen VS Code**
3. Open a **new terminal**
4. Run the test again

### Issue 4: Permission Denied

**Cause:** File permissions or antivirus blocking

**Solution:**
```powershell
# Run VS Code as Administrator
# Or check file permissions
Get-Acl "samples/test.mp3"
```

---

## 📋 Quick Reference Commands

```powershell
# Install FFmpeg (Chocolatey)
choco install ffmpeg -y

# Verify FFmpeg
ffmpeg -version

# Check setup
cd "d:\Speech-to-Text Converter\backend"
.\venv\Scripts\Activate.ps1
python check_setup.py

# Test preprocessing
python preprocess_audio.py

# Test with specific file
python -c "from preprocess_audio import preprocess_audio; preprocess_audio('samples/test.mp3')"

# Test in Python shell
python
>>> from preprocess_audio import preprocess_audio
>>> preprocess_audio('samples/test.mp3')
>>> exit()
```

---

## ✅ Success Checklist

- [ ] FFmpeg installed (via Chocolatey or manually)
- [ ] FFmpeg added to system PATH
- [ ] Terminal restarted after installation
- [ ] VS Code restarted after PATH change
- [ ] `ffmpeg -version` shows version info
- [ ] `python check_setup.py` shows all green checks
- [ ] Sample audio file placed in `samples/` folder
- [ ] `python preprocess_audio.py` runs successfully
- [ ] Output file created in `output/clean.wav`

---

## 🎯 Next Steps After FFmpeg Setup

Once FFmpeg is working:

1. **Test the Full Backend**:
   ```powershell
   cd "d:\Speech-to-Text Converter\backend"
   .\venv\Scripts\Activate.ps1
   python app.py
   ```

2. **Use the Web Interface**:
   - Open: http://localhost:3000
   - Upload an audio file
   - See the transcription!

3. **Test Whisper Transcription**:
   ```powershell
   python -c "from transcribe_whisper import transcribe_audio; print(transcribe_audio('output/clean.wav'))"
   ```

---

## 💡 Pro Tips

1. **Always use absolute paths** when debugging
2. **Restart terminal** after changing PATH
3. **Check file exists** before processing: `Test-Path filename`
4. **Use smaller audio files** for testing (< 5MB)
5. **Read error messages carefully** - the updated script gives detailed info

---

## 🆘 Still Having Issues?

Run the diagnostic script:

```powershell
cd "d:\Speech-to-Text Converter\backend"
.\venv\Scripts\Activate.ps1
python check_setup.py
```

This will show you exactly what's missing!

---

**Remember:** After installing FFmpeg or changing PATH, you MUST:
1. Close ALL terminals
2. Close VS Code
3. Reopen everything
4. The changes won't work in existing terminals!

---

Good luck! 🚀
