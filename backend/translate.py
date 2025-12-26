"""
Translation module for converting text between languages.
Supports multiple translation backends.
"""
from deep_translator import GoogleTranslator
import os


class TextTranslator:
    """Advanced text translation with multiple language support."""
    
    def __init__(self):
        """Initialize the translator."""
        self.supported_languages = self._get_supported_languages()
    
    def translate_text(self, text, target_lang, source_lang='auto'):
        """
        Translate text to target language.
        
        Args:
            text (str): Text to translate
            target_lang (str): Target language code (e.g., 'en', 'es', 'fr')
            source_lang (str): Source language code (default: 'auto' for auto-detect)
        
        Returns:
            dict: {
                'original_text': original text,
                'translated_text': translated text,
                'source_lang': source language,
                'target_lang': target language,
                'success': bool
            }
        """
        if not text or not text.strip():
            return {
                'original_text': text,
                'translated_text': '',
                'source_lang': source_lang,
                'target_lang': target_lang,
                'success': False,
                'error': 'Empty text provided'
            }
        
        try:
            print(f"Translating from '{source_lang}' to '{target_lang}'")
            
            # Use GoogleTranslator
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated = translator.translate(text)
            
            result = {
                'original_text': text,
                'translated_text': translated,
                'source_lang': source_lang,
                'target_lang': target_lang,
                'success': True
            }
            
            print(f"Translation complete: {len(text)} -> {len(translated)} chars")
            return result
            
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return {
                'original_text': text,
                'translated_text': '',
                'source_lang': source_lang,
                'target_lang': target_lang,
                'success': False,
                'error': str(e)
            }
    
    def translate_segments(self, segments, target_lang, source_lang='auto'):
        """
        Translate list of text segments (e.g., timestamped segments).
        
        Args:
            segments (list): List of dicts with 'text' field
            target_lang (str): Target language code
            source_lang (str): Source language code
        
        Returns:
            list: Translated segments with same structure
        """
        translated_segments = []
        
        for segment in segments:
            translated_text = self.translate_text(
                segment['text'], 
                target_lang, 
                source_lang
            )
            
            translated_segment = segment.copy()
            translated_segment['original_text'] = segment['text']
            translated_segment['text'] = translated_text['translated_text']
            translated_segments.append(translated_segment)
        
        return translated_segments
    
    def batch_translate(self, texts, target_lang, source_lang='auto'):
        """
        Translate multiple texts at once.
        
        Args:
            texts (list): List of texts to translate
            target_lang (str): Target language code
            source_lang (str): Source language code
        
        Returns:
            list: List of translated texts
        """
        results = []
        for text in texts:
            result = self.translate_text(text, target_lang, source_lang)
            results.append(result['translated_text'] if result['success'] else text)
        return results
    
    def _get_supported_languages(self):
        """Get list of supported language codes."""
        return {
            'auto': 'Auto-detect',
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'zh-CN': 'Chinese (Simplified)',
            'zh-TW': 'Chinese (Traditional)',
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
    
    def get_language_name(self, lang_code):
        """Get full language name from code."""
        return self.supported_languages.get(lang_code, lang_code.upper())
    
    def is_language_supported(self, lang_code):
        """Check if language is supported."""
        return lang_code in self.supported_languages


# Global translator instance
_translator = None

def get_translator():
    """Get or create global translator instance."""
    global _translator
    if _translator is None:
        _translator = TextTranslator()
    return _translator


def translate_text(text, target_lang, source_lang='auto'):
    """
    Quick translation function.
    
    Args:
        text (str): Text to translate
        target_lang (str): Target language code
        source_lang (str): Source language code (default: 'auto')
    
    Returns:
        dict: Translation result
    """
    translator = get_translator()
    return translator.translate_text(text, target_lang, source_lang)


if __name__ == "__main__":
    # Test the translator
    import sys
    
    if len(sys.argv) > 2:
        text = sys.argv[1]
        target_lang = sys.argv[2]
        source_lang = sys.argv[3] if len(sys.argv) > 3 else 'auto'
        
        result = translate_text(text, target_lang, source_lang)
        
        if result['success']:
            print(f"\nOriginal ({result['source_lang']}): {result['original_text']}")
            print(f"Translated ({result['target_lang']}): {result['translated_text']}")
        else:
            print(f"Error: {result.get('error', 'Translation failed')}")
    else:
        print("Usage: python translate.py <text> <target_lang> [source_lang]")
        print("Example: python translate.py 'Hello world' 'es' 'en'")
