import streamlit as st
import logging
from dotenv import load_dotenv
from sqlalchemy import text

# 🔐 Auth + DB Imports
from auth.signup import signup
from auth.login import login
from database.db import get_engine

# 🤖 Assistant Imports
from assistant import Assistant
from gui import AssistantGUI
from prompt import SYSTEM_PROMPT, WELCOME_MESSAGE
from langchain_groq import ChatGroq  # or your preferred model

# 🧱 Setup
load_dotenv()
logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="Umbrella Onboarding Assistant",
    layout="wide",
    page_icon="☂"
)

# -----------------------------------------------------------------------------
# 🧭 Navigation & Layout
# -----------------------------------------------------------------------------


def main():
    st.sidebar.title("☂️ Umbrella Corporation Assistant")

    # Initialize session state
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "employee" not in st.session_state:
        st.session_state["employee"] = None
    if "assistant" not in st.session_state:
        st.session_state["assistant"] = None

    # Authentication flow
    if not st.session_state["user"]:
        auth_mode = st.sidebar.radio("Select Mode", ["Login", "Sign Up"])

        if auth_mode == "Login":
            user = login()
        else:
            signup()
            st.stop()

        # Stop here until login completes
        if "employee" not in st.session_state or not st.session_state["employee"]:
            st.stop()

    # -------------------------------------------------------------------------
    # Logged-in view
    # -------------------------------------------------------------------------
    employee = st.session_state["employee"]
    user = st.session_state["user"]

    # Sidebar profile summary
    st.sidebar.markdown("---")
    st.sidebar.success(
        f"👋 **Welcome, {employee['name']} {employee['lastname']}**\n\n"
        f"**Role:** {employee['position']}  \n"
        f"**Department:** {employee['department']}  \n"
        f"**Supervisor:** {employee['supervisor']}"
    )

    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

    # -------------------------------------------------------------------------
    # Main Layout
    # -------------------------------------------------------------------------
    st.title("Umbrella Corporation Internal Assistant 🧬")
    st.markdown(
        "<p style='color:#c4c4c4;font-size:16px;'>"
        "Welcome to your secure Umbrella onboarding environment."
        " Proceed with caution and adhere to internal protocols.</p>",
        unsafe_allow_html=True,
    )

    st.markdown(f"---\n{WELCOME_MESSAGE}\n---")

    # Initialize the Assistant only once per session
    if not st.session_state["assistant"]:
        # You can swap to OpenAI
        llm = ChatGroq(model="llama-3.3-70b-versatile")
        st.session_state["assistant"] = Assistant(
            system_prompt=SYSTEM_PROMPT,
            llm=llm,
            employee_information=employee
        )

    # Launch the GUI
    gui = AssistantGUI(assistant=st.session_state["assistant"])
    gui.render()

# -----------------------------------------------------------------------------
# 🧩 Helper: Initialize DB connection (optional check)
# -----------------------------------------------------------------------------


def check_db_connection():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        st.sidebar.info("✅ Database Connected")
    except Exception as e:
        st.sidebar.error(f"Database Error: {e}")


# -----------------------------------------------------------------------------
# 🚀 Entry Point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    check_db_connection()
    main()
