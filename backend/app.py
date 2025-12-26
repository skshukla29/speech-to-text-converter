from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
from werkzeug.utils import secure_filename
from preprocess_audio import preprocess_audio
from transcribe_whisper import WhisperTranscriber
from multilingual_transcribe import MultilingualTranscriber
from translate import TextTranslator

app = Flask(__name__)
CORS(app)

# Ensure UTF-8 encoding for all responses
app.config['JSON_AS_ASCII'] = False

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'webm', 'ogg', 'm4a', 'flac', 'aac', 'wma'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Initialize transcribers (loads model once at startup)
print("Loading Whisper model...")
transcriber = WhisperTranscriber(model_size="base")  # Original transcriber
multilingual_transcriber = MultilingualTranscriber(model_size="base")  # Advanced multilingual transcriber

# Initialize translator
translator = TextTranslator()

# Create output directory
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_audio():
    """Handle audio file upload and transcription"""
    uploaded_file_path = None
    cleaned_audio_path = None
    
    try:
        # Check if file is present in request
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed types: ' + ', '.join(ALLOWED_EXTENSIONS)}), 400
        
        # Get language preference from request (optional)
        language = request.form.get('language', None)
        if language == 'auto':
            language = None
        
        # Save file securely
        filename = secure_filename(file.filename)
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(uploaded_file_path)
        
        print(f"Processing file: {filename}")
        if language:
            print(f"Expected language: {language}")
        
        # Preprocess audio (convert to 16kHz mono WAV)
        cleaned_audio_path = preprocess_audio(uploaded_file_path)
        
        # Transcribe audio using Whisper with language hint
        result = transcriber.transcribe(cleaned_audio_path, language=language)
        
        # Clean up temporary files
        if uploaded_file_path and os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)
        if cleaned_audio_path and os.path.exists(cleaned_audio_path):
            os.remove(cleaned_audio_path)
        
        return jsonify({
            'success': True,
            'transcript': result['transcript'],
            'language': result['language'],
            'segments': result['segments']
        }), 200
        
    except Exception as e:
        # Clean up temporary files in case of error
        if uploaded_file_path and os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)
        if cleaned_audio_path and os.path.exists(cleaned_audio_path):
            os.remove(cleaned_audio_path)
        
        print(f"Error processing audio: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/live-record', methods=['POST'])
def live_record():
    """Handle live microphone recording and transcription"""
    uploaded_file_path = None
    cleaned_audio_path = None
    
    try:
        # Check if file is present in request
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio data provided'}), 400
        
        file = request.files['audio']
        
        # Get language preference from request (optional)
        language = request.form.get('language', None)
        if language == 'auto':
            language = None
        
        # Save file temporarily
        filename = secure_filename('recording.webm')
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(uploaded_file_path)
        
        print("Processing live recording...")
        if language:
            print(f"Expected language: {language}")
        
        # Preprocess audio (convert to 16kHz mono WAV)
        cleaned_audio_path = preprocess_audio(uploaded_file_path)
        
        # Transcribe audio using Whisper with language hint
        result = transcriber.transcribe(cleaned_audio_path, language=language)
        
        # Clean up temporary files
        if uploaded_file_path and os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)
        if cleaned_audio_path and os.path.exists(cleaned_audio_path):
            os.remove(cleaned_audio_path)
        
        return jsonify({
            'success': True,
            'transcript': result['transcript'],
            'language': result['language'],
            'segments': result['segments']
        }), 200
        
    except Exception as e:
        # Clean up temporary files in case of error
        if uploaded_file_path and os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)
        if cleaned_audio_path and os.path.exists(cleaned_audio_path):
            os.remove(cleaned_audio_path)
        
        print(f"Error processing recording: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Speech-to-Text API is running'
    }), 200

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Advanced multilingual transcription endpoint.
    Automatically detects language and transcribes without forcing translation.
    """
    uploaded_file_path = None
    cleaned_audio_path = None
    
    try:
        # Check if file is present in request
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed types: ' + ', '.join(ALLOWED_EXTENSIONS)}), 400
        
        # Get optional language parameter
        force_language = request.form.get('force_language', None)
        
        # Save file securely
        filename = secure_filename(file.filename)
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(uploaded_file_path)
        
        print(f"Transcribing file: {filename}")
        
        # Preprocess audio (convert to 16kHz mono WAV)
        cleaned_audio_path = preprocess_audio(uploaded_file_path)
        
        # Transcribe using advanced multilingual transcriber
        result = multilingual_transcriber.transcribe_audio(
            cleaned_audio_path, 
            detect_language=True,
            force_language=force_language
        )
        
        # Clean up temporary files
        if uploaded_file_path and os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)
        if cleaned_audio_path and os.path.exists(cleaned_audio_path):
            os.remove(cleaned_audio_path)
        
        return jsonify({
            'success': True,
            'language': result['language'],
            'language_name': result['language_name'],
            'raw_text': result['raw_text'],
            'corrected_text': result['corrected_text'],
            'text': result['text'],  # For backward compatibility, points to corrected_text
            'segments': result['segments'],
            'confidence': result['confidence']
        }), 200
        
    except Exception as e:
        # Clean up temporary files in case of error
        if uploaded_file_path and os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)
        if cleaned_audio_path and os.path.exists(cleaned_audio_path):
            os.remove(cleaned_audio_path)
        
        print(f"Error during transcription: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/translate', methods=['POST'])
def translate_text_endpoint():
    """
    Translate text from one language to another.
    Only translates when explicitly requested (no automatic translation).
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        source_lang = data.get('source_lang', 'auto')
        target_lang = data.get('target_lang', 'en')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if not target_lang:
            return jsonify({'error': 'Target language not specified'}), 400
        
        print(f"Translating from '{source_lang}' to '{target_lang}'")
        
        # Use the translator
        result = translator.translate_text(text, target_lang, source_lang)
        
        if result['success']:
            return jsonify({
                'success': True,
                'original_text': result['original_text'],
                'translated_text': result['translated_text'],
                'source_lang': result['source_lang'],
                'target_lang': result['target_lang']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Translation failed')
            }), 500
        
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500

@app.route('/api/live', methods=['POST'])
def live_transcription():
    """
    Real-time transcription endpoint for live microphone streaming.
    Handles WebM audio chunks from browser MediaRecorder.
    """
    uploaded_file_path = None
    cleaned_audio_path = None
    
    try:
        # Check if file is present in request
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio data provided'}), 400
        
        file = request.files['audio']
        
        # Get optional language parameter
        force_language = request.form.get('force_language', None)
        
        # Save file temporarily
        filename = secure_filename('live_recording.webm')
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(uploaded_file_path)
        
        print("Processing live audio stream...")
        
        # Preprocess audio (convert to 16kHz mono WAV)
        cleaned_audio_path = preprocess_audio(uploaded_file_path)
        
        # Transcribe using multilingual transcriber
        result = multilingual_transcriber.transcribe_audio(
            cleaned_audio_path,
            detect_language=True,
            force_language=force_language
        )
        
        # Clean up temporary files
        if uploaded_file_path and os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)
        if cleaned_audio_path and os.path.exists(cleaned_audio_path):
            os.remove(cleaned_audio_path)
        
        return jsonify({
            'success': True,
            'language': result['language'],
            'language_name': result['language_name'],
            'raw_text': result['raw_text'],
            'corrected_text': result['corrected_text'],
            'text': result['text'],  # For backward compatibility, points to corrected_text
            'segments': result['segments'],
            'confidence': result['confidence']
        }), 200
        
    except Exception as e:
        # Clean up temporary files in case of error
        if uploaded_file_path and os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)
        if cleaned_audio_path and os.path.exists(cleaned_audio_path):
            os.remove(cleaned_audio_path)
        
        print(f"Error processing live audio: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
