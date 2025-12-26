"""
NLP-based text correction module for improving transcription quality.
Handles grammar correction, sentence normalization, and filler word removal.
"""
import re
import language_tool_python
from typing import Dict, List


class NLPCorrector:
    """
    Advanced NLP corrector for post-processing speech transcriptions.
    Uses LanguageTool for grammar correction and custom rules for speech-specific issues.
    """
    
    def __init__(self, language='en-US'):
        """
        Initialize the NLP corrector.
        
        Args:
            language (str): Language code for correction (default: 'en-US')
        """
        self.language = language
        print(f"Initializing NLP corrector for language: {language}")
        try:
            self.tool = language_tool_python.LanguageTool(language)
            print("✓ LanguageTool loaded successfully")
        except Exception as e:
            print(f"⚠️  LanguageTool initialization warning: {e}")
            print("   Correction will use basic rules only")
            self.tool = None
        
        # Common filler words to remove
        self.filler_words = {
            'en': ['uh', 'um', 'hmm', 'hm', 'er', 'ah', 'like', 'you know', 'basically', 'actually'],
            'es': ['eh', 'este', 'pues', 'bueno', 'entonces'],
            'fr': ['euh', 'ben', 'quoi', 'genre'],
            'de': ['äh', 'ähm', 'also', 'ja'],
        }
    
    def correct_text(self, text: str, source_language: str = 'en') -> Dict:
        """
        Correct text using NLP techniques.
        
        Args:
            text (str): Raw transcription text
            source_language (str): Source language code
        
        Returns:
            dict: {
                'raw_text': original text,
                'corrected_text': corrected text,
                'corrections_made': list of corrections,
                'filler_words_removed': list of removed fillers
            }
        """
        if not text or not text.strip():
            return {
                'raw_text': text,
                'corrected_text': text,
                'corrections_made': [],
                'filler_words_removed': []
            }
        
        corrections_log = []
        removed_fillers = []
        
        # Step 1: Remove filler words
        cleaned_text, removed_fillers = self._remove_filler_words(text, source_language)
        if removed_fillers:
            corrections_log.append(f"Removed {len(removed_fillers)} filler words")
        
        # Step 2: Fix capitalization
        capitalized_text = self._fix_capitalization(cleaned_text)
        if capitalized_text != cleaned_text:
            corrections_log.append("Fixed capitalization")
        
        # Step 3: Fix spacing and punctuation
        spaced_text = self._fix_spacing(capitalized_text)
        if spaced_text != capitalized_text:
            corrections_log.append("Fixed spacing")
        
        # Step 4: Grammar correction (if LanguageTool is available)
        if self.tool and source_language.startswith('en'):
            corrected_text = self._apply_grammar_correction(spaced_text, corrections_log)
        else:
            corrected_text = spaced_text
        
        # Step 5: Final cleanup
        final_text = self._final_cleanup(corrected_text)
        
        return {
            'raw_text': text,
            'corrected_text': final_text,
            'corrections_made': corrections_log,
            'filler_words_removed': removed_fillers
        }
    
    def _remove_filler_words(self, text: str, language: str) -> tuple:
        """Remove filler words based on language."""
        # Get filler words for the language (default to English)
        lang_code = language.split('-')[0] if '-' in language else language
        fillers = self.filler_words.get(lang_code, self.filler_words['en'])
        
        removed = []
        result = text
        
        for filler in fillers:
            # Create pattern: match filler as whole word, case-insensitive
            pattern = r'\b' + re.escape(filler) + r'\b'
            matches = re.findall(pattern, result, re.IGNORECASE)
            if matches:
                removed.extend(matches)
                result = re.sub(pattern, '', result, flags=re.IGNORECASE)
        
        # Clean up extra spaces created by removal
        result = re.sub(r'\s+', ' ', result).strip()
        
        return result, removed
    
    def _fix_capitalization(self, text: str) -> str:
        """Fix sentence capitalization."""
        # Split into sentences
        sentences = re.split(r'([.!?]+\s*)', text)
        
        fixed_sentences = []
        for i, sentence in enumerate(sentences):
            if sentence.strip() and not re.match(r'[.!?]+\s*', sentence):
                # Capitalize first letter of sentence
                sentence = sentence.strip()
                if sentence:
                    sentence = sentence[0].upper() + sentence[1:]
                fixed_sentences.append(sentence)
            else:
                fixed_sentences.append(sentence)
        
        result = ''.join(fixed_sentences)
        
        # Ensure first letter is capitalized
        if result:
            result = result[0].upper() + result[1:]
        
        return result
    
    def _fix_spacing(self, text: str) -> str:
        """Fix spacing around punctuation."""
        # Remove spaces before punctuation
        text = re.sub(r'\s+([,.!?;:])', r'\1', text)
        
        # Add space after punctuation if missing
        text = re.sub(r'([,.!?;:])([A-Za-z])', r'\1 \2', text)
        
        # Fix multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Fix quotes
        text = re.sub(r'\s*"\s*', '"', text)
        text = re.sub(r'\s*\'\s*', "'", text)
        
        return text.strip()
    
    def _apply_grammar_correction(self, text: str, corrections_log: List) -> str:
        """Apply LanguageTool grammar corrections."""
        if not self.tool:
            return text
        
        try:
            matches = self.tool.check(text)
            
            if matches:
                # Apply corrections
                corrected = language_tool_python.utils.correct(text, matches)
                
                # Log significant corrections
                grammar_fixes = len(matches)
                if grammar_fixes > 0:
                    corrections_log.append(f"Fixed {grammar_fixes} grammar issues")
                
                return corrected
            else:
                return text
        except Exception as e:
            print(f"⚠️  Grammar correction error: {e}")
            return text
    
    def _final_cleanup(self, text: str) -> str:
        """Final cleanup and normalization."""
        # Remove multiple punctuation marks
        text = re.sub(r'([.!?]){2,}', r'\1', text)
        
        # Fix common transcription errors
        text = text.replace(' i ', ' I ')  # Fix lowercase 'i'
        text = re.sub(r"\bi'm\b", "I'm", text, flags=re.IGNORECASE)
        text = re.sub(r"\bi'll\b", "I'll", text, flags=re.IGNORECASE)
        text = re.sub(r"\bi've\b", "I've", text, flags=re.IGNORECASE)
        
        # Ensure sentence ends with punctuation
        if text and not text[-1] in '.!?':
            text += '.'
        
        return text.strip()
    
    def correct_segments(self, segments: List[Dict], source_language: str = 'en') -> List[Dict]:
        """
        Correct text in timestamped segments.
        
        Args:
            segments (list): List of segment dicts with 'text', 'start', 'end'
            source_language (str): Source language code
        
        Returns:
            list: Corrected segments with both raw and corrected text
        """
        corrected_segments = []
        
        for segment in segments:
            if 'text' in segment:
                correction_result = self.correct_text(segment['text'], source_language)
                
                corrected_segment = segment.copy()
                corrected_segment['raw_text'] = segment['text']
                corrected_segment['text'] = correction_result['corrected_text']
                corrected_segments.append(corrected_segment)
            else:
                corrected_segments.append(segment)
        
        return corrected_segments


# Convenience function for quick correction
def correct_transcript(text: str, language: str = 'en') -> str:
    """
    Quick function to correct a transcript.
    
    Args:
        text (str): Raw transcript
        language (str): Language code
    
    Returns:
        str: Corrected text
    """
    corrector = NLPCorrector(language=language if '-' in language else f'{language}-US')
    result = corrector.correct_text(text, language)
    return result['corrected_text']


if __name__ == "__main__":
    # Test the corrector
    print("Testing NLP Corrector...")
    print("=" * 60)
    
    # Test English correction
    test_text = "um hello my name is john uh i am a student basically i study computer science you know"
    
    corrector = NLPCorrector('en-US')
    result = corrector.correct_text(test_text, 'en')
    
    print(f"Raw Text:\n{result['raw_text']}\n")
    print(f"Corrected Text:\n{result['corrected_text']}\n")
    print(f"Corrections Made: {result['corrections_made']}")
    print(f"Fillers Removed: {result['filler_words_removed']}")
    print("=" * 60)
