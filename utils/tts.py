from gtts import gTTS
import os

def text_to_speech(text, lang='en'):
    """Convert text to speech and save it as an audio file."""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_path = "assets/audio/speech.mp3"
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        return f"Error: {str(e)}"
