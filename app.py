import streamlit as st
import logging
from dotenv import load_dotenv
from sqlalchemy import text
# from langchain_openai import ChatOpenAI

# 🔐 Auth + DB
from auth.signup import signup
from auth.login import login
from database.db import get_engine

# 🤖 Assistant
from assistant import Assistant
from prompt import SYSTEM_PROMPT, WELCOME_MESSAGE
from langchain_groq import ChatGroq

load_dotenv()
logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="Umbrella Onboarding Assistant",
                   layout="wide", page_icon="☂")


def main():
    st.sidebar.title("☂️ Umbrella Corporation Assistant")

    # Session init
    for k, v in {
        "user": None,
        "employee": None,
        "assistant": None,
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Auth
    if not st.session_state["user"]:
        auth_mode = st.sidebar.radio("Select Mode", ["Login", "Sign Up"])
        if auth_mode == "Login":
            _ = login()
        else:
            signup()
            st.stop()

        if not st.session_state.get("employee"):
            st.stop()

    employee = st.session_state["employee"]

    # Sidebar profile
    st.sidebar.markdown("---")
    st.sidebar.success(
        f"👋 **Welcome, {employee['name']} {employee['lastname']}**  \n"
        f"**Role:** {employee['position']}  \n"
        f"**Department:** {employee['department']}  \n"
        f"**Supervisor:** {employee['supervisor']}"
    )
    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

    # Header
    st.title("Umbrella Corporation Internal Assistant ☂️")
    st.markdown(
        "<p style='color:#c4c4c4;font-size:16px;'>Welcome to your secure Umbrella onboarding environment. "
        "Proceed with caution and adhere to internal protocols.</p>",
        unsafe_allow_html=True,
    )
    st.markdown(f"---\n{WELCOME_MESSAGE}\n---")

    # Assistant once per session
    if not st.session_state["assistant"]:
        # llama-3.1-8b-instant or llama-3.3-70b-versatile
        llm = ChatGroq(model="llama-3.3-70b-versatile")
        # llm = ChatOpenAI(model="gpt-4o-mini")
        st.session_state["assistant"] = Assistant(
            system_prompt=SYSTEM_PROMPT,
            llm=llm,
            employee_information=employee,
        )

    # Lazy import to avoid circulars
    from gui import AssistantGUI
    AssistantGUI(assistant=st.session_state["assistant"]).render()


def check_db_connection():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        st.sidebar.info("✅ Database Connected")
    except Exception as e:
        st.sidebar.error(f"Database Error: {e}")


if __name__ == "__main__":
    check_db_connection()
    main()
