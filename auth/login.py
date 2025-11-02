# Handles secure login

import streamlit as st
from auth.auth_utils import get_user_by_email, verify_password
from sqlalchemy import text
from database.db import get_engine


def login():
    st.subheader("🔐 Employee Login")
    email = st.text_input("Corporate Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user_by_email(email)
        if not user:
            st.error("User not found. Please sign up first.")
            return None

        if verify_password(password, user["password_hash"]):
            st.success("✅ Login successful.")
            st.session_state["user"] = user
            # Fetch employee info
            engine = get_engine()
            with engine.connect() as conn:
                emp = conn.execute(text("SELECT * FROM employees WHERE employee_id = :eid"), {
                                   "eid": user["employee_id"]}).fetchone()
                if emp is not None:
                    st.session_state["employee"] = dict(emp._mapping)
                else:
                    st.session_state["employee"] = None
            return user
        else:
            st.error("Invalid password.")
            return None
