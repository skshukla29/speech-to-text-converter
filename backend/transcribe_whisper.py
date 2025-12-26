"""
Whisper transcription module.
Loads Whisper model and transcribes audio files.
"""
import whisper
import os


class WhisperTranscriber:
    """Wrapper class for Whisper model transcription."""
    
    def __init__(self, model_size="base"):
        """
        Initialize Whisper transcriber with specified model size.
        
        Args:
            model_size (str): Size of Whisper model to use 
                             (tiny, base, small, medium, large)
                             Default: base
        """
        self.model_size = model_size
        self.model = None
        print(f"Initializing Whisper model: {model_size}")
        self._load_model()
    
    def _load_model(self):
        """Load the Whisper model."""
        try:
            self.model = whisper.load_model(self.model_size)
            print(f"Whisper model '{self.model_size}' loaded successfully")
        except Exception as e:
            raise Exception(f"Failed to load Whisper model: {str(e)}")
    
    def transcribe(self, audio_path, language=None):
        """
        Transcribe audio file using Whisper.
        
        Args:
            audio_path (str): Path to audio file
            language (str, optional): Language code (e.g., 'en', 'es', 'fr')
                                     If None, language is auto-detected
        
        Returns:
            dict: Dictionary containing:
                - transcript (str): The transcribed text
                - language (str): Detected or specified language
                - segments (list): Detailed segments with timestamps
        
        Raises:
            Exception: If transcription fails
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        try:
            print(f"Transcribing audio: {audio_path}")
            
            # Transcribe audio
            options = {}
            if language:
                options['language'] = language
            
            result = self.model.transcribe(audio_path, **options)
            
            # Extract relevant information
            transcript_data = {
                'transcript': result['text'].strip(),
                'language': result.get('language', 'unknown'),
                'segments': [
                    {
                        'start': seg['start'],
                        'end': seg['end'],
                        'text': seg['text'].strip()
                    }
                    for seg in result.get('segments', [])
                ]
            }
            
            print(f"Transcription complete. Language detected: {transcript_data['language']}")
            return transcript_data
        
        except Exception as e:
            raise Exception(f"Error during transcription: {str(e)}")


def transcribe_audio(audio_path, model_size="base", language=None):
    """
    Convenience function to transcribe audio in one call.
    
    Args:
        audio_path (str): Path to audio file
        model_size (str): Whisper model size (default: base)
        language (str, optional): Language code
    
    Returns:
        dict: Transcription results
    """
    transcriber = WhisperTranscriber(model_size=model_size)
    return transcriber.transcribe(audio_path, language=language)


if __name__ == "__main__":
    # Test the transcription function
    test_audio = "output/clean.wav"
    if os.path.exists(test_audio):
        result = transcribe_audio(test_audio)
        print(f"\nTranscript: {result['transcript']}")
        print(f"Language: {result['language']}")
    else:
        print(f"Test file '{test_audio}' not found. Please run preprocess_audio first.")
