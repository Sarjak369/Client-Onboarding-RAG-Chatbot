# Convert assistant reply to audio

from io import BytesIO
import tempfile
import contextlib
import streamlit as st
import os

# Optional deps
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    gTTS = None

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


def _pyttsx3_bytes(text: str) -> bytes:
    """Fallback offline TTS using pyttsx3."""
    if not PYTTSX3_AVAILABLE:
        raise ImportError("pyttsx3 is not available for offline TTS")

    import pyttsx3
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        path = f.name

    try:
        eng = pyttsx3.init()
        eng.setProperty('rate', 150)  # Speed of speech
        eng.setProperty('volume', 0.9)  # Volume level
        eng.save_to_file(text, path)
        eng.runAndWait()

        with open(path, "rb") as r:
            return r.read()
    finally:
        with contextlib.suppress(Exception):
            os.remove(path)


@st.cache_data(show_spinner=False, ttl=3600)
def tts_generate(text: str, *, offline: bool = False) -> bytes:
    """
    Generate audio bytes for given text.
    Cached to avoid re-synthesis on reruns.

    Args:
        text: The text to convert to speech
        offline: If True, use offline TTS (pyttsx3), else use gTTS (online)

    Returns:
        Audio bytes in WAV or MP3 format
    """
    # Clean and validate input
    text = (text or "").strip()
    if not text:
        return b""

    # Truncate very long texts to avoid issues
    if len(text) > 5000:
        text = text[:5000] + "..."

    try:
        if offline:
            if not PYTTSX3_AVAILABLE:
                st.warning("⚠️ Offline TTS not available. Using online TTS.")
                offline = False
            else:
                return _pyttsx3_bytes(text)

        # Online TTS with gTTS
        if GTTS_AVAILABLE and gTTS is not None:
            try:
                buf = BytesIO()
                tts = gTTS(text=text, lang="en", slow=False)
                tts.write_to_fp(buf)
                buf.seek(0)
                return buf.getvalue()
            except Exception as e:
                st.warning(f"⚠️ Online TTS failed: {e}. Trying offline TTS...")
                if PYTTSX3_AVAILABLE:
                    return _pyttsx3_bytes(text)
                raise
        else:
            # Fallback to offline if gTTS not available
            if PYTTSX3_AVAILABLE:
                return _pyttsx3_bytes(text)
            else:
                st.error("❌ No TTS engine available (install gtts or pyttsx3)")
                return b""

    except Exception as e:
        st.error(f"❌ Text-to-speech generation failed: {e}")
        return b""
