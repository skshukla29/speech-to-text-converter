"""
Multilingual transcription module with automatic language detection.
Uses OpenAI Whisper for speech recognition.
"""
import whisper
import os
import json
from datetime import datetime
from nlp_corrector import NLPCorrector


class MultilingualTranscriber:
    """Advanced transcriber with automatic language detection."""
    
    # Language name mappings
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'zh': 'Chinese',
        'ko': 'Korean',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'ur': 'Urdu',
        'tr': 'Turkish',
        'pl': 'Polish',
        'nl': 'Dutch',
        'sv': 'Swedish',
        'da': 'Danish',
        'no': 'Norwegian',
        'fi': 'Finnish',
        'uk': 'Ukrainian',
        'el': 'Greek',
        'cs': 'Czech',
        'ro': 'Romanian',
        'vi': 'Vietnamese',
        'th': 'Thai',
        'id': 'Indonesian',
        'ms': 'Malay',
        'he': 'Hebrew',
        'fa': 'Persian'
    }
    
    def __init__(self, model_size="base", enable_nlp_correction=True):
        """
        Initialize the transcriber with specified Whisper model.
        
        Args:
            model_size (str): Whisper model size (tiny, base, small, medium, large)
            enable_nlp_correction (bool): Enable NLP-based grammar correction
        """
        self.model_size = model_size
        self.model = None
        self.enable_nlp_correction = enable_nlp_correction
        self.nlp_corrector = None
        self._load_model()
        
        if enable_nlp_correction:
            print("Initializing NLP corrector...")
            try:
                self.nlp_corrector = NLPCorrector('en-US')
                print("✓ NLP correction enabled")
            except Exception as e:
                print(f"⚠️  NLP corrector initialization failed: {e}")
                print("   Continuing without NLP correction")
                self.enable_nlp_correction = False
    
    def _load_model(self):
        """Load the Whisper model."""
        print(f"Loading Whisper model: {self.model_size}")
        self.model = whisper.load_model(self.model_size)
        print(f"Model loaded successfully")
    
    def transcribe_audio(self, audio_path, detect_language=True, force_language=None):
        """
        Transcribe audio with automatic language detection.
        
        Args:
            audio_path (str): Path to audio file
            detect_language (bool): Whether to auto-detect language
            force_language (str): Force specific language code (optional)
        
        Returns:
            dict: {
                'language': detected language code,
                'language_name': full language name,
                'text': transcribed text,
                'segments': list of segments with timestamps,
                'confidence': detection confidence
            }
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"Transcribing: {audio_path}")
        
        # Transcribe with or without language specification
        if force_language:
            print(f"Forcing language: {force_language}")
            result = self.model.transcribe(audio_path, language=force_language)
            detected_lang = force_language
        elif detect_language:
            print("Auto-detecting language...")
            result = self.model.transcribe(audio_path)
            detected_lang = result.get('language', 'unknown')
        else:
            result = self.model.transcribe(audio_path)
            detected_lang = result.get('language', 'unknown')
        
        language_name = self.SUPPORTED_LANGUAGES.get(detected_lang, 'Unknown')
        
        # Get raw transcript
        raw_text = result['text'].strip()
        
        # Apply NLP correction if enabled
        corrected_text = raw_text
        corrections_info = None
        
        if self.enable_nlp_correction and self.nlp_corrector:
            print("Applying NLP corrections...")
            try:
                correction_result = self.nlp_corrector.correct_text(raw_text, detected_lang)
                corrected_text = correction_result['corrected_text']
                corrections_info = {
                    'corrections_made': correction_result['corrections_made'],
                    'filler_words_removed': correction_result['filler_words_removed']
                }
                print(f"✓ Applied {correction_result['corrections_made']} corrections")
            except Exception as e:
                print(f"⚠️  NLP correction failed: {e}")
                corrected_text = raw_text
        
        # Process segments
        raw_segments = [
            {
                'start': seg['start'],
                'end': seg['end'],
                'text': seg['text'].strip()
            }
            for seg in result.get('segments', [])
        ]
        
        # Apply correction to segments if enabled
        corrected_segments = raw_segments
        if self.enable_nlp_correction and self.nlp_corrector:
            try:
                corrected_segments = self.nlp_corrector.correct_segments(raw_segments, detected_lang)
            except Exception as e:
                print(f"⚠️  Segment correction failed: {e}")
        
        # Build response
        transcription_data = {
            'language': detected_lang,
            'language_name': language_name,
            'raw_text': raw_text,
            'corrected_text': corrected_text,
            'text': corrected_text,  # For backward compatibility
            'raw_segments': raw_segments,
            'corrected_segments': corrected_segments,
            'segments': corrected_segments,  # For backward compatibility
            'confidence': self._calculate_confidence(result),
            'nlp_corrections': corrections_info
        }
        
        # Save transcript to file
        self._save_transcript(transcription_data)
        
        print(f"Transcription complete. Detected language: {language_name} ({detected_lang})")
        return transcription_data
    
    def _calculate_confidence(self, result):
        """Calculate average confidence from segments."""
        segments = result.get('segments', [])
        if not segments:
            return 0.0
        
        # Average the 'no_speech_prob' (lower is better)
        total_confidence = sum(1 - seg.get('no_speech_prob', 0.5) for seg in segments)
        return round(total_confidence / len(segments), 2)
    
    def _save_transcript(self, data):
        """Save transcript to file."""
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transcript_{data['language']}_{timestamp}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # Save text transcript
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Language: {data['language_name']} ({data['language']})\n")
            f.write(f"Confidence: {data['confidence']}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'-' * 60}\n\n")
            f.write(data['text'])
            f.write(f"\n\n{'-' * 60}\n\n")
            f.write("Segments:\n\n")
            for seg in data['segments']:
                f.write(f"[{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text']}\n")
        
        # Save JSON version
        json_filepath = filepath.replace('.txt', '.json')
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Transcript saved: {filepath}")
        print(f"JSON data saved: {json_filepath}")
    
    def _get_language_name(self, lang_code):
        """Get full language name from code."""
        language_names = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'zh': 'Chinese',
            'ko': 'Korean',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'tr': 'Turkish',
            'pl': 'Polish',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'da': 'Danish',
            'no': 'Norwegian',
            'fi': 'Finnish',
            'uk': 'Ukrainian',
            'el': 'Greek',
            'cs': 'Czech',
            'ro': 'Romanian',
            'vi': 'Vietnamese',
            'th': 'Thai',
            'id': 'Indonesian',
            'ms': 'Malay',
            'he': 'Hebrew',
            'fa': 'Persian',
            'ur': 'Urdu',
            'bn': 'Bengali'
        }
        return language_names.get(lang_code, lang_code.upper())


def transcribe_audio_file(audio_path, model_size="base", force_language=None):
    """
    Convenience function to transcribe audio in one call.
    
    Args:
        audio_path (str): Path to audio file
        model_size (str): Whisper model size
        force_language (str): Optional language code to force
    
    Returns:
        dict: Transcription results
    """
    transcriber = MultilingualTranscriber(model_size=model_size)
    return transcriber.transcribe_audio(audio_path, force_language=force_language)


if __name__ == "__main__":
    # Test the transcriber
    import sys
    
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        if os.path.exists(audio_file):
            result = transcribe_audio_file(audio_file)
            print(f"\nDetected Language: {result['language_name']}")
            print(f"Transcript: {result['text'][:200]}...")
        else:
            print(f"File not found: {audio_file}")
    else:
        print("Usage: python multilingual_transcribe.py <audio_file>")
