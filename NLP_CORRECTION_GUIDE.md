# NLP Grammar Correction Feature

## Overview
The Speech-to-Text Converter now includes advanced NLP-based grammar correction to enhance transcript quality. This feature automatically processes raw Whisper transcriptions and returns both the original and corrected versions.

## Features

### 1. **Filler Word Removal**
Automatically removes common filler words in multiple languages:
- **English**: "uh", "um", "hmm", "like", "you know", "basically", "actually"
- **Spanish**: "eh", "este", "mmm", "pues", "bueno"
- **French**: "euh", "hein", "bon", "ben", "quoi", "voilà"
- **German**: "ähm", "äh", "also", "halt", "na ja"

### 2. **Grammar Correction**
Uses LanguageTool to fix common grammatical errors:
- Subject-verb agreement
- Article usage (a/an/the)
- Preposition mistakes
- Punctuation errors
- And more...

### 3. **Capitalization Fixes**
- Capitalizes the first letter of sentences
- Converts standalone "i" to "I"
- Proper sentence-level capitalization

### 4. **Spacing & Punctuation**
- Removes extra spaces before punctuation (`, ! ? . ; :`)
- Adds proper spacing after punctuation
- Removes multiple consecutive punctuation marks
- Ensures sentences end with punctuation

## Architecture

### Backend Components

#### 1. `nlp_corrector.py`
The core NLP correction module with the `NLPCorrector` class:

```python
from nlp_corrector import NLPCorrector

# Initialize corrector for English
corrector = NLPCorrector(language='en-US')

# Correct text
result = corrector.correct_text(
    "uh so like this is um a test you know",
    source_language='en'
)

# Output:
# {
#     'raw_text': 'uh so like this is um a test you know',
#     'corrected_text': 'So this is a test.',
#     'corrections_made': 5,
#     'filler_words_removed': ['uh', 'like', 'um', 'you know']
# }
```

**Key Methods:**
- `correct_text(text, source_language)`: Main correction method
- `correct_segments(segments, source_language)`: Corrects timestamped segments
- `_remove_filler_words(text, language)`: Removes filler words
- `_fix_capitalization(text)`: Fixes sentence capitalization
- `_fix_spacing(text)`: Fixes punctuation spacing
- `_apply_grammar_correction(text)`: Applies LanguageTool corrections

#### 2. `multilingual_transcribe.py`
Updated to integrate NLP correction:

```python
# Initialization
transcriber = MultilingualTranscriber(
    model_size="base",
    enable_nlp_correction=True  # Enabled by default
)

# Transcription returns both versions
result = transcriber.transcribe_audio(audio_path)

# Output structure:
# {
#     'language': 'en',
#     'language_name': 'English',
#     'raw_text': '...original Whisper output...',
#     'corrected_text': '...NLP-corrected version...',
#     'text': '...points to corrected_text...',
#     'raw_segments': [...original segments...],
#     'corrected_segments': [...corrected segments...],
#     'segments': [...points to corrected_segments...],
#     'nlp_corrections': {
#         'corrections_made': 5,
#         'filler_words_removed': ['uh', 'um']
#     },
#     'confidence': 0.95
# }
```

#### 3. `app.py` API Endpoints
Both `/api/transcribe` and `/api/live` now return:
- `raw_text`: Original Whisper transcription
- `corrected_text`: NLP-enhanced version
- `text`: Points to `corrected_text` (backward compatibility)

### Frontend Components

#### 1. `App.js`
Main application now supports toggle between raw and corrected views:

**State Variables:**
```javascript
const [rawTranscript, setRawTranscript] = useState('');
const [correctedTranscript, setCorrectedTranscript] = useState('');
const [showRaw, setShowRaw] = useState(false); // false = show corrected by default
```

**Toggle Button UI:**
```jsx
<label className="toggle-switch">
  <input 
    type="checkbox" 
    checked={showRaw} 
    onChange={() => setShowRaw(!showRaw)}
  />
  <span className="toggle-slider"></span>
</label>
<span className="toggle-label">
  {showRaw ? 'Raw (Whisper Output)' : 'Corrected (NLP Enhanced)'}
</span>
```

#### 2. `AudioUpload.js` & `LiveRecording.js`
Both components updated to:
- Accept `setRawTranscript` and `setCorrectedTranscript` props
- Store both versions locally
- Display the corrected version by default
- Pass both versions to parent component

#### 3. `App.css`
New CSS for toggle switch and correction indicator:
- `.toggle-switch` - Toggle switch styling
- `.toggle-slider` - Animated slider
- `.toggle-label` - Label text
- `.correction-note` - Info banner for corrected text

## Installation

### Requirements
Add to `backend/requirements.txt`:
```
language-tool-python==2.8.1
```

### Install Dependencies
```bash
cd backend
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Install package
pip install language-tool-python==2.8.1
```

### First Run
On first run, LanguageTool will automatically download required language data (~200MB). This is a one-time download.

## Usage

### 1. **File Upload**
1. Upload an audio file in the "Upload Audio" tab
2. Select language (or use auto-detect)
3. Click "Upload & Transcribe"
4. View corrected transcript (default)
5. Toggle to "Raw" to see original Whisper output
6. Optionally translate to another language

### 2. **Live Recording**
1. Go to "Live Recording" tab
2. Select language preference
3. Click "Start Recording"
4. Speak into microphone
5. Click "Stop Recording"
6. View corrected transcript with toggle option

### 3. **Translation**
The translation feature works with both raw and corrected transcripts:
- If showing corrected view → translates corrected text
- If showing raw view → translates raw text

## API Response Format

### `/api/transcribe` and `/api/live`

**Request:**
```bash
POST /api/transcribe
Content-Type: multipart/form-data

audio: <audio file>
force_language: "en"  # optional
```

**Response:**
```json
{
  "success": true,
  "language": "en",
  "language_name": "English",
  "raw_text": "uh so like this is um a test you know",
  "corrected_text": "So this is a test.",
  "text": "So this is a test.",
  "segments": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "So this is a test."
    }
  ],
  "confidence": 0.95
}
```

## Configuration

### Disable NLP Correction
If you want to disable NLP correction:

**In `backend/multilingual_transcribe.py`:**
```python
transcriber = MultilingualTranscriber(
    model_size="base",
    enable_nlp_correction=False  # Disable NLP correction
)
```

### Change LanguageTool Language
**In `backend/nlp_corrector.py`:**
```python
corrector = NLPCorrector(language='de-DE')  # German
corrector = NLPCorrector(language='fr-FR')  # French
corrector = NLPCorrector(language='es-ES')  # Spanish
```

## Performance Considerations

1. **Processing Time**: NLP correction adds ~100-500ms per transcription
2. **Memory Usage**: LanguageTool requires ~200MB additional RAM
3. **First Run**: Downloads language data (one-time, ~200MB)
4. **Graceful Degradation**: If correction fails, returns original text

## Troubleshooting

### Issue: LanguageTool Download Fails
**Solution:**
```bash
# Manual download
pip install language-tool-python==2.8.1
python -c "import language_tool_python; language_tool_python.LanguageTool('en-US')"
```

### Issue: Correction Too Aggressive
**Solution:** Adjust correction rules in `nlp_corrector.py`:
```python
# Reduce correction level
matches = self.tool.check(text)
# Filter matches by category
filtered_matches = [m for m in matches if m.category != 'STYLE']
```

### Issue: Wrong Language Detected
**Solution:** Force language in transcription:
```python
result = transcriber.transcribe_audio(
    audio_path,
    force_language='en'  # Force English
)
```

## Examples

### Example 1: English Filler Words
**Input (Raw):**
```
"uh so like I was um thinking you know that we should like go there"
```

**Output (Corrected):**
```
"So I was thinking that we should go there."
```

### Example 2: Grammar Correction
**Input (Raw):**
```
"he dont have no time for this kind of thing"
```

**Output (Corrected):**
```
"He doesn't have time for this kind of thing."
```

### Example 3: Capitalization
**Input (Raw):**
```
"hello world. i am a test. this is great."
```

**Output (Corrected):**
```
"Hello world. I am a test. This is great."
```

## Future Enhancements

- [ ] Custom filler word dictionaries per user
- [ ] Correction confidence scores
- [ ] Side-by-side comparison view
- [ ] Highlight changes in UI
- [ ] Export both versions to separate files
- [ ] Domain-specific correction rules (medical, legal, etc.)
- [ ] Multi-speaker detection with speaker-specific correction
- [ ] Real-time correction streaming
- [ ] Undo/redo correction changes

## Credits

- **LanguageTool**: Grammar correction engine (https://languagetool.org/)
- **OpenAI Whisper**: Speech recognition model
- **React**: Frontend framework

## License

This feature is part of the Speech-to-Text Converter project.

---

**Last Updated:** December 26, 2024
