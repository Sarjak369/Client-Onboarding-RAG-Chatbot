# Groq Whisper transcription with improved error handling

import os
import tempfile
from groq import Groq
import streamlit as st

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Transcribe speech to text using Groq Whisper-large-v3.

    Args:
        audio_bytes: Raw audio data in bytes

    Returns:
        Transcribed text string, or empty string on failure
    """
    if not audio_bytes:
        return ""

    if not client.api_key:
        st.error("❌ GROQ_API_KEY not found in environment variables")
        return ""

    # Create temporary file for audio
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav", mode='wb') as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        # Transcribe using Groq Whisper
        with open(tmp_path, "rb") as audio_file:
            result = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file,
                response_format="text",
                language="en",  # Specify language for better accuracy
            )

        # Handle different response formats
        if isinstance(result, str):
            text = result.strip()
        elif isinstance(result, dict) and "text" in result:
            text = result["text"].strip()
        elif hasattr(result, 'text'):
            text = result.text.strip()
        else:
            st.warning("⚠️ Unexpected response format from Groq Whisper")
            return ""

        # Validate transcription
        if not text:
            st.warning("⚠️ No speech detected in audio")
            return ""

        return text

    except FileNotFoundError:
        st.error("❌ Audio file not found during transcription")
        return ""

    except Exception as e:
        error_msg = str(e)
        if "rate limit" in error_msg.lower():
            st.error("❌ Rate limit exceeded. Please wait a moment and try again.")
        elif "api key" in error_msg.lower():
            st.error("❌ Invalid API key. Please check your GROQ_API_KEY.")
        else:
            st.error(f"❌ Speech-to-text failed: {error_msg}")
        return ""

    finally:
        # Clean up temporary file
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass  # Ignore cleanup errors
