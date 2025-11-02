import streamlit as st
from datetime import datetime
from voice.speech_to_text import transcribe_audio
from voice.text_to_speech import tts_generate


class AssistantGUI:
    def __init__(self, assistant):
        self.assistant = assistant
        self.employee_information = assistant.employee_information

        defaults = {
            "messages": [],
            "pending_input": None,
            "pending_origin": None,
            "processing": False,
            "last_response_id": 0,
            "audio_bytes": None,
            "autoplay_audio": False,
            "last_audio_hash": None,
        }
        for k, v in defaults.items():
            if k not in st.session_state:
                st.session_state[k] = v

    # ----------------------------------------------------------
    # 🎨 CSS: Enhanced styling with fixed voice input bar
    # ----------------------------------------------------------

    def _inject_sticky_css(self):
        st.markdown(
            """
            <style>
            /* Prevent chat area overlap with fixed elements */
            section.main > div.block-container {
                padding-bottom: 200px !important;
            }

            /* Fixed bottom voice bar container */
            #voice-fixed-bar {
                position: fixed;
                left: 50%;
                transform: translateX(-50%);
                bottom: 88px;
                width: min(1000px, calc(100vw - 6rem));
                z-index: 999;
                background: transparent;
            }

            /* Voice expander styling */
            #voice-fixed-bar details[data-testid="stExpander"] {
                background: rgba(31, 31, 31, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            }

            #voice-fixed-bar details[data-testid="stExpander"] > summary {
                border-radius: 12px;
                padding: 0.75rem 1rem;
                background: linear-gradient(135deg, #1f1f1f 0%, #2a2a2a 100%);
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: all 0.3s ease;
            }

            #voice-fixed-bar details[data-testid="stExpander"] > summary:hover {
                background: linear-gradient(135deg, #2a2a2a 0%, #353535 100%);
                border-color: rgba(255, 255, 255, 0.2);
            }

            /* Smooth scrolling for chat */
            .main .block-container {
                scroll-behavior: smooth;
            }

            /* Audio player styling */
            audio {
                width: 100%;
                margin-top: 0.75rem;
                border-radius: 8px;
                outline: none;
            }

            /* Enhanced chat message styling */
            .stChatMessage {
                padding: 1rem;
                margin: 0.5rem 0;
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.05);
            }

            /* User message accent */
            [data-testid="stChatMessageContent"] {
                padding: 0.5rem 0;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    # ----------------------------------------------------------
    # 🧠 Core response generator
    # ----------------------------------------------------------
    def get_response(self, user_input: str):
        return self.assistant.get_response(user_input)

    # ----------------------------------------------------------
    # 💬 Chat message renderer
    # ----------------------------------------------------------
    def render_messages(self):
        if not st.session_state["messages"]:
            with st.chat_message("ai", avatar="🧰"):
                st.markdown(
                    "**Umbrella Assistant Online.** How can I assist you today?")

        for msg in st.session_state["messages"]:
            avatar = "👤" if msg["role"] == "user" else "🧰"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    # ----------------------------------------------------------
    # 🎙️ Voice input bar (fixed at bottom)
    # ----------------------------------------------------------
    def _voice_section(self):
        # Create a placeholder div that will hold the voice input
        st.markdown('<div id="voice-fixed-bar">', unsafe_allow_html=True)

        with st.expander("🎙️ Voice input (optional)", expanded=False):
            audio = st.audio_input(
                "Record voice",
                label_visibility="collapsed",
                key="voice_rec"
            )

            if audio is not None:
                # Create unique hash for this audio to prevent reprocessing
                import hashlib
                audio_bytes = audio.read()
                audio_hash = hashlib.md5(audio_bytes).hexdigest()

                # Only process if this is new audio
                if audio_hash != st.session_state.get("last_audio_hash"):
                    with st.status("🎧 Processing your voice input...", expanded=True) as status:
                        text = transcribe_audio(audio_bytes)

                    if text:
                        st.success(f"🗣️ You said: **{text}**")
                        st.session_state["pending_input"] = text
                        st.session_state["pending_origin"] = "voice"
                        st.session_state["last_audio_hash"] = audio_hash
                        status.update(
                            label="✅ Transcription complete!", state="complete")
                        st.rerun()
                    else:
                        status.update(
                            label="⚠️ Could not transcribe audio", state="error")

        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------------
    # ⌨️ Text input bar
    # ----------------------------------------------------------
    def _text_row(self):
        user_text = st.chat_input("Type your message...")
        if user_text and user_text.strip():
            st.session_state["pending_input"] = user_text.strip()
            st.session_state["pending_origin"] = "text"
            # Trigger rerun to process input
            st.rerun()

    # ----------------------------------------------------------
    # ⚙️ Process a single query (voice or text)
    # ----------------------------------------------------------
    def _process_once(self):
        # Prevent duplicate processing
        if st.session_state["processing"]:
            return

        # Check if there's pending input to process
        if not st.session_state["pending_input"]:
            return

        # Lock processing
        st.session_state["processing"] = True

        try:
            user_input = st.session_state["pending_input"]
            origin = st.session_state["pending_origin"]

            # Clear pending immediately to prevent reprocessing
            st.session_state["pending_input"] = None
            st.session_state["pending_origin"] = None

            # 1️⃣ Display user message immediately
            st.session_state["messages"].append(
                {"role": "user", "content": user_input}
            )

            # Render the user message
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_input)

            # 2️⃣ Generate assistant reply with streaming
            with st.chat_message("ai", avatar="🧰"):
                with st.spinner("Thinking..."):
                    stream = self.get_response(user_input)
                    response_text = st.write_stream(stream)

            # Store assistant message
            st.session_state["messages"].append(
                {"role": "ai", "content": response_text}
            )
            st.session_state["last_response_id"] += 1

            # 3️⃣ Generate audio (always generate, but control autoplay)
            response_str = ' '.join(response_text) if isinstance(
                response_text, list) else str(response_text)

            st.session_state["audio_bytes"] = tts_generate(
                response_str, offline=False
            )

            # Set autoplay based on origin: voice queries autoplay, text queries don't
            st.session_state["autoplay_audio"] = (origin == "voice")

        finally:
            # Unlock processing
            st.session_state["processing"] = False

    # ----------------------------------------------------------
    # 🔊 Audio renderer with conditional autoplay
    # ----------------------------------------------------------
    def _render_audio_player(self):
        if not st.session_state["audio_bytes"]:
            return

        # Convert audio bytes to base64
        import base64
        audio_b64 = base64.b64encode(
            st.session_state["audio_bytes"]
        ).decode()

        # Determine autoplay attribute
        autoplay_attr = "autoplay" if st.session_state["autoplay_audio"] else ""

        # Render audio player
        st.markdown(
            f"""
            <div style="margin-top: 0.5rem; padding: 0.75rem; background: rgba(255,255,255,0.03); 
                        border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
                <div style="margin-bottom: 0.5rem; color: #888; font-size: 0.875rem;">
                    🔊 Audio Response
                </div>
                <audio controls {autoplay_attr} style="width:100%;">
                    <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                    Your browser does not support audio playback.
                </audio>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ----------------------------------------------------------
    # 🧾 Sidebar employee profile
    # ----------------------------------------------------------
    def _render_sidebar_profile(self):
        with st.sidebar:
            # Umbrella logo
            st.image(
                "https://upload.wikimedia.org/wikipedia/commons/0/0e/Umbrella_Corporation_logo.svg",
                width=120,
            )

            st.markdown("### 🧾 Employee Profile")
            st.markdown(
                f"**Name:** {self.employee_information['name']} "
                f"{self.employee_information['lastname']}"
            )
            st.markdown(f"**Email:** {self.employee_information['email']}")
            st.markdown(
                f"**Department:** {self.employee_information['department']}"
            )
            st.markdown(
                f"**Position:** {self.employee_information['position']}"
            )
            st.markdown(
                f"**Supervisor:** {self.employee_information['supervisor']}"
            )
            st.markdown(
                f"**Location:** {self.employee_information['location']}"
            )

            st.markdown("---")
            st.caption(
                f"🕐 Active Session: {datetime.now().strftime('%H:%M:%S')}"
            )

    # ----------------------------------------------------------
    # 🚀 Main entry point
    # ----------------------------------------------------------
    def render(self):
        # Inject CSS first
        self._inject_sticky_css()

        # Render sidebar
        self._render_sidebar_profile()

        # Render existing messages
        self.render_messages()

        # Process any pending input
        self._process_once()

        # Render audio player if available
        self._render_audio_player()

        # Render voice section (fixed position)
        self._voice_section()

        # Render text input (at bottom)
        self._text_row()
