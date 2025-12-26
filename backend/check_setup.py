"""
Setup verification script for Speech-to-Text Converter
Checks if all dependencies are properly installed
"""
import os
import sys
import shutil

def main():
    print("=" * 70)
    print(" Speech-to-Text Converter - Setup Verification")
    print("=" * 70)
    
    all_ok = True
    
    # Check 1: FFmpeg
    print("\n[1/5] Checking FFmpeg installation...")
    if shutil.which("ffmpeg"):
        print("      ✓ FFmpeg is installed and in PATH")
        try:
            import subprocess
            result = subprocess.run(["ffmpeg", "-version"], 
                                  capture_output=True, text=True)
            version_line = result.stdout.split('\n')[0]
            print(f"      {version_line}")
        except Exception as e:
            print(f"      ⚠ Could not get version: {e}")
    else:
        print("      ❌ FFmpeg NOT found in PATH")
        print("      → Please install FFmpeg:")
        print("         choco install ffmpeg")
        print("         OR download from: https://www.gyan.dev/ffmpeg/builds/")
        all_ok = False
    
    # Check 2: Python packages
    print("\n[2/5] Checking Python packages...")
    
    required_packages = {
        'flask': 'Flask',
        'flask_cors': 'flask-cors',
        'ffmpeg': 'ffmpeg-python',
        'whisper': 'openai-whisper',
        'torch': 'torch',
        'torchaudio': 'torchaudio'
    }
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"      ✓ {package_name} is installed")
        except ImportError:
            print(f"      ❌ {package_name} NOT installed")
            print(f"         → Run: pip install {package_name}")
            all_ok = False
    
    # Check 3: Directory structure
    print("\n[3/5] Checking directory structure...")
    
    required_dirs = ['output']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"      ✓ {dir_name}/ directory exists")
        else:
            print(f"      ⚠ {dir_name}/ directory missing (will be created automatically)")
    
    # Check 4: Required files
    print("\n[4/5] Checking required files...")
    
    required_files = [
        'app.py',
        'preprocess_audio.py',
        'transcribe_whisper.py',
        'requirements.txt'
    ]
    
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"      ✓ {file_name} exists")
        else:
            print(f"      ❌ {file_name} NOT found")
            all_ok = False
    
    # Check 5: Sample audio files
    print("\n[5/5] Checking for sample audio files...")
    
    audio_extensions = ('.mp3', '.wav', '.m4a', '.flac', '.ogg', '.webm')
    sample_dirs = ['samples', '.', '../samples']
    found_audio = []
    
    for dir_path in sample_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            audio_files = [f for f in os.listdir(dir_path) 
                          if f.lower().endswith(audio_extensions)]
            if audio_files:
                for file in audio_files[:3]:  # Show first 3
                    full_path = os.path.join(dir_path, file)
                    found_audio.append(full_path)
                    print(f"      ✓ Found: {full_path}")
    
    if not found_audio:
        print("      ⚠ No audio files found for testing")
        print("      → Add some audio files to test the transcription")
        print("         Example: samples/test.mp3")
    
    # Summary
    print("\n" + "=" * 70)
    if all_ok:
        print(" ✓ All critical dependencies are installed!")
        print(" → You can run: python app.py")
        if found_audio:
            print(f" → Test preprocessing with: python preprocess_audio.py")
    else:
        print(" ❌ Some dependencies are missing!")
        print(" → Please install the missing items listed above")
        print(" → Then run this script again to verify")
    print("=" * 70)
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
