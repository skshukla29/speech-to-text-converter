"""
Audio preprocessing module using ffmpeg-python.
Converts any input audio to 16kHz mono WAV format.
"""
import os
import sys
import shutil
import ffmpeg


def check_ffmpeg_installed():
    """
    Check if FFmpeg is installed and available in PATH.
    
    Returns:
        bool: True if FFmpeg is found, False otherwise
    """
    return shutil.which("ffmpeg") is not None


def preprocess_audio(input_path, output_path="output/clean.wav"):
    """
    Convert input audio file to 16kHz mono WAV format.
    
    Args:
        input_path (str): Path to input audio file
        output_path (str): Path to save cleaned audio (default: output/clean.wav)
    
    Returns:
        str: Path to the cleaned audio file
    
    Raises:
        FileNotFoundError: If input file doesn't exist
        RuntimeError: If FFmpeg is not installed
        Exception: If audio conversion fails
    """
    # Check if FFmpeg is installed
    if not check_ffmpeg_installed():
        raise RuntimeError(
            "FFmpeg is not installed or not in PATH.\n"
            "Please install FFmpeg:\n"
            "1. Download from: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip\n"
            "2. Extract to C:\\ffmpeg\n"
            "3. Add C:\\ffmpeg\\bin to system PATH\n"
            "4. Restart terminal and verify with: ffmpeg -version"
        )
    
    # Convert to absolute path for clarity
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)
    
    # Check if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(
            f"Input audio file not found: {input_path}\n"
            f"Please check the file path and try again."
        )
    
    # Check if input is a file (not a directory)
    if not os.path.isfile(input_path):
        raise ValueError(f"Input path is not a file: {input_path}")
    
    print(f"Processing audio file: {input_path}")
    print(f"Output will be saved to: {output_path}")
    
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            print(f"Output directory ready: {output_dir}")
        
        # Use ffmpeg to convert audio to 16kHz mono WAV
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(
            stream,
            output_path,
            acodec='pcm_s16le',  # 16-bit PCM
            ac=1,                 # Mono audio
            ar='16000'            # 16kHz sample rate
        )
        
        # Overwrite output file if it exists
        print("Running FFmpeg conversion...")
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
        
        print(f"✓ Audio preprocessed successfully: {output_path}")
        return output_path
    
    except ffmpeg.Error as e:
        error_message = e.stderr.decode() if e.stderr else str(e)
        raise Exception(f"FFmpeg error during audio preprocessing: {error_message}")
    except FileNotFoundError as e:
        if "ffmpeg" in str(e).lower():
            raise RuntimeError(
                "FFmpeg executable not found. Please install FFmpeg and add it to PATH."
            )
        raise
    except Exception as e:
        raise Exception(f"Error preprocessing audio: {str(e)}")


if __name__ == "__main__":
    # Test the preprocessing function
    print("=" * 60)
    print("Audio Preprocessing Test")
    print("=" * 60)
    
    # Check FFmpeg installation first
    if not check_ffmpeg_installed():
        print("❌ ERROR: FFmpeg is not installed or not in PATH!")
        print("\nPlease follow these steps:")
        print("1. Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/")
        print("2. Extract to C:\\ffmpeg")
        print("3. Add C:\\ffmpeg\\bin to system PATH")
        print("4. Restart terminal and run: ffmpeg -version")
        sys.exit(1)
    else:
        print("✓ FFmpeg is installed and ready")
    
    # Test with sample audio file
    test_files = [
        "test_audio.wav",
        "samples/test.mp3",
        "../samples/test.mp3",
        "test.mp3"
    ]
    
    test_file = None
    for file_path in test_files:
        if os.path.exists(file_path):
            test_file = file_path
            break
    
    if test_file:
        print(f"\nFound test file: {test_file}")
        try:
            result = preprocess_audio(test_file)
            print(f"\n✓ SUCCESS! Preprocessed audio saved to: {result}")
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            sys.exit(1)
    else:
        print("\n⚠ No test audio file found.")
        print("Please provide an audio file path:")
        print("  python preprocess_audio.py")
        print("\nOr test with a specific file:")
        print("  python -c \"from preprocess_audio import preprocess_audio; preprocess_audio('path/to/audio.mp3')\"")
        print("\nSearched for files:", test_files)
